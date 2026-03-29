# 🌍 4D Dynamic Scene / World

> Dynamic 3D/4D scenes, world models, simulation, autonomous driving, game worlds, and interactive world modeling.

**Curated entries:** 24

[← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)

## Research Pattern

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

## Quick Navigation

[`autonomous-driving`](autonomous-driving.md) · [`4d-generation`](4d-generation.md) · [`world-models`](world-models.md) · [`simulation`](simulation.md) · [`game-worlds`](game-worlds.md) · [`robotics-worlds`](robotics-worlds.md)

## Selected Papers

### [VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs](https://arxiv.org/abs/2603.17652)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative) ![Org: Independent](https://img.shields.io/static/v1?label=Org&message=Independent&color=475569&style=flat-square&labelColor=111827)

> VectorWorld is a streaming autonomous-driving world model that incrementally generates ego-centric lane-agent vector-graph tiles during rollout. It uses a motion-aware VAE and one-step masked completion on vector graphs to achieve stable, real-time long-horizon simulation. The work is valuable because it targets policy-compatible closed-loop generation instead of offline video-only realism.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.17652) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/jiangchaokang/VectorWorld)

![Method: vae](https://img.shields.io/static/v1?label=Method&message=vae&color=7C3AED&style=flat-square&labelColor=111827) ![Method: diffusion](https://img.shields.io/static/v1?label=Method&message=diffusion&color=7C3AED&style=flat-square&labelColor=111827) ![Repr: vector-graph](https://img.shields.io/static/v1?label=Repr&message=vector-graph&color=0D9488&style=flat-square&labelColor=111827) ![Cond: trajectory](https://img.shields.io/static/v1?label=Cond&message=trajectory&color=475569&style=flat-square&labelColor=111827)

### [ABot-PhysWorld: Interactive World Foundation Model for Robotic Manipulation with Physics Alignment](https://arxiv.org/abs/2603.23376)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: robotics-worlds](https://img.shields.io/static/v1?label=Track&message=robotics-worlds&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A robotics-oriented interactive world model emphasizing physics alignment for manipulation-centric simulation and planning.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.23376)

![Domain: robotics](https://img.shields.io/static/v1?label=Domain&message=robotics&color=EA580C&style=flat-square&labelColor=111827)

### [DiffusionHarmonizer: Bridging Neural Reconstruction and Photorealistic Simulation with Online Diffusion Enhancer](https://arxiv.org/abs/2602.24096)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: simulation](https://img.shields.io/static/v1?label=Track&message=simulation&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Enhances reconstructed 3D scenes into temporally consistent photorealistic simulation outputs with online diffusion.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.24096) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://research.nvidia.com/labs/sil/projects/diffusion-harmonizer/)

![Domain: autonomous-driving](https://img.shields.io/static/v1?label=Domain&message=autonomous-driving&color=EA580C&style=flat-square&labelColor=111827)

### [DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving](https://arxiv.org/abs/2602.06521)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Deeply couples a VLA planner with a latent driving world model for planning-aware rollout.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.06521) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/liulin815/DriveWorld-VLA)

## By Task

## [autonomous-driving](autonomous-driving.md)

**10 entries**

### [VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs](https://arxiv.org/abs/2603.17652)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative) ![Org: Independent](https://img.shields.io/static/v1?label=Org&message=Independent&color=475569&style=flat-square&labelColor=111827)

> VectorWorld is a streaming autonomous-driving world model that incrementally generates ego-centric lane-agent vector-graph tiles during rollout. It uses a motion-aware VAE and one-step masked completion on vector graphs to achieve stable, real-time long-horizon simulation. The work is valuable because it targets policy-compatible closed-loop generation instead of offline video-only realism.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.17652) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/jiangchaokang/VectorWorld)

![Method: vae](https://img.shields.io/static/v1?label=Method&message=vae&color=7C3AED&style=flat-square&labelColor=111827) ![Method: diffusion](https://img.shields.io/static/v1?label=Method&message=diffusion&color=7C3AED&style=flat-square&labelColor=111827) ![Repr: vector-graph](https://img.shields.io/static/v1?label=Repr&message=vector-graph&color=0D9488&style=flat-square&labelColor=111827) ![Cond: trajectory](https://img.shields.io/static/v1?label=Cond&message=trajectory&color=475569&style=flat-square&labelColor=111827)

### [DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving](https://arxiv.org/abs/2602.06521)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Deeply couples a VLA planner with a latent driving world model for planning-aware rollout.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.06521) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/liulin815/DriveWorld-VLA)

### [DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving](https://arxiv.org/abs/2603.19675)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A flow-based latent dynamics model for action-conditioned autonomous-driving world simulation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.19675) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/xiaolul2/DynFlowDrive)

### [UniDWM: Towards a Unified Driving World Model via Multifaceted Representation Learning](https://arxiv.org/abs/2602.01536)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A unified driving world model that explicitly balances geometry, appearance, and dynamics in one latent space.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.01536)

### [DynamicCity: Large-Scale 4D Occupancy Generation from Dynamic Scenes](https://arxiv.org/abs/2410.18084)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> An occupancy-generation framework for large-scale dynamic urban scenes with strong 4D structural priors.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2410.18084) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://dynamic-city.github.io/)

### [Epona: Autoregressive Diffusion World Model for Autonomous Driving](https://arxiv.org/abs/2506.24113)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Combines autoregression and diffusion inside a driving world model for controllable long-horizon rollout.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2506.24113) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Kevin-thu/Epona)

### [GEM: A Generalizable Ego-Vision Multimodal World Model for Fine-Grained Ego-Motion, Object Dynamics, and Scene Composition Control](https://arxiv.org/abs/2412.11198)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A multimodal world model that jointly controls ego motion, object dynamics, and scene composition across domains.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2412.11198)

### [HERMES: A Unified Self-Driving World Model for Simultaneous 3D Scene Understanding and Generation](https://arxiv.org/abs/2501.14729)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Unifies driving-scene understanding and future scene generation within one BEV-centric world model.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2501.14729) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/LMD0311/HERMES)

### [UniScene: Unified Occupancy-centric Driving Scene Generation](https://arxiv.org/abs/2412.05435)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A unified occupancy-centric generator for semantic occupancy, video, and LiDAR in driving scenes.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2412.05435)

### [World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model](https://arxiv.org/abs/2507.00603)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: autonomous-driving](https://img.shields.io/static/v1?label=Track&message=autonomous-driving&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A physical latent world model that couples intention-aware scene evolution with planning-oriented driving control.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2507.00603) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/ucaszyp/World4Drive)

## [4d-generation](4d-generation.md)

**2 entries**

### [HunyuanWorld 1.0: Generating Immersive, Explorable, and Interactive 3D Worlds from Words or Pixels](https://arxiv.org/abs/2507.21809)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: 4d-generation](https://img.shields.io/static/v1?label=Track&message=4d-generation&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827) ![Org: Tencent Hunyuan](https://img.shields.io/static/v1?label=Org&message=Tencent+Hunyuan&color=0064FF&style=flat-square&labelColor=111827&logo=tencentqq)

> HunyuanWorld 1.0 is Tencent Hunyuan’s 3D world generation system for building explorable interactive worlds from text or images, combining panoramic initialization with long-range world expansion.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2507.21809) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Tencent-Hunyuan/HunyuanWorld-1.0)

### [Voyager: Long-Range and World-Consistent Video Diffusion for Explorable 3D Scene Generation](https://arxiv.org/abs/2506.04225)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: 4d-generation](https://img.shields.io/static/v1?label=Track&message=4d-generation&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative) ![Org: Tencent Hunyuan](https://img.shields.io/static/v1?label=Org&message=Tencent+Hunyuan&color=0064FF&style=flat-square&labelColor=111827&logo=tencentqq)

> Voyager is a long-range RGB-D video diffusion model for explorable 3D scene generation with camera control and native 3D reconstruction support.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2506.04225) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://3d-models.hunyuan.tencent.com/world/)

## [world-models](world-models.md)

**4 entries**

### [AdaWorld: Learning Adaptable World Models with Latent Actions](https://arxiv.org/abs/2503.18938)

![Venue: ICML 2025](https://img.shields.io/static/v1?label=Venue&message=ICML+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: world-models](https://img.shields.io/static/v1?label=Track&message=world-models&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Pretrains adaptable world models with self-supervised latent actions for efficient transfer to new environments.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2503.18938)

### [Cosmos World Foundation Model Platform for Physical AI](https://arxiv.org/abs/2501.03575)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: world-models](https://img.shields.io/static/v1?label=Track&message=world-models&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> NVIDIA’s open world foundation model platform spanning tokenizers, pretrained models, and post-training recipes for physical AI.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2501.03575) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/NVIDIA/Cosmos) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://www.nvidia.com/en-us/ai/cosmos/)

### [HY-World 1.5 (WorldPlay): A Systematic Framework for Interactive World Modeling with Real-Time Latency and Geometric Consistency](https://arxiv.org/abs/2512.14614)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: world-models](https://img.shields.io/static/v1?label=Track&message=world-models&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A real-time interactive world model focused on streaming generation, low latency, and long-horizon geometric consistency.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2512.14614) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Tencent-Hunyuan/HY-WorldPlay) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://3d-models.hunyuan.tencent.com/world/)

![Domain: gameplay](https://img.shields.io/static/v1?label=Domain&message=gameplay&color=EA580C&style=flat-square&labelColor=111827)

### [WORLDMEM: Long-term Consistent World Simulation with Memory](https://arxiv.org/abs/2504.12369)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: world-models](https://img.shields.io/static/v1?label=Track&message=world-models&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Adds explicit memory banks and memory attention to improve long-term consistency in world simulation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2504.12369)

## [simulation](simulation.md)

**3 entries**

### [DiffusionHarmonizer: Bridging Neural Reconstruction and Photorealistic Simulation with Online Diffusion Enhancer](https://arxiv.org/abs/2602.24096)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: simulation](https://img.shields.io/static/v1?label=Track&message=simulation&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Enhances reconstructed 3D scenes into temporally consistent photorealistic simulation outputs with online diffusion.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.24096) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://research.nvidia.com/labs/sil/projects/diffusion-harmonizer/)

![Domain: autonomous-driving](https://img.shields.io/static/v1?label=Domain&message=autonomous-driving&color=EA580C&style=flat-square&labelColor=111827)

### [DrivingSphere: Building a High-fidelity 4D World for Closed-loop Simulation](https://arxiv.org/abs/2411.11252)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: simulation](https://img.shields.io/static/v1?label=Track&message=simulation&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Builds a realistic 4D world and visual synthesis stack for closed-loop autonomous-driving simulation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2411.11252)

![Domain: autonomous-driving](https://img.shields.io/static/v1?label=Domain&message=autonomous-driving&color=EA580C&style=flat-square&labelColor=111827)

### [Waymax: An Accelerated, Data-Driven Simulator for Large-Scale Autonomous Driving Research](https://arxiv.org/abs/2310.08710)

![Venue: NeurIPS 2024](https://img.shields.io/static/v1?label=Venue&message=NeurIPS+2024&color=7C3AED&style=flat-square&labelColor=111827) ![Track: simulation](https://img.shields.io/static/v1?label=Track&message=simulation&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative) ![Legacy: Active since 2025](https://img.shields.io/static/v1?label=Legacy&message=Active+since+2025&color=F59E0B&style=flat-square&labelColor=111827)

> A widely used large-scale autonomous-driving simulator that remained actively relevant throughout 2025 evaluation workflows.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2310.08710) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/waymo-research/waymax)

![Domain: autonomous-driving](https://img.shields.io/static/v1?label=Domain&message=autonomous-driving&color=EA580C&style=flat-square&labelColor=111827)

_Scope note: Kept because Waymax remained a core simulator in 2025 autonomous-driving research._

## [game-worlds](game-worlds.md)

**4 entries**

### [Diffusion Models Are Real-Time Game Engines](https://arxiv.org/abs/2408.14837)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: game-worlds](https://img.shields.io/static/v1?label=Track&message=game-worlds&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Shows that a diffusion model can function as a real-time neural game engine over long interactive rollouts.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2408.14837)

![Domain: gameplay](https://img.shields.io/static/v1?label=Domain&message=gameplay&color=EA580C&style=flat-square&labelColor=111827)

### [GameFactory: Creating New Games with Generative Interactive Videos](https://arxiv.org/abs/2501.08325)

![Venue: ICCV 2025](https://img.shields.io/static/v1?label=Venue&message=ICCV+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: game-worlds](https://img.shields.io/static/v1?label=Track&message=game-worlds&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A framework for creating entirely new interactive games from generative video building blocks.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2501.08325)

![Domain: gameplay](https://img.shields.io/static/v1?label=Domain&message=gameplay&color=EA580C&style=flat-square&labelColor=111827)

### [GameGen-X: Interactive Open-world Game Video Generation](https://arxiv.org/abs/2411.00769)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: game-worlds](https://img.shields.io/static/v1?label=Track&message=game-worlds&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> An open-world game video generator built for both open-domain synthesis and interactive controllability.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2411.00769)

![Domain: gameplay](https://img.shields.io/static/v1?label=Domain&message=gameplay&color=EA580C&style=flat-square&labelColor=111827)

### [Matrix-Game: Interactive World Foundation Model](https://arxiv.org/abs/2506.18701)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: game-worlds](https://img.shields.io/static/v1?label=Track&message=game-worlds&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A large Minecraft-style interactive world foundation model with strong action controllability and open benchmark release.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2506.18701) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/SkyworkAI/Matrix-Game)

![Domain: gameplay](https://img.shields.io/static/v1?label=Domain&message=gameplay&color=EA580C&style=flat-square&labelColor=111827)

## [robotics-worlds](robotics-worlds.md)

**1 entries**

### [ABot-PhysWorld: Interactive World Foundation Model for Robotic Manipulation with Physics Alignment](https://arxiv.org/abs/2603.23376)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: robotics-worlds](https://img.shields.io/static/v1?label=Track&message=robotics-worlds&color=B31B1B&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A robotics-oriented interactive world model emphasizing physics alignment for manipulation-centric simulation and planning.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.23376)

![Domain: robotics](https://img.shields.io/static/v1?label=Domain&message=robotics&color=EA580C&style=flat-square&labelColor=111827)

## Compact Index

<details>
<summary><b>Open compact index</b></summary>

| Title | Task | Venue | Links |
|:--|:--|:--|:--|
| **[VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs](https://arxiv.org/abs/2603.17652)** | autonomous-driving | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.17652) / [Code](https://github.com/jiangchaokang/VectorWorld) |
| **[ABot-PhysWorld: Interactive World Foundation Model for Robotic Manipulation with Physics Alignment](https://arxiv.org/abs/2603.23376)** | robotics-worlds | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.23376) |
| **[DiffusionHarmonizer: Bridging Neural Reconstruction and Photorealistic Simulation with Online Diffusion Enhancer](https://arxiv.org/abs/2602.24096)** | simulation | arXiv 2026 | [Paper](https://arxiv.org/abs/2602.24096) / [Project](https://research.nvidia.com/labs/sil/projects/diffusion-harmonizer/) |
| **[DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving](https://arxiv.org/abs/2602.06521)** | autonomous-driving | arXiv 2026 | [Paper](https://arxiv.org/abs/2602.06521) / [Code](https://github.com/liulin815/DriveWorld-VLA) |
| **[DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving](https://arxiv.org/abs/2603.19675)** | autonomous-driving | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.19675) / [Code](https://github.com/xiaolul2/DynFlowDrive) |
| **[UniDWM: Towards a Unified Driving World Model via Multifaceted Representation Learning](https://arxiv.org/abs/2602.01536)** | autonomous-driving | arXiv 2026 | [Paper](https://arxiv.org/abs/2602.01536) |
| **[AdaWorld: Learning Adaptable World Models with Latent Actions](https://arxiv.org/abs/2503.18938)** | world-models | ICML 2025 | [Paper](https://arxiv.org/abs/2503.18938) |
| **[Cosmos World Foundation Model Platform for Physical AI](https://arxiv.org/abs/2501.03575)** | world-models | arXiv 2025 | [Paper](https://arxiv.org/abs/2501.03575) / [Code](https://github.com/NVIDIA/Cosmos) / [Project](https://www.nvidia.com/en-us/ai/cosmos/) |
| **[Diffusion Models Are Real-Time Game Engines](https://arxiv.org/abs/2408.14837)** | game-worlds | ICLR 2025 | [Paper](https://arxiv.org/abs/2408.14837) |
| **[DrivingSphere: Building a High-fidelity 4D World for Closed-loop Simulation](https://arxiv.org/abs/2411.11252)** | simulation | CVPR 2025 | [Paper](https://arxiv.org/abs/2411.11252) |
| **[DynamicCity: Large-Scale 4D Occupancy Generation from Dynamic Scenes](https://arxiv.org/abs/2410.18084)** | autonomous-driving | ICLR 2025 | [Paper](https://arxiv.org/abs/2410.18084) / [Project](https://dynamic-city.github.io/) |
| **[Epona: Autoregressive Diffusion World Model for Autonomous Driving](https://arxiv.org/abs/2506.24113)** | autonomous-driving | arXiv 2025 | [Paper](https://arxiv.org/abs/2506.24113) / [Code](https://github.com/Kevin-thu/Epona) |
| **[GameFactory: Creating New Games with Generative Interactive Videos](https://arxiv.org/abs/2501.08325)** | game-worlds | ICCV 2025 | [Paper](https://arxiv.org/abs/2501.08325) |
| **[GameGen-X: Interactive Open-world Game Video Generation](https://arxiv.org/abs/2411.00769)** | game-worlds | ICLR 2025 | [Paper](https://arxiv.org/abs/2411.00769) |
| **[GEM: A Generalizable Ego-Vision Multimodal World Model for Fine-Grained Ego-Motion, Object Dynamics, and Scene Composition Control](https://arxiv.org/abs/2412.11198)** | autonomous-driving | CVPR 2025 | [Paper](https://arxiv.org/abs/2412.11198) |
| **[HERMES: A Unified Self-Driving World Model for Simultaneous 3D Scene Understanding and Generation](https://arxiv.org/abs/2501.14729)** | autonomous-driving | arXiv 2025 | [Paper](https://arxiv.org/abs/2501.14729) / [Code](https://github.com/LMD0311/HERMES) |
| **[HunyuanWorld 1.0: Generating Immersive, Explorable, and Interactive 3D Worlds from Words or Pixels](https://arxiv.org/abs/2507.21809)** | 4d-generation | arXiv 2025 | [Paper](https://arxiv.org/abs/2507.21809) / [Code](https://github.com/Tencent-Hunyuan/HunyuanWorld-1.0) |
| **[HY-World 1.5 (WorldPlay): A Systematic Framework for Interactive World Modeling with Real-Time Latency and Geometric Consistency](https://arxiv.org/abs/2512.14614)** | world-models | arXiv 2025 | [Paper](https://arxiv.org/abs/2512.14614) / [Code](https://github.com/Tencent-Hunyuan/HY-WorldPlay) / [Project](https://3d-models.hunyuan.tencent.com/world/) |
| **[Matrix-Game: Interactive World Foundation Model](https://arxiv.org/abs/2506.18701)** | game-worlds | arXiv 2025 | [Paper](https://arxiv.org/abs/2506.18701) / [Code](https://github.com/SkyworkAI/Matrix-Game) |
| **[UniScene: Unified Occupancy-centric Driving Scene Generation](https://arxiv.org/abs/2412.05435)** | autonomous-driving | CVPR 2025 | [Paper](https://arxiv.org/abs/2412.05435) |
| **[Voyager: Long-Range and World-Consistent Video Diffusion for Explorable 3D Scene Generation](https://arxiv.org/abs/2506.04225)** | 4d-generation | arXiv 2025 | [Paper](https://arxiv.org/abs/2506.04225) / [Code](https://github.com/Tencent-Hunyuan/HunyuanWorld-Voyager) / [Project](https://3d-models.hunyuan.tencent.com/world/) |
| **[Waymax: An Accelerated, Data-Driven Simulator for Large-Scale Autonomous Driving Research](https://arxiv.org/abs/2310.08710)** | simulation | NeurIPS 2024 | [Paper](https://arxiv.org/abs/2310.08710) / [Code](https://github.com/waymo-research/waymax) |
| **[World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model](https://arxiv.org/abs/2507.00603)** | autonomous-driving | arXiv 2025 | [Paper](https://arxiv.org/abs/2507.00603) / [Code](https://github.com/ucaszyp/World4Drive) |
| **[WORLDMEM: Long-term Consistent World Simulation with Memory](https://arxiv.org/abs/2504.12369)** | world-models | arXiv 2025 | [Paper](https://arxiv.org/abs/2504.12369) |

</details>
