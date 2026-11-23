#!/usr/bin/env python3
"""Render data/*.jsonl into README.md and all generated catalog pages.

Design goals for the generated markdown (see docs/taxonomy.md for the data
contract itself):

- Progressive disclosure: a small "Spotlight" of the strongest recent work is
  rendered as rich cards; everything else lives in a dense, scannable table.
  This avoids the old pattern of repeating 8-12 image badges per entry across
  hundreds of entries, which was slow to load and hard to skim.
- Badges are reserved for things that deserve visual weight and benefit from
  brand colors: header stats and the Paper/Code/Project buttons on spotlight
  cards. Per-entry metadata (venue, tags, open-source status) is plain text /
  inline-code chips so the bulk listing stays lightweight and fast.
- Every generated page is self-contained and honest about scope: freshness
  (build date), counts, and empty states are always shown rather than implied.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode, urlparse
import json
import re

from catalog_common import (
    ARTIFACT_META,
    ARTIFACT_ORDER,
    ARTIFACT_TASK_ORDER,
    DOMAIN_IGNORE,
    ROOT,
    SURVEY_LINKS,
    VENUE_COLORS,
    compact_number,
    load_records,
    org_badge_meta_for,
    parse_github_repo,
    slugify,
)

CACHE_DIR = ROOT / "metadata" / "cache"
WEEKLY_DATA_DIR = ROOT / "data" / "weekly"
WEEKLY_ARCHIVE_DIR = ROOT / "weekly"

WEEKLY_START_MARKER = "<!-- WEEKLY:START -->"
WEEKLY_END_MARKER = "<!-- WEEKLY:END -->"
WEEKLY_BLOCK_RE = re.compile(
    rf"{re.escape(WEEKLY_START_MARKER)}.*?{re.escape(WEEKLY_END_MARKER)}",
    re.DOTALL,
)

TRACK_DISPLAY = {
    "image-2d": "Image 2D",
    "video": "Video",
    "3d-object": "3D Object",
    "3d-scene": "3D Scene",
    "4d-world": "4D / World",
}

REPO_SLUG = "jiangchaokang/awesome-generative-models"

ARTIFACT_COLORS = {
    "image-2d": "2563EB",
    "video": "7C3AED",
    "3d-object-asset": "0D9488",
    "3d-scene": "EA580C",
    "4d-dynamic-scene-world": "B31B1B",
}

# Full pipeline diagrams shown on each category page (in a collapsible
# section so they don't dominate the page).
MODEL_PATTERNS = {
    "image-2d": """Prompt / control / reference
        ↓
Text / multimodal encoder
        ↓
Latent generator (Diffusion / Flow / AR / VQ)
        ↓
Decoder / upsampler / reward correction
        ↓
Single 2D image""",
    "video": """Text / image / pose / sketch / camera
        ↓
Condition encoders + video tokenizer / VAE
        ↓
Spatiotemporal generator (DiT / diffusion / flow)
        ↓
Temporal consistency / editing / motion control
        ↓
Video clip / surround-view sequence""",
    "3d-object-asset": """Text / image / multiview / structure prior
        ↓
Asset encoder + 3D latent generator
        ↓
Geometry head (mesh / point / triplane / octree)
        ↓
Texture / material / articulation head
        ↓
Reusable 3D object / asset / avatar""",
    "3d-scene": """Text / layout / references / room constraints
        ↓
Planner / layout / scene graph / object set
        ↓
Scene generator (3DGS / mesh / occupancy / latent scene)
        ↓
Renderer / consistency / editing loop
        ↓
Static multi-object 3D scene""",
    "4d-dynamic-scene-world": """Observation / map / action / trajectory / prompt
        ↓
State encoder + memory / scene cache
        ↓
Dynamics rollout / world model / simulator
        ↓
Render heads (RGB / depth / occupancy / tokens)
        ↓
Interactive future world / closed-loop simulation""",
}

# Condensed 4-stage version of MODEL_PATTERNS for the single overview table
# on the root README (kept collapsed there; the full diagram lives on each
# category page instead of being repeated five times on the landing page).
MODEL_STAGES = {
    "image-2d": ("Prompt / control / reference", "Diffusion · Flow · AR · VQ latent generator", "Single 2D image"),
    "video": ("Text / image / pose / camera", "Spatiotemporal DiT · diffusion · flow", "Video clip / surround-view sequence"),
    "3d-object-asset": ("Text / image / multiview prior", "3D latent generator + geometry / texture heads", "Reusable 3D object / asset / avatar"),
    "3d-scene": ("Text / layout / room constraints", "3DGS · mesh · occupancy scene generator", "Static multi-object 3D scene"),
    "4d-dynamic-scene-world": ("Observation / action / trajectory", "Dynamics rollout · world model · simulator", "Interactive world / closed-loop simulation"),
}

ARTIFACT_HIGHLIGHTS_PER_PAGE = 3
# Below this many entries, a spotlight card would just repeat the whole
# table right underneath it, so smaller task/topic/org pages skip it.
SPOTLIGHT_MIN_POOL = 4
TOPIC_INDEX_LIMIT = 20
ORG_INDEX_LIMIT = 20

LEGEND = "**Legend:** 🟢 code publicly available · ⚪ code not (yet) public · ★ live GitHub stars (refreshed weekly)"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def shields_url(
    label: str,
    message: str,
    color: str = "2563EB",
    logo: str | None = None,
    style: str = "flat-square",
    label_color: str = "111827",
) -> str:
    params = {
        "label": label,
        "message": message,
        "color": color,
        "style": style,
        "labelColor": label_color,
    }
    if logo:
        params["logo"] = logo
    return "https://img.shields.io/static/v1?" + urlencode(params)


def badge(
    label: str,
    message: str,
    color: str = "2563EB",
    logo: str | None = None,
    link: str = "",
    style: str = "flat-square",
    label_color: str = "111827",
) -> str:
    alt = f"{label}: {message}"
    image = f"![{alt}]({shields_url(label, message, color, logo, style, label_color)})"
    return f"[{image}]({link})" if link else image


def record_repo_stats(rec: dict, repo_stats: dict) -> dict:
    full_name = parse_github_repo(rec.get("repo", ""))
    return repo_stats.get(full_name, {}) if full_name else {}


def record_stars(rec: dict, repo_stats: dict) -> int:
    stats = record_repo_stats(rec, repo_stats)
    return int(stats.get("stars", rec.get("stars", 0)) or 0)


def sort_records(records: list[dict], repo_stats: dict) -> list[dict]:
    return sorted(
        records,
        key=lambda r: (
            0 if r.get("featured") else 1,
            -max(r.get("year", 0), r.get("active_since", 0)),
            -record_stars(r, repo_stats),
            r.get("title", "").lower(),
        ),
    )


def pick_highlights(records: list[dict], repo_stats: dict, limit: int) -> list[dict]:
    return sort_records(records, repo_stats)[:limit]


def paper_badge_message(url: str) -> str:
    domain = urlparse(url).netloc.lower()
    if "arxiv.org" in domain:
        return "arXiv"
    if "openreview.net" in domain:
        return "OpenReview"
    if "openaccess.thecvf.com" in domain:
        return "CVF"
    if "proceedings.neurips.cc" in domain:
        return "NeurIPS"
    if "proceedings.mlr.press" in domain:
        return "PMLR"
    return "Link"


def record_primary_link(rec: dict) -> str:
    return rec.get("paper") or rec.get("homepage") or rec.get("repo") or ""


def linked_title(rec: dict) -> str:
    link = record_primary_link(rec)
    if not link:
        return rec["title"]
    return f"[{rec['title']}]({link})"


def escape_table_cell(text: str) -> str:
    """Defensive escaping for free-text values interpolated into markdown
    table cells: an unescaped `|` in a title/venue/summary would silently
    break the row's column alignment, and this repo's own contract does not
    forbid `|` in text -- only forbids fabricated links."""
    return (text or "").replace("|", "\\|").replace("\n", " ")


def count_label(count: int, noun: str) -> str:
    if count == 1:
        return f"1 {noun}"
    plural = f"{noun[:-1]}ies" if noun.endswith("y") else f"{noun}s"
    return f"{count} {plural}"


def status_dot(rec: dict) -> str:
    return "🟢" if rec.get("open_source") else "⚪"


def truncate_text(text: str, limit: int = 90) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    head = text[:limit].rsplit(" ", 1)[0].rstrip(",.;:")
    return f"{head}…"


def format_venue(rec: dict) -> str:
    venue = rec.get("venue") or "—"
    if rec.get("year", 0) < 2025 and rec.get("active_since", 0) >= 2025:
        return f"{venue} · since {rec['active_since']}"
    return venue


def collect_tags(rec: dict, limit: int = 4) -> list[str]:
    """Merge method/representation/conditioning/domain into one short,
    de-duplicated tag list, dropping the catch-all "general" domain and any
    domain tag that just repeats the task name."""
    tags: list[str] = []
    seen: set[str] = set()

    def add(items: list[str]) -> None:
        for item in items:
            key = slugify(item)
            if not item or key in seen:
                continue
            seen.add(key)
            tags.append(item)

    add(rec.get("method", []))
    add(rec.get("representation", []))
    add(rec.get("conditioning", []))
    add([d for d in rec.get("domain", []) if d != "general" and slugify(d) != slugify(rec.get("task", ""))])
    return tags[:limit]


def tag_chips(rec: dict, limit: int = 4) -> str:
    return " ".join(f"`{t}`" for t in collect_tags(rec, limit=limit))


def venue_badge(rec: dict) -> str:
    head = (rec.get("venue", "").split() or ["Other"])[0].upper()
    color = VENUE_COLORS.get(head, "64748B")
    return badge("Venue", rec.get("venue", "Unknown"), color, link=rec.get("venue_url", ""))


def task_badge(rec: dict) -> str:
    return badge("Track", rec["task"], ARTIFACT_COLORS.get(rec["artifact"], "0EA5E9"))


def scope_badge(rec: dict) -> str:
    if rec.get("year", 0) < 2025 and rec.get("active_since", 0) >= 2025:
        return badge("Legacy", f"Active since {rec['active_since']}", "F59E0B")
    return ""


def link_badges(rec: dict, repo_stats: dict) -> str:
    """Button-style badges for the actual clickable links. This is the one
    place badges stay image-based: brand colors (arXiv red / GitHub black)
    make Paper vs. Code vs. Project instantly recognizable."""
    parts: list[str] = []

    if rec.get("paper"):
        logo = "arxiv" if "arxiv.org" in rec["paper"].lower() else None
        parts.append(badge("Paper", paper_badge_message(rec["paper"]), "B31B1B", logo=logo, link=rec["paper"]))

    if rec.get("repo"):
        stars = record_stars(rec, repo_stats)
        msg = "GitHub" if stars <= 0 else f"GitHub ★ {compact_number(stars)}"
        parts.append(badge("Code", msg, "181717", "github", rec["repo"]))

    if rec.get("homepage"):
        parts.append(badge("Project", "Site", "0EA5E9", "googlechrome", rec["homepage"]))

    return " ".join(parts)


def spotlight_badges(rec: dict) -> list[str]:
    out = [venue_badge(rec), task_badge(rec)]
    for org in rec.get("orgs", [])[:1]:
        meta = org_badge_meta_for(org)
        out.append(badge("Org", meta["label"], meta["color"], meta.get("logo")))
    if rec.get("open_source"):
        out.append(badge("Source", "Open", "16A34A", "opensourceinitiative"))
    legacy = scope_badge(rec)
    if legacy:
        out.append(legacy)
    return [b for b in out if b]


def render_spotlight_card(rec: dict, repo_stats: dict) -> str:
    lines = [
        f"#### 🌟 {linked_title(rec)}",
        "",
        " ".join(spotlight_badges(rec)),
        "",
        f"> {rec['summary']}",
        "",
    ]
    links = link_badges(rec, repo_stats)
    if links:
        lines.extend([links, ""])
    chips = tag_chips(rec)
    if chips:
        lines.extend([chips, ""])
    if rec.get("scope_note"):
        lines.extend([f"_Scope note: {rec['scope_note']}_", ""])
    return "\n".join(lines)


def compact_links(rec: dict, repo_stats: dict) -> str:
    """Plain-text link list for table rows: no external images, so a table
    of 50+ rows still renders instantly."""
    parts: list[str] = []
    if rec.get("paper"):
        parts.append(f"[📄 {paper_badge_message(rec['paper'])}]({rec['paper']})")
    if rec.get("repo"):
        stars = record_stars(rec, repo_stats)
        star_text = f" ★{compact_number(stars)}" if stars > 0 else ""
        parts.append(f"[💻 Code{star_text}]({rec['repo']})")
    if rec.get("homepage"):
        parts.append(f"[🌐 Project]({rec['homepage']})")
    return " · ".join(parts) if parts else "—"


def render_table(records: list[dict], repo_stats: dict, show_artifact: bool = False) -> str:
    header = ["Title"]
    if show_artifact:
        header.append("Artifact")
    header.extend(["Venue", "What it does", "Links"])

    lines = [
        "| " + " | ".join(header) + " |",
        "|" + "|".join([":--"] * len(header)) + "|",
    ]

    for rec in records:
        cells = [f"{status_dot(rec)} **{escape_table_cell(linked_title(rec))}**"]
        if show_artifact:
            meta = ARTIFACT_META[rec["artifact"]]
            cells.append(f"{meta['emoji']} {meta['title']}")
        cells.append(escape_table_cell(format_venue(rec)))

        # Every record has a curated summary (schema-required), but only
        # ~1 in 4 have method/representation/conditioning/domain tags, so the
        # always-present summary -- not sparse tags -- carries this column.
        # Tags are appended underneath only when they genuinely exist.
        tags = collect_tags(rec, limit=3)
        if show_artifact:
            tags = [rec["task"], *tags]
        summary_cell = escape_table_cell(truncate_text(rec.get("summary", "")))
        if tags:
            summary_cell += "<br>" + " ".join(f"`{t}`" for t in tags[:4])
        cells.append(summary_cell)

        cells.append(compact_links(rec, repo_stats))
        lines.append("| " + " | ".join(cells) + " |")

    return "\n".join(lines)


def render_artifact_navigation(by_artifact: dict[str, list[dict]]) -> str:
    lines = ["| Track | Papers | Direct Task Shortcuts |", "|:--|--:|:--|"]

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        items = by_artifact.get(artifact, [])
        present_tasks = {item["task"] for item in items}
        task_links = [
            f"[{task}]({meta['dir']}/{slugify(task)}.md)"
            for task in ARTIFACT_TASK_ORDER[artifact]
            if task in present_tasks
        ]
        track_cell = f"**[{meta['emoji']} {meta['title']}]({meta['dir']}/README.md)**<br><sub>{meta['short']}</sub>"
        tasks_cell = " · ".join(task_links) if task_links else "—"
        lines.append(f"| {track_cell} | **{len(items)}** | {tasks_cell} |")

    return "\n".join(lines)


def render_pipeline_overview_table() -> str:
    lines = ["| Track | Input | Core Generator | Output |", "|:--|:--|:--|:--|"]
    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        stage_in, stage_core, stage_out = MODEL_STAGES[artifact]
        lines.append(f"| {meta['emoji']} {meta['title']} | {stage_in} | {stage_core} | {stage_out} |")
    return "\n".join(lines)


def build_foundations_page(papers: list[dict]) -> None:
    lines = [
        "# 📚 Surveys & Foundations",
        "",
        "> Contract, surveys, and maintenance notes for the catalog.",
        "",
        "## Repository Contract",
        "",
        "- Source of truth lives in `data/*.jsonl`.",
        "- Generated pages must be rebuilt via `python scripts/build.py`.",
        "- Public links must be exact, never search-result placeholders.",
        "- Inclusion is human-reviewed even when candidate harvesting is automatic.",
        "- Primary artifact decides placement; other axes stay metadata.",
        "",
        "## Quick Links",
        "",
        "- [Root README](../README.md)",
        "- [Candidate Inbox](../metadata/candidates/latest.md)",
        "- [Validation Report](../metadata/validation/latest.md)",
        "- [Contributing](../CONTRIBUTING.md)",
        "",
        "## Recommended Surveys",
        "",
    ]
    for title, url in SURVEY_LINKS:
        lines.append(f"- [{title}]({url})")

    write_text(ROOT / "00-surveys-and-foundations" / "README.md", "\n".join(lines))


def build_artifact_pages(papers: list[dict], repo_stats: dict) -> None:
    by_artifact: dict[str, list[dict]] = defaultdict(list)
    for paper in papers:
        by_artifact[paper["artifact"]].append(paper)

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        out_dir = ROOT / meta["dir"]
        items = sort_records(by_artifact.get(artifact, []), repo_stats)

        by_task: dict[str, list[dict]] = defaultdict(list)
        for item in items:
            by_task[item["task"]].append(item)
        task_order = [task for task in ARTIFACT_TASK_ORDER[artifact] if task in by_task]

        spotlight = pick_highlights(items, repo_stats, limit=min(ARTIFACT_HIGHLIGHTS_PER_PAGE, len(items)))

        lines = [
            f"# {meta['emoji']} {meta['title']}",
            "",
            f"> {meta['short']}",
            "",
            f"**{count_label(len(items), 'curated paper')}** · [← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · "
            "[Candidate Inbox](../metadata/candidates/latest.md)",
            "",
            "<details>",
            "<summary><b>📐 How this pipeline works</b></summary>",
            "",
            "```text",
            MODEL_PATTERNS[artifact].strip(),
            "```",
            "",
            "</details>",
            "",
            "## Tasks in this category",
            "",
            " · ".join(f"[{task}]({slugify(task)}.md) <sub>({len(by_task[task])})</sub>" for task in task_order)
            if task_order
            else "_No tasks yet._",
            "",
        ]

        if spotlight:
            lines.extend(["## 🌟 Spotlight", ""])
            lines.extend(render_spotlight_card(rec, repo_stats) for rec in spotlight)

        lines.extend(["## Full Catalog", "", LEGEND, ""])
        for task in task_order:
            lines.extend(
                [
                    f"### [{task}]({slugify(task)}.md) · {len(by_task[task])}",
                    "",
                    render_table(sort_records(by_task[task], repo_stats), repo_stats),
                    "",
                ]
            )

        write_text(out_dir / "README.md", "\n".join(lines))

        for task in task_order:
            task_items = sort_records(by_task[task], repo_stats)
            task_spotlight = (
                pick_highlights(task_items, repo_stats, limit=1) if len(task_items) >= SPOTLIGHT_MIN_POOL else []
            )

            task_lines = [
                f"# {meta['emoji']} {meta['title']} / {task}",
                "",
                f"**{count_label(len(task_items), 'entry')}** · [← Root](../README.md) · [← {meta['title']}](README.md)",
                "",
            ]
            if task_spotlight:
                task_lines.extend(["## 🌟 Spotlight", ""])
                task_lines.extend(render_spotlight_card(rec, repo_stats) for rec in task_spotlight)
                task_lines.extend(["## Full List", "", LEGEND, ""])
            else:
                task_lines.extend([LEGEND, ""])

            task_lines.append(render_table(task_items, repo_stats))
            write_text(out_dir / f"{slugify(task)}.md", "\n".join(task_lines))


def _build_crosscut_pages(
    title_prefix: str,
    emoji: str,
    out_dir: Path,
    groups: dict[str, list[dict]],
    repo_stats: dict,
    index_title: str,
    index_note: str,
    column_label: str,
) -> None:
    """Shared renderer for the topic pages (grouped by `domain`) and the
    organization pages (grouped by `orgs`) -- both are "one group per file,
    plus one index" cross-cuts over the same records, differing only in
    labels and grouping key."""
    ranked = sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0].lower()))
    max_count = max((len(items) for _, items in ranked), default=0)

    index_lines = [
        f"# {emoji} {index_title}",
        "",
        f"> {index_note}",
        "",
        "[← Root](../README.md)",
        "",
    ]

    if not ranked:
        index_lines.append(f"_No {column_label.lower()} metadata has been added yet._")
        write_text(out_dir / "README.md", "\n".join(index_lines))
        return

    index_lines.extend([f"| {column_label} | Papers |", "|:--|--:|"])
    for key, items in ranked:
        index_lines.append(f"| [{key}]({slugify(key)}.md) | **{len(items)}** |")

    for key, items in ranked:
        items_sorted = sort_records(items, repo_stats)
        spotlight = pick_highlights(items_sorted, repo_stats, limit=1) if len(items_sorted) >= SPOTLIGHT_MIN_POOL else []

        lines = [
            f"# {emoji} {title_prefix}: {key}",
            "",
            f"**{count_label(len(items_sorted), 'entry')}** · [← Root](../README.md) · [← {index_title}](README.md)",
            "",
        ]
        if spotlight:
            lines.extend(["## 🌟 Spotlight", ""])
            lines.extend(render_spotlight_card(rec, repo_stats) for rec in spotlight)
            lines.extend(["## Full List", "", LEGEND, ""])
        else:
            lines.extend([LEGEND, ""])

        lines.append(render_table(items_sorted, repo_stats, show_artifact=True))
        write_text(out_dir / f"{slugify(key)}.md", "\n".join(lines))

    write_text(out_dir / "README.md", "\n".join(index_lines))


def build_topic_pages(papers: list[dict], repo_stats: dict) -> None:
    by_domain: dict[str, list[dict]] = defaultdict(list)
    for paper in papers:
        for domain in paper.get("domain", []):
            if domain not in DOMAIN_IGNORE:
                by_domain[domain].append(paper)

    _build_crosscut_pages(
        title_prefix="Topic",
        emoji="🏷️",
        out_dir=ROOT / "90-topics",
        groups=by_domain,
        repo_stats=repo_stats,
        index_title="Topic Pages",
        index_note="Cross-cutting topic views generated from `domain` tags.",
        column_label="Topic",
    )


def build_organization_pages(papers: list[dict], repo_stats: dict) -> None:
    by_org: dict[str, list[dict]] = defaultdict(list)
    for paper in papers:
        for org in paper.get("orgs", []):
            by_org[org].append(paper)

    _build_crosscut_pages(
        title_prefix="Organization",
        emoji="🏢",
        out_dir=ROOT / "91-organizations",
        groups=by_org,
        repo_stats=repo_stats,
        index_title="Organization Pages",
        index_note="Cross-cutting views generated from the `orgs` field. Add `orgs` to high-value entries to enable more of these.",
        column_label="Organization",
    )


def load_weekly_issues(weekly_dir: Path = WEEKLY_DATA_DIR) -> list[dict]:
    """Load all data/weekly/YYYY-Www.json issues in reverse-chronological order."""
    if not weekly_dir.exists():
        return []
    issues: list[dict] = []
    for path in sorted(weekly_dir.glob("*-W*.json"), reverse=True):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict) and payload.get("week"):
            issues.append(payload)
    issues.sort(key=lambda x: str(x.get("week", "")), reverse=True)
    return issues


def format_authors(authors: list[str]) -> str:
    cleaned = [a.strip() for a in (authors or []) if str(a).strip()]
    if not cleaned:
        return "Unknown"
    if len(cleaned) <= 2:
        return ", ".join(cleaned)
    return f"{cleaned[0]}, {cleaned[1]} et al."


def format_affiliations(affiliations: list[dict]) -> str:
    names = [str(a.get("name", "")).strip() for a in (affiliations or []) if isinstance(a, dict) and a.get("name")]
    return " · ".join(names) if names else "Unverified"


def format_weekly_links(item: dict) -> str:
    """Format Paper / Code / Project / HF links. Never show placeholders for missing links.
    GitHub stars include fetch-date tooltip."""
    links = item.get("links") or {}
    stats = item.get("stats") or {}
    fetched_date = str(stats.get("fetched_at") or "")[:10]
    parts: list[str] = []

    if links.get("paper"):
        parts.append(f"[Paper]({links['paper']})")
    if links.get("code"):
        stars = int(stats.get("github_stars", 0) or 0)
        star_label = f"Code ★{compact_number(stars)}" if stars > 0 else "Code"
        if stars > 0 and fetched_date:
            parts.append(f'[{star_label}]({links["code"]} "GitHub stars fetched {fetched_date}")')
        else:
            parts.append(f"[{star_label}]({links['code']})")
    if links.get("project"):
        parts.append(f"[Project]({links['project']})")
    if links.get("hf"):
        parts.append(f"[HF]({links['hf']})")

    return " · ".join(parts)


def render_weekly_items_table(items: list[dict]) -> str:
    lines = [
        "| Date | Work | Affiliation | Track | Score | Links |",
        "|:--|:--|:--|:--|--:|:--|",
    ]
    ordered = sorted(
        items,
        key=lambda x: (
            0 if x.get("is_pick_of_the_week") else 1,
            -int((x.get("score") or {}).get("total", 0)),
            str(x.get("title", "")).lower(),
        ),
    )
    for item in ordered:
        date_str = escape_table_cell(str(item.get("published_date") or "—"))
        trophy = "🏆 " if item.get("is_pick_of_the_week") else ""
        paper_url = (item.get("links") or {}).get("paper") or ""
        title_text = escape_table_cell(str(item.get("title") or ""))
        title_md = f"**[{title_text}]({paper_url})**" if paper_url else f"**{title_text}**"
        authors_md = escape_table_cell(format_authors(item.get("authors") or []))
        highlight_md = escape_table_cell(str(item.get("highlight") or ""))
        work_cell = f"{trophy}{title_md}<br>{authors_md}<br>{highlight_md}"
        aff_cell = escape_table_cell(format_affiliations(item.get("affiliations") or []))
        track_cell = TRACK_DISPLAY.get(str(item.get("track") or ""), str(item.get("track") or "—"))
        score_val = int((item.get("score") or {}).get("total", 0))
        links_cell = format_weekly_links(item)
        lines.append(
            f"| {date_str} | {work_cell} | {aff_cell} | {track_cell} | {score_val} | {links_cell} |"
        )
    return "\n".join(lines)


def render_weekly_block(
    latest_issue: dict | None,
    previous_issue: dict | None = None,
) -> str:
    """Render the README top Weekly Top Picks block wrapped in WEEKLY:START/END markers."""
    if not latest_issue:
        inner = "\n".join(
            [
                "## 🔥 This Week's Top Picks",
                "> No weekly issue has been published yet. · [How we select](docs/SELECTION.md) · [Past weeks](weekly/README.md)",
            ]
        )
        return f"{WEEKLY_START_MARKER}\n{inner}\n{WEEKLY_END_MARKER}"

    week = latest_issue["week"]
    window = latest_issue["window"]
    generated_at = str(latest_issue.get("generated_at") or "").replace("T", " ").replace("Z", " UTC")
    items = latest_issue.get("items") or []
    honorable = latest_issue.get("honorable_mentions") or []
    status = latest_issue.get("status", "empty")
    notes = str(latest_issue.get("notes") or "").strip()

    lines = [
        f"## 🔥 This Week's Top Picks · {week} ({window['start']} → {window['end']})",
        f"> Updated {generated_at} · Score ≥ 75 · [How we select](docs/SELECTION.md) · [Past weeks](weekly/README.md) · [Full issue](weekly/{week}.md)",
        "",
    ]

    if items:
        lines.append(render_weekly_items_table(items))
        empty_tracks = latest_issue.get("empty_tracks") or []
        if empty_tracks:
            labels = ", ".join(TRACK_DISPLAY.get(t, t) for t in empty_tracks)
            lines.extend(["", f"_No qualifying pick (≥ 75) this week for: {labels}._"])
        fetch_dates = sorted(
            {str((it.get("stats") or {}).get("fetched_at") or "")[:10] for it in items if (it.get("stats") or {}).get("fetched_at")}
        )
        if fetch_dates:
            lines.append(f"_GitHub star counts fetched on {fetch_dates[-1]} (hover Code link for date; not real-time)._")
    else:
        lines.append(f"**No qualifying Top Picks (≥ 75) for {week}.**")
        if notes:
            lines.extend(["", f"> {notes}"])
        if previous_issue:
            prev_w = previous_issue["week"]
            lines.extend(["", f"See previous issue: [{prev_w}](weekly/{prev_w}.md) · [All past weeks](weekly/README.md)"])
        else:
            lines.extend(["", "See [Weekly Archive](weekly/README.md) and [Hall of Fame](weekly/hall-of-fame.md)."])

    if honorable:
        lines.extend(["", f"### Notable (Score 65–74) · {len(honorable)}", "", render_weekly_items_table(honorable)])

    inner = "\n".join(lines)
    return f"{WEEKLY_START_MARKER}\n{inner}\n{WEEKLY_END_MARKER}"


def replace_weekly_block(readme_text: str, weekly_block: str) -> str:
    """Deterministically and idempotently replace ONLY the content between
    <!-- WEEKLY:START --> and <!-- WEEKLY:END -->."""
    if WEEKLY_START_MARKER not in readme_text or WEEKLY_END_MARKER not in readme_text:
        raise ValueError("README is missing <!-- WEEKLY:START --> / <!-- WEEKLY:END --> markers.")
    return WEEKLY_BLOCK_RE.sub(lambda _: weekly_block, readme_text, count=1)


def build_weekly_archive(issues: list[dict], out_dir: Path = WEEKLY_ARCHIVE_DIR) -> None:
    """Generate weekly/YYYY-Www.md for every issue and reverse-chronological weekly/README.md."""
    out_dir.mkdir(parents=True, exist_ok=True)

    for idx, issue in enumerate(issues):
        week = issue["week"]
        window = issue["window"]
        generated_at = str(issue.get("generated_at") or "").replace("T", " ").replace("Z", " UTC")
        items = issue.get("items") or []
        honorable = issue.get("honorable_mentions") or []
        empty_tracks = issue.get("empty_tracks") or []
        notes = str(issue.get("notes") or "").strip()

        lines = [
            f"# 🔥 Weekly Top Picks · {week} ({window['start']} → {window['end']})",
            "",
            f"> Generated `{generated_at}` · Status: `{issue.get('status', 'empty')}` · "
            "[← Homepage](../README.md) · [← All Weeks](README.md) · [Selection Rubric](../docs/SELECTION.md)",
            "",
        ]

        if items:
            lines.extend(["## Top Picks (Score ≥ 75)", "", render_weekly_items_table(items), ""])
            if empty_tracks:
                labels = ", ".join(TRACK_DISPLAY.get(t, t) for t in empty_tracks)
                lines.extend([f"_No qualifying pick this week for: {labels} (tracks are never padded)._", ""])
        else:
            lines.extend(
                [
                    "## Top Picks (Score ≥ 75)",
                    "",
                    "_No qualifying Top Picks this week._",
                    "",
                ]
            )
            if notes:
                lines.extend([f"> {notes}", ""])

        if honorable:
            lines.extend(["## Notable (Score 65–74)", "", render_weekly_items_table(honorable), ""])

        if notes and items:
            lines.extend(["## Notes", "", notes, ""])

        prev_issue = issues[idx + 1] if idx + 1 < len(issues) else None
        if prev_issue:
            lines.extend([f"Previous issue: [{prev_issue['week']}]({prev_issue['week']}.md)", ""])

        fetch_dates = sorted(
            {
                str((it.get("stats") or {}).get("fetched_at") or "")[:10]
                for it in (items + honorable)
                if (it.get("stats") or {}).get("fetched_at")
            }
        )
        star_note = fetch_dates[-1] if fetch_dates else window["end"]
        lines.extend(
            [
                "---",
                f"_GitHub star counts shown on this page were fetched on `{star_note}` and are not real-time._",
            ]
        )
        write_text(out_dir / f"{week}.md", "\n".join(lines))

    # Reverse-chronological index weekly/README.md
    index_lines = [
        "# 📅 Weekly Top Picks Archive",
        "",
        "> Reverse-chronological archive of weekly curated issues (Monday 00:00 → Sunday 23:59 UTC).  ",
        "> [← Homepage](../README.md) · [Selection Rubric](../docs/SELECTION.md) · [Hall of Fame (Legacy Editor's Picks)](hall-of-fame.md)",
        "",
    ]
    if issues:
        index_lines.extend(["| Week | Window (UTC) | Status | Top Picks | Notable |", "|:--|:--|:--|--:|--:|"])
        for issue in issues:
            w = issue["week"]
            win = issue["window"]
            index_lines.append(
                f"| [{w}]({w}.md) | {win['start']} → {win['end']} | `{issue.get('status', 'empty')}` | "
                f"{len(issue.get('items') or [])} | {len(issue.get('honorable_mentions') or [])} |"
            )
    else:
        index_lines.append("_No weekly issues published yet._")

    write_text(out_dir / "README.md", "\n".join(index_lines))


def build_root_readme(papers: list[dict], repo_stats: dict, weekly_issues: list[dict]) -> None:
    by_artifact: dict[str, list[dict]] = defaultdict(list)
    by_domain: Counter = Counter()
    by_org: Counter = Counter()

    for paper in papers:
        by_artifact[paper["artifact"]].append(paper)
        for domain in paper.get("domain", []):
            if domain not in DOMAIN_IGNORE:
                by_domain[domain] += 1
        for org in paper.get("orgs", []):
            by_org[org] += 1

    open_count = sum(1 for p in papers if p.get("open_source"))
    latest_issue = weekly_issues[0] if weekly_issues else None
    previous_issue = weekly_issues[1] if len(weekly_issues) > 1 else None
    content_date = latest_issue["window"]["end"] if latest_issue else "uninitialized"

    stars_badge = (
        f"[![GitHub Stars](https://img.shields.io/github/stars/{REPO_SLUG}"
        "?style=flat-square&labelColor=111827&color=F59E0B)]"
        f"(https://github.com/{REPO_SLUG}/stargazers)"
    )

    weekly_block = render_weekly_block(latest_issue, previous_issue)

    topic_pills = (
        " · ".join(
            f"[{domain}](90-topics/{slugify(domain)}.md) `({count})`"
            for domain, count in by_domain.most_common(TOPIC_INDEX_LIMIT)
        )
        if by_domain
        else "_No topic pages yet._"
    )
    org_pills = (
        " · ".join(
            f"[{org}](91-organizations/{slugify(org)}.md) `({count})`"
            for org, count in by_org.most_common(ORG_INDEX_LIMIT)
        )
        if by_org
        else "_No organization metadata yet._"
    )

    lines = [
        "<!-- AUTO-GENERATED by scripts/build.py — DO NOT EDIT MANUALLY -->",
        "",
        '<div align="center">',
        "",
        "# ✨ Awesome Generative Models",
        "",
        "**A self-healing, verified weekly catalog of generative models**  ",
        "Image · Video · 3D Assets · 3D Scenes · 4D Worlds",
        "",
        badge("Papers", str(len(papers)), "2563EB", "googlescholar")
        + " "
        + badge("Open Source", str(open_count), "16A34A", "opensourceinitiative")
        + " "
        + badge("Updated", content_date, "0EA5E9", "githubactions")
        + " "
        + stars_badge
        + " "
        + badge("License", "MIT", "0F766E", link="LICENSE"),
        "",
        "[🧭 Tracks](#-browse-by-track) · "
        "[🏢 Organizations](#-browse-by-organization) · "
        "[🏷️ Topics](#-browse-by-topic) · "
        "[📅 Weekly Archive](weekly/README.md) · "
        "[🏛️ Hall of Fame](weekly/hall-of-fame.md) · "
        "[📖 Surveys](#-recommended-surveys) · "
        "[🤝 Contribute](CONTRIBUTING.md)",
        "",
        "</div>",
        "",
        "---",
        "",
        WEEKLY_START_MARKER,
        WEEKLY_END_MARKER,
        "",
        "---",
        "",
        "## 🧭 Browse by Track",
        "",
        render_artifact_navigation(by_artifact),
        "",
        "## 🏢 Browse by Organization",
        "",
        f"{org_pills} · [All organizations →](91-organizations/README.md)",
        "",
        "## 🏷️ Browse by Topic",
        "",
        f"{topic_pills} · [All topics →](90-topics/README.md)",
        "",
        "## 📖 Recommended Surveys",
        "",
    ]
    for title, url in SURVEY_LINKS:
        lines.append(f"- [{title}]({url})")

    lines.extend(
        [
            "",
            "---",
            "",
            "<details>",
            "<summary><b>📐 Architecture, Selection Rubric &amp; Local Commands</b></summary>",
            "",
            "### Generative Pipelines by Track",
            "",
            render_pipeline_overview_table(),
            "",
            "### Self-Healing Curation Pipeline",
            "",
            "```text",
            "Multi-source weekly harvest (arXiv + HF Daily Papers + GitHub + OpenAlex + Inbox)",
            "  -> Hard Gates H1-H8 -> 100-pt Evidence Rubric -> data/weekly/YYYY-Www.json",
            "  -> Deterministic PR CI (fast validate + build diff) -> README & Weekly Archive",
            "  -> Wednesday Deep Validate (24h two-strike quarantine, never breaks scheduled CI)",
            "```",
            "",
            "### Documentation & Reports",
            "",
            "- [Selection Rubric (`docs/SELECTION.md`)](docs/SELECTION.md) — Hard gates H1–H8, 100-pt rubric, anti-gaming rules",
            "- [Operations Manual (`docs/OPERATIONS.md`)](docs/OPERATIONS.md) — Re-running weekly picks, quarantine release, thresholds",
            "- [Repository Audit (`docs/AUDIT.md`)](docs/AUDIT.md) — Root-cause analysis and 6 blocking-error fixes",
            "- [Validation Report (`metadata/validation/latest.md`)](metadata/validation/latest.md) — Fast & deep verification status",
            "",
            "### Local Commands",
            "",
            "```bash",
            "python scripts/validate_data.py --skip-network   # deterministic validation",
            "python scripts/weekly/pipeline.py --dry-run      # preview weekly top picks",
            "python scripts/build.py                          # rebuild README & all pages",
            "python -m unittest discover -s tests -v          # run offline test suite",
            "```",
            "",
            "</details>",
            "",
            '<div align="center">',
            "",
            "<sub>Every displayed fact is verifiable from primary sources · "
            "If this catalog helps your research, consider giving it a ⭐.</sub>",
            "",
            "</div>",
        ]
    )

    rendered = replace_weekly_block("\n".join(lines), weekly_block)
    write_text(ROOT / "README.md", rendered)


def main() -> None:
    papers = load_records(include_quarantined=False)
    repo_stats = load_json(CACHE_DIR / "repo_stats.json")
    weekly_issues = load_weekly_issues()

    build_foundations_page(papers)
    build_artifact_pages(papers, repo_stats)
    build_topic_pages(papers, repo_stats)
    build_organization_pages(papers, repo_stats)
    build_weekly_archive(weekly_issues)
    build_root_readme(papers, repo_stats, weekly_issues)

    print(f"[build] generated pages for {len(papers)} entries and {len(weekly_issues)} weekly issue(s).")


if __name__ == "__main__":
    main()
