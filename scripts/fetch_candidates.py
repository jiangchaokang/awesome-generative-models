#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from catalog_common import (
    ROOT,
    SCOPE_START_DATE,
    WATCH_ORGS,
    arxiv_id_from_url,
    load_records,
    normalize_title,
    parse_github_repo,
)

OUT_DIR = ROOT / "metadata" / "candidates"
SEEN_INDEX_PATH = OUT_DIR / "seen_index.json"
TIMEOUT = 20

# A candidate must clear this score to be worth a human's attention. This is
# the "quality only" gate: everything below it is dropped before it ever
# reaches candidates.json / report.md.
MIN_SCORE_ARXIV = 38
MIN_SCORE_GITHUB = 40

# Per-day scratch files are disposable once folded into SEEN_INDEX_PATH, so
# only a recent rolling window is kept on disk -- otherwise the inbox grows
# forever (98+ dated folders / 18MB+ before this fix) while nobody reviews it.
RETENTION_DAYS = 30

# Long-term memory of every candidate ever surfaced, keyed by a stable
# identity (arXiv id or GitHub repo full name). Without this, an item that
# is not merged into data/*.jsonl reappears as "new" in every single daily
# report forever. Entries older than this TTL are forgotten and may resurface
# for one more look.
SEEN_TTL_DAYS = 365


ARXIV_QUERIES = {
    "image-2d": [
        "text-to-image generation technical report",
        "image generation foundation model",
        "image generation diffusion transformer",
        "image generation rectified flow",
        "text rendering image generation",
    ],
    "video": [
        "video foundation model",
        "text-to-video generation technical report",
        "image-to-video generation",
        "video editing diffusion",
        "surround-view video generation",
    ],
    "3d-object-asset": [
        "3D asset generation",
        "image-to-3D generation",
        "text-to-3D generation",
        "part-aware 3D generation",
        "controllable 3D asset generation",
    ],
    "3d-scene": [
        "3D scene generation",
        "explorable 3D scene generation",
        "single image to 3D scene",
        "indoor scene generation",
        "gaussian splatting scene generation",
    ],
    "4d-dynamic-scene-world": [
        "world model technical report",
        "interactive world model",
        "autonomous driving world model",
        "explorable 3D world generation",
        "simulation capable world model",
    ],
}

KEYWORDS = {
    "image-2d": ["text-to-image", "image generation", "diffusion", "flux", "rectified flow", "t2i"],
    "video": ["video generation", "text-to-video", "image-to-video", "video editing", "human animation", "surround-view"],
    "3d-object-asset": ["3d", "text-to-3d", "image-to-3d", "mesh", "avatar", "asset", "shape generation"],
    "3d-scene": ["3d scene", "layout", "indoor scene", "outdoor scene", "navigable", "scene generation"],
    "4d-dynamic-scene-world": ["world model", "autonomous driving", "simulation", "interactive world", "4d", "game world", "closed-loop"],
}

TOP_LAB_HINTS = [
    "google", "deepmind", "nvidia", "nvlabs", "waymo",
    "tencent", "hunyuan", "tencentarc",
    "alibaba", "qwen", "wan", "vilab",
    "bytedance", "seed", "adobe", "xiaomi", "tesla",
    "mit", "berkeley", "tsinghua", "sjtu",
]

MODEL_FAMILY_HINTS = [
    "qwen-image", "hunyuanimage", "seedream", "seedance",
    "wan2.1", "wan2.2", "sana", "cosmos",
    "hunyuanvideo", "hunyuan3d", "hunyuanworld",
    "voyager", "worldplay", "flashworld", "vectorworld",
]

def normalize_match_text(text: str) -> str:
    """Lowercase and turn hyphen/underscore/slash separators into spaces so
    phrase- and token-matching both operate on the same normalized form."""
    text = (text or "").lower()
    text = re.sub(r"[-_/]+", " ", text)
    return " ".join(text.split())

def matches_keyword(keyword: str, norm_text: str, tokens: set[str]) -> bool:
    """Word-aware keyword match.

    Multi-word phrases (e.g. "text-to-video") match as substrings of the
    normalized text, which is safe because an accidental match is very
    unlikely. Single words must match a *whole token*, not a substring --
    this is what stops an ambiguous keyword like "mesh" from falsely
    matching inside an unrelated repo topic such as "polarismesh".
    """
    norm_kw = normalize_match_text(keyword)
    if not norm_kw:
        return False
    if " " in norm_kw:
        return f" {norm_kw} " in f" {norm_text} "
    return norm_kw in tokens

def matches_any_keyword(keywords: list[str], text: str) -> bool:
    norm_text = normalize_match_text(text)
    tokens = set(norm_text.split())
    return any(matches_keyword(kw, norm_text, tokens) for kw in keywords)

def write_json(path: Path, data: dict | list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def api_headers(token: str = "") -> dict:
    headers = {
        "User-Agent": "awesome-generative-models/3.0",
        "Accept": "application/vnd.github+json",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def load_existing_keys() -> tuple[set[str], set[str], set[str]]:
    records = load_records()
    title_keys: set[str] = set()
    repo_keys: set[str] = set()
    paper_keys: set[str] = set()

    for rec in records:
        title_keys.add(normalize_title(rec["title"]))
        if rec.get("repo"):
            repo = parse_github_repo(rec["repo"])
            if repo:
                repo_keys.add(repo.lower())
        if rec.get("paper"):
            paper_keys.add(rec["paper"].rstrip("/").lower())

    return title_keys, repo_keys, paper_keys

def guess_artifact(text: str) -> str:
    lowered = (text or "").lower()

    if any(k in lowered for k in ["world model", "autonomous driving", "simulation", "interactive world", "4d", "closed-loop", "game world"]):
        return "4d-dynamic-scene-world"
    if any(k in lowered for k in ["3d scene", "layout", "indoor scene", "outdoor scene", "navigable scene"]):
        return "3d-scene"
    if any(k in lowered for k in ["text-to-3d", "image-to-3d", "3d asset", "3d shape", "mesh", "avatar", "object generation"]):
        return "3d-object-asset"
    if any(k in lowered for k in ["video generation", "text-to-video", "image-to-video", "video editing", "human animation", "surround-view"]):
        return "video"
    return "image-2d"

def guess_task(artifact: str, text: str) -> str:
    lowered = (text or "").lower()

    if artifact == "image-2d":
        if "personal" in lowered:
            return "personalization"
        if "safe" in lowered or "alignment" in lowered:
            return "alignment-safety"
        if "control" in lowered:
            return "controllable-generation"
        if "one-step" in lowered or "efficient" in lowered or "distill" in lowered:
            return "model-efficiency"
        return "text-to-image"

    if artifact == "video":
        if "editing" in lowered:
            return "video-editing"
        if "human" in lowered or "animation" in lowered:
            return "human-animation"
        if "image-to-video" in lowered or "i2v" in lowered:
            return "image-to-video"
        if "surround-view" in lowered:
            return "surround-view-video"
        if "long video" in lowered or "minute-long" in lowered:
            return "long-video"
        if "driving" in lowered or "autonomous" in lowered:
            return "autonomous-driving-video"
        return "text-to-video"

    if artifact == "3d-object-asset":
        if "avatar" in lowered:
            return "human-avatar"
        if "articulated" in lowered:
            return "articulated-asset"
        if "part" in lowered:
            return "part-aware-generation"
        if "image-to-3d" in lowered:
            return "image-to-3d"
        if "text-to-3d" in lowered:
            return "text-to-3d"
        return "3d-shape-generation"

    if artifact == "3d-scene":
        if "layout" in lowered:
            return "layout-to-scene"
        if "indoor" in lowered:
            return "indoor"
        if "outdoor" in lowered or "urban" in lowered:
            return "outdoor-urban"
        if "edit" in lowered:
            return "scene-editing"
        if "single image" in lowered:
            return "single-image-to-scene"
        if "agent" in lowered:
            return "agentic-scene-generation"
        return "general-scene-generation"

    if "simulation" in lowered:
        return "simulation"
    if "game" in lowered:
        return "game-worlds"
    if "robot" in lowered:
        return "robotics-worlds"
    if "autonomous" in lowered or "driving" in lowered:
        return "autonomous-driving"
    if "4d" in lowered:
        return "4d-generation"
    return "world-models"

def arxiv_query(terms: list[str]) -> str:
    return " OR ".join(f'all:"{term}"' for term in terms)

def fetch_arxiv(query: str, max_results: int = 40) -> list[dict]:
    url = (
        "http://export.arxiv.org/api/query?search_query="
        + quote(query)
        + f"&start=0&max_results={max_results}"
        + "&sortBy=submittedDate&sortOrder=descending"
    )
    request = Request(url, headers={"User-Agent": "awesome-generative-models/3.0"})
    try:
        with urlopen(request, timeout=TIMEOUT) as response:
            xml_data = response.read()
    except Exception as exc:
        return [{"error": str(exc)}]

    root = ET.fromstring(xml_data)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items: list[dict] = []

    for entry in root.findall("a:entry", ns):
        title = " ".join((entry.findtext("a:title", "", ns) or "").split())
        abstract = " ".join((entry.findtext("a:summary", "", ns) or "").split())
        paper = entry.findtext("a:id", "", ns) or ""
        published = entry.findtext("a:published", "", ns) or ""
        items.append(
            {
                "title": title,
                "abstract": abstract,
                "paper": paper,
                "published": published,
            }
        )
    return items

def github_org_repos(org: str, token: str) -> list[dict]:
    # Sort by creation date, not last-update: `updated`/`pushed` is bumped by
    # any trivial commit on a repo that may be years old, which is what
    # previously let ancient projects resurface as "new" candidates.
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100&type=public&sort=created&direction=desc"
    request = Request(url, headers=api_headers(token))
    try:
        with urlopen(request, timeout=TIMEOUT) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        return [{"error": f"HTTP {exc.code}"}]
    except URLError as exc:
        return [{"error": str(exc.reason)}]
    except Exception as exc:
        return [{"error": str(exc)}]

def score_arxiv_candidate(item: dict, now: datetime) -> int:
    score = 20
    text = f"{item['title']} {item['abstract']}".lower()

    try:
        published_dt = datetime.fromisoformat(item["published"].replace("Z", "+00:00"))
        age_days = max(0, (now - published_dt).days)
        score += max(0, 30 - age_days)
    except Exception:
        pass

    if matches_any_keyword(["code", "open-source", "opensource", "release", "weights", "github"], text):
        score += 18

    # Word-aware matching matters here: several lab hints are short, common
    # English words (e.g. "mit", "wan", "seed") that would otherwise falsely
    # match inside unrelated words like "submit", "wanted", or "random seed".
    if matches_any_keyword(TOP_LAB_HINTS, text):
        score += 10

    if matches_any_keyword(MODEL_FAMILY_HINTS, text):
        score += 12

    if matches_any_keyword([
        "world model", "interactive world", "closed-loop", "autonomous driving",
        "3d scene", "3d asset", "video foundation model", "surround-view",
    ], text):
        score += 10

    if matches_any_keyword(["survey", "benchmark"], text) and "generation" not in text and "world model" not in text:
        score -= 6

    return score

def score_github_candidate(item: dict, now: datetime) -> int:
    # Every candidate scored here already comes from a hand-curated WATCH_ORGS
    # entry, which is itself a strong quality signal (a top research org),
    # independent of whether that org name happens to also appear in the
    # repo's own name/description/topics.
    score = 15 + 12
    text = f"{item.get('name', '')} {item.get('description', '')} {' '.join(item.get('topics', []))}".lower()

    # Reward true novelty -- when the repo was actually created -- not merely
    # "was pushed to recently", which any routine commit satisfies even for a
    # repo that is years old.
    try:
        created_dt = datetime.fromisoformat(item["created_at"].replace("Z", "+00:00"))
        age_days = max(0, (now - created_dt).days)
        score += max(0, 24 - age_days)
    except Exception:
        pass

    score += min(int(item.get("stargazers_count", 0) or 0) // 50, 25)

    if matches_any_keyword(TOP_LAB_HINTS, text):
        score += 10

    if matches_any_keyword(MODEL_FAMILY_HINTS, text):
        score += 12

    if matches_any_keyword([
        "world-model", "video-generation", "image-to-video",
        "scene-generation", "3d-generation", "autonomous-driving",
    ], text):
        score += 10

    return score

def dedupe_candidates(items: list[dict]) -> list[dict]:
    seen: set[tuple[str, str]] = set()
    out: list[dict] = []

    for item in sorted(items, key=lambda x: (-int(x.get("score", 0)), x.get("title", "").lower())):
        key = (item.get("source", ""), normalize_title(item.get("title", "")))
        if key in seen:
            continue
        seen.add(key)
        out.append(item)

    return out

def build_report(candidates: list[dict], watched_repos: list[dict], days: int, fetch_errors: list[str] | None = None) -> str:
    now_text = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    by_artifact: dict[str, list[dict]] = {}
    for item in candidates:
        by_artifact.setdefault(item["artifact"], []).append(item)

    lines = [
        "# 📬 Daily Candidate Inbox",
        "",
        "> Auto-generated harvesting report. **Manual review is required before touching `data/*.jsonl`.**",
        "> Shows only items never surfaced in an earlier run — a delta, not a re-scan.",
        "",
        f"- Generated: `{now_text}`",
        f"- Scope floor: **{SCOPE_START_DATE.isoformat()}** — anything published/created earlier is dropped automatically",
        f"- Lookback window: last **{days}** days",
        f"- Raw files: `metadata/candidates/{datetime.now(timezone.utc).strftime('%Y-%m-%d')}/`",
        f"- New candidates today: **{len(candidates)}**",
        f"- New watched-org repositories today: **{len(watched_repos)}**",
        "",
    ]

    if fetch_errors:
        # Surfaced separately from the counts above on purpose: "0 new" must
        # never be ambiguous between "genuinely nothing new" and "a source
        # failed to respond", otherwise an outage silently looks like a quiet
        # day instead of a pipeline problem worth investigating.
        lines.extend(["## ⚠️ Fetch Errors", "", "Some sources could not be reached this run; today's report may be incomplete for those sources only.", ""])
        lines.extend(f"- {item}" for item in fetch_errors)
        lines.append("")

    lines.extend([
        "## Review Checklist",
        "",
        "- Is the artifact classification correct?",
        "- Is the link exact and canonical?",
        "- Is the summary worth writing for the public catalog?",
        "- Does it belong in the main catalog or only in the watchlist?",
        "",
    ])

    for artifact, items in sorted(by_artifact.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines.extend([f"## {artifact}", ""])
        lines.extend(["| Score | Source | Date | Candidate | Suggested Task | Why it matters | Links |", "|--:|:--|:--|:--|:--|:--|:--|"])

        for item in sorted(items, key=lambda x: (-int(x["score"]), x["title"].lower())):
            links = []
            if item.get("paper"):
                links.append(f"[Paper]({item['paper']})")
            if item.get("repo"):
                links.append(f"[Repo]({item['repo']})")
            if item.get("homepage"):
                links.append(f"[Home]({item['homepage']})")

            date_str = item.get("published", "")[:10] or item.get("created_at", "")[:10] or item.get("updated_at", "")[:10]
            lines.append(
                f"| {item['score']} | {item['source']} | {date_str} | "
                f"**{item['title']}** | {item.get('task', '—')} | {item.get('why', '—')} | "
                f"{' / '.join(links) if links else '—'} |"
            )
        lines.append("")

    lines.extend(["## New Repositories in Watched Organizations", ""])
    if watched_repos:
        lines.extend(["| Organization | Repo | Stars | Created | Why it may matter |", "|:--|:--|--:|:--|:--|"])
        for repo in sorted(watched_repos, key=lambda r: (-int(r.get("stargazers_count", 0)), r["full_name"].lower())):
            lines.append(
                f"| {repo['watch_org']} | [{repo['full_name']}]({repo['html_url']}) | "
                f"{int(repo.get('stargazers_count', 0) or 0)} | {repo.get('created_at', '')[:10]} | "
                f"{repo.get('why', '—')} |"
            )
    else:
        lines.append("- No new watched-org repositories were found.")
    lines.append("")

    return "\n".join(lines)

def create_github_issue(report_path: Path, total: int) -> None:
    title = f"📬 Daily candidates — {datetime.now(timezone.utc).strftime('%Y-%m-%d')} ({total} items)"
    try:
        subprocess.run(
            [
                "gh",
                "issue",
                "create",
                "--title",
                title,
                "--body-file",
                str(report_path),
                "--label",
                "daily-candidates",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        print(f"[fetch] created issue: {title}")
    except FileNotFoundError:
        print("[fetch] gh CLI not found, skipping issue creation.")
    except subprocess.CalledProcessError as exc:
        print(f"[fetch] failed to create issue: {exc.stderr}")

def load_seen_index() -> dict:
    if SEEN_INDEX_PATH.exists():
        try:
            data = json.loads(SEEN_INDEX_PATH.read_text(encoding="utf-8"))
            return {"arxiv": dict(data.get("arxiv", {})), "github": dict(data.get("github", {}))}
        except Exception:
            pass
    return {"arxiv": {}, "github": {}}

def prune_seen_index(index: dict, now: datetime) -> dict:
    """Drop ledger entries older than SEEN_TTL_DAYS so an item that was never
    merged gets one more chance to be reconsidered instead of being forgotten
    forever, while still keeping the ledger small."""
    pruned: dict = {"arxiv": {}, "github": {}}
    for bucket in ("arxiv", "github"):
        for key, seen_date in index.get(bucket, {}).items():
            try:
                seen_dt = datetime.strptime(seen_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            except Exception:
                continue
            if (now - seen_dt).days <= SEEN_TTL_DAYS:
                pruned[bucket][key] = seen_date
    return pruned

def prune_old_candidate_dirs(today: str) -> None:
    """Keep only a rolling window of raw dated folders on disk. Long-term
    dedupe memory lives in the compact SEEN_INDEX_PATH instead, so nothing of
    value is lost -- this only removes scratch files nobody reviewed in time."""
    if not OUT_DIR.exists():
        return
    cutoff = datetime.strptime(today, "%Y-%m-%d") - timedelta(days=RETENTION_DAYS)
    for child in OUT_DIR.iterdir():
        if not child.is_dir():
            continue
        try:
            child_date = datetime.strptime(child.name, "%Y-%m-%d")
        except ValueError:
            continue
        if child_date < cutoff:
            shutil.rmtree(child, ignore_errors=True)

def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest daily candidate papers and repo updates.")
    parser.add_argument("--days", type=int, default=14, help="Lookback window in days.")
    parser.add_argument("--issue", action="store_true", help="Create a GitHub issue.")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN", "").strip()
    existing_titles, existing_repos, existing_papers = load_existing_keys()

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=args.days)
    today = now.strftime("%Y-%m-%d")

    # Cross-day memory: an item already surfaced once must not be reported as
    # "new" again tomorrow just because nobody has reviewed it yet.
    seen_index = prune_seen_index(load_seen_index(), now)
    all_keywords = [kw for values in KEYWORDS.values() for kw in values]

    new_candidates: list[dict] = []
    watched_repos: list[dict] = []
    fetch_errors: list[str] = []

    # --- arXiv harvesting: `published` (first submission) is the true
    # novelty signal, and is always checked against the hard SCOPE_START_DATE
    # floor regardless of --days. ---
    for artifact, terms in ARXIV_QUERIES.items():
        items = fetch_arxiv(arxiv_query(terms))
        if items and "error" in items[0]:
            fetch_errors.append(f"arXiv query for `{artifact}` failed: {items[0]['error']}")
            continue

        for item in items:
            try:
                published_dt = datetime.fromisoformat(item["published"].replace("Z", "+00:00"))
            except Exception:
                continue

            if published_dt < since or published_dt.date() < SCOPE_START_DATE:
                continue

            arxiv_key = arxiv_id_from_url(item["paper"]) or normalize_title(item["title"])
            if arxiv_key in seen_index["arxiv"]:
                continue

            title_key = normalize_title(item["title"])
            paper_key = item["paper"].rstrip("/").lower()

            if title_key in existing_titles or paper_key in existing_papers:
                continue

            score = score_arxiv_candidate(item, now)
            if score < MIN_SCORE_ARXIV:
                continue

            text = f"{item['title']} {item['abstract']}"
            artifact_guess = guess_artifact(text)
            task_guess = guess_task(artifact_guess, text)

            new_candidates.append(
                {
                    "source": "arXiv",
                    "artifact": artifact_guess,
                    "task": task_guess,
                    "title": item["title"],
                    "paper": item["paper"],
                    "repo": "",
                    "homepage": "",
                    "abstract": item["abstract"],
                    "published": item["published"],
                    "score": score,
                    "why": "recent paper candidate",
                }
            )
            seen_index["arxiv"][arxiv_key] = today

    # --- watched GitHub org repos: `created_at` is the true novelty signal,
    # never `updated_at`/`pushed_at`, which any trivial commit bumps even on
    # a repo that is many years old and completely out of scope. ---
    for watch in WATCH_ORGS:
        org_name = watch["name"]
        org_slug = watch["github"]

        repos = github_org_repos(org_slug, token=token)
        if repos and "error" in repos[0]:
            fetch_errors.append(f"GitHub org `{org_slug}` ({org_name}) failed: {repos[0]['error']}")
            continue

        for repo in repos:
            if repo.get("private"):
                continue

            try:
                created_dt = datetime.fromisoformat(repo["created_at"].replace("Z", "+00:00"))
            except Exception:
                continue

            if created_dt < since or created_dt.date() < SCOPE_START_DATE:
                continue

            full_name = repo.get("full_name", "")
            repo_key = full_name.lower()
            if repo_key in existing_repos or repo_key in seen_index["github"]:
                continue

            text = " ".join(
                [
                    repo.get("name", ""),
                    repo.get("description", "") or "",
                    " ".join(repo.get("topics", []) or []),
                ]
            )

            # Word-aware match: prevents e.g. "mesh" from falsely matching
            # inside an unrelated topic like "polarismesh".
            if not matches_any_keyword(all_keywords, text):
                continue

            score = score_github_candidate(repo, now)
            if score < MIN_SCORE_GITHUB:
                continue

            lowered = text.lower()
            artifact_guess = guess_artifact(lowered)
            task_guess = guess_task(artifact_guess, lowered)

            why = f"new repository in watched organization `{org_name}`"
            watched_repos.append(
                {
                    "watch_org": org_name,
                    "full_name": full_name,
                    "html_url": repo.get("html_url", ""),
                    "stargazers_count": int(repo.get("stargazers_count", 0) or 0),
                    "created_at": repo.get("created_at", ""),
                    "updated_at": repo.get("updated_at", ""),
                    "why": why,
                }
            )

            title_key = normalize_title(repo.get("name", ""))
            if title_key not in existing_titles:
                new_candidates.append(
                    {
                        "source": "GitHub",
                        "artifact": artifact_guess,
                        "task": task_guess,
                        "title": repo.get("name", ""),
                        "paper": "",
                        "repo": repo.get("html_url", ""),
                        "homepage": repo.get("homepage", "") or "",
                        "abstract": repo.get("description", "") or "",
                        "published": "",
                        "created_at": repo.get("created_at", ""),
                        "updated_at": repo.get("updated_at", ""),
                        "score": score,
                        "why": why,
                    }
                )

            seen_index["github"][repo_key] = today

    new_candidates = dedupe_candidates(new_candidates)

    day_dir = OUT_DIR / today
    day_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(new_candidates, watched_repos, args.days, fetch_errors)

    write_json(day_dir / "candidates.json", new_candidates)
    write_json(day_dir / "watched_repos.json", watched_repos)
    (day_dir / "report.md").write_text(report.rstrip() + "\n", encoding="utf-8")

    write_json(OUT_DIR / "latest.json", new_candidates)
    (OUT_DIR / "latest.md").write_text(report.rstrip() + "\n", encoding="utf-8")
    write_json(SEEN_INDEX_PATH, seen_index)

    prune_old_candidate_dirs(today)

    print(
        f"[fetch] wrote {len(new_candidates)} new candidates "
        f"({len(watched_repos)} watched-org repos) to metadata/candidates/latest.md"
    )
    if fetch_errors:
        print(f"[fetch] {len(fetch_errors)} source(s) failed and were skipped (see report.md):")
        for item in fetch_errors:
            print(f"  - {item}")

    if args.issue and new_candidates:
        create_github_issue(day_dir / "report.md", len(new_candidates))

if __name__ == "__main__":
    main()
