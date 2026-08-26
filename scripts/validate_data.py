#!/usr/bin/env python3
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import socket
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass
from datetime import date, datetime, timedelta, timezone
from html import unescape
from http.client import IncompleteRead, RemoteDisconnected
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
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
    SCOPE_START_DATE,
    arxiv_id_from_url,
    arxiv_year_from_url,
    has_cjk,
    load_records,
    normalize_title,
    normalize_whitespace,
    parse_github_repo,
    sentence_count,
    suggested_org_from_repo,
)

CACHE_DIR = ROOT / "metadata" / "cache"
VALIDATION_ROOT = ROOT / "metadata" / "validation"
NETWORK_CACHE_FILE = CACHE_DIR / "network_cache_v2.json"

DEFAULT_WORKERS = min(8, max(2, os.cpu_count() or 2))
MAX_RESPONSE_BYTES = 200_000

SEARCH_URL_TOKENS = (
    "scholar.google.com",
    "github.com/search",
    "google.com/search",
    "bing.com/search",
)

CHALLENGE_TITLE_TOKENS = (
    "verifying your browser",
    "just a moment",
    "attention required",
    "access denied",
    "captcha",
    "cloudflare",
    "checking your browser",
)

GENERIC_TITLE_TOKENS = (
    "social media title tag",
    "untitled document",
)

TRANSIENT_HTTP_CODES = {408, 425, 429, 500, 502, 503, 504}
UNKNOWN_HTTP_CODES = {401, 403, 407, 409, 423, 451}
BROKEN_HTTP_CODES = {404, 410}

SEVERITY_ORDER = {
    "error": 0,
    "warning": 1,
    "notice": 2,
}


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    location: str
    message: str

    def markdown(self) -> str:
        return f"- `{self.code}` — {self.location}: {self.message}"


@dataclass
class Probe:
    state: str
    status: int = 0
    final_url: str = ""
    title: str = ""
    content_type: str = ""
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TtlCache:
    def __init__(self, path: Path | None, ttl_hours: float) -> None:
        self.path = path
        self.ttl_seconds = max(0.0, ttl_hours) * 3600.0
        self.entries: dict[str, dict[str, Any]] = {}
        self.lock = threading.Lock()

        if not path or not path.exists():
            return

        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.entries = payload.get("entries", {})
        except (OSError, json.JSONDecodeError, TypeError):
            self.entries = {}

    def get(self, key: str) -> Any | None:
        with self.lock:
            item = self.entries.get(key)
            if not item:
                return None

            timestamp = float(item.get("timestamp", item.get("ts", 0)) or 0)
            if (
                self.ttl_seconds
                and timestamp
                and time.time() - timestamp > self.ttl_seconds
            ):
                self.entries.pop(key, None)
                return None

            return item.get("value")

    def set(self, key: str, value: Any, persist: bool = True) -> None:
        with self.lock:
            self.entries[key] = {
                "timestamp": time.time(),
                "value": value,
                "persist": bool(persist),
            }

    def save(self) -> None:
        if not self.path:
            return

        with self.lock:
            entries = {
                key: {
                    "timestamp": item.get("timestamp", item.get("ts", time.time())),
                    "value": item.get("value"),
                    "persist": True,
                }
                for key, item in self.entries.items()
                if item.get("persist", True)
            }

        write_json(
            self.path,
            {
                "version": 2,
                "generated_at": utc_now(),
                "ttl_hours": self.ttl_seconds / 3600.0,
                "entries": entries,
            },
        )


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def write_json(path: Path, payload: Any) -> None:
    atomic_write_text(
        path,
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
    )


def record_location(record: dict[str, Any]) -> str:
    directory = ARTIFACT_META[record["artifact"]]["dir"]
    return (
        f"{directory}/{record['id']} "
        f"({record['_source_file']}:{record['_lineno']})"
    )


def record_key(record: dict[str, Any]) -> tuple[str, int]:
    return record["_source_file"], int(record["_lineno"])


def finding(
    severity: str,
    code: str,
    location: str,
    message: str,
) -> Finding:
    return Finding(
        severity=severity,
        code=code,
        location=location,
        message=normalize_whitespace(message),
    )


def is_valid_http_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except ValueError:
        return False

    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_search_placeholder(url: str) -> bool:
    lowered = (url or "").lower()
    return any(token in lowered for token in SEARCH_URL_TOKENS)


def canonical_arxiv_id(url: str) -> str:
    return arxiv_id_from_url(url).lower()


def openreview_forum_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc.lower() not in {"openreview.net", "www.openreview.net"}:
        return ""

    return (parse_qs(parsed.query).get("id") or [""])[0].strip()


def canonical_paper_key(url: str) -> str:
    arxiv_id = canonical_arxiv_id(url)
    if arxiv_id:
        return f"arxiv:{arxiv_id}"

    forum_id = openreview_forum_id(url)
    if forum_id:
        return f"openreview:{forum_id.lower()}"

    return url.rstrip("/")


def canonical_repo_key(url: str) -> str:
    full_name = parse_github_repo(url)
    if full_name:
        return f"github:{full_name.lower()}"

    return url.rstrip("/")


def request_for(
    url: str,
    *,
    accept: str = "text/html,*/*",
    token: str = "",
) -> Request:
    headers = {
        "User-Agent": "awesome-generative-models/5.0",
        "Accept": accept,
        "Accept-Encoding": "identity",
        "Cache-Control": "no-cache",
    }

    if token:
        headers["Authorization"] = f"Bearer {token}"

    return Request(url, headers=headers)


def read_limited(response: Any, limit: int = MAX_RESPONSE_BYTES) -> bytes:
    chunks: list[bytes] = []
    remaining = limit

    while remaining > 0:
        try:
            chunk = response.read(min(65_536, remaining))
        except IncompleteRead as exc:
            chunk = exc.partial or b""
            if chunk:
                chunks.append(chunk[:remaining])
            break

        if not chunk:
            break

        chunks.append(chunk)
        remaining -= len(chunk)

    return b"".join(chunks)


def clean_html_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value or "")
    return normalize_whitespace(unescape(value))


def extract_meta_content(html: str, keys: tuple[str, ...]) -> str:
    for key in keys:
        escaped = re.escape(key)
        patterns = (
            rf'<meta[^>]+name=["\']{escaped}["\'][^>]+content=["\'](.*?)["\']',
            rf'<meta[^>]+property=["\']{escaped}["\'][^>]+content=["\'](.*?)["\']',
            rf'<meta[^>]+content=["\'](.*?)["\'][^>]+name=["\']{escaped}["\']',
            rf'<meta[^>]+content=["\'](.*?)["\'][^>]+property=["\']{escaped}["\']',
        )

        for pattern in patterns:
            match = re.search(pattern, html, re.IGNORECASE | re.DOTALL)
            if match:
                return clean_html_text(match.group(1))

    return ""


def extract_html_title(html: str) -> str:
    meta_title = extract_meta_content(
        html,
        ("citation_title", "og:title", "twitter:title"),
    )
    if meta_title:
        return meta_title

    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        html or "",
        re.IGNORECASE | re.DOTALL,
    )
    return clean_html_text(match.group(1)) if match else ""


def is_unreliable_title(title: str) -> bool:
    lowered = normalize_whitespace(title).lower()
    if not lowered:
        return True

    return any(
        token in lowered
        for token in CHALLENGE_TITLE_TOKENS + GENERIC_TITLE_TOKENS
    )


def classify_http_status(status: int) -> str:
    if 200 <= status < 400:
        return "ok"
    if status in BROKEN_HTTP_CODES:
        return "broken"
    return "unknown"


def probe_http(
    url: str,
    *,
    timeout: int,
    retries: int,
    cache: TtlCache,
) -> Probe:
    cache_key = f"v2:http:{url}"
    cached = cache.get(cache_key)
    if isinstance(cached, dict):
        return Probe(**cached)

    if not is_valid_http_url(url):
        return Probe(
            state="broken",
            final_url=url,
            reason="URL is not an absolute HTTP(S) URL.",
        )

    last_probe = Probe(
        state="unknown",
        final_url=url,
        reason="Unknown network failure.",
    )

    for attempt in range(retries + 1):
        try:
            with urlopen(request_for(url), timeout=timeout) as response:
                status = int(getattr(response, "status", 200) or 200)
                body = read_limited(response)
                content_type = response.headers.get("Content-Type", "") or ""
                html = body.decode("utf-8", errors="ignore")

                probe = Probe(
                    state=classify_http_status(status),
                    status=status,
                    final_url=response.geturl(),
                    title=extract_html_title(html),
                    content_type=content_type,
                )
                cache.set(cache_key, probe.to_dict(), persist=probe.state == "ok")
                return probe

        except HTTPError as exc:
            status = int(exc.code or 0)
            body = b""

            try:
                body = read_limited(exc)
            except Exception:
                body = b""

            html = body.decode("utf-8", errors="ignore")
            state = classify_http_status(status)

            last_probe = Probe(
                state=state,
                status=status,
                final_url=getattr(exc, "url", url),
                title=extract_html_title(html),
                reason=f"HTTP {status}",
            )

            if status in TRANSIENT_HTTP_CODES and attempt < retries:
                time.sleep(min(2**attempt, 3))
                continue

            cache.set(
                cache_key,
                last_probe.to_dict(),
                persist=state == "ok",
            )
            return last_probe

        except (
            URLError,
            TimeoutError,
            socket.timeout,
            RemoteDisconnected,
            ConnectionResetError,
            IncompleteRead,
        ) as exc:
            reason = getattr(exc, "reason", exc)
            last_probe = Probe(
                state="unknown",
                final_url=url,
                reason=str(reason),
            )

            if attempt < retries:
                time.sleep(min(2**attempt, 3))
                continue

        except Exception as exc:
            last_probe = Probe(
                state="unknown",
                final_url=url,
                reason=str(exc),
            )
            break

    cache.set(cache_key, last_probe.to_dict(), persist=False)
    return last_probe


TITLE_STOPWORDS = {
    "the",
    "a",
    "an",
    "for",
    "of",
    "with",
    "via",
    "to",
    "and",
    "in",
    "on",
    "from",
    "by",
    "using",
    "towards",
    "toward",
    "into",
    "based",
    "model",
    "models",
    "framework",
    "system",
}


def title_tokens(value: str) -> set[str]:
    return {
        token
        for token in normalize_title(value).split()
        if len(token) >= 4 and token not in TITLE_STOPWORDS
    }


def title_match_score(expected: str, observed: str) -> float:
    expected_normalized = normalize_title(expected)
    observed_normalized = normalize_title(observed)

    if not expected_normalized or not observed_normalized:
        return 0.0

    if expected_normalized == observed_normalized:
        return 1.0

    ratio = difflib.SequenceMatcher(
        None,
        expected_normalized,
        observed_normalized,
    ).ratio()

    expected_tokens = title_tokens(expected)
    observed_tokens = title_tokens(observed)

    overlap = 0.0
    if expected_tokens and observed_tokens:
        overlap = len(expected_tokens & observed_tokens) / max(
            1,
            min(len(expected_tokens), len(observed_tokens)),
        )

    if (
        expected_normalized in observed_normalized
        or observed_normalized in expected_normalized
    ):
        ratio = max(ratio, 0.9)

    return max(ratio, overlap)


def title_matches(expected: str, observed: str) -> tuple[bool, float]:
    score = title_match_score(expected, observed)
    expected_tokens = title_tokens(expected)
    observed_tokens = title_tokens(observed)

    overlap = 0.0
    if expected_tokens and observed_tokens:
        overlap = len(expected_tokens & observed_tokens) / max(
            1,
            min(len(expected_tokens), len(observed_tokens)),
        )

    matched = score >= 0.82 or overlap >= 0.80
    return matched, max(score, overlap)


def fetch_arxiv_titles(
    arxiv_ids: set[str],
    *,
    timeout: int,
    cache: TtlCache,
) -> tuple[dict[str, str], bool]:
    titles: dict[str, str] = {}
    unresolved: list[str] = []

    for arxiv_id in sorted(arxiv_ids):
        cached = cache.get(f"v2:arxiv-title:{arxiv_id}")
        if isinstance(cached, str) and cached:
            titles[arxiv_id] = cached
        else:
            unresolved.append(arxiv_id)

    failed = False

    for offset in range(0, len(unresolved), 40):
        chunk = unresolved[offset : offset + 40]
        query = urlencode(
            {
                "id_list": ",".join(chunk),
                "max_results": len(chunk),
            }
        )
        url = f"https://export.arxiv.org/api/query?{query}"

        try:
            with urlopen(
                request_for(
                    url,
                    accept="application/atom+xml,text/xml,*/*",
                ),
                timeout=timeout,
            ) as response:
                xml_data = read_limited(response, 1_000_000)

            root = ET.fromstring(xml_data)
            namespace = {"atom": "http://www.w3.org/2005/Atom"}

            for entry in root.findall("atom:entry", namespace):
                entry_id = entry.findtext("atom:id", "", namespace)
                title = normalize_whitespace(
                    entry.findtext("atom:title", "", namespace)
                )

                match = re.search(
                    r"/abs/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?",
                    entry_id,
                )
                if not match or not title:
                    continue

                arxiv_id = match.group(1)
                titles[arxiv_id] = title
                cache.set(
                    f"v2:arxiv-title:{arxiv_id}",
                    title,
                    persist=True,
                )

        except Exception:
            failed = True

    return titles, failed


def extract_openreview_title(payload: dict[str, Any]) -> str:
    notes = payload.get("notes") or []
    if not notes:
        return ""

    content = notes[0].get("content") or {}
    title = content.get("title", "")

    if isinstance(title, dict):
        title = title.get("value", "")

    return normalize_whitespace(str(title or ""))


def fetch_openreview_title(
    forum_id: str,
    *,
    timeout: int,
    cache: TtlCache,
) -> str:
    cache_key = f"v2:openreview-title:{forum_id}"
    cached = cache.get(cache_key)
    if isinstance(cached, str) and cached:
        return cached

    endpoints = (
        "https://api2.openreview.net/notes",
        "https://api.openreview.net/notes",
    )

    for endpoint in endpoints:
        for parameter in ("id", "forum"):
            url = f"{endpoint}?{urlencode({parameter: forum_id, 'limit': 1})}"

            try:
                with urlopen(
                    request_for(url, accept="application/json"),
                    timeout=timeout,
                ) as response:
                    payload = json.loads(read_limited(response, 500_000))

                title = extract_openreview_title(payload)
                if title:
                    cache.set(cache_key, title, persist=True)
                    return title

            except Exception:
                continue

    return ""


def github_repo_meta(
    url: str,
    *,
    token: str,
    timeout: int,
    cache: TtlCache,
) -> tuple[Probe, dict[str, Any]]:
    full_name = parse_github_repo(url)
    if not full_name:
        return (
            Probe(
                state="broken",
                final_url=url,
                reason="Not a canonical GitHub repository URL.",
            ),
            {},
        )

    cache_key = f"v2:github:{full_name.lower()}"
    cached = cache.get(cache_key)
    if isinstance(cached, dict):
        probe_data = cached.get("probe") or {}
        return Probe(**probe_data), cached.get("meta") or {}

    api_url = f"https://api.github.com/repos/{full_name}"

    try:
        request = request_for(
            api_url,
            accept="application/vnd.github+json",
            token=token,
        )
        request.add_header("X-GitHub-Api-Version", "2022-11-28")

        with urlopen(request, timeout=timeout) as response:
            payload = json.loads(read_limited(response, 1_000_000))
            status = int(getattr(response, "status", 200) or 200)

        meta = {
            "full_name": payload.get("full_name", full_name),
            "stars": int(payload.get("stargazers_count", 0) or 0),
            "pushed_at": payload.get("pushed_at", ""),
            "archived": bool(payload.get("archived", False)),
            "license": (payload.get("license") or {}).get("spdx_id", ""),
            "description": normalize_whitespace(
                payload.get("description", "") or ""
            ),
            "homepage": normalize_whitespace(payload.get("homepage", "") or ""),
        }
        probe = Probe(
            state="ok",
            status=status,
            final_url=url,
        )

        cache.set(
            cache_key,
            {
                "probe": probe.to_dict(),
                "meta": meta,
            },
            persist=True,
        )
        return probe, meta

    except HTTPError as exc:
        status = int(exc.code or 0)
        return (
            Probe(
                state=classify_http_status(status),
                status=status,
                final_url=url,
                reason=f"GitHub API HTTP {status}",
            ),
            {},
        )

    except Exception as exc:
        return (
            Probe(
                state="unknown",
                final_url=url,
                reason=f"GitHub API unavailable: {exc}",
            ),
            {},
        )


def validate_schema(
    record: dict[str, Any],
) -> tuple[list[Finding], bool]:
    findings: list[Finding] = []
    invalid = False
    location = record_location(record)

    def add_error(code: str, message: str) -> None:
        nonlocal invalid
        invalid = True
        findings.append(finding("error", code, location, message))

    def add_warning(code: str, message: str) -> None:
        findings.append(finding("warning", code, location, message))

    for field_name in ("id", "title", "venue", "task", "summary"):
        if not record.get(field_name):
            add_error("schema.required", f"Missing required field `{field_name}`.")

    record_id = record.get("id", "")
    if record_id and not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", record_id):
        add_error(
            "schema.id",
            "`id` must contain only lowercase letters, digits, dots, underscores "
            "or hyphens.",
        )

    task = record.get("task", "")
    if task and task not in ALLOWED_TASKS[record["artifact"]]:
        allowed = ", ".join(sorted(ALLOWED_TASKS[record["artifact"]]))
        add_error(
            "schema.task",
            f"Task `{task}` is invalid for `{record['artifact']}`. "
            f"Allowed values: {allowed}.",
        )

    vocabulary_checks = (
        ("domain", DOMAIN_VOCAB),
        ("representation", REPRESENTATION_VOCAB),
        ("method", METHOD_VOCAB),
        ("conditioning", CONDITIONING_VOCAB),
    )

    for field_name, vocabulary in vocabulary_checks:
        unknown = [
            value
            for value in record.get(field_name, [])
            if value not in vocabulary
        ]
        if unknown:
            add_error(
                "schema.vocabulary",
                f"Unknown `{field_name}` values: {unknown}.",
            )

    for field_name in ("title", "venue", "summary", "task", "scope_note"):
        if has_cjk(record.get(field_name, "")):
            add_error(
                "schema.language",
                f"`{field_name}` must be English-only.",
            )

    for field_name in (
        "domain",
        "representation",
        "method",
        "conditioning",
        "orgs",
    ):
        if has_cjk(" ".join(record.get(field_name, []))):
            add_error(
                "schema.language",
                f"`{field_name}` must be English-only.",
            )

    summary_sentences = sentence_count(record.get("summary", ""))
    if summary_sentences < 1 or summary_sentences > 3:
        add_error(
            "schema.summary",
            "`summary` must contain 1–3 English sentences; "
            f"found {summary_sentences}.",
        )

    published_at = normalize_whitespace(str(record.get("published_at", "")))
    if published_at:
        try:
            published_date = date.fromisoformat(published_at)
        except ValueError:
            add_error(
                "date.invalid",
                "`published_at` must use ISO format YYYY-MM-DD.",
            )
        else:
            if published_date < SCOPE_START_DATE:
                add_error(
                    "date.out_of_scope",
                    f"`published_at` {published_at} is before "
                    f"{SCOPE_START_DATE.isoformat()}.",
                )

            if published_date > date.today() + timedelta(days=1):
                add_error(
                    "date.future",
                    f"`published_at` {published_at} is in the future.",
                )

    year = int(record.get("year", 0) or 0)
    active_since = int(record.get("active_since", 0) or 0)

    if not published_at and year and year < SCOPE_START_DATE.year:
        if active_since < SCOPE_START_DATE.year:
            add_error(
                "date.legacy_scope",
                "Pre-2025 entries require `active_since >= 2025`.",
            )
        if not record.get("scope_note"):
            add_error(
                "date.scope_note",
                "Pre-2025 entries require a non-empty `scope_note`.",
            )

    if (
        record.get("paper")
        and "arxiv.org" in record["paper"].lower()
        and "arxiv" in record.get("venue", "").lower()
    ):
        paper_year = arxiv_year_from_url(record["paper"])
        if paper_year and year and paper_year != year:
            add_error(
                "date.arxiv_year",
                f"Venue year `{year}` does not match arXiv year `{paper_year}`.",
            )

    if record.get("open_source") and not record.get("repo"):
        add_error(
            "link.open_source",
            "`open_source: true` requires an exact `repo` URL.",
        )

    if not any(
        record.get(field_name)
        for field_name in ("paper", "repo", "homepage")
    ):
        add_error(
            "link.required",
            "At least one exact `paper`, `repo`, or `homepage` URL is required.",
        )

    for field_name in ("paper", "repo", "homepage"):
        url = record.get(field_name, "")
        if not url:
            continue

        if not is_valid_http_url(url):
            add_error(
                "link.url",
                f"`{field_name}` is not an absolute HTTP(S) URL: {url}",
            )

        if is_search_placeholder(url):
            add_error(
                "link.search_placeholder",
                f"`{field_name}` cannot be a search-result URL: {url}",
            )

    repo_url = record.get("repo", "")
    if repo_url and urlparse(repo_url).netloc.lower() in {
        "github.com",
        "www.github.com",
    }:
        path_parts = [
            part
            for part in urlparse(repo_url).path.strip("/").split("/")
            if part
        ]
        if len(path_parts) != 2:
            add_error(
                "link.github_repo",
                "`repo` must point to the repository root, not a file, branch, "
                "release, issue, or search page.",
            )

    if not record.get("paper"):
        add_warning("metadata.missing_paper", "Missing `paper` link.")

    if record.get("featured") and not record.get("orgs"):
        add_warning(
            "metadata.featured_org",
            "Featured entries should include at least one organization.",
        )

    if (
        record.get("homepage")
        and record.get("repo")
        and record["homepage"].rstrip("/") == record["repo"].rstrip("/")
    ):
        add_warning(
            "metadata.duplicate_homepage",
            "`homepage` duplicates `repo`; keep only the exact repository URL.",
        )

    suggested_org = suggested_org_from_repo(record.get("repo", ""))
    if suggested_org and suggested_org not in record.get("orgs", []):
        add_warning(
            "metadata.organization",
            f"Repository owner suggests organization `{suggested_org}`.",
        )

    return findings, invalid


def validate_duplicates(
    records: list[dict[str, Any]],
) -> tuple[list[Finding], set[tuple[str, int]]]:
    findings: list[Finding] = []
    invalid_keys: set[tuple[str, int]] = set()

    seen_ids: dict[str, str] = {}
    seen_titles: dict[str, str] = {}
    seen_papers: dict[str, str] = {}
    seen_repos: dict[str, str] = {}

    for record in records:
        location = record_location(record)
        key = record_key(record)

        checks = (
            (
                seen_ids,
                record["id"],
                "duplicate.id",
                "Duplicate ID",
            ),
            (
                seen_titles,
                normalize_title(record["title"]),
                "duplicate.title",
                "Duplicate normalized title",
            ),
        )

        for seen, value, code, label in checks:
            if not value:
                continue

            if value in seen:
                findings.append(
                    finding(
                        "error",
                        code,
                        location,
                        f"{label}; first seen at {seen[value]}.",
                    )
                )
                invalid_keys.add(key)
            else:
                seen[value] = location

        if record.get("paper"):
            paper_key = canonical_paper_key(record["paper"])
            if paper_key in seen_papers:
                findings.append(
                    finding(
                        "error",
                        "duplicate.paper",
                        location,
                        f"Duplicate paper URL; first seen at "
                        f"{seen_papers[paper_key]}.",
                    )
                )
                invalid_keys.add(key)
            else:
                seen_papers[paper_key] = location

        if record.get("repo"):
            repo_key = canonical_repo_key(record["repo"])
            if repo_key in seen_repos:
                findings.append(
                    finding(
                        "error",
                        "duplicate.repo",
                        location,
                        f"Duplicate repository URL; first seen at "
                        f"{seen_repos[repo_key]}.",
                    )
                )
                invalid_keys.add(key)
            else:
                seen_repos[repo_key] = location

    return findings, invalid_keys


def state_finding(
    record: dict[str, Any],
    field_name: str,
    probe: Probe,
    *,
    authoritative_evidence: bool = False,
) -> Finding | None:
    location = record_location(record)

    if probe.state == "broken":
        return finding(
            "error",
            f"network.{field_name}.broken",
            location,
            f"`{field_name}` URL is confirmed broken: "
            f"{probe.reason or f'HTTP {probe.status}'}.",
        )

    if probe.state == "unknown":
        severity = "notice" if authoritative_evidence else "warning"
        return finding(
            severity,
            f"network.{field_name}.unknown",
            location,
            f"`{field_name}` could not be conclusively verified: "
            f"{probe.reason or f'HTTP {probe.status}'}.",
        )

    return None


def validate_record_network(
    record: dict[str, Any],
    *,
    token: str,
    timeout: int,
    retries: int,
    cache: TtlCache,
    arxiv_titles: dict[str, str],
) -> tuple[list[Finding], dict[str, Any], dict[str, Any]]:
    findings: list[Finding] = []
    report: dict[str, Any] = {}
    repo_stats: dict[str, Any] = {}
    location = record_location(record)

    paper_url = record.get("paper", "")
    if paper_url and is_valid_http_url(paper_url):
        arxiv_id = canonical_arxiv_id(paper_url)
        forum_id = openreview_forum_id(paper_url)

        authoritative_title = ""
        authoritative_source = ""

        if arxiv_id:
            authoritative_title = arxiv_titles.get(arxiv_id, "")
            authoritative_source = "arXiv API"
        elif forum_id:
            authoritative_title = fetch_openreview_title(
                forum_id,
                timeout=timeout,
                cache=cache,
            )
            authoritative_source = "OpenReview API"

        paper_probe = probe_http(
            paper_url,
            timeout=timeout,
            retries=retries,
            cache=cache,
        )
        report["paper"] = paper_probe.to_dict()

        state_issue = state_finding(
            record,
            "paper",
            paper_probe,
            authoritative_evidence=bool(authoritative_title),
        )
        if state_issue:
            findings.append(state_issue)

        observed_title = authoritative_title or paper_probe.title
        title_source = authoritative_source or "HTML metadata"

        semantic_report = {
            "source": title_source,
            "observed_title": observed_title,
        }

        if observed_title and not is_unreliable_title(observed_title):
            matched, score = title_matches(record["title"], observed_title)
            semantic_report.update(
                {
                    "ok": matched,
                    "score": round(score, 3),
                }
            )

            if not matched and authoritative_source:
                findings.append(
                    finding(
                        "error",
                        "semantic.paper_mismatch",
                        location,
                        f"Paper title mismatch. Expected `{record['title']}`; "
                        f"{authoritative_source} returned `{observed_title}` "
                        f"(score={score:.2f}).",
                    )
                )
            elif not matched and score < 0.35:
                findings.append(
                    finding(
                        "warning",
                        "semantic.paper_weak_match",
                        location,
                        f"HTML title weakly matches the catalog title: "
                        f"`{observed_title}` (score={score:.2f}).",
                    )
                )

        elif paper_probe.title and is_unreliable_title(paper_probe.title):
            semantic_report.update(
                {
                    "ok": None,
                    "reason": "Bot challenge or generic page title.",
                }
            )
            findings.append(
                finding(
                    "warning",
                    "semantic.paper_unverified",
                    location,
                    "Paper title could not be verified because the remote site "
                    "returned a bot-challenge or generic page.",
                )
            )
        else:
            semantic_report.update(
                {
                    "ok": None,
                    "reason": "No reliable title metadata was available.",
                }
            )

        report["paper_semantics"] = semantic_report

    repo_url = record.get("repo", "")
    if repo_url and is_valid_http_url(repo_url):
        if parse_github_repo(repo_url):
            repo_probe, meta = github_repo_meta(
                repo_url,
                token=token,
                timeout=timeout,
                cache=cache,
            )
            report["repo"] = {
                **repo_probe.to_dict(),
                **meta,
            }

            state_issue = state_finding(record, "repo", repo_probe)
            if state_issue:
                findings.append(state_issue)

            if repo_probe.state == "ok" and meta:
                full_name = meta.get("full_name", "")
                if full_name:
                    repo_stats[full_name] = {
                        "stars": int(meta.get("stars", 0) or 0),
                        "pushed_at": meta.get("pushed_at", ""),
                        "archived": bool(meta.get("archived", False)),
                        "license": meta.get("license", ""),
                    }

                if meta.get("archived"):
                    findings.append(
                        finding(
                            "warning",
                            "repository.archived",
                            location,
                            "Repository is archived.",
                        )
                    )

                repo_text = normalize_whitespace(
                    f"{full_name} {meta.get('description', '')}"
                )
                score = title_match_score(record["title"], repo_text)
                report["repo_semantics"] = {
                    "ok": score >= 0.20,
                    "score": round(score, 3),
                }

                if score < 0.20:
                    findings.append(
                        finding(
                            "notice",
                            "semantic.repo_weak_match",
                            location,
                            f"Repository name/description weakly matches the "
                            f"catalog title (score={score:.2f}).",
                        )
                    )
        else:
            repo_probe = probe_http(
                repo_url,
                timeout=timeout,
                retries=retries,
                cache=cache,
            )
            report["repo"] = repo_probe.to_dict()

            state_issue = state_finding(record, "repo", repo_probe)
            if state_issue:
                findings.append(state_issue)

    homepage_url = record.get("homepage", "")
    if homepage_url and is_valid_http_url(homepage_url):
        homepage_probe = probe_http(
            homepage_url,
            timeout=timeout,
            retries=retries,
            cache=cache,
        )
        report["homepage"] = homepage_probe.to_dict()

        state_issue = state_finding(record, "homepage", homepage_probe)
        if state_issue:
            findings.append(state_issue)

        if homepage_probe.title and not is_unreliable_title(homepage_probe.title):
            matched, score = title_matches(
                record["title"],
                homepage_probe.title,
            )
            report["homepage_semantics"] = {
                "ok": matched,
                "observed_title": homepage_probe.title,
                "score": round(score, 3),
            }

            if not matched and score < 0.25:
                findings.append(
                    finding(
                        "notice",
                        "semantic.homepage_weak_match",
                        location,
                        f"Homepage title weakly matches the catalog title: "
                        f"`{homepage_probe.title}` (score={score:.2f}).",
                    )
                )

    return findings, report, repo_stats


def validate_network(
    records: list[dict[str, Any]],
    *,
    token: str,
    timeout: int,
    retries: int,
    workers: int,
    cache: TtlCache,
) -> tuple[list[Finding], dict[str, Any], dict[str, Any]]:
    findings: list[Finding] = []
    link_report: dict[str, Any] = {}
    repo_stats: dict[str, Any] = {}

    arxiv_ids = {
        canonical_arxiv_id(record.get("paper", ""))
        for record in records
        if canonical_arxiv_id(record.get("paper", ""))
    }
    arxiv_titles, arxiv_failed = fetch_arxiv_titles(
        arxiv_ids,
        timeout=timeout,
        cache=cache,
    )

    missing_arxiv_titles = arxiv_ids - set(arxiv_titles)
    if arxiv_failed and missing_arxiv_titles:
        findings.append(
            finding(
                "warning",
                "source.arxiv_api",
                "catalog",
                f"arXiv API was partially unavailable; "
                f"{len(missing_arxiv_titles)} title checks were skipped.",
            )
        )

    link_records = [
        record
        for record in records
        if any(
            record.get(field_name)
            for field_name in ("paper", "repo", "homepage")
        )
    ]

    max_workers = max(1, min(workers, len(link_records) or 1))

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(
                validate_record_network,
                record,
                token=token,
                timeout=timeout,
                retries=retries,
                cache=cache,
                arxiv_titles=arxiv_titles,
            ): record
            for record in link_records
        }

        completed = 0

        for future in as_completed(future_map):
            record = future_map[future]
            location = record_location(record)

            try:
                record_findings, record_report, record_stats = future.result()
            except Exception as exc:
                record_findings = [
                    finding(
                        "warning",
                        "network.internal_exception",
                        location,
                        f"Unexpected network-validation exception: {exc}",
                    )
                ]
                record_report = {
                    "internal_error": {
                        "state": "unknown",
                        "reason": str(exc),
                    }
                }
                record_stats = {}

            findings.extend(record_findings)
            link_report[location] = record_report
            repo_stats.update(record_stats)

            completed += 1
            if completed % 25 == 0 or completed == len(link_records):
                print(
                    f"[validate] network progress: "
                    f"{completed}/{len(link_records)}",
                    file=sys.stderr,
                )

    return findings, link_report, repo_stats


def sort_findings(findings: list[Finding]) -> list[Finding]:
    return sorted(
        findings,
        key=lambda item: (
            SEVERITY_ORDER[item.severity],
            item.location.lower(),
            item.code,
            item.message.lower(),
        ),
    )


def render_report(
    *,
    mode: str,
    records_count: int,
    findings: list[Finding],
    repo_stats: dict[str, Any],
) -> str:
    grouped = {
        severity: [
            item for item in findings if item.severity == severity
        ]
        for severity in ("error", "warning", "notice")
    }

    status = "FAIL" if grouped["error"] else "PASS"
    commit = os.environ.get("GITHUB_SHA", "")[:12] or "local"

    lines = [
        f"# Validation Report — {mode.title()}",
        "",
        f"- Status: **{status}**",
        f"- Generated: `{utc_now()}`",
        f"- Commit: `{commit}`",
        f"- Records checked: **{records_count}**",
        f"- Blocking errors: **{len(grouped['error'])}**",
        f"- Warnings: **{len(grouped['warning'])}**",
        f"- Notices: **{len(grouped['notice'])}**",
        "",
        "## Blocking Errors",
        "",
    ]

    if grouped["error"]:
        lines.extend(item.markdown() for item in grouped["error"])
    else:
        lines.append("- None.")

    lines.extend(["", "## Warnings", ""])
    if grouped["warning"]:
        lines.extend(item.markdown() for item in grouped["warning"])
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "<details>",
            f"<summary>Notices ({len(grouped['notice'])})</summary>",
            "",
        ]
    )
    if grouped["notice"]:
        lines.extend(item.markdown() for item in grouped["notice"])
    else:
        lines.append("- None.")
    lines.extend(["", "</details>", ""])

    if mode == "deep":
        lines.extend(["## Refreshed GitHub Repository Stats", ""])

        if repo_stats:
            lines.extend(
                [
                    "| Repository | Stars | Last push | Archived | License |",
                    "|:--|--:|:--|:--:|:--|",
                ]
            )

            for full_name, stats in sorted(
                repo_stats.items(),
                key=lambda item: (
                    -int(item[1].get("stars", 0)),
                    item[0].lower(),
                ),
            ):
                lines.append(
                    f"| `{full_name}` | "
                    f"{int(stats.get('stars', 0))} | "
                    f"{str(stats.get('pushed_at', ''))[:10] or '—'} | "
                    f"{'Yes' if stats.get('archived') else 'No'} | "
                    f"{stats.get('license') or '—'} |"
                )
        else:
            lines.append("- No repository statistics were refreshed.")

        lines.append("")

    return "\n".join(lines)


def write_report_index(report_root: Path) -> None:
    rows: list[str] = []

    for mode in ("fast", "deep"):
        summary_path = report_root / mode / "latest.json"
        if not summary_path.exists():
            rows.append(f"| {mode.title()} | Never run | — | — |")
            continue

        try:
            payload = json.loads(summary_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            rows.append(f"| {mode.title()} | Invalid report | — | — |")
            continue

        rows.append(
            f"| [{mode.title()}]({mode}/latest.md) | "
            f"{payload.get('generated_at', '—')} | "
            f"{payload.get('blocking_errors', 0)} | "
            f"{payload.get('warnings', 0)} |"
        )

    content = "\n".join(
        [
            "# Validation Reports",
            "",
            "> Fast validation checks deterministic catalog correctness.",
            "> Deep validation checks live links, semantic identity, and "
            "repository statistics.",
            "",
            "| Report | Generated | Blocking errors | Warnings |",
            "|:--|:--|--:|--:|",
            *rows,
            "",
        ]
    )

    atomic_write_text(report_root / "latest.md", content)


def append_github_summary(
    mode: str,
    findings: list[Finding],
    report_path: Path,
) -> None:
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if not summary_file:
        return

    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]

    lines = [
        f"## Catalog validation: {mode}",
        "",
        f"- Blocking errors: **{len(errors)}**",
        f"- Warnings: **{len(warnings)}**",
        f"- Report: `{report_path}`",
        "",
    ]

    if errors:
        lines.extend(item.markdown() for item in errors[:20])

    with open(summary_file, "a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def write_github_outputs(
    findings: list[Finding],
    report_path: Path,
) -> None:
    output_file = os.environ.get("GITHUB_OUTPUT", "")
    if not output_file:
        return

    errors = sum(item.severity == "error" for item in findings)
    warnings = sum(item.severity == "warning" for item in findings)

    with open(output_file, "a", encoding="utf-8") as handle:
        handle.write(f"blocking_errors={errors}\n")
        handle.write(f"warnings={warnings}\n")
        handle.write(f"report={report_path.as_posix()}\n")


def merged_repo_stats(
    records: list[dict[str, Any]],
    refreshed: dict[str, Any],
) -> dict[str, Any]:
    existing_path = CACHE_DIR / "repo_stats.json"
    existing: dict[str, Any] = {}

    if existing_path.exists():
        try:
            existing = json.loads(existing_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            existing = {}

    current_repos = {
        full_name
        for record in records
        if (full_name := parse_github_repo(record.get("repo", "")))
    }

    merged: dict[str, Any] = {}
    for full_name in current_repos:
        if full_name in refreshed:
            merged[full_name] = refreshed[full_name]
        elif full_name in existing:
            merged[full_name] = existing[full_name]

    return merged


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate catalog data and exact links."
    )
    parser.add_argument(
        "--mode",
        choices=("fast", "deep"),
        help="fast = deterministic checks; deep = deterministic + network.",
    )
    parser.add_argument(
        "--skip-network",
        action="store_true",
        help="Backward-compatible alias for --mode fast.",
    )
    parser.add_argument(
        "--write-cache",
        action="store_true",
        help="Persist deep network cache and repository statistics.",
    )
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--cache-ttl-hours", type=float, default=24.0)
    parser.add_argument(
        "--report-root",
        type=Path,
        default=VALIDATION_ROOT,
        help="Alternative report directory, useful in CI.",
    )
    args = parser.parse_args()

    mode = args.mode
    if args.skip_network:
        mode = "fast"
    elif not mode:
        mode = "deep" if args.write_cache else "deep"

    report_root = args.report_root.resolve()
    default_report_root = VALIDATION_ROOT.resolve()
    writes_repository_artifacts = report_root == default_report_root

    cache = TtlCache(
        NETWORK_CACHE_FILE
        if mode == "deep" and args.write_cache and writes_repository_artifacts
        else None,
        ttl_hours=args.cache_ttl_hours,
    )

    try:
        records = load_records()
    except Exception as exc:
        print(f"[validate] unable to load catalog data: {exc}", file=sys.stderr)
        return 1

    findings: list[Finding] = []
    deterministic_invalid: set[tuple[str, int]] = set()

    for record in records:
        record_findings, invalid = validate_schema(record)
        findings.extend(record_findings)
        if invalid:
            deterministic_invalid.add(record_key(record))

    duplicate_findings, duplicate_invalid = validate_duplicates(records)
    findings.extend(duplicate_findings)
    deterministic_invalid |= duplicate_invalid

    missing_exact_dates = sum(
        not normalize_whitespace(str(record.get("published_at", "")))
        for record in records
    )
    if missing_exact_dates:
        findings.append(
            finding(
                "warning",
                "date.precision",
                "catalog",
                f"{missing_exact_dates} records do not have `published_at`; "
                "day-level freshness cannot be guaranteed until they are "
                "backfilled.",
            )
        )

    link_report: dict[str, Any] = {}
    refreshed_repo_stats: dict[str, Any] = {}

    if mode == "deep":
        network_findings, link_report, refreshed_repo_stats = validate_network(
            records,
            token=os.environ.get("GH_TOKEN", "").strip(),
            timeout=max(1, args.timeout),
            retries=max(0, args.retries),
            workers=max(1, args.workers),
            cache=cache,
        )
        findings.extend(network_findings)

    findings = sort_findings(findings)

    report_markdown = render_report(
        mode=mode,
        records_count=len(records),
        findings=findings,
        repo_stats=refreshed_repo_stats,
    )

    mode_directory = report_root / mode
    report_path = mode_directory / "latest.md"
    json_path = mode_directory / "latest.json"

    atomic_write_text(report_path, report_markdown.rstrip() + "\n")

    errors = [item for item in findings if item.severity == "error"]
    warnings = [item for item in findings if item.severity == "warning"]
    notices = [item for item in findings if item.severity == "notice"]

    write_json(
        json_path,
        {
            "version": 2,
            "mode": mode,
            "status": "fail" if errors else "pass",
            "generated_at": utc_now(),
            "commit": os.environ.get("GITHUB_SHA", "") or "local",
            "records_checked": len(records),
            "blocking_errors": len(errors),
            "warnings": len(warnings),
            "notices": len(notices),
            "findings": [asdict(item) for item in findings],
        },
    )

    if writes_repository_artifacts:
        write_report_index(report_root)

        # Only deterministic data problems go into invalid_records.json.
        # Temporary network problems must never silently remove catalog rows.
        write_json(
            CACHE_DIR / "invalid_records.json",
            {
                "version": 2,
                "reason": "deterministic-validation-only",
                "records": [
                    {
                        "source_file": source_file,
                        "lineno": line_number,
                    }
                    for source_file, line_number in sorted(
                        deterministic_invalid
                    )
                ],
            },
        )

        if mode == "deep" and args.write_cache:
            write_json(CACHE_DIR / "link_report.json", link_report)
            write_json(
                CACHE_DIR / "repo_stats.json",
                merged_repo_stats(records, refreshed_repo_stats),
            )
            cache.save()

    append_github_summary(mode, findings, report_path)
    write_github_outputs(findings, report_path)

    print(
        f"[validate] mode={mode} records={len(records)} "
        f"errors={len(errors)} warnings={len(warnings)} "
        f"notices={len(notices)}"
    )
    print(f"[validate] report={report_path}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())