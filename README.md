# awesome-generative-models

> Auto-generated from `data/*.jsonl` by `scripts/build.py`.

**Single source of truth:** only edit the files in `data/`.

## Design rules

- 一级目录只看 **最终产物** `primary_artifact`。
- 二级页面只看 **任务** `task`。
- `domain / representation / method / conditioning` 全部做 tags 或 topic pages。
- 每篇工作只出现一次；跨领域能力用 tags 表达。
- 日更采用“候选自动抓取 + 人工审核入库”。

## Taxonomy axes

| Axis | Role in repo | Examples |
|---|---|---|
| `primary_artifact` | 一级目录 | image-2d, video, 3d-object-asset, 3d-scene, 4d-dynamic-scene-world |
| `task` | 二级页面 | text-to-image, video-editing, indoor, autonomous-driving |
| `domain` | topic page / tag | indoor, autonomous-driving, human-avatar, gameplay |
| `representation` | tag | mesh, point-cloud, occupancy, 3dgs, vector-graph |
| `method` | tag | diffusion, autoregressive, vae, flow, llm-agent |
| `conditioning` | tag | text, image, video, camera, pose, layout, action |

## Directories

| Directory | Focus | Count |
|---|---|---:|
| [00-surveys-and-foundations](00-surveys-and-foundations/README.md) | Surveys, taxonomy, maintenance policy | - |
| [10-image-2d](10-image-2d/README.md) | 最终产物是单张 2D 图像。 | 31 |
| [20-video](20-video/README.md) | 最终产物是视频或视频编辑结果。 | 34 |
| [30-3d-object-asset](30-3d-object-asset/README.md) | 单物体、3D 资产、可复用 avatar / articulated asset。 | 30 |
| [40-3d-scene](40-3d-scene/README.md) | 多物体 3D 场景、室内、城市、可探索 scene。 | 32 |
| [50-4d-dynamic-scene-world](50-4d-dynamic-scene-world/README.md) | 显式动态 3D/4D 场景、world model、仿真与自动驾驶。 | 37 |
| [90-topics](90-topics/README.md) | Cross-cutting topic pages | 53 tag hits |

## Stats

- **Seed papers:** 164
- **Topic pages:** 6

## Topics

- [autonomous-driving](90-topics/autonomous-driving.md) (24)
- [human-avatar](90-topics/human-avatar.md) (10)
- [indoor](90-topics/indoor.md) (9)
- [gameplay](90-topics/gameplay.md) (6)
- [outdoor-urban](90-topics/outdoor-urban.md) (3)
- [tabletop](90-topics/tabletop.md) (1)

## Latest / highlighted seed entries

- [Captain Safari: A World Engine](https://scholar.google.com/scholar?q=Captain%20Safari%3A%20A%20World%20Engine) — `CVPR 2026` `4d-dynamic-scene-world` `4d-generation`
- [PerpetualWonder: Long-Horizon Action-Conditioned 4D Scene Generation](https://scholar.google.com/scholar?q=PerpetualWonder%3A%20Long-Horizon%20Action-Conditioned%204D%20Scene%20Generation) — `CVPR 2026` `4d-dynamic-scene-world` `4d-generation`
- [FantasyWorld: Geometry-Consistent World Modeling via Unified Video and 3D Prediction](https://scholar.google.com/scholar?q=FantasyWorld%3A%20Geometry-Consistent%20World%20Modeling%20via%20Unified%20Video%20and%203D%20Prediction) — `ICLR 2026` `4d-dynamic-scene-world` `4d-generation`
- [Minute-Long Videos with Dual Parallelisms](https://scholar.google.com/scholar?q=Minute-Long%20Videos%20with%20Dual%20Parallelisms) — `AAAI 2026` `video` `long-video`
- [SPATIALGEN: Layout-guided 3D Indoor Scene Generation](https://scholar.google.com/scholar?q=SPATIALGEN%3A%20Layout-guided%203D%20Indoor%20Scene%20Generation) — `3DV 2026` `3d-scene` `layout-to-scene`
- [Seeing the Future, Perceiving the Future: A Unified Driving World Model for Future Generation and Perception](https://scholar.google.com/scholar?q=Seeing%20the%20Future%2C%20Perceiving%20the%20Future%3A%20A%20Unified%20Driving%20World%20Model%20for%20Future%20Generation%20and%20Perception) — `ICRA 2026` `4d-dynamic-scene-world` `autonomous-driving`
- [AssetFormer: Modular 3D Assets Generation with Autoregressive Transformer](https://arxiv.org/abs/2602.12100) — `arXiv 2026` `3d-object-asset` `text-to-3d`
- [DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving](https://arxiv.org/abs/2602.06521) — `arXiv 2026` `4d-dynamic-scene-world` `autonomous-driving`
- [DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving](https://arxiv.org/abs/2603.19675) — `arXiv 2026` `4d-dynamic-scene-world` `autonomous-driving`
- [Fuse3D: Generating 3D Assets Controlled by Multi-Image Fusion](https://arxiv.org/abs/2602.17040) — `arXiv 2026` `3d-object-asset` `image-to-3d`
- [GeoDiff3D: Self-Supervised 3D Scene Generation with Geometry-Constrained 2D Diffusion Guidance](https://arxiv.org/search/?query=GeoDiff3D%3A%20Self-Supervised%203D%20Scene%20Generation%20with%20Geometry-Constrained%202D%20Diffusion%20Guidance&searchtype=all&abstracts=show&order=-announced_date_first&size=50) — `arXiv 2026` `3d-scene` `general-scene-generation`
- [iFSQ: Improving FSQ for Image Generation with 1 Line of Code](https://arxiv.org/abs/2601.17124) — `arXiv 2026` `image-2d` `model-efficiency`
- [LINA: Linear Autoregressive Image Generative Models with Continuous Tokens](https://arxiv.org/abs/2601.22630) — `arXiv 2026` `image-2d` `text-to-image`
- [UniDWM: Towards a Unified Driving World Model via Multifaceted Representation Learning](https://arxiv.org/abs/2602.01536) — `arXiv 2026` `4d-dynamic-scene-world` `autonomous-driving`
- [VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs](https://arxiv.org/abs/2603.17652) — `arXiv 2026` `4d-dynamic-scene-world` `autonomous-driving`

## Build

```bash
python scripts/build.py
```

## Daily candidate harvesting

```bash
python scripts/fetch_candidates.py
```

Daily candidates will be written to:

- `metadata/candidates/latest.md`

## Editing workflow

1. Add / edit lines in `data/*.jsonl`
2. Run `python scripts/build.py`
3. Commit generated pages together with the data change
