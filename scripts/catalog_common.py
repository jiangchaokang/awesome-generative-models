#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

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
        "emoji": "🖼️",
        "title": "Image 2D",
        "short": "Final output is a single 2D image: text-to-image, controllable generation, safety, personalization, and efficient inference.",
    },
    "video": {
        "dir": "20-video",
        "emoji": "🎬",
        "title": "Video",
        "short": "Final output is a video: text-to-video, image-to-video, editing, human animation, long video, and surround-view video.",
    },
    "3d-object-asset": {
        "dir": "30-3d-object-asset",
        "emoji": "🧊",
        "title": "3D Object / Asset",
        "short": "Reusable 3D objects, assets, avatars, articulated assets, and part-aware generation.",
    },
    "3d-scene": {
        "dir": "40-3d-scene",
        "emoji": "🏙️",
        "title": "3D Scene",
        "short": "Multi-object 3D scene generation, indoor/outdoor scenes, layout-conditioned scenes, and scene editing.",
    },
    "4d-dynamic-scene-world": {
        "dir": "50-4d-dynamic-scene-world",
        "emoji": "🌍",
        "title": "4D Dynamic Scene / World",
        "short": "Dynamic 3D/4D scenes, world models, simulation, autonomous driving, game worlds, and interactive world modeling.",
    },
}

ARTIFACT_TASK_ORDER = {
    "image-2d": [
        "text-to-image",
        "controllable-generation",
        "model-efficiency",
        "alignment-safety",
        "personalization",
    ],
    "video": [
        "text-to-video",
        "image-to-video",
        "video-editing",
        "human-animation",
        "long-video",
        "autonomous-driving-video",
        "surround-view-video",
    ],
    "3d-object-asset": [
        "3d-shape-generation",
        "image-to-3d",
        "text-to-3d",
        "part-aware-generation",
        "articulated-asset",
        "human-avatar",
    ],
    "3d-scene": [
        "general-scene-generation",
        "layout-to-scene",
        "agentic-scene-generation",
        "indoor",
        "outdoor-urban",
        "single-image-to-scene",
        "scene-editing",
    ],
    "4d-dynamic-scene-world": [
        "autonomous-driving",
        "4d-generation",
        "world-models",
        "simulation",
        "game-worlds",
        "robotics-worlds",
    ],
}

ALLOWED_TASKS = {
    artifact: set(tasks)
    for artifact, tasks in ARTIFACT_TASK_ORDER.items()
}

DOMAIN_VOCAB = {
    "general",
    "indoor",
    "outdoor-urban",
    "autonomous-driving",
    "human-avatar",
    "gameplay",
    "tabletop",
    "robotics",
}

REPRESENTATION_VOCAB = {
    "pixel",
    "latent",
    "token",
    "mesh",
    "point-cloud",
    "octree",
    "occupancy",
    "bev",
    "3dgs",
    "4dgs",
    "vector-graph",
    "world-latent",
    "part-graph",
    "triplane",
    "trajectory",
    "layout",
    "video-latent",
    "depth",
    "multiview",
    "point-latent",
}

METHOD_VOCAB = {
    "diffusion",
    "autoregressive",
    "flow",
    "rectified-flow",
    "flow-matching",
    "vae",
    "transformer",
    "llm-agent",
    "world-model",
    "splatting",
    "procedural",
    "training-free",
    "drifting",
}

CONDITIONING_VOCAB = {
    "text",
    "image",
    "video",
    "camera",
    "layout",
    "pose",
    "trajectory",
    "action",
    "depth",
    "multiview",
    "audio",
    "mask",
    "sketch",
    "motion",
}

DOMAIN_IGNORE = {"general"}

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
        "Foundation Models in Autonomous Driving: Scenario Generation and Analysis",
        "https://arxiv.org/abs/2506.11526",
    ),
]

WATCH_ORGS = [
    {"name": "NVIDIA", "github": "NVIDIA"},
    {"name": "NVLabs", "github": "NVlabs"},
    {"name": "Google Research", "github": "google-research"},
    {"name": "Google DeepMind", "github": "google-deepmind"},
    {"name": "Waymo", "github": "waymo-research"},
    {"name": "Tencent", "github": "Tencent"},
    {"name": "Tencent Hunyuan", "github": "Tencent-Hunyuan"},
    {"name": "Tencent ARC", "github": "TencentARC"},
    {"name": "Alibaba", "github": "QwenLM"},
    {"name": "Alibaba Wan", "github": "Wan-Video"},
    {"name": "Alibaba VILab", "github": "ali-vilab"},
    {"name": "ByteDance Seed", "github": "ByteDance-Seed"},
    {"name": "Adobe Research", "github": "adobe-research"},
    {"name": "Xiaomi", "github": "XiaomiMi"},
    {"name": "Tesla", "github": "tesla"},
    {"name": "THUDM", "github": "THUDM"},
    {"name": "Black Forest Labs", "github": "black-forest-labs"},
    {"name": "Stability AI", "github": "Stability-AI"},
]

VENUE_COLORS = {
    "CVPR": "2563EB",
    "ICCV": "2563EB",
    "ECCV": "2563EB",
    "ICLR": "7C3AED",
    "NEURIPS": "7C3AED",
    "ICML": "7C3AED",
    "SIGGRAPH": "EA580C",
    "SGP": "EA580C",
    "AAAI": "059669",
    "3DV": "059669",
    "ICRA": "059669",
    "ARXIV": "B31B1B",
    "TECHNICAL": "64748B",
    "MODEL": "64748B",
}

ORG_BADGE_META = {
    "nvidia": {"label": "NVIDIA", "color": "76B900", "logo": "nvidia"},
    "nvlabs": {"label": "NVLabs", "color": "76B900", "logo": "nvidia"},
    "google": {"label": "Google", "color": "4285F4", "logo": "google"},
    "google-research": {"label": "Google Research", "color": "4285F4", "logo": "google"},
    "google-deepmind": {"label": "Google DeepMind", "color": "4285F4", "logo": "google"},
    "waymo": {"label": "Waymo", "color": "00A1F1", "logo": "waymo"},
    "waymo-research": {"label": "Waymo", "color": "00A1F1", "logo": "waymo"},
    "tencent": {"label": "Tencent", "color": "0064FF", "logo": "tencentqq"},
    "tencent-hunyuan": {"label": "Tencent Hunyuan", "color": "0064FF", "logo": "tencentqq"},
    "tencentarc": {"label": "Tencent ARC", "color": "0064FF", "logo": "tencentqq"},
    "bytedance": {"label": "ByteDance", "color": "161823", "logo": "bytedance"},
    "bytedance-seed": {"label": "ByteDance Seed", "color": "161823", "logo": "bytedance"},
    "xiaomi": {"label": "Xiaomi", "color": "FF6900", "logo": "xiaomi"},
    "tesla": {"label": "Tesla", "color": "CC0000", "logo": "tesla"},
    "adobe": {"label": "Adobe", "color": "FF0000", "logo": "adobe"},
    "adobe-research": {"label": "Adobe Research", "color": "FF0000", "logo": "adobe"},
    "alibaba": {"label": "Alibaba", "color": "FF6A00", "logo": "alibabacloud"},
    "ali-vilab": {"label": "Alibaba VILab", "color": "FF6A00", "logo": "alibabacloud"},
    "wan-video": {"label": "Wan", "color": "FF6A00", "logo": "alibabacloud"},
    "black-forest-labs": {"label": "Black Forest Labs", "color": "111827", "logo": None},
    "stability-ai": {"label": "Stability AI", "color": "111827", "logo": None},
    "mit": {"label": "MIT", "color": "A31F34", "logo": None},
    "uc-berkeley": {"label": "UC Berkeley", "color": "003262", "logo": None},
    "berkeley": {"label": "UC Berkeley", "color": "003262", "logo": None},
    "tsinghua-university": {"label": "Tsinghua", "color": "660000", "logo": None},
    "shanghai-jiao-tong-university": {"label": "SJTU", "color": "8C1515", "logo": None},
    "independent": {"label": "Independent", "color": "475569", "logo": None},
}

def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()

def ensure_list(value: Any, default: list[str] | None = None) -> list[str]:
    if value is None:
        return list(default or [])
    if isinstance(value, list):
        out = [normalize_whitespace(str(v)) for v in value]
        return [v for v in out if v]
    text = normalize_whitespace(str(value))
    return [text] if text else list(default or [])

def slugify(text: str) -> str:
    text = normalize_whitespace(text).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text or "item"

def normalize_title(text: str) -> str:
    text = normalize_whitespace(text).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return normalize_whitespace(text)

def extract_year(text: str) -> int:
    match = re.search(r"(20\d{2})", text or "")
    return int(match.group(1)) if match else 0

def has_cjk(text: str) -> bool:
    return bool(re.search(r"[\u3400-\u9FFF]", text or ""))

def sentence_count(text: str) -> int:
    text = normalize_whitespace(text)
    if not text:
        return 0
    parts = re.split(r"(?<=[.!?])\s+", text)
    return len([p for p in parts if p.strip()])

def parse_github_repo(url: str) -> str:
    if not url:
        return ""
    parsed = urlparse(url)
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        return ""
    path = parsed.path.strip("/").removesuffix(".git")
    parts = [part for part in path.split("/") if part]
    if len(parts) < 2:
        return ""
    return f"{parts[0]}/{parts[1]}"

REPO_OWNER_TO_ORG = {
    "nvidia": "NVIDIA",
    "nvlabs": "NVLabs",
    "google-research": "Google Research",
    "google-deepmind": "Google DeepMind",
    "waymo-research": "Waymo",
    "tencent": "Tencent",
    "tencent-hunyuan": "Tencent Hunyuan",
    "tencentarc": "Tencent ARC",
    "qwenlm": "Alibaba",
    "wan-video": "Alibaba Wan",
    "ali-vilab": "Alibaba VILab",
    "bytedance-seed": "ByteDance Seed",
    "adobe-research": "Adobe Research",
    "xiaomimi": "Xiaomi",
    "tesla": "Tesla",
    "thudm": "THUDM",
    "black-forest-labs": "Black Forest Labs",
    "stability-ai": "Stability AI",
}

def repo_owner_from_url(url: str) -> str:
    full_name = parse_github_repo(url)
    if not full_name:
        return ""
    return full_name.split("/", 1)[0].strip()

def suggested_org_from_repo(url: str) -> str:
    owner = repo_owner_from_url(url).lower()
    return REPO_OWNER_TO_ORG.get(owner, "")

def arxiv_id_from_url(url: str) -> str:
    if not url:
        return ""
    match = re.search(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5})(?:v\d+)?", url)
    return match.group(1) if match else ""

def arxiv_year_from_url(url: str) -> int:
    arxiv_id = arxiv_id_from_url(url)
    if not arxiv_id:
        return 0
    return 2000 + int(arxiv_id[:2])

def compact_number(value: int) -> str:
    value = int(value or 0)
    if value >= 1_000_000:
        text = f"{value / 1_000_000:.1f}M"
        return text.rstrip("0").rstrip(".")
    if value >= 1_000:
        text = f"{value / 1_000:.1f}k"
        return text.rstrip("0").rstrip(".")
    return str(value)

def load_records(root: Path | None = None) -> list[dict]:
    repo_root = root or ROOT
    data_dir = repo_root / "data"
    records: list[dict] = []

    for file_name, artifact in FILE_ARTIFACT.items():
        path = data_dir / file_name
        if not path.exists():
            continue

        with path.open("r", encoding="utf-8") as handle:
            for lineno, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw or raw.startswith("#"):
                    continue

                record = json.loads(raw)
                record["_source_file"] = file_name
                record["_source_path"] = str(path)
                record["_lineno"] = lineno
                record["artifact"] = artifact

                record["id"] = normalize_whitespace(record.get("id") or slugify(record.get("title", "")))
                record["title"] = normalize_whitespace(record.get("title", ""))
                record["venue"] = normalize_whitespace(record.get("venue", ""))
                record["task"] = normalize_whitespace(record.get("task", ""))
                record["summary"] = normalize_whitespace(record.get("summary", ""))
                record["scope_note"] = normalize_whitespace(record.get("scope_note", ""))
                record["paper"] = normalize_whitespace(record.get("paper", ""))
                record["repo"] = normalize_whitespace(record.get("repo", ""))
                record["homepage"] = normalize_whitespace(record.get("homepage", ""))
                record["venue_url"] = normalize_whitespace(record.get("venue_url", ""))

                record["domain"] = ensure_list(record.get("domain"), ["general"])
                record["representation"] = ensure_list(record.get("representation"))
                record["method"] = ensure_list(record.get("method"))
                record["conditioning"] = ensure_list(record.get("conditioning"))
                record["orgs"] = ensure_list(record.get("orgs"))

                record["open_source"] = bool(record.get("open_source", False))
                record["featured"] = bool(record.get("featured", False))
                record["stars"] = int(record.get("stars", 0) or 0)
                record["year"] = int(record.get("year") or extract_year(record["venue"]) or 0)
                record["active_since"] = int(record.get("active_since", 0) or 0)

                records.append(record)

    records.sort(
        key=lambda r: (
            0 if r.get("featured") else 1,
            -max(r.get("year", 0), r.get("active_since", 0)),
            -int(r.get("stars", 0)),
            r.get("title", "").lower(),
        )
    )
    return records
