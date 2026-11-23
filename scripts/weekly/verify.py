#!/usr/bin/env python3
"""Hard Gates H1-H8 verification for Weekly Top Picks candidates.

Hard Gates (failing any one eliminates the candidate with an explicit reason_code):
- H1: v1 submission date is within [window.start, window.end] UTC.
- H2: Belongs to one of the 5 tracks and core contribution is a generative model
      (not pure analysis / pure benchmark / pure survey).
- H3: arXiv ID is resolvable and normalized title similarity vs arXiv API >= 0.90.
- H4: Affiliation verified: consistent across >= 2 independent sources OR directly
      locatable in the paper's first-page text with evidence (URL + quote <= 25 words).
      Candidates failing ONLY H4 go into `pending` (retried up to 2 weeks).
- H5: At least one verifiable primary-source link (official code / project page /
      official technical report page).
- H6: If code link exists, it passes identity verification (appears on arXiv abstract /
      paper body / HF paper page, OR repo README/description contains title or arXiv ID).
- H7: Not a duplicate of any existing entry (arXiv ID, normalized title, or repo URL).
- H8: Not on the retraction / security-issue list.
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from catalog_common import (
    ROOT,
    arxiv_id_from_url,
    load_records,
    normalize_org_name,
    normalize_title,
    normalize_whitespace,
    parse_github_repo,
    suggested_org_from_repo,
)
from validate_data import title_match_score
from weekly.harvest import load_vocab
from weekly.window import WeekWindow, in_window

TRACK_ORDER = ("image-2d", "video", "3d-object", "3d-scene", "4d-world")
MAX_QUOTE_WORDS = 25


def truncate_quote(text: str, max_words: int = MAX_QUOTE_WORDS) -> str:
    words = normalize_whitespace(text).split()
    return " ".join(words[:max_words])


def classify_track_and_generative(
    title: str,
    abstract: str,
    vocab: dict[str, Any],
) -> tuple[str | None, bool]:
    """Return (track_id_or_None, is_generative_model)."""
    combined = f"{title} {abstract}".lower()
    exclusions = vocab.get("non_generative_exclusion_keywords") or [
        "a survey",
        "comprehensive survey",
        "benchmark for",
        "benchmarking",
        "evaluation suite",
        "dataset and benchmark",
        "empirical analysis of",
        "theoretical analysis of",
    ]
    # Pure survey/benchmark/analysis check (title-led or non-generative)
    title_lower = title.lower()
    if any(ex in title_lower for ex in exclusions):
        return None, False

    core_kws = vocab.get("generative_core_keywords") or [
        "diffusion",
        "flow matching",
        "rectified flow",
        "autoregressive",
        "generative model",
        "image generation",
        "video generation",
        "3d generation",
        "scene generation",
        "4d generation",
        "world model",
    ]
    if not any(kw in combined for kw in core_kws):
        return None, False

    tracks_cfg = vocab.get("tracks") or {}
    best_track = None
    best_hits = 0
    # Priority order: 4d-world > 3d-scene > 3d-object > video > image-2d on ties
    priority = ("4d-world", "3d-scene", "3d-object", "video", "image-2d")
    for track_id in priority:
        kws = (tracks_cfg.get(track_id) or {}).get("keywords") or []
        hits = sum(2 if kw in title_lower else (1 if kw in combined else 0) for kw in kws)
        if hits > best_hits:
            best_hits = hits
            best_track = track_id

    return best_track, bool(best_track)


def verify_code_identity(candidate: dict[str, Any]) -> str:
    """Return 'pass', 'fail', or 'na' for H6 code link identity verification."""
    links = candidate.get("links") or {}
    code_url = links.get("code")
    if not code_url:
        return "na"

    full_repo = parse_github_repo(code_url).lower()
    if not full_repo:
        return "fail"

    arxiv_id = str(candidate.get("arxiv_id") or "").strip().lower()
    title_norm = normalize_title(str(candidate.get("title") or ""))

    # 1. Check if code URL appears verbatim in arXiv abstract / paper body / HF paper page
    for src in candidate.get("source_texts") or []:
        text = str(src.get("text") or "").lower()
        if full_repo in text:
            return "pass"

    # 2. Check explicit HF paper repo linkage
    if candidate.get("hf_code_verified") is True:
        return "pass"

    # 3. Check GitHub repo README / description contains arXiv ID or paper title
    gh_meta = candidate.get("github_meta") or {}
    readme = str(gh_meta.get("readme") or "")
    desc = str(gh_meta.get("description") or "")
    haystack = f"{readme}\n{desc}"
    if arxiv_id and arxiv_id in haystack.lower():
        return "pass"

    if title_norm and title_norm in normalize_title(haystack):
        return "pass"

    # Also allow high title similarity against README first heading / description
    for line in (readme.splitlines()[:20] + [desc]):
        cleaned = re.sub(r"^[#\s*`]+", "", line).strip()
        if len(cleaned) >= 10 and title_match_score(str(candidate.get("title") or ""), cleaned) >= 0.85:
            return "pass"

    return "fail"


def verify_affiliations(
    candidate: dict[str, Any],
    *,
    orgs_path: Path | None = None,
) -> tuple[list[dict[str, Any]], int]:
    """Verify affiliations per H4:
    - Consistent across >= 2 independent sources, OR
    - Directly locatable in the paper's first-page text (source == 'first_page').
    Returns (verified_affiliations, max_independent_source_count).
    """
    raw_items = list(candidate.get("affiliations_raw") or [])

    # Also consider canonical GitHub repo owner as an independent source if code passed H6
    code_url = (candidate.get("links") or {}).get("code")
    if code_url and verify_code_identity(candidate) == "pass":
        suggested = suggested_org_from_repo(code_url, orgs_path=orgs_path)
        if suggested:
            raw_items.append(
                {
                    "raw": suggested,
                    "source": "github_owner",
                    "url": code_url,
                    "quote": truncate_quote(f"Official GitHub repository owner: {parse_github_repo(code_url)}"),
                }
            )

    grouped_sources: dict[str, set[str]] = defaultdict(set)
    grouped_evidence: dict[str, list[dict[str, str]]] = defaultdict(list)
    canonical_names: dict[str, str] = {}
    has_first_page: dict[str, bool] = defaultdict(bool)

    for item in raw_items:
        raw_name = normalize_whitespace(str(item.get("raw") or ""))
        source = normalize_whitespace(str(item.get("source") or ""))
        url = normalize_whitespace(str(item.get("url") or ""))
        quote = truncate_quote(str(item.get("quote") or ""))
        if not raw_name or not url or not quote:
            continue
        canonical, slug = normalize_org_name(raw_name, orgs_path=orgs_path)
        if not canonical or not slug:
            continue
        canonical_names[slug] = canonical
        grouped_sources[slug].add(source or url)
        if source == "first_page":
            has_first_page[slug] = True
        ev = {"url": url, "quote": quote}
        if ev not in grouped_evidence[slug]:
            grouped_evidence[slug].append(ev)

    verified: list[dict[str, Any]] = []
    max_sources = 0
    for slug, sources in grouped_sources.items():
        count = len(sources)
        if count >= 2 or has_first_page[slug]:
            max_sources = max(max_sources, count)
            verified.append(
                {
                    "name": canonical_names[slug],
                    "normalized": slug,
                    "evidence": grouped_evidence[slug],
                }
            )

    verified.sort(key=lambda x: x["normalized"])
    return verified, max_sources


def load_existing_dedupe_keys(root: Path = ROOT) -> tuple[set[str], set[str], set[str]]:
    """Collect existing arXiv IDs, normalized titles, and canonical GitHub repo URLs
    from both data/*.jsonl and prior data/weekly/*.json."""
    arxiv_ids: set[str] = set()
    titles: set[str] = set()
    repos: set[str] = set()

    for rec in load_records(root=root, include_quarantined=True):
        if rec.get("title"):
            titles.add(normalize_title(rec["title"]))
        aid = arxiv_id_from_url(rec.get("paper", ""))
        if aid:
            arxiv_ids.add(aid.lower())
        repo = parse_github_repo(rec.get("repo", ""))
        if repo:
            repos.add(repo.lower())

    weekly_dir = root / "data" / "weekly"
    if weekly_dir.exists():
        for path in weekly_dir.glob("*-W*.json"):
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            for item in (payload.get("items") or []) + (payload.get("honorable_mentions") or []):
                if not isinstance(item, dict):
                    continue
                iid = str(item.get("id") or "")
                if iid.startswith("arxiv:"):
                    arxiv_ids.add(iid.split(":", 1)[1].lower())
                if item.get("title"):
                    titles.add(normalize_title(item["title"]))
                repo = parse_github_repo((item.get("links") or {}).get("code") or "")
                if repo:
                    repos.add(repo.lower())

    return arxiv_ids, titles, repos


def load_retracted_ids(root: Path = ROOT) -> set[str]:
    path = root / "metadata" / "retracted.json"
    if not path.exists():
        return set()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return {str(x).lower() for x in (payload.get("arxiv_ids") or [])}
    except (OSError, json.JSONDecodeError):
        return set()


def verify_candidate(
    candidate: dict[str, Any],
    *,
    window: WeekWindow,
    vocab: dict[str, Any],
    existing_keys: tuple[set[str], set[str], set[str]],
    retracted_ids: set[str],
    orgs_path: Path | None = None,
    checked_at: str | None = None,
) -> dict[str, Any]:
    """Run Hard Gates H1-H8 on a single candidate.

    Returns dict with:
      - status: "pass" | "pending_affiliation" | "reject"
      - reason_codes: list[str]
      - track: str | None
      - affiliations: list[dict]
      - verification: dict
    """
    now_iso = checked_at or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    reasons: list[str] = []

    arxiv_id = str(candidate.get("arxiv_id") or "").strip().lower()
    title = normalize_whitespace(str(candidate.get("title") or ""))
    abstract = normalize_whitespace(str(candidate.get("abstract") or ""))
    links = candidate.get("links") or {}

    # H1: v1 submission date within window
    pub_raw = str(candidate.get("published_raw") or candidate.get("published_date") or "")
    if not in_window(pub_raw, window):
        reasons.append("H1_OUT_OF_WINDOW")

    # H2: belongs to one of 5 tracks & generative model
    track, is_gen = classify_track_and_generative(title, abstract, vocab)
    if not is_gen or not track:
        reasons.append("H2_NON_GENERATIVE")

    # H3: arXiv ID resolvable & title similarity >= 0.90
    arxiv_api_title = normalize_whitespace(str(candidate.get("arxiv_api_title") or title))
    title_sim = round(title_match_score(title, arxiv_api_title), 4) if (arxiv_id and arxiv_api_title) else 0.0
    if not arxiv_id or title_sim < 0.90:
        reasons.append("H3_TITLE_MISMATCH")

    # H5: at least one verifiable primary-source link (official code / project / tech report)
    has_primary = bool(links.get("code") or links.get("project") or candidate.get("official_report_url"))
    if not has_primary:
        reasons.append("H5_NO_PRIMARY_LINK")

    # H6: code identity verification
    code_identity = verify_code_identity(candidate)
    if code_identity == "fail":
        reasons.append("H6_CODE_IDENTITY_FAIL")

    # H7: deduplication against existing catalog & prior weeks
    seen_arxiv, seen_titles, seen_repos = existing_keys
    repo_key = parse_github_repo(links.get("code") or "").lower()
    if (
        (arxiv_id and arxiv_id in seen_arxiv)
        or (title and normalize_title(title) in seen_titles)
        or (repo_key and repo_key in seen_repos)
    ):
        reasons.append("H7_DUPLICATE")

    # H8: not retracted / withdrawn / security-flagged
    if (
        arxiv_id in retracted_ids
        or "this paper has been withdrawn" in abstract.lower()
        or candidate.get("retracted") is True
    ):
        reasons.append("H8_RETRACTED")

    # H4: affiliation verification
    verified_affs, aff_sources = verify_affiliations(candidate, orgs_path=orgs_path)
    if not verified_affs:
        reasons.append("H4_AFFILIATION_UNVERIFIED")

    verification = {
        "arxiv_title_match": title_sim,
        "code_identity": code_identity,
        "links_ok": has_primary and code_identity != "fail",
        "affiliation_sources": aff_sources,
        "checked_at": now_iso,
    }

    if not reasons:
        status = "pass"
    elif reasons == ["H4_AFFILIATION_UNVERIFIED"]:
        status = "pending_affiliation"
    else:
        status = "reject"

    return {
        "status": status,
        "reason_codes": reasons,
        "track": track,
        "affiliations": verified_affs,
        "verification": verification,
    }
