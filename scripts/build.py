#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlencode, urlparse

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

HOME_HIGHLIGHTS_PER_ARTIFACT = 1
ARTIFACT_HIGHLIGHTS_PER_PAGE = 4
TOPIC_INDEX_LIMIT = 20
ORG_INDEX_LIMIT = 20


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


def venue_badge(rec: dict) -> str:
    head = (rec.get("venue", "").split() or ["Other"])[0].upper()
    color = VENUE_COLORS.get(head, "64748B")
    return badge("Venue", rec.get("venue", "Unknown"), color, link=rec.get("venue_url", ""))


def task_badge(rec: dict) -> str:
    return badge("Track", rec["task"], ARTIFACT_COLORS.get(rec["artifact"], "0EA5E9"))


def availability_badge(rec: dict) -> str:
    if rec.get("open_source"):
        return badge("Source", "Open", "16A34A", "opensourceinitiative")
    return badge("Source", "Closed", "6B7280")


def scope_badge(rec: dict) -> str:
    if rec.get("year", 0) < 2025 and rec.get("active_since", 0) >= 2025:
        return badge("Legacy", f"Active since {rec['active_since']}", "F59E0B")
    return ""


def org_badges(rec: dict) -> list[str]:
    out: list[str] = []
    for org in rec.get("orgs", [])[:3]:
        meta = ORG_BADGE_META.get(slugify(org), {"label": org, "color": "334155", "logo": None})
        out.append(badge("Org", meta["label"], meta["color"], meta.get("logo")))
    return out


def append_tag(out: list[str], seen: set[str], label: str, message: str, color: str) -> None:
    key = f"{label}:{slugify(message)}"
    if not message or key in seen:
        return
    seen.add(key)
    out.append(badge(label, message, color))


def tag_badges(rec: dict) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()

    for item in rec.get("method", [])[:2]:
        append_tag(out, seen, "Method", item, "7C3AED")

    for item in rec.get("representation", [])[:1]:
        append_tag(out, seen, "Repr", item, "0D9488")

    for item in rec.get("conditioning", [])[:1]:
        append_tag(out, seen, "Cond", item, "475569")

    for item in rec.get("domain", [])[:1]:
        if item != "general" and slugify(item) != slugify(rec["task"]):
            append_tag(out, seen, "Domain", item, "EA580C")

    return out


def link_badges(rec: dict, repo_stats: dict) -> str:
    parts: list[str] = []

    if rec.get("paper"):
        logo = "arxiv" if "arxiv.org" in rec["paper"].lower() else None
        parts.append(
            badge(
                "Paper",
                paper_badge_message(rec["paper"]),
                "B31B1B",
                logo=logo,
                link=rec["paper"],
            )
        )

    if rec.get("repo"):
        stars = record_stars(rec, repo_stats)
        msg = "GitHub" if stars <= 0 else f"GitHub ★ {compact_number(stars)}"
        parts.append(badge("Code", msg, "181717", "github", rec["repo"]))

    if rec.get("homepage"):
        parts.append(badge("Project", "Site", "0EA5E9", "googlechrome", rec["homepage"]))

    return " ".join(parts) if parts else "—"


def render_record_card(rec: dict, repo_stats: dict) -> str:
    top_badges = [
        venue_badge(rec),
        task_badge(rec),
        availability_badge(rec),
        scope_badge(rec),
        *org_badges(rec),
    ]
    top_badges = [x for x in top_badges if x]

    lines = [
        f"### {linked_title(rec)}",
        "",
        " ".join(top_badges),
        "",
        f"> {rec['summary']}",
        "",
        link_badges(rec, repo_stats),
    ]

    tags = tag_badges(rec)
    if tags:
        lines.extend(["", " ".join(tags)])

    if rec.get("scope_note"):
        lines.extend(["", f"_Scope note: {rec['scope_note']}_"])

    lines.append("")
    return "\n".join(lines)


def render_compact_index(records: list[dict], repo_stats: dict, include_artifact: bool = False) -> str:
    header = ["| Title |", " Artifact |" if include_artifact else "", " Task | Venue | Links |"]
    align = ["|:--|", ":--|" if include_artifact else "", ":--|:--|:--|"]
    lines = ["".join(header), "".join(align)]

    for rec in records:
        links: list[str] = []
        if rec.get("paper"):
            links.append(f"[Paper]({rec['paper']})")
        if rec.get("repo"):
            links.append(f"[Code]({rec['repo']})")
        if rec.get("homepage"):
            links.append(f"[Project]({rec['homepage']})")

        artifact_text = f" {ARTIFACT_META[rec['artifact']]['title']} |" if include_artifact else ""
        title_text = linked_title(rec)
        lines.append(
            f"| **{title_text}** |{artifact_text} {rec['task']} | {rec['venue']} | "
            f"{' / '.join(links) if links else '—'} |"
        )

    return "\n".join(lines)


def render_artifact_navigation(by_artifact: dict[str, list[dict]]) -> str:
    lines = [
        "| Artifact | Focus | Quick links | Count |",
        "|:--|:--|:--|--:|",
    ]

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
            f"| [{meta['emoji']} {meta['title']}]({meta['dir']}/README.md) | "
            f"{meta['short']} | {' · '.join(task_links) if task_links else '—'} | {len(items)} |"
        )

    return "\n".join(lines)


def render_model_patterns() -> str:
    lines: list[str] = []
    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        lines.extend(
            [
                f"### [{meta['emoji']} {meta['title']}]({meta['dir']}/README.md)",
                "",
                "```text",
                MODEL_PATTERNS[artifact].strip(),
                "```",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


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
        "- [Root README](../README.mdaxonomy.md)",
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
        highlights = pick_highlights(items, repo_stats, limit=min(ARTIFACT_HIGHLIGHTS_PER_PAGE, len(items)))

        lines = [
            f"# {meta['emoji']} {meta['title']}",
            "",
            f"> {meta['short']}",
            "",
            f"**Curated entries:** {len(items)}",
            "",
            "[← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)",
            "",
            "## Research Pattern",
            "",
            "```text",
            MODEL_PATTERNS[artifact].strip(),
            "```",
            "",
            "## Quick Navigation",
            "",
            " · ".join([f"[`{task}`]({slugify(task)}.md)" for task in task_order]) if task_order else "_No tasks yet._",
            "",
        ]

        if highlights:
            lines.extend(["## Selected Papers", ""])
            for rec in highlights:
                lines.append(render_record_card(rec, repo_stats))

        lines.extend(["## By Task", ""])
        for task in task_order:
            lines.extend([f"## [{task}]({slugify(task)}.md)", "", f"**{len(by_task[task])} entries**", ""])
            for rec in sort_records(by_task[task], repo_stats):
                lines.append(render_record_card(rec, repo_stats))

        lines.extend(
            [
                "## Compact Index",
                "",
                "<details>",
                "<summary><b>Open compact index</b></summary>",
                "",
                render_compact_index(items, repo_stats),
                "",
                "</details>",
                "",
            ]
        )

        write_text(out_dir / "README.md", "\n".join(lines))

        for task in task_order:
            task_path = out_dir / f"{slugify(task)}.md"
            task_items = sort_records(by_task[task], repo_stats)
            task_lines = [
                f"# {meta['emoji']} {meta['title']} / {task}",
                "",
                f"**Entries:** {len(task_items)}",
                "",
                "[← Root](../README.md) · [← Category](README.md)",
                "",
            ]
            for rec in task_items:
                task_lines.append(render_record_card(rec, repo_stats))

            task_lines.extend(
                [
                    "## Compact Index",
                    "",
                    "<details>",
                    "<summary><b>Open compact index</b></summary>",
                    "",
                    render_compact_index(task_items, repo_stats),
                    "",
                    "</details>",
                    "",
                ]
            )
            write_text(task_path, "\n".join(task_lines))


def build_topic_pages(papers: list[dict], repo_stats: dict) -> None:
    out_dir = ROOT / "90-topics"
    by_domain: dict[str, list[dict]] = defaultdict(list)

    for paper in papers:
        for domain in paper.get("domain", []):
            if domain not in DOMAIN_IGNORE:
                by_domain[domain].append(paper)

    index_lines = [
        "# 🏷️ Topic Pages",
        "",
        "> Cross-cutting topic views generated from `domain` tags.",
        "",
        "[← Root](../README.md)",
        "",
        "| Topic | Papers |",
        "|:--|--:|",
    ]

    for domain, items in sorted(by_domain.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        index_lines.append(f"| [{domain}]({slugify(domain)}.md) | {len(items)} |")

        lines = [
            f"# 🏷️ Topic: {domain}",
            "",
            f"**Entries:** {len(items)}",
            "",
            "[← Root](../README.md) · [← Topics](README.md)",
            "",
        ]

        for rec in sort_records(items, repo_stats):
            lines.append(render_record_card(rec, repo_stats))

        lines.extend(
            [
                "## Compact Index",
                "",
                "<details>",
                "<summary><b>Open compact index</b></summary>",
                "",
                render_compact_index(sort_records(items, repo_stats), repo_stats, include_artifact=True),
                "",
                "</details>",
                "",
            ]
        )

        write_text(out_dir / f"{slugify(domain)}.md", "\n".join(lines))

    write_text(out_dir / "README.md", "\n".join(index_lines))


def build_organization_pages(papers: list[dict], repo_stats: dict) -> None:
    out_dir = ROOT / "91-organizations"
    by_org: dict[str, list[dict]] = defaultdict(list)

    for paper in papers:
        for org in paper.get("orgs", []):
            by_org[org].append(paper)

    index_lines = [
        "# 🏢 Organization Pages",
        "",
        "> Cross-cutting views generated from the `orgs` field.",
        "",
        "[← Root](../README.md)",
        "",
    ]

    if not by_org:
        index_lines.extend(
            [
                "_No organization metadata has been added yet._",
                "",
                "Add `orgs` to high-value entries to enable organization badges and pages.",
            ]
        )
        write_text(out_dir / "README.md", "\n".join(index_lines))
        return

    index_lines.extend(["| Organization | Papers |", "|:--|--:|"])
    for org, items in sorted(by_org.items(), key=lambda kv: (-len(kv[1]), kv[0].lower())):
        index_lines.append(f"| [{org}]({slugify(org)}.md) | {len(items)} |")

        lines = [
            f"# 🏢 Organization: {org}",
            "",
            f"**Entries:** {len(items)}",
            "",
            "[← Root](../README.md) · [← Organizations](README.md)",
            "",
        ]
        for rec in sort_records(items, repo_stats):
            lines.append(render_record_card(rec, repo_stats))

        lines.extend(
            [
                "## Compact Index",
                "",
                "<details>",
                "<summary><b>Open compact index</b></summary>",
                "",
                render_compact_index(sort_records(items, repo_stats), repo_stats, include_artifact=True),
                "",
                "</details>",
                "",
            ]
        )
        write_text(out_dir / f"{slugify(org)}.md", "\n".join(lines))

    write_text(out_dir / "README.md", "\n".join(index_lines))


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

    lines = [
        "<!-- AUTO-GENERATED by scripts/build.py — DO NOT EDIT MANUALLY -->",
        "",
        '<div align="center">',
        "",
        "# ✨ Awesome Generative Models",
        "",
        "**A high-precision, exact-link catalog of recent generative-model work**  ",
        "**for images, videos, 3D assets, 3D scenes, and 4D dynamic worlds.**",
        "",
        badge("Papers", str(len(papers)), "2563EB", "googlescholar", style="for-the-badge"),
        badge("Open Source", str(open_count), "16A34A", "opensourceinitiative", style="for-the-badge"),
        badge("Scope", "2025+", "0EA5E9", style="for-the-badge"),
        badge("Links", "Exact Only", "B31B1B", "link", style="for-the-badge"),
        badge("Review", "Human Curated", "7C3AED", "github", style="for-the-badge"),
        "",
        badge("License", "MIT", "0F766E", link="LICENSE"),
        badge("Contributing", "PRs Welcome", "2563EB", "github", "CONTRIBUTING.md"),
        badge("Candidates", "Daily Inbox", "EA580C", "githubactions", "metadata/candidates/latest.md"),
        "",
        "</div>",
        "",
        "---",
        "",
        "## Quick Navigation",
        "",
        render_artifact_navigation(by_artifact),
        "",
        "## Model Patterns at a Glance",
        "",
        render_model_patterns(),
        "",
        "## Selected Frontier Reads",
        "",
        "> Each title links to the canonical paper page when available; otherwise it links to the exact project or repo page.",
        "",
    ]

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        highlights = pick_highlights(by_artifact.get(artifact, []), repo_stats, limit=HOME_HIGHLIGHTS_PER_ARTIFACT)
        if not highlights:
            continue
        lines.extend([f"### [{meta['emoji']} {meta['title']}]({meta['dir']}/README.md)", ""])
        for rec in highlights:
            lines.append(render_record_card(rec, repo_stats))

    lines.extend(["## Topic Pages", "", "| Topic | Papers |", "|:--|--:|"])
    if by_domain:
        for domain, count in by_domain.most_common(TOPIC_INDEX_LIMIT):
            lines.append(f"| [{domain}](90-topics/{slugify(domain)}.md) | {count} |")
    else:
        lines.append("| _No topic pages yet_ | 0 |")
    lines.append("")

    lines.extend(["## Organization Pages", "", "| Organization | Papers |", "|:--|--:|"])
    if by_org:
        for org, count in by_org.most_common(ORG_INDEX_LIMIT):
            lines.append(f"| [{org}](91-organizations/{slugify(org)}.md) | {count} |")
    else:
        lines.append("| _No organization metadata yet_ | 0 |")
    lines.append("")

    lines.extend(
        [
            "## Curation Pipeline",
            "",
            "```text",
            "Daily harvesting -> metadata/candidates/YYYY-MM-DD/ -> human review -> data/*.jsonl -> validate -> build -> publish",
            "```",
            "",
            "## Build & Maintenance",
            "",
            "```bash",
            "# validate source data and refresh repo stats cache",
            "python scripts/validate_data.py --write-cache",
            "",
            "# rebuild README and all generated pages",
            "python scripts/build.py",
            "",
            "# refresh the daily candidate inbox",
            "python scripts/fetch_candidates.py --days 14",
            "```",
            "",
            "## Recommended Surveys",
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
            "**If this repository helps your research or engineering work, consider giving it a star.**",
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