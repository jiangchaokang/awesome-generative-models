# Taxonomy for `awesome-generative-models`

## 1. 核心原则

本仓库用一个固定六元组描述每个工作：

```text
(primary_artifact, task, domain, representation, method, conditioning)
```

其中：

- `primary_artifact`：最终生成对象，决定**一级目录**
- `task`：用户真正检索时最常用的任务，决定**二级页面**
- `domain`：应用场景，只做**标签 / topic page**
- `representation`：表示形式，只做**标签**
- `method`：方法家族，只做**标签**
- `conditioning`：条件输入，只做**标签**

---

## 2. 一级目录：按最终生成对象分

| 一级目录 | `primary_artifact` | 说明 |
|---|---|---|
| `10-image-2d/` | `image-2d` | 最终产物是单张 2D 图像 |
| `20-video/` | `video` | 最终产物是视频或视频编辑结果 |
| `30-3d-object-asset/` | `3d-object-asset` | 单物体 / 资产 / avatar asset |
| `40-3d-scene/` | `3d-scene` | 多物体 3D 场景、室内、城市、可探索 3D scene |
| `50-4d-dynamic-scene-world/` | `4d-dynamic-scene-world` | 显式动态 3D/4D 世界、world model、仿真、自动驾驶 |

---

## 3. 二级页面：按任务分

### Image 2D
- `text-to-image`
- `controllable-generation`
- `personalization`
- `model-efficiency`
- `alignment-safety`

### Video
- `text-to-video`
- `image-to-video`
- `video-editing`
- `human-animation`
- `long-video`
- `autonomous-driving-video`

### 3D Object / Asset
- `3d-shape-generation`
- `text-to-3d`
- `image-to-3d`
- `part-aware-generation`
- `articulated-asset`
- `human-avatar`

### 3D Scene
- `agentic-scene-generation`
- `indoor`
- `layout-to-scene`
- `scene-editing`
- `general-scene-generation`
- `single-image-to-scene`
- `outdoor-urban`

### 4D / World
- `autonomous-driving`
- `4d-generation`
- `world-models`
- `game-worlds`
- `simulation`

---

## 4. 标签轴：不要升成主目录

### `domain`
- `general`
- `indoor`
- `outdoor-urban`
- `autonomous-driving`
- `human-avatar`
- `gameplay`
- `tabletop`

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
- `vector-graph`
- `world-latent`
- `part-graph`
- `triplane`
- `trajectory`
- `layout`

### `method`
- `diffusion`
- `autoregressive`
- `flow`
- `rectified-flow`
- `vae`
- `transformer`
- `llm-agent`
- `world-model`
- `splatting`
- `flow-matching`

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

---

## 5. 判定规则

### Rule A — 永远按“最终产物”归类
- 最终产物是单张图：进 `10-image-2d`
- 最终产物是视频：进 `20-video`
- 最终产物是 3D asset：进 `30-3d-object-asset`
- 最终产物是 3D scene：进 `40-3d-scene`
- 最终产物是显式动态世界 / world model / 4D scene：进 `50-4d-dynamic-scene-world`

### Rule B — `domain` 不得与 `artifact` 并列
- `autonomous-driving` 不是一级目录
- `indoor` 不是一级目录
- `human-avatar` 不是一级目录

它们只能是标签或 topic page。

### Rule C — `representation` 和 `method` 不得做一级目录
- 不要把 `3DGS / BEV / occupancy / NeRF / vector-graph` 放成一级目录
- 不要把 `diffusion / autoregressive / VAE / flow` 放成一级目录

### Rule D — 每篇论文只能有一个主归属
一个工作只能在一个主页面出现一次；跨域能力通过 tags 和 topic pages 体现。

### Rule E — 有争议时，优先看“用户会怎么找”
例如：
- driving video generation：若产物本质是视频，归 `20-video`，加 `autonomous-driving`
- driving world model：若产物是 world state / occupancy / BEV / 4D scene / simulation，归 `50-4d-dynamic-scene-world`

---

## 6. 例子

### 例子 1：VectorWorld
- `primary_artifact = 4d-dynamic-scene-world`
- `task = autonomous-driving`
- `domain = autonomous-driving`
- `representation = vector-graph`
- `method = vae + diffusion + flow + world-model`
- `conditioning = trajectory / history`

### 例子 2：RoomCraft
- `primary_artifact = 3d-scene`
- `task = indoor`
- `domain = indoor`

### 例子 3：LINA
- `primary_artifact = image-2d`
- `task = text-to-image`
- `method = autoregressive`

---

## 7. 数据文件 schema

本仓库只手工维护 `data/*.jsonl`。

每行一篇论文，例如：

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
  "paper": "https://arxiv.org/abs/2603.17652",
  "repo": "https://github.com/jiangchaokang/VectorWorld",
  "summary": "流式向量图世界模型，适合放在 4D world / autonomous-driving 主线。"
}
```

### 字段说明

- `id`：唯一 slug
- `title`：论文标题
- `venue`：如 `CVPR 2025`、`ICLR 2025`、`arXiv 2026`
- `task`：二级页面名
- `domain`：可选，默认 `general`
- `representation`：可选
- `method`：可选
- `conditioning`：可选
- `open_source`：可选，默认 `false`
- `paper`：可选；若留空，生成器会自动回退到 paper search
- `repo`：可选；若留空且 `open_source=true`，生成器会回退到 GitHub search
- `summary`：可选；若留空，生成器会自动生成一句 TL;DR
