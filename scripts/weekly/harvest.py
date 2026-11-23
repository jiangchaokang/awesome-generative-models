#!/usr/bin/env python3
"""Multi-source candidate harvesting for Weekly Top Picks.

Sources (all redundant; failure of any single source degrades gracefully):
1. Existing daily candidate inbox (`metadata/candidates/YYYY-MM-DD/candidates.json`)
   within/around the target window (reused, not re-fetched).
2. arXiv API (cs.CV / cs.GR / cs.LG / cs.AI / cs.RO, >=3s rate limit, 3 retries).
3. Hugging Face Daily Papers + HF Paper API (upvotes, authors, code/project links).
4. GitHub API (repo stars, created_at, license, README for identity check).
5. OpenAlex API (auxiliary affiliation lookup).

All network calls go through an injectable `HttpClient` so tests run 100% offline.
"""
from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from datetime import timedelta
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

import yaml

from catalog_common import (
    ROOT,
    arxiv_id_from_url,
    normalize_whitespace,
    parse_github_repo,
)
from weekly.window import WeekWindow, in_window, parse_utc_datetime

USER_AGENT = "awesome-generative-models/6.0 (+https://github.com/jiangchaokang/awesome-generative-models)"
ARXIV_MIN_INTERVAL = 3.1
DEFAULT_TIMEOUT = 10
DEFAULT_RETRIES = 3

GITHUB_URL_RE = re.compile(r"https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
PROJECT_URL_RE = re.compile(
    r"https?://(?:[A-Za-z0-9-]+\.github\.io(?:/[^\s)\"'>]*)?|[A-Za-z0-9.-]+/projects?/[A-Za-z0-9_.-]+)"
)


@dataclass
class HttpResponse:
    status: int
    body: bytes
    headers: dict[str, str] = field(default_factory=dict)


class HttpClient:
    """Minimal HTTP client with fixed User-Agent, timeout, and exponential backoff."""

    def __init__(
        self,
        *,
        timeout: int = DEFAULT_TIMEOUT,
        retries: int = DEFAULT_RETRIES,
        github_token: str = "",
        fetcher: Callable[[str, dict[str, str], int], HttpResponse] | None = None,
        sleep_fn: Callable[[float], None] = time.sleep,
    ) -> None:
        self.timeout = timeout
        self.retries = retries
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN", "") or os.environ.get("GH_TOKEN", "")
        self._fetcher = fetcher
        self._sleep = sleep_fn
        self._last_arxiv_call = 0.0

    def get(self, url: str, *, accept: str = "application/json,text/xml,*/*", is_github: bool = False) -> HttpResponse | None:
        if "arxiv.org" in url:
            if self._last_arxiv_call > 0.0:
                elapsed = time.monotonic() - self._last_arxiv_call
                if elapsed < ARXIV_MIN_INTERVAL:
                    self._sleep(ARXIV_MIN_INTERVAL - elapsed)
            self._last_arxiv_call = time.monotonic()

        headers = {"User-Agent": USER_AGENT, "Accept": accept}
        if is_github and self.github_token:
            headers["Authorization"] = f"Bearer {self.github_token}"
            headers["X-GitHub-Api-Version"] = "2022-11-28"

        for attempt in range(self.retries + 1):
            try:
                if self._fetcher is not None:
                    resp = self._fetcher(url, headers, self.timeout)
                else:
                    req = Request(url, headers=headers)
                    with urlopen(req, timeout=self.timeout) as r:
                        resp = HttpResponse(
                            status=int(getattr(r, "status", 200) or 200),
                            body=r.read(2_000_000),
                            headers={k.lower(): v for k, v in r.headers.items()},
                        )
                if resp.status in {408, 425, 429, 500, 502, 503, 504} and attempt < self.retries:
                    self._sleep(min(2**attempt, 8))
                    continue
                return resp
            except HTTPError as exc:
                status = int(exc.code or 0)
                if status in {408, 425, 429, 500, 502, 503, 504} and attempt < self.retries:
                    self._sleep(min(2**attempt, 8))
                    continue
                return HttpResponse(status=status, body=b"")
            except (URLError, TimeoutError, OSError):
                if attempt < self.retries:
                    self._sleep(min(2**attempt, 8))
                    continue
                return None
        return None


def load_vocab(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "vocab.yml"
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def extract_links_from_text(text: str) -> tuple[str | None, str | None]:
    code = None
    project = None
    gh_match = GITHUB_URL_RE.search(text or "")
    if gh_match:
        raw = gh_match.group(0).rstrip(".,;:)\\]")
        full = parse_github_repo(raw)
        if full:
            code = f"https://github.com/{full}"
    proj_match = PROJECT_URL_RE.search(text or "")
    if proj_match:
        project = proj_match.group(0).rstrip(".,;:)\\]")
    return code, project


def load_inbox_candidates(window: WeekWindow, root: Path = ROOT) -> list[dict[str, Any]]:
    """Reuse existing daily metadata/candidates/YYYY-MM-DD/candidates.json without re-fetching."""
    candidates_root = root / "metadata" / "candidates"
    if not candidates_root.exists():
        return []

    results: list[dict[str, Any]] = []
    # Scan window dates plus 2 days after end (in case Sunday papers landed Monday/Tuesday)
    day = window.start
    end_scan = window.end + timedelta(days=2)
    while day <= end_scan:
        cfile = candidates_root / day.isoformat() / "candidates.json"
        if cfile.exists():
            try:
                items = json.loads(cfile.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                items = []
            for item in items:
                if not isinstance(item, dict):
                    continue
                paper_url = str(item.get("paper") or "").strip()
                arxiv_id = arxiv_id_from_url(paper_url)
                pub = str(item.get("published") or "").strip()
                if not arxiv_id or not pub:
                    continue
                if not in_window(pub, window):
                    continue
                abstract = normalize_whitespace(str(item.get("abstract") or ""))
                code_from_abs, proj_from_abs = extract_links_from_text(abstract)
                results.append(
                    {
                        "arxiv_id": arxiv_id,
                        "title": normalize_whitespace(str(item.get("title") or "")),
                        "abstract": abstract,
                        "published_date": pub[:10],
                        "published_raw": pub,
                        "authors": item.get("authors") or [],
                        "links": {
                            "paper": f"https://arxiv.org/abs/{arxiv_id}",
                            "code": item.get("repo") or code_from_abs,
                            "project": item.get("homepage") or proj_from_abs,
                            "hf": None,
                        },
                        "sources": ["daily_inbox"],
                        "source_texts": [
                            {"url": f"https://arxiv.org/abs/{arxiv_id}", "text": abstract}
                        ],
                    }
                )
        day += timedelta(days=1)
    return results


def fetch_arxiv_candidates(
    window: WeekWindow,
    client: HttpClient,
    vocab: dict[str, Any],
    *,
    max_results: int = 50,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Fetch recent generative-model papers from arXiv API and filter to window."""
    errors: list[str] = []
    categories = vocab.get("arxiv_categories") or ["cs.CV", "cs.GR", "cs.LG", "cs.AI", "cs.RO"]
    cat_clause = " OR ".join(f"cat:{c}" for c in categories)
    kw_clause = 'ti:"diffusion" OR ti:"world model" OR ti:"video generation" OR ti:"image generation" OR ti:"3D" OR ti:"4D" OR ti:"flow matching"'
    query = f"({cat_clause}) AND ({kw_clause})"
    url = (
        "https://export.arxiv.org/api/query?search_query="
        + quote(query)
        + f"&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    )
    resp = client.get(url, accept="application/atom+xml,text/xml,*/*")
    if not resp or resp.status != 200:
        code = resp.status if resp else "network_error"
        errors.append(f"arxiv_api: unavailable ({code})")
        return [], errors

    try:
        root = ET.fromstring(resp.body)
    except ET.ParseError as exc:
        errors.append(f"arxiv_api: xml parse error ({exc})")
        return [], errors

    ns = {"a": "http://www.w3.org/2005/Atom"}
    items: list[dict[str, Any]] = []
    for entry in root.findall("a:entry", ns):
        entry_id = entry.findtext("a:id", "", ns) or ""
        arxiv_id = arxiv_id_from_url(entry_id)
        if not arxiv_id:
            continue
        published = (entry.findtext("a:published", "", ns) or "").strip()
        if not in_window(published, window):
            continue
        title = normalize_whitespace(entry.findtext("a:title", "", ns) or "")
        abstract = normalize_whitespace(entry.findtext("a:summary", "", ns) or "")
        authors = [
            normalize_whitespace(a.findtext("a:name", "", ns) or "")
            for a in entry.findall("a:author", ns)
            if normalize_whitespace(a.findtext("a:name", "", ns) or "")
        ]
        code_url, proj_url = extract_links_from_text(abstract)
        items.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "arxiv_api_title": title,
                "abstract": abstract,
                "published_date": published[:10],
                "published_raw": published,
                "authors": authors,
                "links": {
                    "paper": f"https://arxiv.org/abs/{arxiv_id}",
                    "code": code_url,
                    "project": proj_url,
                    "hf": None,
                },
                "sources": ["arxiv_api"],
                "source_texts": [
                    {"url": f"https://arxiv.org/abs/{arxiv_id}", "text": abstract}
                ],
            }
        )
    return items, errors


def fetch_hf_daily_papers(
    window: WeekWindow,
    client: HttpClient,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Fetch Hugging Face Daily Papers (degrades gracefully on error)."""
    errors: list[str] = []
    url = "https://huggingface.co/api/daily_papers?limit=100"
    resp = client.get(url, accept="application/json")
    if not resp or resp.status != 200:
        code = resp.status if resp else "network_error"
        errors.append(f"hf_daily_papers: unavailable ({code})")
        return [], errors

    try:
        payload = json.loads(resp.body.decode("utf-8", errors="ignore"))
    except json.JSONDecodeError as exc:
        errors.append(f"hf_daily_papers: json error ({exc})")
        return [], errors

    if not isinstance(payload, list):
        return [], errors

    items: list[dict[str, Any]] = []
    for row in payload:
        paper = row.get("paper") if isinstance(row, dict) else None
        if not isinstance(paper, dict):
            continue
        arxiv_id = str(paper.get("id") or "").strip()
        if not re.fullmatch(r"[0-9]{4}\.[0-9]{4,5}", arxiv_id):
            continue
        pub = str(paper.get("publishedAt") or row.get("publishedAt") or "").strip()
        if not in_window(pub, window):
            continue
        title = normalize_whitespace(str(paper.get("title") or row.get("title") or ""))
        abstract = normalize_whitespace(str(paper.get("summary") or row.get("summary") or ""))
        authors = [
            normalize_whitespace(str(a.get("name") or ""))
            for a in (paper.get("authors") or [])
            if isinstance(a, dict) and normalize_whitespace(str(a.get("name") or ""))
        ]
        org_obj = paper.get("organization") or row.get("organization") or {}
        org_name = normalize_whitespace(str(org_obj.get("fullname") or org_obj.get("name") or "")) if isinstance(org_obj, dict) else ""
        hf_url = f"https://huggingface.co/papers/{arxiv_id}"
        code_url = paper.get("githubRepo") or None
        if not code_url:
            code_url, _ = extract_links_from_text(abstract)
        proj_url = paper.get("projectPage") or None
        if not proj_url:
            _, proj_url = extract_links_from_text(abstract)
        affiliations_raw: list[dict[str, Any]] = []
        if org_name:
            affiliations_raw.append(
                {
                    "raw": org_name,
                    "source": "huggingface",
                    "url": hf_url,
                    "quote": f"Hugging Face paper organization: {org_name}",
                }
            )
        items.append(
            {
                "arxiv_id": arxiv_id,
                "title": title,
                "abstract": abstract,
                "published_date": pub[:10],
                "published_raw": pub,
                "authors": authors,
                "links": {
                    "paper": f"https://arxiv.org/abs/{arxiv_id}",
                    "code": code_url,
                    "project": proj_url,
                    "hf": hf_url,
                },
                "hf_upvotes": int(paper.get("upvotes") or row.get("upvotes") or 0),
                "affiliations_raw": affiliations_raw,
                "sources": ["hf_daily_papers"],
                "source_texts": [
                    {"url": hf_url, "text": abstract}
                ],
            }
        )
    return items, errors


def enrich_github_repo(
    code_url: str,
    client: HttpClient,
) -> dict[str, Any]:
    """Fetch GitHub repository metadata and README excerpt for identity & openness checks."""
    full_name = parse_github_repo(code_url)
    if not full_name:
        return {}
    resp = client.get(f"https://api.github.com/repos/{full_name}", accept="application/vnd.github+json", is_github=True)
    if not resp or resp.status != 200:
        return {}
    try:
        meta = json.loads(resp.body.decode("utf-8", errors="ignore"))
    except json.JSONDecodeError:
        return {}

    readme_text = ""
    readme_resp = client.get(
        f"https://api.github.com/repos/{full_name}/readme",
        accept="application/vnd.github.raw+json",
        is_github=True,
    )
    if readme_resp and readme_resp.status == 200:
        readme_text = readme_resp.body.decode("utf-8", errors="ignore")[:20_000]

    return {
        "full_name": meta.get("full_name", full_name),
        "stars": int(meta.get("stargazers_count", 0) or 0),
        "created_at": str(meta.get("created_at") or ""),
        "size": int(meta.get("size", 0) or 0),
        "archived": bool(meta.get("archived", False)),
        "license": (meta.get("license") or {}).get("spdx_id") or "",
        "description": normalize_whitespace(str(meta.get("description") or "")),
        "homepage": normalize_whitespace(str(meta.get("homepage") or "")),
        "readme": readme_text,
    }


def enrich_openalex_affiliations(
    arxiv_id: str,
    client: HttpClient,
) -> list[dict[str, Any]]:
    """Auxiliary affiliation lookup via OpenAlex (graceful degradation)."""
    url = f"https://api.openalex.org/works?{urlencode({'search': arxiv_id, 'per-page': 1})}"
    resp = client.get(url, accept="application/json")
    if not resp or resp.status != 200:
        return []
    try:
        payload = json.loads(resp.body.decode("utf-8", errors="ignore"))
    except json.JSONDecodeError:
        return []
    results = payload.get("results") or []
    if not results:
        return []
    work = results[0]
    work_url = str(work.get("id") or url)
    out: list[dict[str, Any]] = []
    seen: set[str] = set()
    for authorship in work.get("authorships") or []:
        for inst in authorship.get("institutions") or []:
            name = normalize_whitespace(str(inst.get("display_name") or ""))
            if name and name.lower() not in seen:
                seen.add(name.lower())
                out.append(
                    {
                        "raw": name,
                        "source": "openalex",
                        "url": work_url,
                        "quote": f"OpenAlex author institution: {name}",
                    }
                )
    return out


def merge_candidates(lists: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    """Merge multi-source candidates by canonical arXiv ID."""
    merged: dict[str, dict[str, Any]] = {}
    for bucket in lists:
        for item in bucket:
            aid = str(item.get("arxiv_id") or "").strip()
            if not aid:
                continue
            if aid not in merged:
                merged[aid] = {
                    **item,
                    "links": dict(item.get("links") or {}),
                    "sources": list(item.get("sources") or []),
                    "affiliations_raw": list(item.get("affiliations_raw") or []),
                    "source_texts": list(item.get("source_texts") or []),
                }
                continue
            cur = merged[aid]
            if item.get("arxiv_api_title"):
                cur["arxiv_api_title"] = item["arxiv_api_title"]
                cur["title"] = item["arxiv_api_title"]
            elif not cur.get("title") and item.get("title"):
                cur["title"] = item["title"]
            if len(item.get("abstract", "")) > len(cur.get("abstract", "")):
                cur["abstract"] = item["abstract"]
            if len(item.get("authors") or []) > len(cur.get("authors") or []):
                cur["authors"] = item["authors"]
            for k in ("paper", "code", "project", "hf"):
                if not cur["links"].get(k) and (item.get("links") or {}).get(k):
                    cur["links"][k] = item["links"][k]
            cur["hf_upvotes"] = max(int(cur.get("hf_upvotes", 0) or 0), int(item.get("hf_upvotes", 0) or 0))
            for s in item.get("sources") or []:
                if s not in cur["sources"]:
                    cur["sources"].append(s)
            cur["affiliations_raw"].extend(item.get("affiliations_raw") or [])
            cur["source_texts"].extend(item.get("source_texts") or [])
    return list(merged.values())


def harvest_week(
    window: WeekWindow,
    *,
    client: HttpClient | None = None,
    root: Path = ROOT,
    offline: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Harvest candidates for `window` from inbox + live APIs (unless offline=True)."""
    errors: list[str] = []
    vocab = load_vocab(root)
    inbox_items = load_inbox_candidates(window, root=root)
    buckets: list[list[dict[str, Any]]] = [inbox_items]

    if not offline:
        http = client or HttpClient()
        arxiv_items, arxiv_errs = fetch_arxiv_candidates(window, http, vocab)
        hf_items, hf_errs = fetch_hf_daily_papers(window, http)
        errors.extend(arxiv_errs)
        errors.extend(hf_errs)
        buckets.extend([arxiv_items, hf_items])

        candidates = merge_candidates(buckets)
        for cand in candidates:
            code_url = (cand.get("links") or {}).get("code")
            if code_url:
                cand["github_meta"] = enrich_github_repo(code_url, http)
            else:
                cand["github_meta"] = {}
            oa_affs = enrich_openalex_affiliations(cand["arxiv_id"], http)
            cand.setdefault("affiliations_raw", []).extend(oa_affs)
        return candidates, errors

    return merge_candidates(buckets), errors
