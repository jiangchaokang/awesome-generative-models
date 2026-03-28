#!/usr/bin/env python3
"""Fetch daily candidate papers from arXiv and optionally create a GitHub Issue.

Usage:
  python scripts/fetch_candidates.py              # write to metadata/candidates/
  python scripts/fetch_candidates.py --issue       # also create a GitHub Issue
"""
from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "metadata" / "candidates"

QUERIES = {
    "image-2d": [
        "text-to-image generation",
        "image generation diffusion transformer",
        "one-step generative model image",
        "controllable image generation",
        "flow matching image generation",
    ],
    "video": [
        "text-to-video generation",
        "image-to-video generation",
        "video editing diffusion",
        "video generation world model",
        "human animation video diffusion",
        "surround-view video generation",
    ],
    "3d-object-asset": [
        "text-to-3D generation",
        "image-to-3D generation",
        "3D shape generation diffusion",
        "3D asset generation",
    ],
    "3d-scene": [
        "3D scene generation",
        "indoor scene generation",
        "layout guided 3D scene",
        "3D scene diffusion",
    ],
    "4d-dynamic-scene-world": [
        "world model autonomous driving",
        "4D scene generation",
        "driving world model simulation",
        "interactive world model generation",
        "world foundation model",
    ],
}

TIMEOUT = 20  # seconds per query
WINDOW_DAYS = 14


def arxiv_query(terms: list[str]) -> str:
    return " OR ".join(f'all:"{t}"' for t in terms)


def fetch_arxiv(query: str, max_results: int = 20) -> list[dict]:
    url = (
        "http://export.arxiv.org/api/query?search_query="
        + quote(query)
        + f"&start=0&max_results={max_results}"
        + "&sortBy=submittedDate&sortOrder=descending"
    )
    req = Request(url, headers={"User-Agent": "awesome-generative-models/2.0"})
    try:
        with urlopen(req, timeout=TIMEOUT) as resp:
            xml = resp.read()
    except Exception as exc:
        return [{"error": str(exc)}]

    root = ET.fromstring(xml)
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items = []
    for entry in root.findall("a:entry", ns):
        title = " ".join((entry.findtext("a:title", "", ns) or "").split())
        abstract = " ".join((entry.findtext("a:summary", "", ns) or "").split())
        link = entry.findtext("a:id", "", ns) or ""
        published = entry.findtext("a:published", "", ns) or ""
        items.append({"title": title, "abstract": abstract, "link": link, "published": published})
    return items


def dedupe(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    out = []
    for it in items:
        key = it.get("title", "").strip().lower()
        if key in seen or not key:
            continue
        seen.add(key)
        out.append(it)
    return out


def clip(text: str, limit: int = 140) -> str:
    text = text.replace("|", "/").replace("\n", " ").strip()
    return text[:limit - 1] + "…" if len(text) > limit else text


def build_report() -> str:
    now = datetime.now(timezone.utc)
    since = now - timedelta(days=WINDOW_DAYS)

    lines = [
        "# 📬 Daily Candidate Papers",
        "",
        "> Auto-generated from arXiv. **Manual review required before adding to `data/*.jsonl`.**",
        "",
        f"- Generated: `{now.strftime('%Y-%m-%d %H:%M UTC')}`",
        f"- Window: last **{WINDOW_DAYS}** days",
        "",
    ]

    total = 0
    for area, terms in QUERIES.items():
        query = arxiv_query(terms)
        items = fetch_arxiv(query)

        if items and "error" in items[0]:
            lines.extend([f"## {area}", "", f"- ⚠️ Fetch failed: `{items[0]['error']}`", ""])
            continue

        filtered = []
        for it in dedupe(items):
            try:
                pub = datetime.fromisoformat(it["published"].replace("Z", "+00:00"))
            except Exception:
                continue
            if pub >= since:
                it["pub_dt"] = pub
                filtered.append(it)
        filtered.sort(key=lambda x: x["pub_dt"], reverse=True)
        total += len(filtered)

        lines.extend([f"## {area}", ""])
        if not filtered:
            lines.extend(["- No candidates found.", ""])
            continue

        lines.extend(["| Date | Title | Abstract |", "|:-----|:------|:---------|"])
        for it in filtered[:20]:
            lines.append(
                f"| {it['pub_dt'].strftime('%Y-%m-%d')} "
                f"| [{clip(it['title'], 100)}]({it['link']}) "
                f"| {clip(it['abstract'])} |"
            )
        lines.append("")

    return "\n".join(lines), total


def create_github_issue(report: str, total: int) -> None:
    """Create a GitHub Issue with the candidate report using gh CLI."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    title = f"📬 Daily candidates — {today} ({total} papers)"
    try:
        subprocess.run(
            ["gh", "issue", "create",
             "--title", title,
             "--body", report,
             "--label", "daily-candidates"],
            check=True, capture_output=True, text=True,
        )
        print(f"[fetch] Created GitHub Issue: {title}")
    except FileNotFoundError:
        print("[fetch] `gh` CLI not found — skipping Issue creation.")
    except subprocess.CalledProcessError as exc:
        print(f"[fetch] Failed to create Issue: {exc.stderr}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--issue", action="store_true", help="Create a GitHub Issue with candidates")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    report, total = build_report()

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    (OUT_DIR / "latest.md").write_text(report.rstrip() + "\n", encoding="utf-8")
    (OUT_DIR / f"{today}.md").write_text(report.rstrip() + "\n", encoding="utf-8")
    print(f"[fetch] Wrote {total} candidates to metadata/candidates/latest.md")

    if args.issue and total > 0:
        create_github_issue(report, total)


if __name__ == "__main__":
    main()