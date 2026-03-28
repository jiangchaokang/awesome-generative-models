# Taxonomy for awesome-generative-models

## 1. Core Principle

Every work is described by a fixed six-tuple:

```
(primary_artifact, task, domain, representation, method, conditioning)
```

- `primary_artifact` → **top-level directory** (what the model ultimately produces)
- `task` → **sub-page** (the specific problem the paper addresses)
- `domain` → **tag / topic page** (application scenario)
- `representation` → **tag** (output format)
- `method` → **tag** (algorithmic family)
- `conditioning` → **tag** (input modalities)

## 2. Top-Level Directories (by Final Artifact)

| Directory | `primary_artifact` | Description |
|:----------|:-------------------|:------------|
| `10-image-2d/` | `image-2d` | Final output is a single 2D image |
| `20-video/` | `video` | Final output is a video or video edit |
| `30-3d-object-asset/` | `3d-object-asset` | Single 3D object / asset / avatar |
| `40-3d-scene/` | `3d-scene` | Multi-object 3D scene (indoor, urban, explorable) |
| `50-4d-dynamic-scene-world/` | `4d-dynamic-scene-world` | Dynamic 3D/4D world, world model, simulation |

## 3. Classification Rules

**Rule A — Always classify by final artifact.** If the output is a video, it belongs in `20-video/`, even if the topic is autonomous driving.

**Rule B — `domain` must not be a top-level directory.** `autonomous-driving`, `indoor`, `human-avatar` are tags/topics only.

**Rule C — `representation` and `method` must not be directories.** `3DGS`, `diffusion`, `occupancy` are tags only.

**Rule D — One paper, one primary location.** Cross-cutting capabilities are expressed through tags and topic pages.

**Rule E — When ambiguous, think: "Where would a user search?"**

## 4. Tag Vocabularies

### `domain`
general, indoor, outdoor-urban, autonomous-driving, human-avatar, gameplay, tabletop, robotics

### `representation`
pixel, latent, token, mesh, point-cloud, octree, occupancy, bev, 3dgs, 4dgs, vector-graph, world-latent, part-graph, triplane, trajectory, layout, video-latent, depth, multiview

### `method`
diffusion, autoregressive, flow, rectified-flow, flow-matching, vae, transformer, llm-agent, world-model, splatting, procedural, training-free, drifting

### `conditioning`
text, image, video, camera, layout, pose, trajectory, action, depth, multiview, audio, mask, sketch, motion

## 5. Data File Schema

Each line in `data/*.jsonl` is a JSON object:

```json
{
  "id": "vectorworld",
  "title": "VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs",
  "venue": "arXiv 2026",
  "task": "autonomous-driving",
  "domain": ["autonomous-driving"],
  "representation": ["vector-graph"],
  "method": ["vae", "diffusion", "flow", "world-model"],
  "conditioning": ["trajectory"],
  "open_source": true,
  "featured": true,
  "stars": 120,
  "paper": "https://arxiv.org/abs/2603.17652",
  "repo": "https://github.com/jiangchaokang/VectorWorld",
  "homepage": "",
  "summary": "Streaming vector-graph world model for km-level driving simulation via motion-aware VAE and flow-based DiT on lane-agent graphs."
}
```