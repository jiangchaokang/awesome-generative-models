# 50-4d-dynamic-scene-world — 🌍 4D Dynamic Scene / World

> 37 papers. 显式动态 3D/4D 场景、world model、仿真与自动驾驶。

[↑ Back to root](../README.md)

## Tasks

- [autonomous-driving](autonomous-driving.md) (17)
- [4d-generation](4d-generation.md) (11)
- [game-worlds](game-worlds.md) (6)
- [world-models](world-models.md) (2)
- [simulation](simulation.md) (1)

## All papers

<details>
<summary><strong>Captain Safari: A World Engine</strong> — `CVPR 2026` `4d-generation` `world-latent` `world-model` `action` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：world-latent；方法：world-model；条件：action。
- **Links**: [Paper](https://scholar.google.com/scholar?q=Captain%20Safari%3A%20A%20World%20Engine) · [Code](https://github.com/search?q=Captain%20Safari%3A%20A%20World%20Engine&type=repositories)

</details>

<details>
<summary><strong>PerpetualWonder: Long-Horizon Action-Conditioned 4D Scene Generation</strong> — `CVPR 2026` `4d-generation` `4dgs` `diffusion` `action` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：4dgs；方法：diffusion；条件：action。
- **Links**: [Paper](https://scholar.google.com/scholar?q=PerpetualWonder%3A%20Long-Horizon%20Action-Conditioned%204D%20Scene%20Generation) · [Code](https://github.com/search?q=PerpetualWonder%3A%20Long-Horizon%20Action-Conditioned%204D%20Scene%20Generation&type=repositories)

</details>

<details>
<summary><strong>FantasyWorld: Geometry-Consistent World Modeling via Unified Video and 3D Prediction</strong> — `ICLR 2026` `4d-generation` `4dgs` `video-latent` `world-model` `video` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：4dgs/video-latent；方法：world-model；条件：video。
- **Links**: [Paper](https://scholar.google.com/scholar?q=FantasyWorld%3A%20Geometry-Consistent%20World%20Modeling%20via%20Unified%20Video%20and%203D%20Prediction) · [Code](https://github.com/search?q=FantasyWorld%3A%20Geometry-Consistent%20World%20Modeling%20via%20Unified%20Video%20and%203D%20Prediction&type=repositories)

</details>

<details>
<summary><strong>Seeing the Future, Perceiving the Future: A Unified Driving World Model for Future Generation and Perception</strong> — `ICRA 2026` `autonomous-driving` `world-latent` `world-model` `trajectory` `open-source`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：world-latent；方法：world-model；条件：trajectory。
- **Links**: [Paper](https://scholar.google.com/scholar?q=Seeing%20the%20Future%2C%20Perceiving%20the%20Future%3A%20A%20Unified%20Driving%20World%20Model%20for%20Future%20Generation%20and%20Perception) · [Code](https://github.com/search?q=Seeing%20the%20Future%2C%20Perceiving%20the%20Future%3A%20A%20Unified%20Driving%20World%20Model%20for%20Future%20Generation%20and%20Perception&type=repositories)

</details>

<details>
<summary><strong>DriveWorld-VLA: Unified Latent-Space World Modeling with Vision-Language-Action for Autonomous Driving</strong> — `arXiv 2026` `autonomous-driving` `world-latent` `trajectory` `world-model` `transformer` `action` `open-source`</summary>

- **TL;DR**: 把 VLA planner 与 latent-space world model 做深度耦合，是 planning-aware world modeling 的代表作。
- **Links**: [Paper](https://arxiv.org/abs/2602.06521) · [Code](https://github.com/liulin815/DriveWorld-VLA.git)

</details>

<details>
<summary><strong>DynFlowDrive: Flow-Based Dynamic World Modeling for Autonomous Driving</strong> — `arXiv 2026` `autonomous-driving` `world-latent` `flow` `world-model` `trajectory` `action` `open-source`</summary>

- **TL;DR**: 用 flow-based dynamics 建模 driving latent transitions，适合放在 world-model / planning 接口分支。
- **Links**: [Paper](https://arxiv.org/abs/2603.19675) · [Code](https://github.com/xiaolul2/DynFlowDrive)

</details>

<details>
<summary><strong>UniDWM: Towards a Unified Driving World Model via Multifaceted Representation Learning</strong> — `arXiv 2026` `autonomous-driving` `world-latent` `vae` `diffusion` `trajectory` `open-source`</summary>

- **TL;DR**: 强调 geometry / appearance / dynamics 的统一 latent 表示，是 2026 初 driving world model 的重要工作。
- **Links**: [Paper](https://arxiv.org/abs/2602.01536) · [Code](https://github.com/Say2L/UniDWM)

</details>

<details>
<summary><strong>VectorWorld: Efficient Streaming World Model via Diffusion Flow on Vector Graphs</strong> — `arXiv 2026` `autonomous-driving` `vector-graph` `vae` `diffusion` `trajectory` `open-source`</summary>

- **TL;DR**: 流式向量图世界模型，按 64m×64m lane-agent tile 增量外扩，结合 motion-aware VAE、EGR-DiT 与 DeltaSim 做 km 级闭环仿真。
- **Links**: [Paper](https://arxiv.org/abs/2603.17652) · [Code](https://github.com/jiangchaokang/VectorWorld)

</details>

<details>
<summary><strong>CAT4D: Create Anything in 4D with Multi-View Video Diffusion Models</strong> — `CVPR 2025` `4d-generation` `multiview` `4dgs` `diffusion` `video`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：multiview/4dgs；方法：diffusion；条件：video/multiview。
- **Links**: [Paper](https://scholar.google.com/scholar?q=CAT4D%3A%20Create%20Anything%20in%204D%20with%20Multi-View%20Video%20Diffusion%20Models)

</details>

<details>
<summary><strong>DrivingSphere: Building a High-fidelity 4D World for Closed-loop Simulation</strong> — `CVPR 2025` `simulation` `autonomous-driving` `4dgs` `world-model` `splatting` `trajectory` `open-source`</summary>

- **TL;DR**: 面向 仿真 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：4dgs；方法：world-model/splatting；条件：trajectory。
- **Links**: [Paper](https://scholar.google.com/scholar?q=DrivingSphere%3A%20Building%20a%20High-fidelity%204D%20World%20for%20Closed-loop%20Simulation) · [Code](https://github.com/search?q=DrivingSphere%3A%20Building%20a%20High-fidelity%204D%20World%20for%20Closed-loop%20Simulation&type=repositories)

</details>

<details>
<summary><strong>GEM: A Generalizable Ego-Vision Multimodal World Model for Fine-Grained Ego-Motion, Object Dynamics, and Scene Composition Control</strong> — `CVPR 2025` `autonomous-driving` `world-latent` `world-model` `trajectory` `action` `open-source`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：world-latent；方法：world-model；条件：trajectory/action。
- **Links**: [Paper](https://scholar.google.com/scholar?q=GEM%3A%20A%20Generalizable%20Ego-Vision%20Multimodal%20World%20Model%20for%20Fine-Grained%20Ego-Motion%2C%20Object%20Dynamics%2C%20and%20Scene%20Composition%20Control) · [Code](https://github.com/search?q=GEM%3A%20A%20Generalizable%20Ego-Vision%20Multimodal%20World%20Model%20for%20Fine-Grained%20Ego-Motion%2C%20Object%20Dynamics%2C%20and%20Scene%20Composition%20Control&type=repositories)

</details>

<details>
<summary><strong>Generating Multimodal Driving Scenes via Next-Scene Prediction</strong> — `CVPR 2025` `autonomous-driving` `world-model` `trajectory` `open-source`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；方法：world-model；条件：trajectory。
- **Links**: [Paper](https://scholar.google.com/scholar?q=Generating%20Multimodal%20Driving%20Scenes%20via%20Next-Scene%20Prediction) · [Code](https://github.com/search?q=Generating%20Multimodal%20Driving%20Scenes%20via%20Next-Scene%20Prediction&type=repositories)

</details>

<details>
<summary><strong>UniScene: Unified Occupancy-centric Driving Scene Generation</strong> — `CVPR 2025` `autonomous-driving` `occupancy` `diffusion` `trajectory` `open-source`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：occupancy；方法：diffusion；条件：trajectory。
- **Links**: [Paper](https://scholar.google.com/scholar?q=UniScene%3A%20Unified%20Occupancy-centric%20Driving%20Scene%20Generation) · [Code](https://github.com/search?q=UniScene%3A%20Unified%20Occupancy-centric%20Driving%20Scene%20Generation&type=repositories)

</details>

<details>
<summary><strong>GameFactory: Creating New Games with Generative Interactive Videos</strong> — `ICCV 2025` `game-worlds` `gameplay` `world-model` `diffusion` `action` `open-source`</summary>

- **TL;DR**: 面向 游戏/交互世界 的 4D 动态场景/世界 工作；领域：游戏/交互；方法：world-model/diffusion；条件：action。
- **Links**: [Paper](https://scholar.google.com/scholar?q=GameFactory%3A%20Creating%20New%20Games%20with%20Generative%20Interactive%20Videos) · [Code](https://github.com/search?q=GameFactory%3A%20Creating%20New%20Games%20with%20Generative%20Interactive%20Videos&type=repositories)

</details>

<details>
<summary><strong>InfiniCube: Unbounded and Controllable Dynamic 3D Driving Scene Generation with World-Guided Video Models</strong> — `ICCV 2025` `4d-generation` `autonomous-driving` `4dgs` `diffusion` `world-model` `image` `trajectory` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：4dgs；方法：diffusion/world-model；条件：image/trajectory。
- **Links**: [Paper](https://scholar.google.com/scholar?q=InfiniCube%3A%20Unbounded%20and%20Controllable%20Dynamic%203D%20Driving%20Scene%20Generation%20with%20World-Guided%20Video%20Models) · [Code](https://github.com/search?q=InfiniCube%3A%20Unbounded%20and%20Controllable%20Dynamic%203D%20Driving%20Scene%20Generation%20with%20World-Guided%20Video%20Models&type=repositories)

</details>

<details>
<summary><strong>Voyaging into Unbounded Dynamic Scenes from a Single View</strong> — `ICCV 2025` `4d-generation` `4dgs` `diffusion` `image` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：4dgs；方法：diffusion；条件：image。
- **Links**: [Paper](https://scholar.google.com/scholar?q=Voyaging%20into%20Unbounded%20Dynamic%20Scenes%20from%20a%20Single%20View) · [Code](https://github.com/search?q=Voyaging%20into%20Unbounded%20Dynamic%20Scenes%20from%20a%20Single%20View&type=repositories)

</details>

<details>
<summary><strong>4K4DGen: Panoramic 4D Generation at 4K Resolution</strong> — `ICLR 2025` `4d-generation` `4dgs` `diffusion` `text` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：4dgs；方法：diffusion；条件：text。
- **Links**: [Paper](https://scholar.google.com/scholar?q=4K4DGen%3A%20Panoramic%204D%20Generation%20at%204K%20Resolution) · [Code](https://github.com/search?q=4K4DGen%3A%20Panoramic%204D%20Generation%20at%204K%20Resolution&type=repositories)

</details>

<details>
<summary><strong>Diffusion Models Are Real-Time Game Engines</strong> — `ICLR 2025` `game-worlds` `gameplay` `diffusion` `world-model` `action`</summary>

- **TL;DR**: 面向 游戏/交互世界 的 4D 动态场景/世界 工作；领域：游戏/交互；方法：diffusion/world-model；条件：action。
- **Links**: [Paper](https://scholar.google.com/scholar?q=Diffusion%20Models%20Are%20Real-Time%20Game%20Engines)

</details>

<details>
<summary><strong>DynamicCity: Large-Scale Occupancy Generation from Dynamic Scenes</strong> — `ICLR 2025` `autonomous-driving` `occupancy` `diffusion` `trajectory` `open-source`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：occupancy；方法：diffusion；条件：trajectory。
- **Links**: [Paper](https://scholar.google.com/scholar?q=DynamicCity%3A%20Large-Scale%20Occupancy%20Generation%20from%20Dynamic%20Scenes) · [Code](https://github.com/search?q=DynamicCity%3A%20Large-Scale%20Occupancy%20Generation%20from%20Dynamic%20Scenes&type=repositories)

</details>

<details>
<summary><strong>GameGen-X: Interactive Open-world Game Video Generation</strong> — `ICLR 2025` `game-worlds` `gameplay` `world-model` `diffusion` `action` `open-source`</summary>

- **TL;DR**: 面向 游戏/交互世界 的 4D 动态场景/世界 工作；领域：游戏/交互；方法：world-model/diffusion；条件：action。
- **Links**: [Paper](https://scholar.google.com/scholar?q=GameGen-X%3A%20Interactive%20Open-world%20Game%20Video%20Generation) · [Code](https://github.com/search?q=GameGen-X%3A%20Interactive%20Open-world%20Game%20Video%20Generation&type=repositories)

</details>

<details>
<summary><strong>Generative World Explorer</strong> — `ICLR 2025` `game-worlds` `gameplay` `world-model` `action` `open-source`</summary>

- **TL;DR**: 面向 游戏/交互世界 的 4D 动态场景/世界 工作；领域：游戏/交互；方法：world-model；条件：action。
- **Links**: [Paper](https://scholar.google.com/scholar?q=Generative%20World%20Explorer) · [Code](https://github.com/search?q=Generative%20World%20Explorer&type=repositories)

</details>

<details>
<summary><strong>Glad: A Streaming Scene Generator for Autonomous Driving</strong> — `ICLR 2025` `autonomous-driving` `world-model` `trajectory`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；方法：world-model；条件：trajectory。
- **Links**: [Paper](https://scholar.google.com/scholar?q=Glad%3A%20A%20Streaming%20Scene%20Generator%20for%20Autonomous%20Driving)

</details>

<details>
<summary><strong>AdaWorld: Learning Adaptable World Models with Latent Actions</strong> — `ICML 2025` `world-models` `world-latent` `world-model` `action` `open-source`</summary>

- **TL;DR**: 面向 世界模型 的 4D 动态场景/世界 工作；表示：world-latent；方法：world-model；条件：action。
- **Links**: [Paper](https://scholar.google.com/scholar?q=AdaWorld%3A%20Learning%20Adaptable%20World%20Models%20with%20Latent%20Actions) · [Code](https://github.com/search?q=AdaWorld%3A%20Learning%20Adaptable%20World%20Models%20with%20Latent%20Actions&type=repositories)

</details>

<details>
<summary><strong>4DNeX: Feed-Forward 4D Generative Modeling Made Easy</strong> — `arXiv 2025` `4d-generation` `4dgs` `diffusion` `image` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：4dgs；方法：diffusion；条件：image。
- **Links**: [Paper](https://arxiv.org/search/?query=4DNeX%3A%20Feed-Forward%204D%20Generative%20Modeling%20Made%20Easy&searchtype=all&abstracts=show&order=-announced_date_first&size=50) · [Code](https://github.com/search?q=4DNeX%3A%20Feed-Forward%204D%20Generative%20Modeling%20Made%20Easy&type=repositories)

</details>

<details>
<summary><strong>4DVD: Cascaded Dense-view Video Diffusion Model for High-quality 4D Content Generation</strong> — `arXiv 2025` `4d-generation` `4dgs` `diffusion` `video`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：4dgs；方法：diffusion；条件：video。
- **Links**: [Paper](https://arxiv.org/search/?query=4DVD%3A%20Cascaded%20Dense-view%20Video%20Diffusion%20Model%20for%20High-quality%204D%20Content%20Generation&searchtype=all&abstracts=show&order=-announced_date_first&size=50)

</details>

<details>
<summary><strong>CoCo4D: Comprehensive and Complex 4D Scene Generation</strong> — `arXiv 2025` `4d-generation` `4dgs` `diffusion` `text` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：4dgs；方法：diffusion；条件：text。
- **Links**: [Paper](https://arxiv.org/search/?query=CoCo4D%3A%20Comprehensive%20and%20Complex%204D%20Scene%20Generation&searchtype=all&abstracts=show&order=-announced_date_first&size=50) · [Code](https://github.com/search?q=CoCo4D%3A%20Comprehensive%20and%20Complex%204D%20Scene%20Generation&type=repositories)

</details>

<details>
<summary><strong>DiST-4D: Disentangled Spatiotemporal Diffusion with Metric Depth for 4D Driving Scene Generation</strong> — `arXiv 2025` `autonomous-driving` `4dgs` `depth` `diffusion` `trajectory` `open-source`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：4dgs/depth；方法：diffusion；条件：trajectory/depth。
- **Links**: [Paper](https://arxiv.org/search/?query=DiST-4D%3A%20Disentangled%20Spatiotemporal%20Diffusion%20with%20Metric%20Depth%20for%204D%20Driving%20Scene%20Generation&searchtype=all&abstracts=show&order=-announced_date_first&size=50) · [Code](https://github.com/search?q=DiST-4D%3A%20Disentangled%20Spatiotemporal%20Diffusion%20with%20Metric%20Depth%20for%204D%20Driving%20Scene%20Generation&type=repositories)

</details>

<details>
<summary><strong>DreamDrive: Generative 4D Scene Modeling from Street View Images</strong> — `arXiv 2025` `autonomous-driving` `4dgs` `diffusion` `image`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：4dgs；方法：diffusion；条件：image。
- **Links**: [Paper](https://arxiv.org/search/?query=DreamDrive%3A%20Generative%204D%20Scene%20Modeling%20from%20Street%20View%20Images&searchtype=all&abstracts=show&order=-announced_date_first&size=50)

</details>

<details>
<summary><strong>Epona: Autoregressive Diffusion World Model for Autonomous Driving</strong> — `arXiv 2025` `autonomous-driving` `world-latent` `autoregressive` `diffusion` `trajectory` `open-source`</summary>

- **TL;DR**: 把 AR 与 diffusion 结合到 driving world model 中，兼顾长时预测与规划接口。
- **Links**: [Paper](https://arxiv.org/abs/2506.24113) · [Code](https://github.com/Kevin-thu/Epona/)

</details>

<details>
<summary><strong>GAIA-2: A Controllable Multi-View Generative World Model for Autonomous Driving</strong> — `arXiv 2025` `autonomous-driving` `multiview` `world-latent` `world-model` `diffusion` `trajectory` `camera`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：multiview/world-latent；方法：world-model/diffusion；条件：trajectory/camera。
- **Links**: [Paper](https://arxiv.org/search/?query=GAIA-2%3A%20A%20Controllable%20Multi-View%20Generative%20World%20Model%20for%20Autonomous%20Driving&searchtype=all&abstracts=show&order=-announced_date_first&size=50)

</details>

<details>
<summary><strong>HERMES: A Unified Self-Driving World Model for Simultaneous 3D Scene Understanding and Generation</strong> — `arXiv 2025` `autonomous-driving` `bev` `world-model` `transformer` `trajectory` `open-source`</summary>

- **TL;DR**: 把 driving scene understanding 与 future generation 合在同一世界模型里，是自动驾驶 world model 路线的重要条目。
- **Links**: [Paper](https://arxiv.org/abs/2501.14729) · [Code](https://github.com/LMD0311/HERMES)

</details>

<details>
<summary><strong>HoloTime: Taming Video Diffusion Models for Panoramic 4D Scene Generation</strong> — `arXiv 2025` `4d-generation` `4dgs` `diffusion` `video` `open-source`</summary>

- **TL;DR**: 面向 4D 生成 的 4D 动态场景/世界 工作；表示：4dgs；方法：diffusion；条件：video。
- **Links**: [Paper](https://arxiv.org/search/?query=HoloTime%3A%20Taming%20Video%20Diffusion%20Models%20for%20Panoramic%204D%20Scene%20Generation&searchtype=all&abstracts=show&order=-announced_date_first&size=50) · [Code](https://github.com/search?q=HoloTime%3A%20Taming%20Video%20Diffusion%20Models%20for%20Panoramic%204D%20Scene%20Generation&type=repositories)

</details>

<details>
<summary><strong>MaskGWM: A Generalizable Driving World Model with Video Mask Reconstruction</strong> — `arXiv 2025` `autonomous-driving` `video-latent` `world-model` `diffusion` `trajectory` `open-source`</summary>

- **TL;DR**: 面向 自动驾驶世界模型 的 4D 动态场景/世界 工作；领域：自动驾驶世界模型；表示：video-latent；方法：world-model/diffusion；条件：trajectory。
- **Links**: [Paper](https://arxiv.org/search/?query=MaskGWM%3A%20A%20Generalizable%20Driving%20World%20Model%20with%20Video%20Mask%20Reconstruction&searchtype=all&abstracts=show&order=-announced_date_first&size=50) · [Code](https://github.com/search?q=MaskGWM%3A%20A%20Generalizable%20Driving%20World%20Model%20with%20Video%20Mask%20Reconstruction&type=repositories)

</details>

<details>
<summary><strong>Matrix-Game 2.0: An Open-Source, Real-Time, and Streaming Interactive World Model</strong> — `arXiv 2025` `game-worlds` `gameplay` `world-model` `action` `open-source`</summary>

- **TL;DR**: 面向 游戏/交互世界 的 4D 动态场景/世界 工作；领域：游戏/交互；方法：world-model；条件：action。
- **Links**: [Paper](https://arxiv.org/search/?query=Matrix-Game%202.0%3A%20An%20Open-Source%2C%20Real-Time%2C%20and%20Streaming%20Interactive%20World%20Model&searchtype=all&abstracts=show&order=-announced_date_first&size=50) · [Code](https://github.com/search?q=Matrix-Game%202.0%3A%20An%20Open-Source%2C%20Real-Time%2C%20and%20Streaming%20Interactive%20World%20Model&type=repositories)

</details>

<details>
<summary><strong>Matrix-Game: Interactive World Foundation Model</strong> — `arXiv 2025` `game-worlds` `gameplay` `world-model` `action` `open-source`</summary>

- **TL;DR**: 面向 游戏/交互世界 的 4D 动态场景/世界 工作；领域：游戏/交互；方法：world-model；条件：action。
- **Links**: [Paper](https://arxiv.org/search/?query=Matrix-Game%3A%20Interactive%20World%20Foundation%20Model&searchtype=all&abstracts=show&order=-announced_date_first&size=50) · [Code](https://github.com/search?q=Matrix-Game%3A%20Interactive%20World%20Foundation%20Model&type=repositories)

</details>

<details>
<summary><strong>World4Drive: End-to-End Autonomous Driving via Intention-aware Physical Latent World Model</strong> — `arXiv 2025` `autonomous-driving` `world-latent` `trajectory` `world-model` `open-source`</summary>

- **TL;DR**: 强调 intention-aware latent world modeling 与规划闭环结合，适合放在 autonomous-driving 主线。
- **Links**: [Paper](https://arxiv.org/abs/2507.00603) · [Code](https://github.com/ucaszyp/World4Drive)

</details>

<details>
<summary><strong>WORLDMEM: Long-term Consistent World Simulation with Memory</strong> — `arXiv 2025` `world-models` `world-latent` `world-model` `action` `open-source`</summary>

- **TL;DR**: 面向 世界模型 的 4D 动态场景/世界 工作；表示：world-latent；方法：world-model；条件：action。
- **Links**: [Paper](https://arxiv.org/search/?query=WORLDMEM%3A%20Long-term%20Consistent%20World%20Simulation%20with%20Memory&searchtype=all&abstracts=show&order=-announced_date_first&size=50) · [Code](https://github.com/search?q=WORLDMEM%3A%20Long-term%20Consistent%20World%20Simulation%20with%20Memory&type=repositories)

</details>
