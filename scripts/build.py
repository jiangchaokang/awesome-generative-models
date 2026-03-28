#!/usr/bin/env python3
"""Build README.md and sub-pages from data/*.jsonl.

Single source of truth: only edit files under data/.
All output (README, category pages, topic pages) is auto-generated.
"""
from __future__ import annotations

import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

# ---------------------------------------------------------------------------
# Mapping: data file -> primary artifact key
# ---------------------------------------------------------------------------
FILE_ARTIFACT = {
    "image_2d.jsonl": "image-2d",
    "video.jsonl": "video",
    "object_3d.jsonl": "3d-object-asset",
    "scene_3d.jsonl": "3d-scene",
    "world_4d.jsonl": "4d-dynamic-scene-world",
}

ARTIFACT_ORDER = [
    "image-2d",
    "video",
    "3d-object-asset",
    "3d-scene",
    "4d-dynamic-scene-world",
]

ARTIFACT_META = {
    "image-2d": {
        "dir": "10-image-2d",
        "emoji": "🖼️",
        "title": "Image 2D",
        "short": "Final artifact is a single 2D image: T2I, controllable generation, editing, super-resolution, etc.",
    },
    "video": {
        "dir": "20-video",
        "emoji": "🎬",
        "title": "Video",
        "short": "Final artifact is a video or video edit: T2V, I2V, video editing, human animation, surround-view video, etc.",
    },
    "3d-object-asset": {
        "dir": "30-3d-object-asset",
        "emoji": "🧊",
        "title": "3D Object / Asset",
        "short": "Single-object 3D assets, reusable avatars, articulated / part-aware assets.",
    },
    "3d-scene": {
        "dir": "40-3d-scene",
        "emoji": "🏙️",
        "title": "3D Scene",
        "short": "Multi-object 3D scenes: indoor, outdoor-urban, explorable scenes, layout-guided generation.",
    },
    "4d-dynamic-scene-world": {
        "dir": "50-4d-dynamic-scene-world",
        "emoji": "🌍",
        "title": "4D Dynamic Scene / World",
        "short": "Explicit dynamic 3D/4D scenes, world models, simulation, autonomous driving, game worlds.",
    },
}

VENUE_ORDER = {
    "CVPR": 1, "ICCV": 2, "ECCV": 3, "NEURIPS": 4, "ICLR": 5,
    "ICML": 6, "SIGGRAPH": 7, "AAAI": 8, "3DV": 9, "ICRA": 10,
    "SGP": 11, "ARXIV": 99,
}

VENUE_COLOR = {
    "CVPR": "blue", "ICCV": "blue", "ECCV": "blue",
    "NEURIPS": "purple", "ICLR": "purple", "ICML": "purple",
    "SIGGRAPH": "orange", "SGP": "orange",
    "AAAI": "green", "3DV": "green", "ICRA": "green",
    "ARXIV": "lightgrey",
}

DOMAIN_IGNORE = {"general"}

# ---------------------------------------------------------------------------
# Survey / foundation reading links
# ---------------------------------------------------------------------------
SURVEY_LINKS = [
    ("Simulating the Real World: A Unified Survey of Multimodal Generative Models",
     "https://arxiv.org/abs/2503.04641"),
    ("A Survey of World Models for Autonomous Driving",
     "https://arxiv.org/abs/2501.11260"),
    ("The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey",
     "https://arxiv.org/abs/2502.10498"),
    ("Foundation Models in Autonomous Driving: Scenario Generation and Analysis",
     "https://arxiv.org/abs/2506.11526"),
]


# ========== helpers ==========

def ensure_list(value, default=None):
    if value is None:
        return list(default or [])
    if isinstance(value, list):
        return value
    return [value]


def extract_year(text: str) -> int:
    m = re.search(r"(20\d{2})", text or "")
    return int(m.group(1)) if m else 0


def venue_rank(venue: str) -> int:
    first = (venue or "").split()[0].upper()
    return VENUE_ORDER.get(first, 999)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "item"


def paper_search_url(title: str, venue: str) -> str:
    if "ARXIV" in (venue or "").upper():
        return (
            "https://arxiv.org/search/?query="
            + quote(title)
            + "&searchtype=all&abstracts=show&order=-announced_date_first&size=50"
        )
    return "https://scholar.google.com/scholar?q=" + quote(title)


def repo_search_url(title: str) -> str:
    return "https://github.com/search?q=" + quote(title) + "&type=repositories"


def venue_badge(venue: str) -> str:
    """Return a shields.io badge image for a venue string."""
    label = venue.replace(" ", "%20")
    first = venue.split()[0].upper()
    color = VENUE_COLOR.get(first, "lightgrey")
    return f"![{venue}](https://img.shields.io/badge/{label}-{color})"


def method_badges(methods: list[str]) -> str:
    parts = []
    for m in methods[:3]:
        parts.append(f"`{m}`")
    return " ".join(parts)


# ========== loading ==========

def load_papers() -> list[dict]:
    papers = []
    seen_ids: set[str] = set()
    data_dir = ROOT / "data"

    for file_name, artifact in FILE_ARTIFACT.items():
        path = data_dir / file_name
        if not path.exists():
            continue
        with path.open("r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue
                record = json.loads(raw)
                record["artifact"] = artifact
                record["domain"] = ensure_list(record.get("domain"), ["general"])
                record["representation"] = ensure_list(record.get("representation"), [])
                record["method"] = ensure_list(record.get("method"), [])
                record["conditioning"] = ensure_list(record.get("conditioning"), [])
                record["open_source"] = bool(record.get("open_source", False))
                record["featured"] = bool(record.get("featured", False))
                record["year"] = int(record.get("year") or extract_year(record.get("venue", "")))
                record["id"] = record.get("id") or slugify(record.get("title", ""))
                record["stars"] = int(record.get("stars", 0))

                for field in ("id", "title", "venue", "task"):
                    if not record.get(field):
                        raise ValueError(f"{path}:{lineno} missing required field `{field}`")
                if record["id"] in seen_ids:
                    raise ValueError(f"Duplicate id: {record['id']} ({path}:{lineno})")
                seen_ids.add(record["id"])
                papers.append(record)

    papers.sort(key=lambda p: (-p["year"], venue_rank(p["venue"]), p["title"].lower()))
    return papers


def paper_link(rec: dict) -> str:
    return rec.get("paper") or paper_search_url(rec["title"], rec["venue"])


def repo_link(rec: dict) -> str:
    if rec.get("repo"):
        return rec["repo"]
    if rec.get("open_source"):
        return repo_search_url(rec["title"])
    return ""


def homepage_link(rec: dict) -> str:
    return rec.get("homepage", "")


def render_links_inline(rec: dict) -> str:
    parts = []
    parts.append(f"[📄 Paper]({paper_link(rec)})")
    repo = repo_link(rec)
    if repo:
        parts.append(f"[💻 Code]({repo})")
    hp = homepage_link(rec)
    if hp:
        parts.append(f"[🌐 Project]({hp})")
    return " &nbsp; ".join(parts)


def auto_summary(rec: dict) -> str:
    if rec.get("summary"):
        return rec["summary"]
    parts = []
    task_str = rec["task"].replace("-", " ")
    artifact_str = rec["artifact"].replace("-", " ")
    parts.append(f"A {task_str} approach targeting {artifact_str} generation")
    if rec["method"]:
        parts.append(f"using {'/'.join(rec['method'][:2])}")
    if rec["conditioning"]:
        parts.append(f"conditioned on {'/'.join(rec['conditioning'][:2])}")
    return " ".join(parts) + "."


def tag_pills(rec: dict) -> str:
    tokens = []
    for m in rec["method"][:2]:
        tokens.append(m)
    for r in rec["representation"][:2]:
        tokens.append(r)
    if rec["open_source"]:
        tokens.append("open-source")
    seen = set()
    out = []
    for t in tokens:
        if t and t not in seen:
            seen.add(t)
            out.append(f"`{t}`")
    return " ".join(out)


# ========== rendering helpers ==========

def render_paper_row(rec: dict) -> str:
    """Render a single paper as a table row (for main tables)."""
    title = rec["title"]
    link = paper_link(rec)
    venue = rec["venue"]
    oss = "✅" if rec["open_source"] else "—"
    links = []
    links.append(f"[Paper]({link})")
    repo = repo_link(rec)
    if repo:
        links.append(f"[Code]({repo})")
    hp = homepage_link(rec)
    if hp:
        links.append(f"[Web]({hp})")
    link_str = " / ".join(links)
    tags = tag_pills(rec)
    return f"| **{title}** | {venue} | {tags} | {oss} | {link_str} |"


def render_paper_detail(rec: dict) -> str:
    """Render a paper as a collapsible detail block (for sub-pages)."""
    title = html.escape(rec["title"])
    summary = auto_summary(rec)
    tags = tag_pills(rec)
    links = render_links_inline(rec)
    venue = rec["venue"]
    oss_badge = "![Open Source](https://img.shields.io/badge/Open_Source-brightgreen)" if rec["open_source"] else ""

    return "\n".join([
        "<details>",
        f"<summary><b>{title}</b> &mdash; <code>{venue}</code> {tags} {oss_badge}</summary>",
        "",
        f"> {summary}",
        "",
        f"{links}",
        "",
        "</details>",
        "",
    ])


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


# ========== page builders ==========

def build_foundations_page(papers: list[dict]) -> None:
    out_dir = ROOT / "00-surveys-and-foundations"
    lines = [
        "# 📚 Surveys & Foundations",
        "",
        "> Auto-generated by `scripts/build.py`. Stable taxonomy principles, maintenance policy, and recommended surveys.",
        "",
        "## Recommended Reading",
        "",
    ]
    for title, url in SURVEY_LINKS:
        lines.append(f"- [{title}]({url})")
    lines.extend([
        "",
        "## Maintenance Policy",
        "",
        "- The primary index is determined solely by `primary_artifact`; `domain / method / representation` never become top-level directories.",
        "- All data lives in `data/*.jsonl`; every page is generated by `scripts/build.py`.",
        "- Daily updates follow a **candidate harvesting → human review → merge** pipeline (see `metadata/candidates/latest.md`).",
        "- When a link is uncertain, leave the field empty — the generator falls back to search URLs automatically.",
        "",
        "## Quick Links",
        "",
        "- [Taxonomy](../docs/taxonomy.md)",
        "- [Daily Candidates](../metadata/candidates/latest.md)",
        "- [Contributing Guide](../CONTRIBUTING.md)",
        "- [Root README](../README.md)",
    ])
    write_text(out_dir / "README.md", "\n".join(lines))


def build_artifact_pages(papers: list[dict]) -> None:
    by_artifact = defaultdict(list)
    for p in papers:
        by_artifact[p["artifact"]].append(p)

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        adir = ROOT / meta["dir"]
        adir.mkdir(parents=True, exist_ok=True)
        aps = by_artifact.get(artifact, [])

        by_task = defaultdict(list)
        for p in aps:
            by_task[p["task"]].append(p)

        # --- artifact README ---
        lines = [
            f"# {meta['emoji']} {meta['dir']} — {meta['title']}",
            "",
            f"> **{len(aps)} papers.** {meta['short']}",
            "",
            f"[↑ Back to root](../README.md)",
            "",
            "## Tasks",
            "",
        ]
        for task, items in sorted(by_task.items(), key=lambda x: (-len(x[1]), x[0])):
            task_file = slugify(task) + ".md"
            lines.append(f"- [{task}]({task_file}) ({len(items)})")

        lines.extend([
            "",
            "## All Papers",
            "",
            "| Title | Venue | Tags | Open | Links |",
            "|:------|:------|:-----|:----:|:------|",
        ])
        for p in aps:
            lines.append(render_paper_row(p))
        lines.append("")

        # Detailed view
        lines.extend(["## Paper Details", ""])
        for p in aps:
            lines.append(render_paper_detail(p))

        write_text(adir / "README.md", "\n".join(lines))

        # --- task sub-pages ---
        for task, items in by_task.items():
            task_file = adir / (slugify(task) + ".md")
            tlines = [
                f"# {meta['emoji']} {meta['dir']} / {task}",
                "",
                f"> **{len(items)} papers.**",
                "",
                "[↑ Root](../README.md) · [↑ Category](README.md)",
                "",
                "| Title | Venue | Tags | Open | Links |",
                "|:------|:------|:-----|:----:|:------|",
            ]
            for p in items:
                tlines.append(render_paper_row(p))
            tlines.extend(["", "## Details", ""])
            for p in items:
                tlines.append(render_paper_detail(p))
            write_text(task_file, "\n".join(tlines))


def build_topic_pages(papers: list[dict]) -> None:
    topic_dir = ROOT / "90-topics"
    topic_dir.mkdir(parents=True, exist_ok=True)

    by_domain: dict[str, list[dict]] = defaultdict(list)
    for p in papers:
        for d in p["domain"]:
            if d not in DOMAIN_IGNORE:
                by_domain[d].append(p)

    idx_lines = [
        "# 🏷️ Cross-Cutting Topics",
        "",
        "> Topic pages generated from `domain` tags. Each paper appears under its primary artifact directory; topics provide cross-cutting views.",
        "",
        "[↑ Back to root](../README.md)",
        "",
        "| Topic | Papers |",
        "|:------|-------:|",
    ]

    for domain, items in sorted(by_domain.items(), key=lambda x: (-len(x[1]), x[0])):
        fname = slugify(domain) + ".md"
        idx_lines.append(f"| [{domain}]({fname}) | {len(items)} |")

        dlines = [
            f"# 🏷️ Topic: {domain}",
            "",
            f"> {len(items)} papers across all artifact categories.",
            "",
            "[↑ Root](../README.md) · [↑ Topics](README.md)",
            "",
            "| Title | Artifact | Venue | Open | Links |",
            "|:------|:---------|:------|:----:|:------|",
        ]
        for p in items:
            link = paper_link(p)
            oss = "✅" if p["open_source"] else "—"
            repo = repo_link(p)
            lnk = f"[Paper]({link})"
            if repo:
                lnk += f" / [Code]({repo})"
            dlines.append(f"| **{p['title']}** | {p['artifact']} | {p['venue']} | {oss} | {lnk} |")
        write_text(topic_dir / fname, "\n".join(dlines))

    write_text(topic_dir / "README.md", "\n".join(idx_lines))


def build_root_readme(papers: list[dict]) -> None:
    by_artifact = defaultdict(list)
    for p in papers:
        by_artifact[p["artifact"]].append(p)

    domains = Counter()
    for p in papers:
        for d in p["domain"]:
            if d not in DOMAIN_IGNORE:
                domains[d] += 1

    open_count = sum(1 for p in papers if p["open_source"])

    # Featured papers: those marked featured=true, or top-starred, or latest highlights
    featured = [p for p in papers if p.get("featured")]
    if len(featured) < 5:
        # Fill with recent open-source high-venue papers
        for p in papers:
            if p not in featured and p["open_source"] and p["year"] >= 2025:
                featured.append(p)
            if len(featured) >= 12:
                break

    lines = [
        "<!-- AUTO-GENERATED by scripts/build.py — DO NOT EDIT MANUALLY -->",
        "",
        '<div align="center">',
        "",
        "# 🚀 Awesome Generative Models",
        "",
        "**A curated, continuously-updated collection of state-of-the-art generative models**",
        "**for images, videos, 3D objects, 3D scenes, and 4D dynamic worlds.**",
        "",
        "![Awesome](https://img.shields.io/badge/Awesome-Generative_Models-FC60A8?style=for-the-badge&logo=awesomelists&logoColor=white)",
        f"![Papers](https://img.shields.io/badge/Papers-{len(papers)}-blue?style=for-the-badge)",
        f"![Open Source](https://img.shields.io/badge/Open_Source-{open_count}-brightgreen?style=for-the-badge)",
        f"![Topics](https://img.shields.io/badge/Topics-{len(domains)}-orange?style=for-the-badge)",
        "![Updated](https://img.shields.io/badge/Updated-2025%2F2026-informational?style=for-the-badge)",
        "",
        "[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)",
        "[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)",
        "",
        "*Only works active or published since 2025 are tracked.*",
        "",
        "</div>",
        "",
        "---",
        "",
        "## ⭐ Featured & Highlighted Works",
        "",
        "| Title | Category | Venue | Tags | Links |",
        "|:------|:---------|:------|:-----|:------|",
    ]

    for p in featured[:15]:
        link = paper_link(p)
        repo = repo_link(p)
        tags = tag_pills(p)
        lnk = f"[Paper]({link})"
        if repo:
            lnk += f" / [Code]({repo})"
        cat_emoji = ARTIFACT_META.get(p["artifact"], {}).get("emoji", "")
        lines.append(
            f"| **{p['title']}** | {cat_emoji} {p['artifact']} | `{p['venue']}` | {tags} | {lnk} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 📂 Directory Structure",
        "",
        "| # | Directory | Focus | Count |",
        "|:-:|:----------|:------|------:|",
        "| 📚 | [00-surveys-and-foundations](00-surveys-and-foundations/README.md) | Surveys, taxonomy, maintenance policy | — |",
    ])

    for i, artifact in enumerate(ARTIFACT_ORDER):
        meta = ARTIFACT_META[artifact]
        count = len(by_artifact.get(artifact, []))
        lines.append(
            f"| {meta['emoji']} | [{meta['dir']}]({meta['dir']}/README.md) | {meta['short'][:80]}… | **{count}** |"
        )
    lines.append(
        f"| 🏷️ | [90-topics](90-topics/README.md) | Cross-cutting topic pages | {sum(domains.values())} tag hits |"
    )

    lines.extend([
        "",
        "---",
        "",
        "## 🗂️ Taxonomy Overview",
        "",
        "| Axis | Role | Examples |",
        "|:-----|:-----|:--------|",
        "| `primary_artifact` | **Top-level directory** | image-2d, video, 3d-object-asset, 3d-scene, 4d-dynamic-scene-world |",
        "| `task` | **Sub-page** | text-to-image, video-editing, autonomous-driving, 4d-generation |",
        "| `domain` | Topic page / tag | indoor, autonomous-driving, human-avatar, gameplay |",
        "| `representation` | Tag | mesh, point-cloud, occupancy, 3dgs, vector-graph |",
        "| `method` | Tag | diffusion, autoregressive, flow, world-model, llm-agent |",
        "| `conditioning` | Tag | text, image, video, camera, pose, action, trajectory |",
        "",
        "**Key rules:** classify by *final artifact*; `domain / method / representation` are tags only; each paper appears exactly once.",
        "",
        "---",
        "",
    ])

    # Per-category quick-view tables
    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        aps = by_artifact.get(artifact, [])
        if not aps:
            continue
        by_task = defaultdict(list)
        for p in aps:
            by_task[p["task"]].append(p)

        lines.extend([
            f"### {meta['emoji']} [{meta['title']}]({meta['dir']}/README.md) ({len(aps)} papers)",
            "",
            "| Task | # | Highlights |",
            "|:-----|--:|:-----------|",
        ])
        for task, items in sorted(by_task.items(), key=lambda x: (-len(x[1]), x[0])):
            highlights = ", ".join(p["title"][:40] for p in items[:3])
            task_link = f"[{task}]({meta['dir']}/{slugify(task)}.md)"
            lines.append(f"| {task_link} | {len(items)} | {highlights}… |")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 🏷️ Topic Pages",
        "",
        "| Topic | Papers |",
        "|:------|-------:|",
    ])
    for d, c in domains.most_common():
        lines.append(f"| [{d}](90-topics/{slugify(d)}.md) | {c} |")

    lines.extend([
        "",
        "---",
        "",
        "## 📊 Statistics",
        "",
        f"- **Total papers:** {len(papers)}",
        f"- **Open-source:** {open_count} ({100*open_count//max(len(papers),1)}%)",
        f"- **Topic pages:** {len(domains)}",
        f"- **Artifact categories:** {len(ARTIFACT_ORDER)}",
        "",
        "---",
        "",
        "## 🛠️ Build & Usage",
        "",
        "```bash",
        "# Generate all pages from data/*.jsonl",
        "python scripts/build.py",
        "",
        "# Fetch daily arXiv candidates (writes to metadata/candidates/)",
        "python scripts/fetch_candidates.py",
        "```",
        "",
        "**Workflow:**",
        "1. Add or edit entries in `data/*.jsonl`",
        "2. Push to `main` — GitHub Actions runs `build.py` automatically",
        "3. Or run `python scripts/build.py` locally before committing",
        "",
        "**Daily candidate harvesting** runs via GitHub Actions cron.",
        "New candidates are posted as a **GitHub Issue** for human review.",
        "Approved papers are manually added to `data/*.jsonl`.",
        "",
        "See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.",
        "",
        "---",
        "",
        "## 📖 Recommended Surveys",
        "",
    ])
    for title, url in SURVEY_LINKS:
        lines.append(f"- [{title}]({url})")

    lines.extend([
        "",
        "---",
        "",
        '<div align="center">',
        "",
        "**If you find this repository useful, please consider giving it a ⭐!**",
        "",
        "</div>",
    ])

    write_text(ROOT / "README.md", "\n".join(lines))


def main():
    papers = load_papers()
    build_foundations_page(papers)
    build_artifact_pages(papers)
    build_topic_pages(papers)
    build_root_readme(papers)
    print(f"[build] Generated pages for {len(papers)} papers.")


if __name__ == "__main__":
    main()