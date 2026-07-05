# 🏙️ 3D Scene

> Multi-object 3D scene generation, indoor/outdoor scenes, layout-conditioned scenes, and scene editing.

**36 curated papers** · [← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)

<details>
<summary><b>📐 How this pipeline works</b></summary>

```text
Text / layout / references / room constraints
        ↓
Planner / layout / scene graph / object set
        ↓
Scene generator (3DGS / mesh / occupancy / latent scene)
        ↓
Renderer / consistency / editing loop
        ↓
Static multi-object 3D scene
```

</details>

## Tasks in this category

[general-scene-generation](general-scene-generation.md) <sub>(14)</sub> · [layout-to-scene](layout-to-scene.md) <sub>(6)</sub> · [agentic-scene-generation](agentic-scene-generation.md) <sub>(5)</sub> · [indoor](indoor.md) <sub>(4)</sub> · [outdoor-urban](outdoor-urban.md) <sub>(3)</sub> · [single-image-to-scene](single-image-to-scene.md) <sub>(3)</sub> · [scene-editing](scene-editing.md) <sub>(1)</sub>

## 🌟 Spotlight

#### 🌟 [FlowScene: Style-Consistent Indoor Scene Generation with Multimodal Graph Rectified Flow](https://arxiv.org/abs/2603.19598)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: indoor](https://img.shields.io/static/v1?label=Track&message=indoor&color=EA580C&style=flat-square&labelColor=111827)

> A graph-based rectified-flow approach to style-consistent indoor scene generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.19598)

#### 🌟 [GeoDiff3D: Self-Supervised 3D Scene Generation with Geometry-Constrained 2D Diffusion Guidance](https://arxiv.org/abs/2601.19785)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: general-scene-generation](https://img.shields.io/static/v1?label=Track&message=general-scene-generation&color=EA580C&style=flat-square&labelColor=111827)

> A self-supervised 3D scene generator using coarse geometry anchors plus geometry-constrained 2D diffusion guidance.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2601.19785)

#### 🌟 [OneWorld: Taming Scene Generation with 3D Unified Representation Autoencoder](https://arxiv.org/abs/2603.16099)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: general-scene-generation](https://img.shields.io/static/v1?label=Track&message=general-scene-generation&color=EA580C&style=flat-square&labelColor=111827)

> Uses a unified 3D representation autoencoder to reduce the cross-view inconsistency of scene generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.16099)

## Full Catalog

**Legend:** 🟢 code publicly available · ⚪ code not (yet) public · ★ live GitHub stars (refreshed weekly)

### [general-scene-generation](general-scene-generation.md) · 14

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[GeoDiff3D: Self-Supervised 3D Scene Generation with Geometry-Constrained 2D Diffusion Guidance](https://arxiv.org/abs/2601.19785)** | arXiv 2026 | A self-supervised 3D scene generator using coarse geometry anchors plus… | [📄 arXiv](https://arxiv.org/abs/2601.19785) |
| ⚪ **[OneWorld: Taming Scene Generation with 3D Unified Representation Autoencoder](https://arxiv.org/abs/2603.16099)** | arXiv 2026 | Uses a unified 3D representation autoencoder to reduce the cross-view inconsistency of… | [📄 arXiv](https://arxiv.org/abs/2603.16099) |
| ⚪ **[WorldMesh: Generating Navigable Multi-Room 3D Scenes via Mesh-Conditioned Image Diffusion](https://arxiv.org/abs/2603.22972)** | arXiv 2026 | A mesh-conditioned image-diffusion route to multi-room navigable 3D scene generation. | [📄 arXiv](https://arxiv.org/abs/2603.22972) |
| ⚪ **[Causal Reasoning Elicits Controllable 3D Scene Generation](https://arxiv.org/abs/2509.15249)** | arXiv 2025 | Injects causal graphs and interventions into scene generation for stronger logical and… | [📄 arXiv](https://arxiv.org/abs/2509.15249) |
| ⚪ **[FlashWorld: High-quality 3D Scene Generation within Seconds](https://arxiv.org/abs/2510.13678)** | arXiv 2025 | A fast 3D-oriented scene generator that directly predicts Gaussian representations from… | [📄 arXiv](https://arxiv.org/abs/2510.13678) |
| ⚪ **[LT3SD: Latent Trees for 3D Scene Diffusion](https://arxiv.org/abs/2409.08215)** | CVPR 2025 | A latent-tree scene representation for large-scale patchwise diffusion over complex 3D… | [📄 arXiv](https://arxiv.org/abs/2409.08215) |
| ⚪ **[Prometheus: 3D-Aware Latent Diffusion Models for Feed-Forward Text-to-3D Scene Generation](https://arxiv.org/abs/2412.21117)** | CVPR 2025 | A feed-forward latent diffusion approach for fast text-to-3D object and scene generation… | [📄 arXiv](https://arxiv.org/abs/2412.21117) · [🌐 Project](https://freemty.github.io/project-prometheus/) |
| ⚪ **[ScenePainter: Semantically Consistent Perpetual 3D Scene Generation with Concept Relation Alignment](https://arxiv.org/abs/2507.19058)** | ICCV 2025 | Reduces semantic drift in long-horizon 3D scene expansion by aligning concept relations… | [📄 arXiv](https://arxiv.org/abs/2507.19058) · [🌐 Project](https://xiac20.github.io/ScenePainter/) |
| ⚪ **[SplatFlow: Multi-View Rectified Flow Model for 3D Gaussian Splatting Synthesis](https://arxiv.org/abs/2411.16443)** | CVPR 2025 | A rectified-flow framework that directly supports 3DGS generation and editing through… | [📄 arXiv](https://arxiv.org/abs/2411.16443) |
| ⚪ **[Terra: Explorable Native 3D World Model with Point Latents](https://arxiv.org/abs/2510.14977)** | arXiv 2025 | A native 3D point-latent scene generator with exact multi-view consistency and… | [📄 arXiv](https://arxiv.org/abs/2510.14977) |
| ⚪ **[TRELLISWorld: Training-Free World Generation from Object Generators](https://arxiv.org/abs/2510.23880)** | arXiv 2025 | Repurposes object generators as modular 3D tiles for scalable training-free scene… | [📄 arXiv](https://arxiv.org/abs/2510.23880) |
| ⚪ **[UniUGG: Unified 3D Understanding and Generation via Geometric-Semantic Encoding](https://arxiv.org/abs/2508.11952)** | arXiv 2025 | A unified framework spanning 3D understanding and generation with shared… | [📄 arXiv](https://arxiv.org/abs/2508.11952) |
| ⚪ **[VideoRFSplat: Direct Scene-Level Text-to-3D Gaussian Splatting Generation with Flexible Pose and Multi-View Joint Modeling](https://arxiv.org/abs/2503.15855)** | arXiv 2025 | Directly generates scene-level 3DGS from text by jointly modeling poses and multi-view… | [📄 arXiv](https://arxiv.org/abs/2503.15855) |
| ⚪ **[WonderZoom: Multi-Scale 3D World Generation](https://arxiv.org/abs/2512.09164)** | arXiv 2025 | A multi-scale 3D world generator that supports progressive zoom-in synthesis of finer… | [📄 arXiv](https://arxiv.org/abs/2512.09164) · [🌐 Project](https://wonderzoom.github.io/) |

### [layout-to-scene](layout-to-scene.md) · 6

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[SPATIALGEN: Layout-guided 3D Indoor Scene Generation](https://arxiv.org/abs/2509.14981)** | 3DV 2026 | A multi-view multi-modal diffusion model for realistic 3D indoor scene generation from…<br>`indoor` | [📄 arXiv](https://arxiv.org/abs/2509.14981) |
| ⚪ **[Direct Numerical Layout Generation for 3D Indoor Scene Synthesis via Spatial Reasoning](https://arxiv.org/abs/2506.05341)** | arXiv 2025 | Directly predicts numerical 3D layouts from text via chain-of-thought spatial reasoning.<br>`indoor` | [📄 arXiv](https://arxiv.org/abs/2506.05341) |
| ⚪ **[DisCo-Layout: Disentangling and Coordinating Semantic and Physical Refinement in a Multi-Agent Framework for 3D Indoor Layout Synthesis](https://arxiv.org/abs/2510.02178)** | arXiv 2025 | Uses coordinated semantic and physical refinement tools inside a multi-agent loop for…<br>`indoor` | [📄 arXiv](https://arxiv.org/abs/2510.02178) |
| ⚪ **[HLG: Comprehensive 3D Room Construction via Hierarchical Layout Generation](https://arxiv.org/abs/2508.17832)** | arXiv 2025 | A coarse-to-fine hierarchical layout generator for more detailed and physically plausible…<br>`indoor` | [📄 arXiv](https://arxiv.org/abs/2508.17832) |
| ⚪ **[LayoutVLM: Differentiable Optimization of 3D Layout via Vision-Language Models](https://arxiv.org/abs/2412.02193)** | CVPR 2025 | Uses a differentiable scene-layout representation and VLM supervision to improve…<br>`indoor` | [📄 arXiv](https://arxiv.org/abs/2412.02193) |
| ⚪ **[MesaTask: Towards Task-Driven Tabletop Scene Generation via 3D Spatial Reasoning](https://arxiv.org/abs/2509.22281)** | NeurIPS 2025 | Formulates task-oriented tabletop generation as spatial reasoning over object inference…<br>`tabletop` | [📄 arXiv](https://arxiv.org/abs/2509.22281) · [🌐 Project](https://mesatask.github.io/) |

### [agentic-scene-generation](agentic-scene-generation.md) · 5

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[3D-GPT: Procedural 3D Modeling with Large Language Models](https://arxiv.org/abs/2310.12945)** | 3DV 2025 | An early but still relevant LLM-driven procedural 3D modeling framework for scene and… | [📄 arXiv](https://arxiv.org/abs/2310.12945) |
| ⚪ **[LatticeWorld: A Multimodal Large Language Model-Empowered Framework for Interactive Complex World Generation](https://arxiv.org/abs/2509.05263)** | arXiv 2025 | An MLLM-plus-engine framework for interactive large-scale world generation with dynamic… | [📄 arXiv](https://arxiv.org/abs/2509.05263) |
| ⚪ **[Scenethesis: A Language and Vision Agentic Framework for 3D Scene Generation](https://arxiv.org/abs/2505.02836)** | arXiv 2025 | Combines LLM planning with vision-guided refinement to produce more realistic and… | [📄 arXiv](https://arxiv.org/abs/2505.02836) |
| ⚪ **[SceneWeaver: All-in-One 3D Scene Synthesis with an Extensible and Self-Reflective Agent](https://arxiv.org/abs/2509.20414)** | NeurIPS 2025 | A reflective agent that plans, evaluates, and repairs 3D scenes by invoking an extensible… | [📄 arXiv](https://arxiv.org/abs/2509.20414) · [🌐 Project](https://scene-weaver.github.io/) |
| ⚪ **[SceneX: Procedural Controllable Large-scale Scene Generation](https://arxiv.org/abs/2403.15698)** | AAAI 2025 | An LLM-assisted procedural generation framework for controllable large-scale scene… | [📄 arXiv](https://arxiv.org/abs/2403.15698) |

### [indoor](indoor.md) · 4

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[FlowScene: Style-Consistent Indoor Scene Generation with Multimodal Graph Rectified Flow](https://arxiv.org/abs/2603.19598)** | arXiv 2026 | A graph-based rectified-flow approach to style-consistent indoor scene generation. | [📄 arXiv](https://arxiv.org/abs/2603.19598) |
| ⚪ **[Global-Local Tree Search in VLMs for 3D Indoor Scene Generation](https://arxiv.org/abs/2503.18476)** | CVPR 2025 | Frames indoor scene synthesis as a global-local search problem over placements using VLMs… | [📄 arXiv](https://arxiv.org/abs/2503.18476) |
| ⚪ **[Hierarchically-Structured Open-Vocabulary Indoor Scene Synthesis with Pre-trained Large Language Model](https://arxiv.org/abs/2502.10675)** | AAAI 2025 | Generates hierarchical scene descriptions and optimizes them into feasible indoor layouts… | [📄 arXiv](https://arxiv.org/abs/2502.10675) |
| ⚪ **[RoomCraft: Controllable and Complete 3D Indoor Scene Generation](https://arxiv.org/abs/2506.22291)** | arXiv 2025 | A controllable indoor scene generator focused on both completeness and realistic… | [📄 arXiv](https://arxiv.org/abs/2506.22291) |

### [outdoor-urban](outdoor-urban.md) · 3

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[MeSS: City Mesh-Guided Outdoor Scene Generation with Cross-View Consistent Diffusion](https://arxiv.org/abs/2508.15169)** | arXiv 2025 | Uses city meshes as geometric priors and diffusion-based view synthesis to create large… | [📄 arXiv](https://arxiv.org/abs/2508.15169) |
| ⚪ **[NuiScene: Exploring Efficient Generation of Unbounded Outdoor Scenes](https://arxiv.org/abs/2503.16375)** | ICCV 2025 | Targets large unbounded outdoor scene generation using chunked vector-set scene latents… | [📄 arXiv](https://arxiv.org/abs/2503.16375) |
| ⚪ **[SynCity: Training-Free Generation of 3D Worlds](https://arxiv.org/abs/2503.16420)** | arXiv 2025 | A training-free tile-based method that combines 3D and 2D generators for ever-expanding… | [📄 arXiv](https://arxiv.org/abs/2503.16420) |

### [single-image-to-scene](single-image-to-scene.md) · 3

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[Bolt3D: Generating 3D Scenes in Seconds](https://arxiv.org/abs/2503.14445)** | ICCV 2025 | A latent diffusion model that directly samples a 3D scene from one or more images in a… | [📄 arXiv](https://arxiv.org/abs/2503.14445) |
| ⚪ **[WonderFree: Enhancing Novel View Quality and Cross-View Consistency for 3D Scene Exploration](https://arxiv.org/abs/2506.20590)** | arXiv 2025 | A follow-up exploration system that restores novel views and improves global cross-view… | [📄 arXiv](https://arxiv.org/abs/2506.20590) · [🌐 Project](https://wonder-free.github.io/) |
| 🟢 **[WonderWorld: Interactive 3D Scene Generation from a Single Image](https://openaccess.thecvf.com/content/CVPR2025/html/Yu_WonderWorld_Interactive_3D_Scene_Generation_from_a_Single_Image_CVPR_2025_paper.html)** | CVPR 2025 | A fast interactive pipeline that turns one image into a connected explorable 3D scene in… | [📄 CVF](https://openaccess.thecvf.com/content/CVPR2025/html/Yu_WonderWorld_Interactive_3D_Scene_Generation_from_a_Single_Image_CVPR_2025_paper.html) · [💻 Code](https://github.com/KovenYu/WonderWorld) · [🌐 Project](https://kovenyu.com/WonderWorld/) |

### [scene-editing](scene-editing.md) · 1

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[ReSpace: Text-Driven 3D Scene Synthesis and Editing with Preference Alignment](https://arxiv.org/abs/2506.02459)** | arXiv 2025 | A language-model-based indoor scene synthesis and editing framework with explicit…<br>`indoor` | [📄 arXiv](https://arxiv.org/abs/2506.02459) |
