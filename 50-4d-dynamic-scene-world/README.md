# 🌍 4D Dynamic Scene / World

> Dynamic 3D/4D scenes, world models, simulation, autonomous driving, game worlds, and interactive world modeling.

**24 curated papers** · [← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)

<details>
<summary><b>📐 How this pipeline works</b></summary>

```text
Observation / map / action / trajectory / prompt
        ↓
State encoder + memory / scene cache
        ↓
Dynamics rollout / world model / simulator
        ↓
Render heads (RGB / depth / occupancy / tokens)
        ↓
Interactive future world / closed-loop simulation
```

</details>

## Tasks in this category

[autonomous-driving](autonomous-driving.md) <sub>(10)</sub> · [4d-generation](4d-generation.md) <sub>(2)</sub> · [world-models](world-models.md) <sub>(4)</sub> · [simulation](simulation.md) <sub>(3)</sub> · [game-worlds](game-worlds.md) <sub>(4)</sub> · [robotics-worlds](robotics-worlds.md) <sub>(1)</sub>

## 🌟 Spotlight

#### 🌟 [VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs](https://arxiv.org/abs/2603.17652)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Org: Independent](https://img.shields.io/static/v1?label=Org&message=Independent&color=475569&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> VectorWorld is a streaming autonomous-driving world model that incrementally generates ego-centric lane-agent vector-graph tiles during rollout. It uses a motion-aware VAE and one-step masked completion on vector graphs to achieve stable, real-time long-horizon simulation. The work is valuable because it targets policy-compatible closed-loop generation instead of offline video-only realism.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.17652) [![Code: GitHub ★ 32](https://img.shields.io/static/v1?label=Code&message=GitHub+%E2%98%85+32&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/jiangchaokang/VectorWorld)

`vae` `diffusion` `flow` `world-model`

#### 🌟 [DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving](https://arxiv.org/abs/2602.06521)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Deeply couples a VLA planner with a latent driving world model for planning-aware rollout.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.06521) [![Code: GitHub ★ 108](https://img.shields.io/static/v1?label=Code&message=GitHub+%E2%98%85+108&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/liulin815/DriveWorld-VLA)

#### 🌟 [DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving](https://arxiv.org/abs/2603.19675)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A flow-based latent dynamics model for action-conditioned autonomous-driving world simulation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.19675) [![Code: GitHub ★ 24](https://img.shields.io/static/v1?label=Code&message=GitHub+%E2%98%85+24&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/xiaolul2/DynFlowDrive)

## Full Catalog

**Legend:** 🟢 code publicly available · ⚪ code not (yet) public · ★ live GitHub stars (refreshed weekly)

### [autonomous-driving](autonomous-driving.md) · 10

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| 🟢 **[VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs](https://arxiv.org/abs/2603.17652)** | arXiv 2026 | VectorWorld is a streaming autonomous-driving world model that incrementally generates…<br>`vae` `diffusion` `flow` | [📄 arXiv](https://arxiv.org/abs/2603.17652) · [💻 Code ★32](https://github.com/jiangchaokang/VectorWorld) |
| 🟢 **[DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving](https://arxiv.org/abs/2602.06521)** | arXiv 2026 | Deeply couples a VLA planner with a latent driving world model for planning-aware rollout. | [📄 arXiv](https://arxiv.org/abs/2602.06521) · [💻 Code ★108](https://github.com/liulin815/DriveWorld-VLA) |
| 🟢 **[DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving](https://arxiv.org/abs/2603.19675)** | arXiv 2026 | A flow-based latent dynamics model for action-conditioned autonomous-driving world… | [📄 arXiv](https://arxiv.org/abs/2603.19675) · [💻 Code ★24](https://github.com/xiaolul2/DynFlowDrive) |
| ⚪ **[UniDWM: Towards a Unified Driving World Model via Multifaceted Representation Learning](https://arxiv.org/abs/2602.01536)** | arXiv 2026 | A unified driving world model that explicitly balances geometry, appearance, and dynamics… | [📄 arXiv](https://arxiv.org/abs/2602.01536) |
| 🟢 **[Epona: Autoregressive Diffusion World Model for Autonomous Driving](https://arxiv.org/abs/2506.24113)** | arXiv 2025 | Combines autoregression and diffusion inside a driving world model for controllable… | [📄 arXiv](https://arxiv.org/abs/2506.24113) · [💻 Code ★372](https://github.com/Kevin-thu/Epona) |
| 🟢 **[HERMES: A Unified Self-Driving World Model for Simultaneous 3D Scene Understanding and Generation](https://arxiv.org/abs/2501.14729)** | arXiv 2025 | Unifies driving-scene understanding and future scene generation within one BEV-centric… | [📄 arXiv](https://arxiv.org/abs/2501.14729) · [💻 Code ★259](https://github.com/LMD0311/HERMES) |
| 🟢 **[World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model](https://arxiv.org/abs/2507.00603)** | arXiv 2025 | A physical latent world model that couples intention-aware scene evolution with… | [📄 arXiv](https://arxiv.org/abs/2507.00603) · [💻 Code ★100](https://github.com/ucaszyp/World4Drive) |
| ⚪ **[DynamicCity: Large-Scale 4D Occupancy Generation from Dynamic Scenes](https://arxiv.org/abs/2410.18084)** | ICLR 2025 | An occupancy-generation framework for large-scale dynamic urban scenes with strong 4D… | [📄 arXiv](https://arxiv.org/abs/2410.18084) · [🌐 Project](https://dynamic-city.github.io/) |
| ⚪ **[GEM: A Generalizable Ego-Vision Multimodal World Model for Fine-Grained Ego-Motion, Object Dynamics, and Scene Composition Control](https://arxiv.org/abs/2412.11198)** | CVPR 2025 | A multimodal world model that jointly controls ego motion, object dynamics, and scene… | [📄 arXiv](https://arxiv.org/abs/2412.11198) |
| ⚪ **[UniScene: Unified Occupancy-centric Driving Scene Generation](https://arxiv.org/abs/2412.05435)** | CVPR 2025 | A unified occupancy-centric generator for semantic occupancy, video, and LiDAR in driving… | [📄 arXiv](https://arxiv.org/abs/2412.05435) |

### [4d-generation](4d-generation.md) · 2

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[HunyuanWorld 1.0: Generating Immersive, Explorable, and Interactive 3D Worlds from Words or Pixels](https://arxiv.org/abs/2507.21809)** | arXiv 2025 | HunyuanWorld 1.0 is Tencent Hunyuan’s 3D world generation system for building explorable… | [📄 arXiv](https://arxiv.org/abs/2507.21809) · [💻 Code ★2.9k](https://github.com/Tencent-Hunyuan/HunyuanWorld-1.0) |
| 🟢 **[Voyager: Long-Range and World-Consistent Video Diffusion for Explorable 3D Scene Generation](https://arxiv.org/abs/2506.04225)** | arXiv 2025 | Voyager is a long-range RGB-D video diffusion model for explorable 3D scene generation… | [📄 arXiv](https://arxiv.org/abs/2506.04225) · [💻 Code ★1.6k](https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager) · [🌐 Project](https://3d-models.hunyuan.tencent.com/world/) |

### [world-models](world-models.md) · 4

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| 🟢 **[HY-World 1.5 (WorldPlay): A Systematic Framework for Interactive World Modeling with Real-Time Latency and Geometric Consistency](https://arxiv.org/abs/2512.14614)** | arXiv 2025 | A real-time interactive world model focused on streaming generation, low latency, and…<br>`gameplay` | [📄 arXiv](https://arxiv.org/abs/2512.14614) · [💻 Code ★1.6k](https://github.com/Tencent-Hunyuan/HY-WorldPlay) · [🌐 Project](https://3d-models.hunyuan.tencent.com/world/) |
| ⚪ **[AdaWorld: Learning Adaptable World Models with Latent Actions](https://arxiv.org/abs/2503.18938)** | ICML 2025 | Pretrains adaptable world models with self-supervised latent actions for efficient… | [📄 arXiv](https://arxiv.org/abs/2503.18938) |
| 🟢 **[Cosmos World Foundation Model Platform for Physical AI](https://arxiv.org/abs/2501.03575)** | arXiv 2025 | NVIDIA’s open world foundation model platform spanning tokenizers, pretrained models, and… | [📄 arXiv](https://arxiv.org/abs/2501.03575) · [💻 Code](https://github.com/NVIDIA/Cosmos) · [🌐 Project](https://www.nvidia.com/en-us/ai/cosmos/) |
| ⚪ **[WORLDMEM: Long-term Consistent World Simulation with Memory](https://arxiv.org/abs/2504.12369)** | arXiv 2025 | Adds explicit memory banks and memory attention to improve long-term consistency in world… | [📄 arXiv](https://arxiv.org/abs/2504.12369) |

### [simulation](simulation.md) · 3

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[DiffusionHarmonizer: Bridging Neural Reconstruction and Photorealistic Simulation with Online Diffusion Enhancer](https://arxiv.org/abs/2602.24096)** | arXiv 2026 | Enhances reconstructed 3D scenes into temporally consistent photorealistic simulation…<br>`autonomous-driving` | [📄 arXiv](https://arxiv.org/abs/2602.24096) · [🌐 Project](https://research.nvidia.com/labs/sil/projects/diffusion-harmonizer/) |
| 🟢 **[Waymax: An Accelerated, Data-Driven Simulator for Large-Scale Autonomous Driving Research](https://arxiv.org/abs/2310.08710)** | NeurIPS 2024 · since 2025 | A widely used large-scale autonomous-driving simulator that remained actively relevant…<br>`autonomous-driving` | [📄 arXiv](https://arxiv.org/abs/2310.08710) · [💻 Code ★1.1k](https://github.com/waymo-research/waymax) |
| ⚪ **[DrivingSphere: Building a High-fidelity 4D World for Closed-loop Simulation](https://arxiv.org/abs/2411.11252)** | CVPR 2025 | Builds a realistic 4D world and visual synthesis stack for closed-loop autonomous-driving…<br>`autonomous-driving` | [📄 arXiv](https://arxiv.org/abs/2411.11252) |

### [game-worlds](game-worlds.md) · 4

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| 🟢 **[Matrix-Game: Interactive World Foundation Model](https://arxiv.org/abs/2506.18701)** | arXiv 2025 | A large Minecraft-style interactive world foundation model with strong action…<br>`gameplay` | [📄 arXiv](https://arxiv.org/abs/2506.18701) · [💻 Code ★2.3k](https://github.com/SkyworkAI/Matrix-Game) |
| ⚪ **[Diffusion Models Are Real-Time Game Engines](https://arxiv.org/abs/2408.14837)** | ICLR 2025 | Shows that a diffusion model can function as a real-time neural game engine over long…<br>`gameplay` | [📄 arXiv](https://arxiv.org/abs/2408.14837) |
| ⚪ **[GameFactory: Creating New Games with Generative Interactive Videos](https://arxiv.org/abs/2501.08325)** | ICCV 2025 | A framework for creating entirely new interactive games from generative video building…<br>`gameplay` | [📄 arXiv](https://arxiv.org/abs/2501.08325) |
| ⚪ **[GameGen-X: Interactive Open-world Game Video Generation](https://arxiv.org/abs/2411.00769)** | ICLR 2025 | An open-world game video generator built for both open-domain synthesis and interactive…<br>`gameplay` | [📄 arXiv](https://arxiv.org/abs/2411.00769) |

### [robotics-worlds](robotics-worlds.md) · 1

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[ABot-PhysWorld: Interactive World Foundation Model for Robotic Manipulation with Physics Alignment](https://arxiv.org/abs/2603.23376)** | arXiv 2026 | A robotics-oriented interactive world model emphasizing physics alignment for…<br>`robotics` | [📄 arXiv](https://arxiv.org/abs/2603.23376) |
