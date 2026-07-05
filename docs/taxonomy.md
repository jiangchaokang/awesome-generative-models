# Taxonomy for awesome-generative-models

## 1. The Core Contract

Each entry is described by the following metadata axes:

```text
(primary_artifact, task, domain, representation, method, conditioning, orgs)
```

- `primary_artifact` → top-level directory
- `task` → sub-page inside the artifact directory
- `domain` → cross-cutting topic page
- `representation` → technical tag
- `method` → technical tag
- `conditioning` → technical tag
- `orgs` → organization badges / organization pages only

Only `primary_artifact` decides the main location of a work.

---

## 2. Top-Level Directories

| Directory | Artifact key | Meaning |
|:--|:--|:--|
| `10-image-2d/` | `image-2d` | Final output is a single 2D image |
| `20-video/` | `video` | Final output is a video |
| `30-3d-object-asset/` | `3d-object-asset` | Final output is a reusable 3D object / asset / avatar |
| `40-3d-scene/` | `3d-scene` | Final output is a multi-object 3D scene |
| `50-4d-dynamic-scene-world/` | `4d-dynamic-scene-world` | Final output is a dynamic 3D/4D world / world model / simulation |

---

## 3. Allowed Tasks by Artifact

### `image-2d`

- `text-to-image`
- `controllable-generation`
- `model-efficiency`
- `alignment-safety`
- `personalization`

### `video`

- `text-to-video`
- `image-to-video`
- `video-editing`
- `human-animation`
- `long-video`
- `autonomous-driving-video`
- `surround-view-video`

### `3d-object-asset`

- `3d-shape-generation`
- `image-to-3d`
- `text-to-3d`
- `part-aware-generation`
- `articulated-asset`
- `human-avatar`

### `3d-scene`

- `general-scene-generation`
- `layout-to-scene`
- `agentic-scene-generation`
- `indoor`
- `outdoor-urban`
- `single-image-to-scene`
- `scene-editing`

### `4d-dynamic-scene-world`

- `autonomous-driving`
- `4d-generation`
- `world-models`
- `simulation`
- `game-worlds`
- `robotics-worlds`

---

## 4. Vocabulary

### `domain`

- `general`
- `indoor`
- `outdoor-urban`
- `autonomous-driving`
- `human-avatar`
- `gameplay`
- `tabletop`
- `robotics`

### `representation`

- `pixel`
- `latent`
- `token`
- `mesh`
- `point-cloud`
- `octree`
- `occupancy`
- `bev`
- `3dgs`
- `4dgs`
- `vector-graph`
- `world-latent`
- `part-graph`
- `triplane`
- `trajectory`
- `layout`
- `video-latent`
- `depth`
- `multiview`

### `method`

- `diffusion`
- `autoregressive`
- `flow`
- `rectified-flow`
- `flow-matching`
- `vae`
- `transformer`
- `llm-agent`
- `world-model`
- `splatting`
- `procedural`
- `training-free`
- `drifting`

### `conditioning`

- `text`
- `image`
- `video`
- `camera`
- `layout`
- `pose`
- `trajectory`
- `action`
- `depth`
- `multiview`
- `audio`
- `mask`
- `sketch`
- `motion`

---

## 5. Scope Policy

### Default rule

Only works **published in 2025 or later** are in scope.

### Legacy exception

A pre-2025 work may remain in the catalog only if:

- it was clearly active in 2025+, and
- `active_since` is provided, and
- `scope_note` explains why it still matters for this repository

This is the only supported mechanism for keeping legacy anchor works.

---

## 6. Link Policy

Public links must be exact.

Allowed:
- exact arXiv page
- exact conference paper page
- exact GitHub repo
- exact project page

Not allowed:
- Google Scholar search
- GitHub search
- generic search results
- “best guess” links

---

## 7. Example Record

```json
{
  "id": "worldplay",
  "title": "WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling",
  "venue": "arXiv 2025",
  "task": "world-models",
  "domain": ["gameplay"],
  "representation": ["world-latent"],
  "method": ["diffusion", "world-model"],
  "conditioning": ["action", "image"],
  "orgs": ["Tencent Hunyuan"],
  "summary": "WorldPlay is a real-time interactive world model designed for long-horizon geometric consistency. It introduces memory-aware context reconstruction and distillation for streaming generation at interactive frame rates. The work matters because it targets real-time controllable world interaction instead of short offline clips.",
  "paper": "https://arxiv.org/abs/2512.14614",
  "repo": "https://github.com/Tencent-Hunyuan/HY-WorldPlay",
  "homepage": "https://3d-models.hunyuan.tencent.com/worldplay",
  "open_source": true,
  "featured": true
}
```
