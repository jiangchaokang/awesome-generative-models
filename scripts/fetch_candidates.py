#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from catalog_common import ROOT, WATCH_ORGS, load_records, normalize_title, parse_github_repo

OUT_DIR = ROOT / "metadata" / "candidates"
TIMEOUT = 20

ARXIV_QUERIES = {
    "image-2d": [
        "text-to-image generation",
        "controllable image generation",
        "image generation diffusion transformer",
        "one-step generative model image",
        "image generation rectified flow",
    ],
    "video": [
        "text-to-video generation",
        "image-to-video generation",
        "video editing diffusion",
        "human animation diffusion",
        "surround-view video generation",
    ],
    "3d-object-asset": [
        "text-to-3D generation",
        "image-to-3D generation",
        "3D asset generation",
        "3D shape generation diffusion",
    ],
    "3d-scene": [
        "3D scene generation",
        "layout guided 3D scene",
        "indoor scene generation",
        "outdoor scene generation 3D",
    ],
    "4d-dynamic-scene-world": [
        "world model autonomous driving",
        "interactive world model",
        "4D scene generation",
        "autonomous driving world model",
        "generative simulation world model",
    ],
}

KEYWORDS = {
    "image-2d": ["text-to-image", "image generation", "diffusion", "flux", "rectified flow", "t2i"],
    "video": ["video generation", "text-to-video", "image-to-video", "video editing", "human animation", "surround-view"],
    "3d-object-asset": ["3d", "text-to-3d", "image-to-3d", "mesh", "avatar", "asset", "shape generation"],
    "3d-scene": ["3d scene", "layout", "indoor scene", "outdoor scene", "navigable", "scene generation"],
    "4d-dynamic-scene-world": ["world model", "autonomous driving", "simulation", "interactive world", "4d", "game world", "closed-loop"],
}

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
    url = f"https://api.github.com/orgs/{org}/repos?per_page=100&type=public&sort=updated"
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
        score += max(0, 25 - age_days)
    except Exception:
        pass

    if any(k in text for k in ["code", "open-source", "opensource", "publicly available", "release", "weights"]):
        score += 18
    if any(k in text for k in ["world model", "real-time", "closed-loop", "interactive", "foundation model"]):
        score += 10
    return score

def score_github_candidate(item: dict, now: datetime) -> int:
    score = 15
    text = f"{item.get('name', '')} {item.get('description', '')} {' '.join(item.get('topics', []))}".lower()

    try:
        updated_dt = datetime.fromisoformat(item["updated_at"].replace("Z", "+00:00"))
        age_days = max(0, (now - updated_dt).days)
        score += max(0, 20 - age_days)
    except Exception:
        pass

    score += min(int(item.get("stargazers_count", 0) or 0) // 100, 20)

    if any(k in text for k in ["world model", "video generation", "3d", "diffusion", "generative"]):
        score += 8

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

def build_report(candidates: list[dict], watched_repos: list[dict], days: int) -> str:
    now_text = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    by_artifact: dict[str, list[dict]] = {}
    for item in candidates:
        by_artifact.setdefault(item["artifact"], []).append(item)

    lines = [
        "# 📬 Daily Candidate Inbox",
        "",
        "> Auto-generated harvesting report. **Manual review is required before touching `data/*.jsonl`.**",
        "",
        f"- Generated: `{now_text}`",
        f"- Window: last **{days}** days",
        f"- Raw files: `metadata/candidates/{datetime.now(timezone.utc).strftime('%Y-%m-%d')}/`",
        f"- Total new candidates: **{len(candidates)}**",
        f"- Recently updated watched repos: **{len(watched_repos)}**",
        "",
        "## Review Checklist",
        "",
        "- Is the artifact classification correct?",
        "- Is the link exact and canonical?",
        "- Is the work in scope (2025+ by default)?",
        "- Is the summary worth writing for the public catalog?",
        "- Does it belong in the main catalog or only in the watchlist?",
        "",
    ]

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

            date_str = item.get("published", "")[:10] or item.get("updated_at", "")[:10]
            lines.append(
                f"| {item['score']} | {item['source']} | {date_str} | "
                f"**{item['title']}** | {item.get('task', '—')} | {item.get('why', '—')} | "
                f"{' / '.join(links) if links else '—'} |"
            )
        lines.append("")

    lines.extend(["## Recently Updated Watched Repositories", ""])
    if watched_repos:
        lines.extend(["| Organization | Repo | Stars | Updated | Why it may matter |", "|:--|:--|--:|:--|:--|"])
        for repo in sorted(watched_repos, key=lambda r: (-int(r.get("stargazers_count", 0)), r["full_name"].lower())):
            lines.append(
                f"| {repo['watch_org']} | [{repo['full_name']}]({repo['html_url']}) | "
                f"{int(repo.get('stargazers_count', 0) or 0)} | {repo.get('updated_at', '')[:10]} | "
                f"{repo.get('why', '—')} |"
            )
    else:
        lines.append("- No notable watched-repo updates were found.")
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

def main() -> None:
    parser = argparse.ArgumentParser(description="Harvest daily candidate papers and repo updates.")
    parser.add_argument("--days", type=int, default=14, help="Lookback window in days.")
    parser.add_argument("--issue", action="store_true", help="Create a GitHub issue.")
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN", "").strip()
    existing_titles, existing_repos, existing_papers = load_existing_keys()

    now = datetime.now(timezone.utc)
    since = now - timedelta(days=args.days)

    new_candidates: list[dict] = []
    watched_repos: list[dict] = []

    # --- arXiv harvesting ---
    for artifact, terms in ARXIV_QUERIES.items():
        items = fetch_arxiv(arxiv_query(terms))
        if items and "error" in items[0]:
            continue

        for item in items:
            try:
                published_dt = datetime.fromisoformat(item["published"].replace("Z", "+00:00"))
            except Exception:
                continue

            if published_dt < since:
                continue

            title_key = normalize_title(item["title"])
            paper_key = item["paper"].rstrip("/").lower()

            if title_key in existing_titles or paper_key in existing_papers:
                continue

            text = f"{item['title']} {item['abstract']}"
            artifact_guess = guess_artifact(text)
            task_guess = guess_task(artifact_guess, text)

            item_out = {
                "source": "arXiv",
                "artifact": artifact_guess,
                "task": task_guess,
                "title": item["title"],
                "paper": item["paper"],
                "repo": "",
                "homepage": "",
                "abstract": item["abstract"],
                "published": item["published"],
                "score": score_arxiv_candidate(item, now),
                "why": "recent paper candidate",
            }
            new_candidates.append(item_out)

    # --- watched GitHub org repos ---
    for watch in WATCH_ORGS:
        org_name = watch["name"]
        org_slug = watch["github"]

        repos = github_org_repos(org_slug, token=token)
        if repos and "error" in repos[0]:
            continue

        for repo in repos:
            if repo.get("private"):
                continue

            updated_at = repo.get("updated_at", "")
            try:
                updated_dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            except Exception:
                continue

            if updated_dt < since:
                continue

            full_name = repo.get("full_name", "")
            if full_name.lower() in existing_repos:
                continue

            text = " ".join(
                [
                    repo.get("name", ""),
                    repo.get("description", "") or "",
                    " ".join(repo.get("topics", []) or []),
                ]
            ).lower()

            if not any(keyword in text for values in KEYWORDS.values() for keyword in values):
                continue

            artifact_guess = guess_artifact(text)
            task_guess = guess_task(artifact_guess, text)

            why = f"recent update in watched organization `{org_name}`"
            watched_repos.append(
                {
                    "watch_org": org_name,
                    "full_name": full_name,
                    "html_url": repo.get("html_url", ""),
                    "stargazers_count": int(repo.get("stargazers_count", 0) or 0),
                    "updated_at": updated_at,
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
                        "updated_at": updated_at,
                        "score": score_github_candidate(repo, now),
                        "why": why,
                    }
                )

    new_candidates = dedupe_candidates(new_candidates)

    today = now.strftime("%Y-%m-%d")
    day_dir = OUT_DIR / today
    day_dir.mkdir(parents=True, exist_ok=True)

    report = build_report(new_candidates, watched_repos, args.days)

    write_json(day_dir / "candidates.json", new_candidates)
    write_json(day_dir / "watched_repos.json", watched_repos)
    (day_dir / "report.md").write_text(report.rstrip() + "\n", encoding="utf-8")

    write_json(OUT_DIR / "latest.json", new_candidates)
    (OUT_DIR / "latest.md").write_text(report.rstrip() + "\n", encoding="utf-8")

    print(f"[fetch] wrote {len(new_candidates)} new candidates to metadata/candidates/latest.md")

    if args.issue and new_candidates:
        create_github_issue(day_dir / "report.md", len(new_candidates))

if __name__ == "__main__":
    main()
