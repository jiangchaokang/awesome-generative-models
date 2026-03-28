from __future__ import annotations

import html
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]

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
        "title": "🖼️ Image 2D",
        "short": "最终产物是单张 2D 图像。",
    },
    "video": {
        "dir": "20-video",
        "title": "🎬 Video",
        "short": "最终产物是视频或视频编辑结果。",
    },
    "3d-object-asset": {
        "dir": "30-3d-object-asset",
        "title": "🧱 3D Object / Asset",
        "short": "单物体、3D 资产、可复用 avatar / articulated asset。",
    },
    "3d-scene": {
        "dir": "40-3d-scene",
        "title": "🏙️ 3D Scene",
        "short": "多物体 3D 场景、室内、城市、可探索 scene。",
    },
    "4d-dynamic-scene-world": {
        "dir": "50-4d-dynamic-scene-world",
        "title": "🌍 4D Dynamic Scene / World",
        "short": "显式动态 3D/4D 场景、world model、仿真与自动驾驶。",
    },
}

VENUE_ORDER = {
    "CVPR": 1,
    "ICCV": 2,
    "ECCV": 3,
    "NEURIPS": 4,
    "ICLR": 5,
    "ICML": 6,
    "SIGGRAPH": 7,
    "AAAI": 8,
    "ACL": 9,
    "UIST": 10,
    "NATURE": 11,
    "3DV": 12,
    "TVCG": 13,
    "TMM": 14,
    "ICRA": 15,
    "ARXIV": 99,
}

HUMANIZE = {
    "image-2d": "2D 图像",
    "video": "视频",
    "3d-object-asset": "3D 资产/物体",
    "3d-scene": "3D 场景",
    "4d-dynamic-scene-world": "4D 动态场景/世界",
    "text-to-image": "文本到图像",
    "controllable-generation": "可控生成",
    "personalization": "个性化生成",
    "model-efficiency": "高效生成/模型压缩",
    "alignment-safety": "对齐/安全/可解释性",
    "text-to-video": "文本到视频",
    "image-to-video": "图像到视频",
    "video-editing": "视频编辑",
    "human-animation": "人物动画",
    "long-video": "长视频生成",
    "autonomous-driving-video": "自动驾驶视频生成",
    "3d-shape-generation": "3D 形状生成",
    "text-to-3d": "文本到 3D",
    "image-to-3d": "图像到 3D",
    "part-aware-generation": "部件级 3D 生成",
    "articulated-asset": "可动/装配式 3D 资产",
    "human-avatar": "3D 人体/Avatar",
    "agentic-scene-generation": "Agent 驱动 3D 场景生成",
    "indoor": "室内场景生成",
    "layout-to-scene": "布局到场景",
    "scene-editing": "场景编辑",
    "general-scene-generation": "通用 3D 场景生成",
    "single-image-to-scene": "单图到 3D 场景",
    "outdoor-urban": "室外/城市场景",
    "autonomous-driving": "自动驾驶世界模型",
    "4d-generation": "4D 生成",
    "world-models": "世界模型",
    "game-worlds": "游戏/交互世界",
    "simulation": "仿真",
    "general": "通用",
    "indoor-domain": "室内",
    "autonomous-driving-domain": "自动驾驶",
    "human-avatar-domain": "人体/Avatar",
    "gameplay": "游戏/交互",
    "tabletop": "桌面任务",
}

SURVEY_LINKS = [
    (
        "Simulating the Real World: A Unified Survey of Multimodal Generative Models",
        "https://arxiv.org/abs/2503.04641",
    ),
    (
        "A Survey of World Models for Autonomous Driving",
        "https://arxiv.org/abs/2501.11260",
    ),
    (
        "The Role of World Models in Shaping Autonomous Driving: A Comprehensive Survey",
        "https://arxiv.org/abs/2502.10498",
    ),
    (
        "Foundation Models in Autonomous Driving: A Survey on Scenario Generation and Scenario Analysis",
        "https://arxiv.org/abs/2506.11526",
    ),
]

DOMAIN_IGNORE = {"general"}


def ensure_list(value, default=None):
    if value is None:
        return list(default or [])
    if isinstance(value, list):
        return value
    return [value]


def extract_year(text: str) -> int:
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else 0


def venue_rank(venue: str) -> int:
    first = (venue or "").split()[0].upper()
    return VENUE_ORDER.get(first, 999)


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "item"


def pretty(token: str) -> str:
    return HUMANIZE.get(token, token.replace("-", " "))


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


def load_papers():
    papers = []
    seen_ids = set()

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
                record["year"] = int(record.get("year") or extract_year(record.get("venue", "")))
                record["id"] = record.get("id") or slugify(record.get("title", ""))

                for field in ("id", "title", "venue", "task"):
                    if not record.get(field):
                        raise ValueError(f"{path}:{lineno} 缺少必要字段 `{field}`")

                if record["id"] in seen_ids:
                    raise ValueError(f"重复 id: {record['id']} ({path}:{lineno})")
                seen_ids.add(record["id"])
                papers.append(record)

    papers.sort(key=lambda p: (-p["year"], venue_rank(p["venue"]), p["title"].lower()))
    return papers


def paper_link(record: dict) -> str:
    return record.get("paper") or paper_search_url(record["title"], record["venue"])


def repo_link(record: dict) -> str:
    if record.get("repo"):
        return record["repo"]
    if record.get("open_source"):
        return repo_search_url(record["title"])
    return ""


def render_links(record: dict) -> str:
    links = [f"[Paper]({paper_link(record)})"]
    repo = repo_link(record)
    if repo:
        links.append(f"[Code]({repo})")
    return " · ".join(links)


def auto_summary(record: dict) -> str:
    if record.get("summary"):
        return record["summary"]

    parts = [
        f"面向 {pretty(record['task'])} 的 {pretty(record['artifact'])} 工作"
    ]

    if record["domain"] and record["domain"] != ["general"]:
        domain_text = "/".join(pretty(x) for x in record["domain"])
        parts.append(f"领域：{domain_text}")

    if record["representation"]:
        rep_text = "/".join(record["representation"][:2])
        parts.append(f"表示：{rep_text}")

    if record["method"]:
        method_text = "/".join(record["method"][:2])
        parts.append(f"方法：{method_text}")

    if record["conditioning"]:
        cond_text = "/".join(record["conditioning"][:2])
        parts.append(f"条件：{cond_text}")

    return "；".join(parts) + "。"


def tag_tokens(record: dict) -> list[str]:
    tokens = [record["venue"], record["task"]]

    for item in record["domain"]:
        if item not in DOMAIN_IGNORE:
            tokens.append(item)

    tokens.extend(record["representation"][:2])
    tokens.extend(record["method"][:2])
    tokens.extend(record["conditioning"][:2])

    if record.get("open_source"):
        tokens.append("open-source")

    # 去重但保持顺序
    output = []
    seen = set()
    for token in tokens:
        if token and token not in seen:
            seen.add(token)
            output.append(token)
    return output


def render_tag_pills(record: dict) -> str:
    return " ".join(f"`{token}`" for token in tag_tokens(record))


def render_paper(record: dict) -> str:
    title = html.escape(record["title"])
    summary = auto_summary(record)
    tags = render_tag_pills(record)
    links = render_links(record)

    return "\n".join(
        [
            "<details>",
            f"<summary><strong>{title}</strong> — {tags}</summary>",
            "",
            f"- **TL;DR**: {summary}",
            f"- **Links**: {links}",
            "",
            "</details>",
            "",
        ]
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def build_foundations_page(papers: list[dict]) -> None:
    out_dir = ROOT / "00-surveys-and-foundations"
    out_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        "# 00-surveys-and-foundations",
        "",
        "> Auto-generated. 这里放稳定的分类原则、维护策略和推荐综述。",
        "",
        "## 推荐先读",
        "",
    ]

    for title, url in SURVEY_LINKS:
        lines.append(f"- [{title}]({url})")

    lines.extend(
        [
            "",
            "## 维护策略",
            "",
            "- 主索引只看 `primary_artifact`，不把 `domain / method / representation` 混入一级目录。",
            "- 数据源只维护 `data/*.jsonl`，所有页面由 `scripts/build.py` 自动生成。",
            "- 每日更新采用“候选抓取 + 人工审核”两段式，见 `metadata/candidates/latest.md`。",
            "- 不确定的链接不要硬写，留空即可，生成器会自动回退到搜索链接。",
            "",
            "## 快速入口",
            "",
            "- [Taxonomy](../docs/taxonomy.md)",
            "- [Daily candidates](../metadata/candidates/latest.md)",
            "- [Root README](../README.md)",
        ]
    )

    write_text(out_dir / "README.md", "\n".join(lines))


def build_artifact_pages(papers: list[dict]) -> None:
    by_artifact = defaultdict(list)
    for paper in papers:
        by_artifact[paper["artifact"]].append(paper)

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        artifact_dir = ROOT / meta["dir"]
        artifact_dir.mkdir(parents=True, exist_ok=True)
        artifact_papers = by_artifact.get(artifact, [])

        by_task = defaultdict(list)
        for paper in artifact_papers:
            by_task[paper["task"]].append(paper)

        # Artifact README
        lines = [
            f"# {meta['dir']} — {meta['title']}",
            "",
            f"> {len(artifact_papers)} papers. {meta['short']}",
            "",
            "[↑ Back to root](../README.md)",
            "",
            "## Tasks",
            "",
        ]

        for task, items in sorted(by_task.items(), key=lambda x: (-len(x[1]), x[0])):
            task_file = slugify(task) + ".md"
            lines.append(f"- [{task}]({task_file}) ({len(items)})")

        lines.extend(["", "## All papers", ""])
        for paper in artifact_papers:
            lines.append(render_paper(paper))

        write_text(artifact_dir / "README.md", "\n".join(lines))

        # Task pages
        for task, items in by_task.items():
            task_file = artifact_dir / (slugify(task) + ".md")
            task_lines = [
                f"# {meta['dir']} / {task}",
                "",
                f"> {len(items)} papers.",
                "",
                "[↑ Back to root](../README.md) · [↑ Back to artifact](README.md)",
                "",
            ]
            for paper in items:
                task_lines.append(render_paper(paper))
            write_text(task_file, "\n".join(task_lines))


def build_topic_pages(papers: list[dict]) -> None:
    topic_dir = ROOT / "90-topics"
    topic_dir.mkdir(parents=True, exist_ok=True)

    by_domain = defaultdict(list)
    for paper in papers:
        for domain in paper["domain"]:
            if domain not in DOMAIN_IGNORE:
                by_domain[domain].append(paper)

    topic_readme = [
        "# 90-topics",
        "",
        "> Cross-cutting topic pages generated from `domain` tags.",
        "",
        "[↑ Back to root](../README.md)",
        "",
        "## Topic index",
        "",
    ]

    for domain, items in sorted(by_domain.items(), key=lambda x: (-len(x[1]), x[0])):
        filename = slugify(domain) + ".md"
        topic_readme.append(f"- [{domain}]({filename}) ({len(items)})")

        artifact_counter = Counter(p["artifact"] for p in items)
        lines = [
            f"# 90-topics / {domain}",
            "",
            f"> {len(items)} papers.",
            "",
            "[↑ Back to root](../README.md) · [↑ Back to topics](README.md)",
            "",
            "## By artifact",
            "",
            "| Artifact | Count |",
            "|---|---:|",
        ]

        for artifact in ARTIFACT_ORDER:
            count = artifact_counter.get(artifact, 0)
            if count:
                lines.append(f"| {artifact} | {count} |")

        lines.extend(["", "## Papers", ""])
        for paper in items:
            lines.append(render_paper(paper))

        write_text(topic_dir / filename, "\n".join(lines))

    write_text(topic_dir / "README.md", "\n".join(topic_readme))


def build_root_readme(papers: list[dict]) -> None:
    by_artifact = defaultdict(list)
    for paper in papers:
        by_artifact[paper["artifact"]].append(paper)

    domains = Counter()
    for paper in papers:
        for domain in paper["domain"]:
            if domain not in DOMAIN_IGNORE:
                domains[domain] += 1

    lines = [
        "# awesome-generative-models",
        "",
        "> Auto-generated from `data/*.jsonl` by `scripts/build.py`.",
        "",
        "**Single source of truth:** only edit the files in `data/`.",
        "",
        "## Design rules",
        "",
        "- 一级目录只看 **最终产物** `primary_artifact`。",
        "- 二级页面只看 **任务** `task`。",
        "- `domain / representation / method / conditioning` 全部做 tags 或 topic pages。",
        "- 每篇工作只出现一次；跨领域能力用 tags 表达。",
        "- 日更采用“候选自动抓取 + 人工审核入库”。",
        "",
        "## Taxonomy axes",
        "",
        "| Axis | Role in repo | Examples |",
        "|---|---|---|",
        "| `primary_artifact` | 一级目录 | image-2d, video, 3d-object-asset, 3d-scene, 4d-dynamic-scene-world |",
        "| `task` | 二级页面 | text-to-image, video-editing, indoor, autonomous-driving |",
        "| `domain` | topic page / tag | indoor, autonomous-driving, human-avatar, gameplay |",
        "| `representation` | tag | mesh, point-cloud, occupancy, 3dgs, vector-graph |",
        "| `method` | tag | diffusion, autoregressive, vae, flow, llm-agent |",
        "| `conditioning` | tag | text, image, video, camera, pose, layout, action |",
        "",
        "## Directories",
        "",
        "| Directory | Focus | Count |",
        "|---|---|---:|",
        "| [00-surveys-and-foundations](00-surveys-and-foundations/README.md) | Surveys, taxonomy, maintenance policy | - |",
    ]

    for artifact in ARTIFACT_ORDER:
        meta = ARTIFACT_META[artifact]
        count = len(by_artifact.get(artifact, []))
        lines.append(
            f"| [{meta['dir']}]({meta['dir']}/README.md) | {meta['short']} | {count} |"
        )

    lines.extend(
        [
            f"| [90-topics](90-topics/README.md) | Cross-cutting topic pages | {sum(domains.values())} tag hits |",
            "",
            f"## Stats",
            "",
            f"- **Seed papers:** {len(papers)}",
            f"- **Topic pages:** {len(domains)}",
            "",
            "## Topics",
            "",
        ]
    )

    for domain, count in domains.most_common():
        lines.append(f"- [{domain}](90-topics/{slugify(domain)}.md) ({count})")

    lines.extend(
        [
            "",
            "## Latest / highlighted seed entries",
            "",
        ]
    )

    for paper in papers[:15]:
        lines.append(
            f"- [{paper['title']}]({paper_link(paper)}) — `{paper['venue']}` `{paper['artifact']}` `{paper['task']}`"
        )

    lines.extend(
        [
            "",
            "## Build",
            "",
            "```bash",
            "python scripts/build.py",
            "```",
            "",
            "## Daily candidate harvesting",
            "",
            "```bash",
            "python scripts/fetch_candidates.py",
            "```",
            "",
            "Daily candidates will be written to:",
            "",
            "- `metadata/candidates/latest.md`",
            "",
            "## Editing workflow",
            "",
            "1. Add / edit lines in `data/*.jsonl`",
            "2. Run `python scripts/build.py`",
            "3. Commit generated pages together with the data change",
        ]
    )

    write_text(ROOT / "README.md", "\n".join(lines))


def main():
    papers = load_papers()
    build_foundations_page(papers)
    build_artifact_pages(papers)
    build_topic_pages(papers)
    build_root_readme(papers)
    print(f"[build] generated README and pages for {len(papers)} papers.")


if __name__ == "__main__":
    main()