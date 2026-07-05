#!/usr/bin/env python3
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import difflib
import json
import os
import re
import shutil
import sys
import threading
import time
from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from catalog_common import (
    ALLOWED_TASKS,
    ARTIFACT_META,
    CONDITIONING_VOCAB,
    DOMAIN_VOCAB,
    FILE_ARTIFACT,
    METHOD_VOCAB,
    REPRESENTATION_VOCAB,
    ROOT,
    arxiv_id_from_url,
    arxiv_year_from_url,
    has_cjk,
    load_records,
    normalize_title,
    normalize_whitespace,
    parse_github_repo,
    sentence_count,
    slugify,
    suggested_org_from_repo,
)

CACHE_DIR = ROOT / "metadata" / "cache"
VALIDATION_DIR = ROOT / "metadata" / "validation"
BACKUP_ROOT = VALIDATION_DIR / "backups"
NETWORK_CACHE_FILE = CACHE_DIR / "network_cache.json"

SEARCH_URL_TOKENS = [
    "scholar.google.com",
    "github.com/search",
    "google.com/search",
    "bing.com/search",
]

SOFT_FAIL_DOMAINS = {
    "openreview.net",
    "proceedings.iclr.cc",
    "openaccess.thecvf.com",
    "www.openaccess.thecvf.com",
}

GITHUB_API_SOFT_CODES = {401, 403, 404, 429}

DEFAULT_MAX_WORKERS = min(8, max(4, (os.cpu_count() or 4) * 2))
PAGE_FETCH_MAX_BYTES = 200_000


def location(rec: dict) -> str:
    meta = ARTIFACT_META[rec["artifact"]]
    return f'{meta["dir"]}/{rec["id"]} ({rec["_source_file"]}:{rec["_lineno"]})'


def record_key(rec: dict) -> tuple[str, int]:
    return rec["_source_file"], int(rec["_lineno"])


def is_search_placeholder(url: str) -> bool:
    lowered = (url or "").lower()
    return any(token in lowered for token in SEARCH_URL_TOKENS)


def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def make_request(url: str, accept: str = "application/json,text/html,*/*") -> Request:
    return Request(
        url,
        headers={
            "User-Agent": "awesome-generative-models/4.0",
            "Accept": accept,
            "Cache-Control": "no-cache",
        },
    )


class NetworkCache:
    def __init__(self, path: Path | None, ttl_hours: float = 24.0) -> None:
        self.path = path
        self.ttl_seconds = max(0.0, float(ttl_hours)) * 3600.0
        self._entries: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._key_locks: dict[str, threading.Lock] = {}

        if self.path and self.path.exists():
            try:
                payload = json.loads(self.path.read_text(encoding="utf-8"))
                raw_entries = payload.get("entries", {})
                now = time.time()
                for key, item in raw_entries.items():
                    ts = float(item.get("ts", 0) or 0)
                    value = item.get("value")
                    if value is None:
                        continue
                    if self.ttl_seconds and ts and now - ts > self.ttl_seconds:
                        continue
                    self._entries[key] = {
                        "ts": ts or now,
                        "value": value,
                        "persist": True,
                    }
            except Exception:
                self._entries = {}

    def _is_expired_locked(self, item: dict[str, Any]) -> bool:
        if not self.ttl_seconds:
            return False
        ts = float(item.get("ts", 0) or 0)
        return bool(ts and time.time() - ts > self.ttl_seconds)

    def _key_lock(self, key: str) -> threading.Lock:
        with self._lock:
            lock = self._key_locks.get(key)
            if lock is None:
                lock = threading.Lock()
                self._key_locks[key] = lock
            return lock

    def get(self, key: str) -> Any | None:
        with self._lock:
            item = self._entries.get(key)
            if item is None:
                return None
            if self._is_expired_locked(item):
                self._entries.pop(key, None)
                return None
            return deepcopy(item["value"])

    def set(self, key: str, value: Any, persist: bool = True) -> None:
        with self._lock:
            self._entries[key] = {
                "ts": time.time(),
                "value": deepcopy(value),
                "persist": bool(persist),
            }

    def get_or_compute(
        self,
        key: str,
        compute: Callable[[], Any],
        persist_if: Callable[[Any], bool] | None = None,
    ) -> Any:
        cached = self.get(key)
        if cached is not None:
            return cached

        key_lock = self._key_lock(key)
        with key_lock:
            cached = self.get(key)
            if cached is not None:
                return cached

            value = compute()
            persist = True if persist_if is None else bool(persist_if(value))
            self.set(key, value, persist=persist)
            return deepcopy(value)

    def save(self) -> None:
        if not self.path:
            return

        payload = {
            "version": 1,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
            "ttl_hours": 0 if not self.ttl_seconds else self.ttl_seconds / 3600.0,
            "entries": {},
        }

        now = time.time()
        with self._lock:
            for key, item in self._entries.items():
                ts = float(item.get("ts", 0) or 0)
                if self.ttl_seconds and ts and now - ts > self.ttl_seconds:
                    continue
                if not item.get("persist", True):
                    continue
                payload["entries"][key] = {
                    "ts": ts,
                    "value": item.get("value"),
                }

        write_json(self.path, payload)


def format_duration(seconds: float) -> str:
    total = max(0, int(seconds))
    minutes, secs = divmod(total, 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours:d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"


class ProgressBar:
    def __init__(self, total: int, label: str = "progress") -> None:
        self.total = max(0, int(total))
        self.label = label
        self.current = 0
        self.started_at = time.monotonic()
        self.last_render_at = 0.0
        self.last_width = 0

        if self.total > 0:
            self._render(force=True)

    def update(self, step: int = 1) -> None:
        self.current += step
        self._render(force=False)

    def _render(self, force: bool) -> None:
        if self.total <= 0:
            return

        now = time.monotonic()
        if not force and self.current < self.total and now - self.last_render_at < 0.1:
            return

        elapsed = now - self.started_at
        progress = min(1.0, self.current / self.total) if self.total else 1.0
        width = 28
        filled = int(width * progress)
        bar = "#" * filled + "." * (width - filled)

        rate = self.current / elapsed if elapsed > 0 else 0.0
        remaining = self.total - self.current
        eta = remaining / rate if rate > 0 else 0.0

        line = (
            f"\r[{self.label}] [{bar}] "
            f"{self.current}/{self.total} "
            f"{progress * 100:5.1f}% "
            f"elapsed {format_duration(elapsed)} "
            f"eta {format_duration(eta)}"
        )

        pad = max(0, self.last_width - len(line))
        sys.stderr.write(line + (" " * pad))
        sys.stderr.flush()
        self.last_width = len(line)
        self.last_render_at = now

    def close(self) -> None:
        if self.total <= 0:
            return
        self._render(force=True)
        sys.stderr.write("\n")
        sys.stderr.flush()


COMMON_TITLE_STOPWORDS = {
    "the", "a", "an", "for", "of", "with", "via", "to", "and", "in",
    "on", "from", "by", "using", "towards", "toward", "into", "based",
    "system", "framework", "technical", "report", "model", "models",
}


def fetch_text(url: str, accept: str = "text/html,*/*", timeout: int = 20, max_bytes: int = 400_000) -> str:
    with urlopen(make_request(url, accept=accept), timeout=timeout) as response:
        return response.read(max_bytes).decode("utf-8", errors="ignore")


def clean_html_text(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    return normalize_whitespace(unescape(text))


def extract_html_meta_content(html: str, keys: list[str]) -> str:
    for key in keys:
        patterns = [
            re.compile(rf'<meta[^>]+name=["\']{re.escape(key)}["\'][^>]+content=["\'](.*?)["\']', re.I | re.S),
            re.compile(rf'<meta[^>]+property=["\']{re.escape(key)}["\'][^>]+content=["\'](.*?)["\']', re.I | re.S),
            re.compile(rf'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']{re.escape(key)}["\']', re.I | re.S),
            re.compile(rf'<meta[^>]+content=["\'](.*?)["\'][^>]+property=["\']{re.escape(key)}["\']', re.I | re.S),
        ]
        for pattern in patterns:
            match = pattern.search(html or "")
            if match:
                return clean_html_text(match.group(1))
    return ""


def extract_html_title(html: str) -> str:
    meta_title = extract_html_meta_content(
        html,
        ["citation_title", "og:title", "twitter:title"],
    )
    if meta_title:
        return meta_title

    match = re.search(r"<title[^>]*>(.*?)</title>", html or "", re.I | re.S)
    if match:
        return clean_html_text(match.group(1))
    return ""


def persist_ok_result(value: Any) -> bool:
    return isinstance(value, dict) and bool(value.get("ok"))


def page_meta_to_probe(page_meta: dict) -> dict:
    probe = {
        "ok": bool(page_meta.get("ok")),
        "status": int(page_meta.get("status", 0) or 0),
        "final_url": page_meta.get("final_url", ""),
    }
    if page_meta.get("warning"):
        probe["warning"] = page_meta["warning"]
    if page_meta.get("error"):
        probe["error"] = page_meta["error"]
    return probe


def fetch_page_meta(
    url: str,
    timeout: int = 20,
    max_bytes: int = PAGE_FETCH_MAX_BYTES,
    retries: int = 1,
    cache: NetworkCache | None = None,
) -> dict:
    cache_key = f"page::{url}"

    def _compute() -> dict:
        domain = urlparse(url).netloc.lower()
        last_soft_warning: dict | None = None

        for _ in range(retries + 1):
            try:
                with urlopen(make_request(url, accept="text/html,*/*"), timeout=timeout) as response:
                    status = int(getattr(response, "status", 200) or 200)
                    final_url = response.geturl()
                    content_type = (response.headers.get("Content-Type", "") or "").lower()

                    binary_like = any(
                        token in content_type
                        for token in (
                            "application/pdf",
                            "application/zip",
                            "application/octet-stream",
                            "image/",
                            "video/",
                            "audio/",
                        )
                    )

                    body = response.read(256 if binary_like else max_bytes)
                    title = ""
                    if not binary_like:
                        title = extract_html_title(body.decode("utf-8", errors="ignore"))

                    return {
                        "ok": True,
                        "status": status,
                        "final_url": final_url,
                        "title": title,
                        "content_type": content_type,
                    }
            except HTTPError as exc:
                if exc.code in {403, 429}:
                    return {
                        "ok": True,
                        "status": exc.code,
                        "final_url": getattr(exc, "url", url),
                        "title": "",
                        "content_type": "",
                        "warning": f"HTTP {exc.code}: blocked by the remote host, but the URL may still be valid.",
                    }
                if exc.code in {500, 502, 503, 504} and domain in SOFT_FAIL_DOMAINS:
                    last_soft_warning = {
                        "ok": True,
                        "status": exc.code,
                        "final_url": url,
                        "title": "",
                        "content_type": "",
                        "warning": f"HTTP {exc.code}: transient upstream failure on {domain}; treating as soft warning.",
                    }
                    continue
                return {
                    "ok": False,
                    "status": exc.code,
                    "final_url": url,
                    "title": "",
                    "content_type": "",
                    "error": f"HTTP {exc.code}",
                }
            except URLError as exc:
                return {
                    "ok": False,
                    "status": 0,
                    "final_url": url,
                    "title": "",
                    "content_type": "",
                    "error": str(exc.reason),
                }
            except Exception as exc:
                return {
                    "ok": False,
                    "status": 0,
                    "final_url": url,
                    "title": "",
                    "content_type": "",
                    "error": str(exc),
                }

        if last_soft_warning:
            return last_soft_warning
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "title": "",
            "content_type": "",
            "error": "Unknown network error",
        }

    if cache is None:
        return _compute()
    return cache.get_or_compute(cache_key, _compute, persist_if=persist_ok_result)


def fetch_arxiv_title(url: str, timeout: int = 20, cache: NetworkCache | None = None) -> str:
    arxiv_id = arxiv_id_from_url(url)
    if not arxiv_id:
        return ""

    def _compute() -> str:
        api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"
        try:
            xml_data = fetch_text(
                api_url,
                accept="application/atom+xml,text/xml,*/*",
                timeout=timeout,
                max_bytes=120_000,
            )
            root = ET.fromstring(xml_data)
            ns = {"a": "http://www.w3.org/2005/Atom"}
            title = root.findtext("a:entry/a:title", "", ns) or ""
            return normalize_whitespace(title)
        except Exception:
            return ""

    if cache is None:
        return _compute()
    return cache.get_or_compute(
        f"arxiv-title::{arxiv_id}",
        _compute,
        persist_if=lambda value: bool(value),
    )


def informative_tokens(text: str) -> set[str]:
    return {
        token
        for token in normalize_title(text).split()
        if len(token) >= 4 and token not in COMMON_TITLE_STOPWORDS
    }


def title_match_score(expected: str, observed: str) -> float:
    exp = normalize_title(expected)
    obs = normalize_title(observed)
    if not exp or not obs:
        return 0.0
    if exp == obs:
        return 1.0

    ratio = difflib.SequenceMatcher(None, exp, obs).ratio()

    exp_tokens = informative_tokens(expected)
    obs_tokens = informative_tokens(observed)
    overlap = 0.0
    if exp_tokens and obs_tokens:
        overlap = len(exp_tokens & obs_tokens) / max(1, min(len(exp_tokens), len(obs_tokens)))

    if (exp in obs or obs in exp) and min(len(exp), len(obs)) >= 24:
        ratio = max(ratio, 0.90)

    return max(ratio, overlap)


def title_matches(expected: str, observed: str) -> tuple[bool, float]:
    score = title_match_score(expected, observed)
    exp = normalize_title(expected)
    obs = normalize_title(observed)

    if exp == obs:
        return True, 1.0

    if score >= 0.88:
        return True, score

    exp_tokens = informative_tokens(expected)
    obs_tokens = informative_tokens(observed)
    if exp_tokens and obs_tokens:
        overlap = len(exp_tokens & obs_tokens) / max(1, min(len(exp_tokens), len(obs_tokens)))
        if overlap >= 0.80 and score >= 0.55:
            return True, max(score, overlap)

    return False, score


def verify_paper_title_match(
    rec: dict,
    timeout: int,
    cache: NetworkCache | None = None,
    page_meta: dict | None = None,
) -> dict:
    url = rec.get("paper", "")
    observed_title = ""
    source = ""

    if arxiv_id_from_url(url):
        observed_title = fetch_arxiv_title(url, timeout=timeout, cache=cache)
        source = "arXiv API"
    else:
        try:
            meta = page_meta if page_meta is not None else fetch_page_meta(url, timeout=timeout, cache=cache)
            if not meta["ok"]:
                return {
                    "ok": True,
                    "warning": f"unable to extract paper title for semantic verification ({meta.get('error', 'fetch failed')}).",
                }
            observed_title = meta.get("title", "")
            source = "HTML title"
        except Exception as exc:
            return {
                "ok": True,
                "warning": f"unable to extract paper title for semantic verification ({exc}).",
            }

    if not observed_title:
        return {
            "ok": True,
            "warning": "unable to extract paper title for semantic verification.",
        }

    matched, score = title_matches(rec["title"], observed_title)
    result = {
        "ok": matched,
        "observed_title": observed_title,
        "score": round(score, 3),
        "source": source,
    }
    if not matched:
        result["error"] = (
            f"paper title mismatch: expected `{rec['title']}` but resolved title is "
            f"`{observed_title}` (score={score:.2f})."
        )
    return result


def verify_homepage_title_match(
    rec: dict,
    timeout: int,
    cache: NetworkCache | None = None,
    page_meta: dict | None = None,
) -> dict:
    try:
        meta = page_meta if page_meta is not None else fetch_page_meta(rec.get("homepage", ""), timeout=timeout, cache=cache)
    except Exception as exc:
        return {
            "ok": True,
            "warning": f"unable to extract homepage title for semantic verification ({exc}).",
        }

    if not meta["ok"]:
        return {
            "ok": True,
            "warning": f"unable to extract homepage title for semantic verification ({meta.get('error', 'fetch failed')}).",
        }

    observed_title = meta.get("title", "")
    if not observed_title:
        return {"ok": True}

    matched, score = title_matches(rec["title"], observed_title)
    if matched or score >= 0.60:
        return {
            "ok": True,
            "observed_title": observed_title,
            "score": round(score, 3),
        }

    return {
        "ok": True,
        "warning": (
            f"homepage title weakly matches record title: `{observed_title}` "
            f"(score={score:.2f}); if this is a suite root / product root page, "
            f"prefer leaving `homepage` empty."
        ),
    }


def verify_repo_semantics(rec: dict, repo_probe: dict) -> dict:
    full_name = repo_probe.get("full_name", "")
    if not full_name:
        return {"ok": True}

    repo_name = full_name.split("/", 1)[-1]
    description = normalize_whitespace(repo_probe.get("description", ""))
    haystack = normalize_whitespace(f"{repo_name} {description}")
    if not haystack:
        return {"ok": True}

    score = title_match_score(rec["title"], haystack)
    if slugify(repo_name) in slugify(rec["title"]) or score >= 0.45:
        return {"ok": True, "score": round(score, 3)}

    return {
        "ok": True,
        "warning": (
            f"repo title/description weakly matches record title (score={score:.2f}); "
            f"verify repo exactness manually."
        ),
    }


def http_probe(
    url: str,
    timeout: int = 20,
    retries: int = 1,
    cache: NetworkCache | None = None,
) -> dict:
    cache_key = f"probe::{url}"

    def _compute() -> dict:
        domain = urlparse(url).netloc.lower()
        last_soft_warning: dict | None = None

        for _ in range(retries + 1):
            try:
                with urlopen(make_request(url), timeout=timeout) as response:
                    response.read(256)
                    return {
                        "ok": True,
                        "status": int(getattr(response, "status", 200) or 200),
                        "final_url": response.geturl(),
                    }
            except HTTPError as exc:
                if exc.code in {403, 429}:
                    return {
                        "ok": True,
                        "status": exc.code,
                        "final_url": getattr(exc, "url", url),
                        "warning": f"HTTP {exc.code}: blocked by the remote host, but the URL may still be valid.",
                    }
                if exc.code in {500, 502, 503, 504} and domain in SOFT_FAIL_DOMAINS:
                    last_soft_warning = {
                        "ok": True,
                        "status": exc.code,
                        "final_url": url,
                        "warning": f"HTTP {exc.code}: transient upstream failure on {domain}; treating as soft warning.",
                    }
                    continue
                return {"ok": False, "status": exc.code, "final_url": url, "error": f"HTTP {exc.code}"}
            except URLError as exc:
                return {"ok": False, "status": 0, "final_url": url, "error": str(exc.reason)}
            except Exception as exc:
                return {"ok": False, "status": 0, "final_url": url, "error": str(exc)}

        if last_soft_warning:
            return last_soft_warning
        return {"ok": False, "status": 0, "final_url": url, "error": "Unknown network error"}

    if cache is None:
        return _compute()
    return cache.get_or_compute(cache_key, _compute, persist_if=persist_ok_result)


def parse_star_count(html: str) -> int:
    patterns = [
        re.compile(r'([\d,]+)\s+stars', re.I),
        re.compile(r'"stargazerCount":\s*([0-9]+)', re.I),
    ]
    for pattern in patterns:
        match = pattern.search(html)
        if match:
            try:
                return int(match.group(1).replace(",", ""))
            except Exception:
                pass
    return 0


def github_repo_html_meta(url: str, timeout: int = 20, cache: NetworkCache | None = None) -> dict:
    full_name = parse_github_repo(url)
    if not full_name:
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "error": "Repo URL is not a canonical GitHub repository URL.",
        }

    cache_key = f"github-html::{full_name}"

    def _compute() -> dict:
        try:
            with urlopen(make_request(url, accept="text/html,*/*"), timeout=timeout) as response:
                html = response.read(PAGE_FETCH_MAX_BYTES).decode("utf-8", errors="ignore")
                final_url = response.geturl()
                final_full_name = parse_github_repo(final_url) or full_name
                archived = "This repository was archived by the owner" in html
                description = extract_html_meta_content(html, ["og:description", "description"])
                return {
                    "ok": True,
                    "status": int(getattr(response, "status", 200) or 200),
                    "final_url": final_url,
                    "full_name": final_full_name,
                    "stars": parse_star_count(html),
                    "pushed_at": "",
                    "archived": archived,
                    "license": "",
                    "description": description,
                    "homepage": "",
                }
        except HTTPError as exc:
            if exc.code in {403, 429}:
                return {
                    "ok": True,
                    "status": exc.code,
                    "final_url": getattr(exc, "url", url),
                    "full_name": full_name,
                    "stars": 0,
                    "pushed_at": "",
                    "archived": False,
                    "license": "",
                    "description": "",
                    "homepage": "",
                    "warning": f"GitHub HTML probe HTTP {exc.code}; repo may still be valid.",
                }
            return {
                "ok": False,
                "status": exc.code,
                "final_url": url,
                "full_name": full_name,
                "error": f"GitHub HTML HTTP {exc.code}",
            }
        except URLError as exc:
            return {
                "ok": False,
                "status": 0,
                "final_url": url,
                "full_name": full_name,
                "error": str(exc.reason),
            }
        except Exception as exc:
            return {
                "ok": False,
                "status": 0,
                "final_url": url,
                "full_name": full_name,
                "error": str(exc),
            }

    if cache is None:
        return _compute()
    return cache.get_or_compute(cache_key, _compute, persist_if=persist_ok_result)


def github_repo_meta(
    url: str,
    token: str,
    timeout: int = 20,
    cache: NetworkCache | None = None,
) -> dict:
    full_name = parse_github_repo(url)
    if not full_name:
        return {
            "ok": False,
            "status": 0,
            "final_url": url,
            "error": "Repo URL is not a canonical GitHub repository URL.",
        }

    cache_key = f"github-meta::{full_name}"

    def _compute() -> dict:
        api_url = f"https://api.github.com/repos/{full_name}"
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "awesome-generative-models/4.0",
        }
        if token:
            headers["Authorization"] = f"Bearer {token}"

        request = Request(api_url, headers=headers)

        try:
            with urlopen(request, timeout=timeout) as response:
                data = json.loads(response.read().decode("utf-8"))
                return {
                    "ok": True,
                    "status": int(getattr(response, "status", 200) or 200),
                    "final_url": url,
                    "full_name": data.get("full_name", full_name),
                    "stars": int(data.get("stargazers_count", 0) or 0),
                    "pushed_at": data.get("pushed_at", ""),
                    "archived": bool(data.get("archived", False)),
                    "license": (data.get("license") or {}).get("spdx_id", ""),
                    "description": normalize_whitespace(data.get("description", "") or ""),
                    "homepage": normalize_whitespace(data.get("homepage", "") or ""),
                }
        except HTTPError as exc:
            if exc.code in GITHUB_API_SOFT_CODES:
                fallback = github_repo_html_meta(url, timeout=timeout, cache=cache)
                if fallback["ok"]:
                    fallback["warning"] = f"GitHub API HTTP {exc.code}; validated via HTML fallback."
                    return fallback
            return {
                "ok": False,
                "status": exc.code,
                "final_url": url,
                "full_name": full_name,
                "error": f"GitHub API HTTP {exc.code}",
            }
        except URLError:
            fallback = github_repo_html_meta(url, timeout=timeout, cache=cache)
            if fallback["ok"]:
                fallback["warning"] = "GitHub API unreachable; validated via HTML fallback."
                return fallback
            return {
                "ok": False,
                "status": 0,
                "final_url": url,
                "full_name": full_name,
                "error": "GitHub API unreachable and HTML fallback failed",
            }
        except Exception as exc:
            fallback = github_repo_html_meta(url, timeout=timeout, cache=cache)
            if fallback["ok"]:
                fallback["warning"] = f"GitHub API exception ({exc}); validated via HTML fallback."
                return fallback
            return {
                "ok": False,
                "status": 0,
                "final_url": url,
                "full_name": full_name,
                "error": str(exc),
            }

    if cache is None:
        return _compute()
    return cache.get_or_compute(cache_key, _compute, persist_if=persist_ok_result)


def validate_record_schema(rec: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for field in ("id", "title", "venue", "task", "summary"):
        if not rec.get(field):
            errors.append(f"{location(rec)}: missing required field `{field}`.")

    if rec.get("task") and rec["task"] not in ALLOWED_TASKS[rec["artifact"]]:
        allowed = ", ".join(sorted(ALLOWED_TASKS[rec["artifact"]]))
        errors.append(
            f"{location(rec)}: task `{rec['task']}` is not allowed for `{rec['artifact']}`. Allowed: {allowed}."
        )

    unknown_domains = [x for x in rec["domain"] if x not in DOMAIN_VOCAB]
    unknown_repr = [x for x in rec["representation"] if x not in REPRESENTATION_VOCAB]
    unknown_methods = [x for x in rec["method"] if x not in METHOD_VOCAB]
    unknown_cond = [x for x in rec["conditioning"] if x not in CONDITIONING_VOCAB]

    if unknown_domains:
        errors.append(f"{location(rec)}: unknown domain tags: {unknown_domains}.")
    if unknown_repr:
        errors.append(f"{location(rec)}: unknown representation tags: {unknown_repr}.")
    if unknown_methods:
        errors.append(f"{location(rec)}: unknown method tags: {unknown_methods}.")
    if unknown_cond:
        errors.append(f"{location(rec)}: unknown conditioning tags: {unknown_cond}.")

    for text_field in ("title", "venue", "summary", "task", "scope_note"):
        if has_cjk(rec.get(text_field, "")):
            errors.append(f"{location(rec)}: `{text_field}` must be English-only.")

    for tag_field in ("domain", "representation", "method", "conditioning", "orgs"):
        joined = " ".join(rec.get(tag_field, []))
        if has_cjk(joined):
            errors.append(f"{location(rec)}: `{tag_field}` must be English-only.")

    summary_sentences = sentence_count(rec.get("summary", ""))
    if summary_sentences < 1 or summary_sentences > 3:
        errors.append(f"{location(rec)}: `summary` must contain 1–3 English sentences; found {summary_sentences}.")

    if rec["year"] and rec["year"] < 2025:
        if rec.get("active_since", 0) < 2025:
            errors.append(f"{location(rec)}: pre-2025 entry must have `active_since >= 2025`.")
        if not rec.get("scope_note"):
            errors.append(f"{location(rec)}: pre-2025 entry must have a non-empty `scope_note`.")

    if rec.get("open_source") and not rec.get("repo"):
        errors.append(f"{location(rec)}: `open_source: true` requires an exact `repo` URL.")

    if not any([rec.get("paper"), rec.get("repo"), rec.get("homepage")]):
        errors.append(f"{location(rec)}: at least one exact link among `paper`, `repo`, or `homepage` is required.")

    for link_field in ("paper", "repo", "homepage"):
        url = rec.get(link_field, "")
        if url and is_search_placeholder(url):
            errors.append(f"{location(rec)}: `{link_field}` cannot be a search-result URL: {url}")

    if rec.get("paper") and "arxiv.org" in rec["paper"].lower() and "arxiv" in rec["venue"].lower():
        arxiv_year = arxiv_year_from_url(rec["paper"])
        if arxiv_year and rec["year"] and arxiv_year != rec["year"]:
            errors.append(
                f"{location(rec)}: venue year `{rec['year']}` does not match arXiv paper year `{arxiv_year}`."
            )

    if not rec.get("paper"):
        warnings.append(f"{location(rec)}: missing `paper` link.")

    if rec.get("featured") and not rec.get("orgs"):
        warnings.append(f"{location(rec)}: featured entries should include `orgs`.")

    if rec.get("open_source") and rec.get("repo") and not parse_github_repo(rec["repo"]):
        warnings.append(f"{location(rec)}: open-source repo is not a canonical GitHub repo URL; verify manually.")

    if rec.get("homepage") and rec.get("repo"):
        if rec["homepage"].rstrip("/") == rec["repo"].rstrip("/"):
            warnings.append(f"{location(rec)}: `homepage` duplicates `repo`; keep only `repo` unless a separate project page exists.")

    suggested_org = suggested_org_from_repo(rec.get("repo", ""))
    if suggested_org and suggested_org not in rec.get("orgs", []):
        warnings.append(f"{location(rec)}: repo owner strongly suggests org `{suggested_org}`; consider adding it to `orgs`.")

    return errors, warnings


def validate_duplicates(records: list[dict]) -> tuple[list[str], set[tuple[str, int]]]:
    errors: list[str] = []
    invalid_keys: set[tuple[str, int]] = set()

    seen_ids: dict[str, str] = {}
    seen_titles: dict[str, str] = {}
    seen_papers: dict[str, str] = {}
    seen_repos: dict[str, str] = {}

    for rec in records:
        rloc = location(rec)
        rkey = record_key(rec)

        rid = rec["id"]
        if rid in seen_ids:
            errors.append(f"{rloc}: duplicate id with {seen_ids[rid]}.")
            invalid_keys.add(rkey)
        else:
            seen_ids[rid] = rloc

        title_key = normalize_title(rec["title"])
        if title_key in seen_titles:
            errors.append(f"{rloc}: duplicate normalized title with {seen_titles[title_key]}.")
            invalid_keys.add(rkey)
        else:
            seen_titles[title_key] = rloc

        if rec.get("paper"):
            paper_key = rec["paper"].rstrip("/")
            if paper_key in seen_papers:
                errors.append(f"{rloc}: duplicate paper URL with {seen_papers[paper_key]}.")
                invalid_keys.add(rkey)
            else:
                seen_papers[paper_key] = rloc

        if rec.get("repo"):
            repo_key = parse_github_repo(rec["repo"]) or rec["repo"].rstrip("/")
            if repo_key in seen_repos:
                errors.append(f"{rloc}: duplicate repo URL with {seen_repos[repo_key]}.")
                invalid_keys.add(rkey)
            else:
                seen_repos[repo_key] = rloc

    return errors, invalid_keys


def verify_record_links(
    rec: dict,
    token: str,
    timeout: int,
    cache: NetworkCache | None = None,
) -> tuple[list[str], list[str], dict[str, dict], dict, bool]:
    errors: list[str] = []
    warnings: list[str] = []
    repo_stats_item: dict[str, dict] = {}
    report_item: dict[str, dict] = {}
    invalid = False

    rloc = location(rec)

    if rec.get("paper"):
        paper_page_meta: dict | None = None

        if arxiv_id_from_url(rec["paper"]):
            paper_probe = http_probe(rec["paper"], timeout=timeout, retries=1, cache=cache)
        else:
            paper_page_meta = fetch_page_meta(rec["paper"], timeout=timeout, retries=1, cache=cache)
            paper_probe = page_meta_to_probe(paper_page_meta)

        report_item["paper"] = paper_probe
        if not paper_probe["ok"]:
            errors.append(f"{rloc}: paper URL failed validation: {paper_probe['error']}")
            invalid = True
        else:
            if paper_probe.get("warning"):
                warnings.append(f"{rloc}: paper URL warning: {paper_probe['warning']}")

            paper_sem = verify_paper_title_match(
                rec,
                timeout=timeout,
                cache=cache,
                page_meta=paper_page_meta,
            )
            report_item["paper_semantics"] = paper_sem
            if not paper_sem["ok"]:
                errors.append(f"{rloc}: {paper_sem['error']}")
                invalid = True
            elif paper_sem.get("warning"):
                warnings.append(f"{rloc}: paper semantic warning: {paper_sem['warning']}")

    if rec.get("repo"):
        if parse_github_repo(rec["repo"]):
            repo_probe = github_repo_meta(rec["repo"], token=token, timeout=timeout, cache=cache)
        else:
            repo_probe = http_probe(rec["repo"], timeout=timeout, retries=1, cache=cache)

        report_item["repo"] = repo_probe
        if not repo_probe["ok"]:
            errors.append(f"{rloc}: repo URL failed validation: {repo_probe['error']}")
            invalid = True
        else:
            if repo_probe.get("warning"):
                warnings.append(f"{rloc}: repo URL warning: {repo_probe['warning']}")
            if repo_probe.get("full_name"):
                repo_stats_item[repo_probe["full_name"]] = {
                    "stars": int(repo_probe.get("stars", 0) or 0),
                    "pushed_at": repo_probe.get("pushed_at", ""),
                    "archived": bool(repo_probe.get("archived", False)),
                    "license": repo_probe.get("license", ""),
                }
                if repo_probe.get("archived"):
                    warnings.append(f"{rloc}: repository is archived.")

            repo_sem = verify_repo_semantics(rec, repo_probe)
            report_item["repo_semantics"] = repo_sem
            if repo_sem.get("warning"):
                warnings.append(f"{rloc}: repo semantic warning: {repo_sem['warning']}")

    if rec.get("homepage"):
        home_page_meta = fetch_page_meta(rec["homepage"], timeout=timeout, retries=1, cache=cache)
        home_probe = page_meta_to_probe(home_page_meta)

        report_item["homepage"] = home_probe
        if not home_probe["ok"]:
            errors.append(f"{rloc}: homepage URL failed validation: {home_probe['error']}")
            invalid = True
        else:
            if home_probe.get("warning"):
                warnings.append(f"{rloc}: homepage URL warning: {home_probe['warning']}")

            home_sem = verify_homepage_title_match(
                rec,
                timeout=timeout,
                cache=cache,
                page_meta=home_page_meta,
            )
            report_item["homepage_semantics"] = home_sem
            if home_sem.get("warning"):
                warnings.append(f"{rloc}: homepage semantic warning: {home_sem['warning']}")

    return errors, warnings, repo_stats_item, report_item, invalid


def verify_links(
    records: list[dict],
    token: str,
    timeout: int,
    skip_network: bool,
    workers: int,
    cache: NetworkCache | None = None,
) -> tuple[list[str], list[str], dict, dict, set[tuple[str, int]]]:
    errors: list[str] = []
    warnings: list[str] = []
    repo_stats: dict[str, dict] = {}
    link_report: dict[str, dict] = {}
    invalid_keys: set[tuple[str, int]] = set()

    if skip_network:
        return errors, warnings, repo_stats, link_report, invalid_keys

    link_records = [
        rec for rec in records
        if any([rec.get("paper"), rec.get("repo"), rec.get("homepage")])
    ]
    if not link_records:
        return errors, warnings, repo_stats, link_report, invalid_keys

    max_workers = max(1, min(int(workers or 1), len(link_records)))
    progress = ProgressBar(total=len(link_records), label="verify-links")

    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_map = {
                executor.submit(verify_record_links, rec, token, timeout, cache): rec
                for rec in link_records
            }

            for future in as_completed(future_map):
                rec = future_map[future]
                rloc = location(rec)
                rkey = record_key(rec)

                try:
                    rec_errors, rec_warnings, rec_repo_stats, rec_report, rec_invalid = future.result()
                except Exception as exc:
                    rec_errors = [f"{rloc}: unexpected link validation exception: {exc}"]
                    rec_warnings = []
                    rec_repo_stats = {}
                    rec_report = {"internal_error": {"ok": False, "error": str(exc)}}
                    rec_invalid = True

                errors.extend(rec_errors)
                warnings.extend(rec_warnings)
                repo_stats.update(rec_repo_stats)
                link_report[rloc] = rec_report
                if rec_invalid:
                    invalid_keys.add(rkey)

                progress.update()
    finally:
        progress.close()

    errors.sort()
    warnings.sort()
    return errors, warnings, repo_stats, link_report, invalid_keys


def run_validation_pass(
    records: list[dict],
    token: str,
    timeout: int,
    skip_network: bool,
    workers: int,
    cache: NetworkCache | None = None,
) -> tuple[list[str], list[str], dict, dict, set[tuple[str, int]]]:
    errors: list[str] = []
    warnings: list[str] = []
    invalid_keys: set[tuple[str, int]] = set()

    for rec in records:
        rec_errors, rec_warnings = validate_record_schema(rec)
        errors.extend(rec_errors)
        warnings.extend(rec_warnings)
        if rec_errors:
            invalid_keys.add(record_key(rec))

    dup_errors, dup_invalid = validate_duplicates(records)
    errors.extend(dup_errors)
    invalid_keys |= dup_invalid

    link_errors, link_warnings, repo_stats, link_report, link_invalid = verify_links(
        records=records,
        token=token,
        timeout=timeout,
        skip_network=skip_network,
        workers=workers,
        cache=cache,
    )
    errors.extend(link_errors)
    warnings.extend(link_warnings)
    invalid_keys |= link_invalid

    errors.sort()
    warnings.sort()
    return errors, warnings, repo_stats, link_report, invalid_keys


def render_report(records: list[dict], errors: list[str], warnings: list[str], repo_stats: dict) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Validation Report",
        "",
        f"- Generated: `{now}`",
        f"- Records checked: **{len(records)}**",
        f"- Blocking errors: **{len(errors)}**",
        f"- Warnings: **{len(warnings)}**",
        "",
        "## Blocking Errors",
        "",
    ]
    if errors:
        lines.extend([f"- {item}" for item in errors])
    else:
        lines.append("- None.")
    lines.extend(["", "## Warnings", ""])
    if warnings:
        lines.extend([f"- {item}" for item in warnings])
    else:
        lines.append("- None.")
    lines.extend(["", "## Refreshed GitHub Repo Stats", ""])
    if repo_stats:
        lines.extend(["| Repo | Stars | Last Push | Archived | License |", "|:--|--:|:--|:--:|:--|"])
        for full_name, stats in sorted(
            repo_stats.items(),
            key=lambda item: (-int(item[1].get("stars", 0)), item[0].lower()),
        ):
            lines.append(
                f"| `{full_name}` | {int(stats.get('stars', 0))} | {stats.get('pushed_at', '')[:10]} | "
                f"{'Yes' if stats.get('archived') else 'No'} | {stats.get('license', '') or '—'} |"
            )
    else:
        lines.append("- No GitHub repo stats were refreshed.")
    lines.append("")
    return "\n".join(lines)


def prompt_yes_no(question: str) -> bool:
    try:
        answer = input(question).strip().lower()
    except EOFError:
        return False
    return answer in {"y", "yes"}


def prune_invalid_records(invalid_keys: set[tuple[str, int]]) -> tuple[Path, dict[str, int]]:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / timestamp / "data"
    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / "data", backup_dir, dirs_exist_ok=True)

    removed_counts: dict[str, int] = defaultdict(int)

    for file_name in FILE_ARTIFACT:
        path = ROOT / "data" / file_name
        if not path.exists():
            continue

        kept_lines: list[str] = []
        with path.open("r", encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    kept_lines.append(line.rstrip("\n"))
                    continue

                if (file_name, lineno) in invalid_keys:
                    removed_counts[file_name] += 1
                    continue

                kept_lines.append(line.rstrip("\n"))

        path.write_text("\n".join(kept_lines).rstrip() + "\n", encoding="utf-8")

    return backup_dir, dict(removed_counts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate catalog data and exact links.")
    parser.add_argument("--skip-network", action="store_true", help="Skip URL / GitHub API verification.")
    parser.add_argument("--write-cache", action="store_true", help="Read/write reusable network cache and write validation artifacts.")
    parser.add_argument("--timeout", type=int, default=20, help="Network timeout in seconds.")
    parser.add_argument("--workers", type=int, default=DEFAULT_MAX_WORKERS, help="Concurrent worker count for network validation.")
    parser.add_argument("--cache-ttl-hours", type=float, default=24.0, help="TTL for reusable network cache when --write-cache is enabled.")
    parser.add_argument("--interactive-clean", action="store_true", help="Prompt to prune invalid rows after reporting errors.")
    parser.add_argument("--prune-invalid", action="store_true", help="Prune invalid rows without prompting, then re-run validation.")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN", "").strip()
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)

    network_cache = NetworkCache(
        path=NETWORK_CACHE_FILE if args.write_cache else None,
        ttl_hours=args.cache_ttl_hours,
    )

    def persist(
        records: list[dict],
        errors: list[str],
        warnings: list[str],
        repo_stats: dict,
        link_report: dict,
        invalid_keys: set[tuple[str, int]],
    ) -> None:
        report = render_report(records, errors, warnings, repo_stats)
        (VALIDATION_DIR / "latest.md").write_text(report.rstrip() + "\n", encoding="utf-8")
        if args.write_cache:
            write_json(CACHE_DIR / "repo_stats.json", repo_stats)
            write_json(CACHE_DIR / "link_report.json", link_report)
            write_json(
                CACHE_DIR / "invalid_records.json",
                {
                    "records": [
                        {"source_file": sf, "lineno": ln}
                        for sf, ln in sorted(invalid_keys)
                    ]
                },
            )
            network_cache.save()

    records = load_records()
    errors, warnings, repo_stats, link_report, invalid_keys = run_validation_pass(
        records=records,
        token=token,
        timeout=args.timeout,
        skip_network=args.skip_network,
        workers=args.workers,
        cache=network_cache,
    )
    persist(records, errors, warnings, repo_stats, link_report, invalid_keys)

    print(f"[validate] records={len(records)} errors={len(errors)} warnings={len(warnings)}")
    if errors:
        print("\n[validate] blocking errors:")
        for item in errors:
            print(f"  - {item}")
    if warnings:
        print("\n[validate] warnings:")
        for item in warnings:
            print(f"  - {item}")

    should_prune = False
    if errors and args.prune_invalid:
        should_prune = True
    elif errors and args.interactive_clean and sys.stdin.isatty():
        should_prune = prompt_yes_no("\nPrune invalid rows now? [y/N]: ")

    if should_prune and invalid_keys:
        backup_dir, removed = prune_invalid_records(invalid_keys)
        print(f"\n[validate] pruned invalid rows. Backup written to: {backup_dir}")
        for file_name, count in sorted(removed.items()):
            print(f"  - {file_name}: removed {count}")

        records = load_records()
        errors, warnings, repo_stats, link_report, invalid_keys = run_validation_pass(
            records=records,
            token=token,
            timeout=args.timeout,
            skip_network=args.skip_network,
            workers=args.workers,
            cache=network_cache,
        )
        persist(records, errors, warnings, repo_stats, link_report, invalid_keys)
        print(f"\n[validate] after prune -> records={len(records)} errors={len(errors)} warnings={len(warnings)}")

    if errors:
        print("[validate] blocking errors found. See metadata/validation/latest.md", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()