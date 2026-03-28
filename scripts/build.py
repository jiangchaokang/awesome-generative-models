#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

from catalog_common import (
    ARTIFACT_META,
    ARTIFACT_ORDER,
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

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")

def shields_url(
    label: str,
    message: str | None = None,
    color: str = "2563EB",
    logo: str | None = None,
    style: str = "flat-square",
) -> str:
    if message:
        url = f"https://img.shields.io/badge/{quote(str(label))}-{quote(str(message))}-{color}?style={style}"
    else:
        url = f"https://img.shields.io/badge/{quote(str(label))}-{color}?style={style}"
    if logo:
        url += f"&logo={quote(logo)}"
    return url

def badge(
    label: str,
    message: str | None = None,
    color: str = "2563EB",
    logo: str | None = None,
    link: str = "",
    style: str = "flat-square",
) -> str:
    alt = f"{label}: {message}" if message else label
    image = f"![{alt}]({shields_url(label, message, color, logo, style)})"
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

def venue_badge(rec: dict) -> str:
    head = (rec.get("venue", "").split() or ["Other"])[0].upper()
    color = VENUE_COLORS.get(head, "64748B")
    return badge("Venue", rec.get("venue", "Unknown"), color, None, rec.get("venue_url", ""))

def task_badge(rec: dict) -> str:
    return badge("Task", rec["task"], "0EA5E9")

def open_source_badge(rec: dict) -> str:
    if rec.get("open_source"):
        return badge("Open Source", None, "16A34A", "opensourceinitiative", rec.get("repo", ""))
    return badge("Closed Source", None, "6B7280")

def scope_badge(rec: dict) -> str:
    if rec.get("year", 0) < 2025 and rec.get("active_since", 0) >= 2025:
        return badge("Scope", f"Active since {rec['active_since']}", "F59E0B")
    return ""

def stars_badge(rec: dict, repo_stats: dict) -> str:
    stars = record_stars(rec, repo_stats)
    if stars <= 0:
        return ""
    return badge("GitHub", f"★ {compact_number(stars)}", "181717", "github", rec.get("repo", ""))

def org_badges(rec: dict) -> list[str]:
    out: list[str] = []
    for org in rec.get("orgs", [])[:4]:
        meta = ORG_BADGE_META.get(slugify(org), {"label": org, "color": "334155", "logo": None})
        out.append(badge(meta["label"], None, meta["color"], meta.get("logo")))
    return out

def tag_badges(rec: dict) -> list[str]:
    out: list[str] = []

    for item in rec.get("method", [])[:3]:
        out.append(badge(item, None, "7C3AED"))

    for item in rec.get("representation", [])[:2]:
        out.append(badge(item, None, "0D9488"))

    for item in rec.get("conditioning", [])[:2]:
        out.append(badge(item, None, "475569"))

    for item in rec.get("domain", [])[:2]:
        if item != "general":
            out.append(badge(item, None, "EA580C"))

    return out

def link_badges(rec: dict, repo_stats: dict) -> str:
    parts: list[str] = []

    if rec.get("paper"):
        if "arxiv.org" in rec["paper"].lower():
            parts.append(badge("Paper", "arXiv", "B31B1B", "arxiv", rec["paper"]))
        else:
            parts.append(badge("Paper", None, "B31B1B", None, rec["paper"]))

    if rec.get("repo"):
        stars = record_stars(rec, repo_stats)
        msg = f"GitHub ★ {compact_number(stars)}" if stars > 0 else "GitHub"
        parts.append(badge("Code", msg, "181717", "github", rec["repo"]))

    if rec.get("homepage"):
        parts.append(badge("Project", None, "0EA5E9", "googlechrome", rec["homepage"]))

    return " ".join(parts) if parts else "—"

def render_record_card(rec: dict, repo_stats: dict) -> str:
    top_badges = [
        venue_badge(rec),
        task_badge(rec),
        open_source_badge(rec),
        scope_badge(rec),
        stars_badge(rec, repo_stats),
        *org_badges(rec),
    ]
    top_badges = [x for x in top_badges if x]

    lines = [
        f"### {rec['title']}",
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
        lines.append(
            f"| **{rec['title']}** |{artifact_text} {rec['task']} | {rec['venue']} | "
            f"{' / '.join(links) if links else '—'} |"
        )

    return "\n".join(lines)

def build_foundations_page(papers: list[dict]) -> None:
    lines = [
        "# 📚 Surveys & Foundations",
        "",
        "> Auto-generated from the catalog source data.",
        "",
        "## Why this repository exists",
        "",
        "- **Strict taxonomy**: `primary_artifact` decides the main location; all other axes are metadata.",
        "- **Exact links only**: public pages never expose guessed search-result URLs.",
        "- **Human-reviewed inclusion**: the daily candidate inbox is only a review queue, not an auto-merge pipeline.",
        "- **English-only summaries**: every accepted entry must have a concise 1–3 sentence English summary.",
        "- **2025+ scope by default**: older entries require explicit `active_since` and `scope_note`.",
        "",
        "## Quick Links",
        "",
        "- [Root README](../README.md)",
        "- [Taxonomy](../docs/taxonomy.md)",
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

        task_order = sorted(by_task.keys(), key=lambda t: (-len(by_task[t]), t))
        highlights = pick_highlights(items, repo_stats, limit=min(6, len(items)))

        lines = [
            f"# {meta['emoji']} {meta['title']}",
            "",
            f"> {meta['short']}",
            "",
            f"**Curated entries:** {len(items)}",
            "",
            "[← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)",
            "",
            "## Quick Navigation",
            "",
            " ".join([f"[`{task}`](#{slugify(task)})" for task in task_order]) if task_order else "_No tasks yet._",
            "",
        ]

        if highlights:
            lines.extend(["## Highlights", ""])
            for rec in highlights:
                lines.append(render_record_card(rec, repo_stats))

        lines.extend(["## By Task", ""])
        for task in task_order:
            lines.extend([f"## {task}", "", f"**{len(by_task[task])} entries**", ""])
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
        "**A rigorously curated, English-only catalog of recent generative-model work**",
        "**for images, videos, 3D assets, 3D scenes, and 4D dynamic worlds.**",
        "",
        badge("Papers", str(len(papers)), "2563EB", "googlescholar", style="for-the-badge"),
        badge("Open Source", str(open_count), "16A34A", "opensourceinitiative", style="for-the-badge"),
        badge("Scope", "2025+", "0EA5E9", style="for-the-badge"),
        badge("Links", "Exact Only", "B31B1B", "link", style="for-the-badge"),
        badge("Review", "Human Curated", "7C3AED", "github", style="for-the-badge"),
        "",
        f"[{badge('License', 'MIT', '0F766E', None, style='flat-square') }](LICENSE)",
        f"[{badge('Contributing', 'PRs Welcome', '2563EB', 'github', 'CONTRIBUTING.md', style='flat-square')}]",
        f"[{badge('Daily Candidates', 'Inbox', 'EA580C', 'githubactions', 'metadata/candidates/latest.md', style='flat-square')}]",
        "",
        "</div>",
        "",
        "---",
        "",
        "## Why this repository is different",
        "",
        "- **Taxonomy does not mix axes.** Primary artifact decides the home page; domain / method / representation / conditioning / orgs are metadata.",
        "- **Public links are exact.** No search-result links are surfaced as if they were canonical paper or code URLs.",
        "- **Daily harvesting is separate from final inclusion.** Candidates go into a review inbox; accepted entries are merged manually.",
        "- **Pages are generated, not hand-edited.** The repo stays consistent as it grows.",
        "",
        "## Browse the Catalog",
        "",
        "| Directory | Focus | Count |",
        "|:--|:--|--:|",
        "| [00-surveys-and-foundations](00-surveys-and-foundations/README.md) | Surveys, policy, and taxonomy | — |",
    ]

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        lines.append(
            f"| [{meta['dir']}]({meta['dir']}/README.md) | {meta['short']} | {len(by_artifact.get(artifact, []))} |"
        )

    lines.append(f"| [90-topics](90-topics/README.md) | Cross-cutting domain pages | {len(by_domain)} |")
    lines.append(f"| [91-organizations](91-organizations/README.md) | Cross-cutting organization pages | {len(by_org)} |")
    lines.append("")

    lines.extend(["## Featured Radar", ""])
    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        highlights = pick_highlights(by_artifact.get(artifact, []), repo_stats, limit=2)
        if not highlights:
            continue
        lines.extend([f"### {meta['emoji']} {meta['title']}", ""])
        for rec in highlights:
            lines.append(render_record_card(rec, repo_stats))

    lines.extend(["## Topic Pages", "", "| Topic | Papers |", "|:--|--:|"])
    for domain, count in by_domain.most_common():
        lines.append(f"| [{domain}](90-topics/{slugify(domain)}.md) | {count} |")
    lines.append("")

    lines.extend(["## Organization Pages", "", "| Organization | Papers |", "|:--|--:|"])
    if by_org:
        for org, count in by_org.most_common(20):
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
