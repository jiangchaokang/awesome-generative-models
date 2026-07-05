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

from catalog_common import (
    ARTIFACT_META,
    ARTIFACT_ORDER,
    ARTIFACT_TASK_ORDER,
    DOMAIN_IGNORE,
    ORG_BADGE_META,
    ROOT,
    SURVEY_LINKS,
    VENUE_COLORS,
    compact_number,
    load_records,
    parse_github_repo,
    slugify,
)

CACHE_DIR = ROOT / "metadata" / "cache"

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

HOME_HIGHLIGHTS_PER_ARTIFACT = 1
ARTIFACT_HIGHLIGHTS_PER_PAGE = 3
# Below this many entries, a spotlight card would just repeat the whole
# table right underneath it, so smaller task/topic/org pages skip it.
SPOTLIGHT_MIN_POOL = 4
TOPIC_INDEX_LIMIT = 20
ORG_INDEX_LIMIT = 20

CANDIDATE_REPORT_DATE_FORMAT = "%Y-%m-%d"
RECENT_CANDIDATE_REPORT_LIMIT = 6
RECENT_CANDIDATE_REPORT_COLUMNS = 3

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


def bar(count: int, max_count: int, width: int = 14) -> str:
    """Tiny text-only bar chart. No images, so it renders instantly and
    identically in light/dark themes and on mobile."""
    if max_count <= 0 or count <= 0:
        return "░" * width
    filled = max(1, round(width * count / max_count))
    return "█" * filled + "░" * (width - filled)


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
        meta = ORG_BADGE_META.get(slugify(org), {"label": org, "color": "334155", "logo": None})
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
    lines = ["| Artifact | Focus | Explore by task | Papers |", "|:--|:--|:--|:--|"]
    max_count = max((len(v) for v in by_artifact.values()), default=0)

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        items = by_artifact.get(artifact, [])
        present_tasks = {item["task"] for item in items}
        task_links = [
            f"[{task}]({meta['dir']}/{slugify(task)}.md)"
            for task in ARTIFACT_TASK_ORDER[artifact]
            if task in present_tasks
        ]
        lines.append(
            f"| [{meta['emoji']} {meta['title']}]({meta['dir']}/README.md) | {meta['short']} | "
            f"{' · '.join(task_links) if task_links else '—'} | `{bar(len(items), max_count)}` {len(items)} |"
        )

    return "\n".join(lines)


def render_pipeline_overview_table() -> str:
    lines = ["| Artifact | Input | Core generator | Output |", "|:--|:--|:--|:--|"]
    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        stage_in, stage_core, stage_out = MODEL_STAGES[artifact]
        lines.append(f"| {meta['emoji']} {meta['title']} | {stage_in} | {stage_core} | {stage_out} |")
    return "\n".join(lines)


def list_recent_candidate_reports(limit: int = RECENT_CANDIDATE_REPORT_LIMIT) -> list[dict[str, str]]:
    candidates_dir = ROOT / "metadata" / "candidates"
    reports: list[dict[str, str]] = []

    if not candidates_dir.exists():
        return reports

    for child in candidates_dir.iterdir():
        if not child.is_dir():
            continue
        try:
            datetime.strptime(child.name, CANDIDATE_REPORT_DATE_FORMAT)
        except ValueError:
            continue

        report_path = child / "report.md"
        if not report_path.exists():
            continue

        reports.append({"date": child.name, "path": report_path.relative_to(ROOT).as_posix()})

    reports.sort(key=lambda item: item["date"], reverse=True)
    return reports[: max(0, int(limit))]


def render_recent_candidate_reports_table(
    limit: int = RECENT_CANDIDATE_REPORT_LIMIT,
    columns: int = RECENT_CANDIDATE_REPORT_COLUMNS,
) -> str:
    reports = list_recent_candidate_reports(limit=limit)
    if not reports:
        return (
            "_No daily reports yet on this freshly reset inbox — the next scheduled run "
            "(daily at 01:25 UTC) will populate this section automatically._"
        )

    cells = [f"[{item['date']}]({item['path']})" for item in reports]
    total_slots = len(cells)
    remainder = total_slots % columns
    if remainder:
        total_slots += columns - remainder
    cells.extend(["—"] * (total_slots - len(cells)))

    lines = ["| " + " | ".join(["Report"] * columns) + " |", "| " + " | ".join([":--"] * columns) + " |"]
    for start in range(0, total_slots, columns):
        lines.append("| " + " | ".join(cells[start : start + columns]) + " |")
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

    index_lines.extend([f"| {column_label} | Papers |", "|:--|:--|"])
    for key, items in ranked:
        index_lines.append(f"| [{key}]({slugify(key)}.md) | `{bar(len(items), max_count)}` {len(items)} |")

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


def build_root_readme(papers: list[dict], repo_stats: dict) -> None:
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
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    lines = [
        "<!-- AUTO-GENERATED by scripts/build.py — DO NOT EDIT MANUALLY -->",
        "",
        '<div align="center">',
        "",
        "# ✨ Awesome Generative Models",
        "",
        "**A high-precision, exact-link catalog of recent generative-model research**  ",
        "**for images, video, 3D assets, 3D scenes, and 4D dynamic worlds.**",
        "",
        badge("Papers", str(len(papers)), "2563EB", "googlescholar", style="for-the-badge")
        + " "
        + badge("Open Source", str(open_count), "16A34A", "opensourceinitiative", style="for-the-badge")
        + " "
        + badge("Scope", "2025-01+", "0EA5E9", style="for-the-badge")
        + " "
        + badge("Updated", today, "F59E0B", "githubactions", style="for-the-badge"),
        "",
        badge("License", "MIT", "0F766E", link="LICENSE")
        + " "
        + badge("Contributing", "PRs Welcome", "2563EB", "github", "CONTRIBUTING.md")
        + " "
        + badge("Candidates", "Daily Inbox", "EA580C", "githubactions", "metadata/candidates/latest.md")
        + " "
        + badge("Validation", "Report", "7C3AED", "checkmarx", "metadata/validation/latest.md"),
        "",
        "*Exact paper / code / project links only — every entry is reviewed before merge.*",
        "",
        "</div>",
        "",
        "---",
        "",
        "## 🧭 Quick Navigation",
        "",
        render_artifact_navigation(by_artifact),
        "",
        "## 🌟 Editor's Picks",
        "",
        "> The highest-signal recent work in each area — newest, most complete, or most widely adopted.",
        "",
    ]

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        highlights = pick_highlights(by_artifact.get(artifact, []), repo_stats, limit=HOME_HIGHLIGHTS_PER_ARTIFACT)
        if not highlights:
            continue
        lines.append(f"**{meta['emoji']} {meta['title']}** · [see all →]({meta['dir']}/README.md)")
        lines.append("")
        lines.extend(render_spotlight_card(rec, repo_stats) for rec in highlights)

    lines.extend(
        [
            "<details>",
            "<summary><b>📐 How each pipeline works</b> (click to expand)</summary>",
            "",
            render_pipeline_overview_table(),
            "",
            "</details>",
            "",
            "## 🏷️ Explore by Topic",
            "",
        ]
    )
    if by_domain:
        max_domain = max(by_domain.values())
        lines.extend(["| Topic | Papers |", "|:--|:--|"])
        for domain, count in by_domain.most_common(TOPIC_INDEX_LIMIT):
            lines.append(f"| [{domain}](90-topics/{slugify(domain)}.md) | `{bar(count, max_domain)}` {count} |")
    else:
        lines.append("_No topic pages yet._")

    lines.extend(["", "## 🏢 Explore by Organization", ""])
    if by_org:
        max_org = max(by_org.values())
        lines.extend(["| Organization | Papers |", "|:--|:--|"])
        for org, count in by_org.most_common(ORG_INDEX_LIMIT):
            lines.append(f"| [{org}](91-organizations/{slugify(org)}.md) | `{bar(count, max_org)}` {count} |")
    else:
        lines.append("_No organization metadata yet._")

    lines.extend(
        [
            "",
            "## 📬 Daily Candidate Inbox",
            "",
            "> Each report lists only candidates never surfaced before (a delta, not a re-scan). "
            "A day with 0 new items is normal — it means nothing new yet cleared the 2025-01-01+ scope and quality bar.",
            "",
            render_recent_candidate_reports_table(),
            "",
            "## ⚙️ Curation Pipeline",
            "",
            "```text",
            "Daily harvesting (2025-01-01+ floor, true-novelty dates, quality score, dedupe ledger)",
            "  -> metadata/candidates/YYYY-MM-DD/ -> human review -> data/*.jsonl",
            "  -> fast validate (schema/scope/dedupe, every push) -> build -> publish",
            "  -> weekly deep validate (live links + stars, non-blocking to daily)",
            "```",
            "",
            "<details>",
            "<summary><b>🛠️ Build &amp; maintenance commands</b></summary>",
            "",
            "```bash",
            "# fast: schema, vocab, dedupe, 2025+ scope -- no network, runs on every push",
            "python scripts/validate_data.py --skip-network",
            "",
            "# deep: also verifies every exact link + refreshes GitHub star/license cache (weekly)",
            "python scripts/validate_data.py --write-cache",
            "",
            "# rebuild README and all generated pages",
            "python scripts/build.py",
            "",
            "# refresh the daily candidate inbox",
            "python scripts/fetch_candidates.py --days 14",
            "```",
            "",
            "</details>",
            "",
            "## 📖 Recommended Surveys",
            "",
        ]
    )
    for title, url in SURVEY_LINKS:
        lines.append(f"- [{title}]({url})")

    lines.extend(
        [
            "",
            "---",
            "",
            '<div align="center">',
            "",
            "**If this repository helps your research or engineering work, please consider giving it a star.**",
            "",
            "</div>",
        ]
    )

    write_text(ROOT / "README.md", "\n".join(lines))


def main() -> None:
    papers = load_records()
    repo_stats = load_json(CACHE_DIR / "repo_stats.json")

    build_foundations_page(papers)
    build_artifact_pages(papers, repo_stats)
    build_topic_pages(papers, repo_stats)
    build_organization_pages(papers, repo_stats)
    build_root_readme(papers, repo_stats)

    print(f"[build] generated pages for {len(papers)} entries.")


if __name__ == "__main__":
    main()
