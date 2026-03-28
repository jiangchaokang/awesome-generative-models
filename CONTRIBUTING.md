# Contributing to awesome-generative-models

Thank you for your interest in contributing! This guide explains how to add papers and keep the repository consistent.

## Golden Rule: Only Edit Data Files

**Modify only these files:**

- `data/image_2d.jsonl`
- `data/video.jsonl`
- `data/object_3d.jsonl`
- `data/scene_3d.jsonl`
- `data/world_4d.jsonl`

**Never manually edit** `README.md` or any file under `10-image-2d/`, `20-video/`, `30-3d-object-asset/`, `40-3d-scene/`, `50-4d-dynamic-scene-world/`, `90-topics/`, or `00-surveys-and-foundations/`. These are **auto-generated** by `python scripts/build.py`.

## Scope

- **Time window:** 2025-01-01 onwards (active or newly published)
- **Priority:** Representative + open-source preferred + high retrieval value
- **Directions:** image / video / 3D object / 3D scene / 4D world

## Adding a Paper

### Required Fields

| Field | Description |
|:------|:-----------|
| `id` | Unique slug (e.g., `vectorworld`) |
| `title` | Full paper title |
| `venue` | e.g., `CVPR 2025`, `arXiv 2026` |
| `task` | Sub-page name (e.g., `text-to-image`, `autonomous-driving`) |

### Recommended Fields

| Field | Description |
|:------|:-----------|
| `summary` | 1–3 English sentences: what it does + core method + why it matters |
| `paper` | Paper URL (arXiv, conference) |
| `repo` | Code repository URL |
| `homepage` | Project page URL |
| `open_source` | `true` / `false` |
| `featured` | `true` for spotlight in README header |
| `method` | List: `["diffusion", "transformer"]` |
| `representation` | List: `["mesh", "3dgs"]` |
| `conditioning` | List: `["text", "image"]` |
| `domain` | List: `["autonomous-driving"]` |
| `stars` | GitHub stars (approximate, for sorting) |

### Classification Rules

1. **Classify by final artifact** — if output is a video, it goes to `video.jsonl`
2. **`domain` is a tag, not a directory** — `autonomous-driving` is never a top-level dir
3. **One paper, one file** — each work appears in exactly one `.jsonl` file
4. **When in doubt, ask:** "Where would a user search for this?"

### Writing a Summary

Template: **What it does + core technique + why it matters.**

Example:
```
Streaming vector-graph world model that scales driving simulation to km-level via motion-aware VAE and flow-based DiT on lane-agent graphs.
```

## Submission Flow

```bash
# 1. Edit the appropriate data file
vim data/world_4d.jsonl

# 2. Rebuild pages locally (optional but recommended)
python scripts/build.py

# 3. Commit and push
git add data/ README.md 10-image-2d/ 20-video/ 30-3d-object-asset/ 40-3d-scene/ 50-4d-dynamic-scene-world/ 90-topics/
git commit -m "data: add <paper-id>"
git push
```

If you push to `main`, GitHub Actions will automatically run `build.py` and commit the generated pages.

## Uncertain Links

If you cannot 100% confirm a URL, **leave the field empty**. The generator automatically falls back to:
- Paper → arXiv search or Google Scholar search
- Code → GitHub repository search

This is better than an incorrect link.