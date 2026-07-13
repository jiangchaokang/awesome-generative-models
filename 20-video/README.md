# 🎬 Video

> Final output is a video: text-to-video, image-to-video, editing, human animation, long video, and surround-view video.

**51 curated papers** · [← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)

<details>
<summary><b>📐 How this pipeline works</b></summary>

```text
Text / image / pose / sketch / camera
        ↓
Condition encoders + video tokenizer / VAE
        ↓
Spatiotemporal generator (DiT / diffusion / flow)
        ↓
Temporal consistency / editing / motion control
        ↓
Video clip / surround-view sequence
```

</details>

## Tasks in this category

[text-to-video](text-to-video.md) <sub>(20)</sub> · [image-to-video](image-to-video.md) <sub>(9)</sub> · [video-editing](video-editing.md) <sub>(7)</sub> · [human-animation](human-animation.md) <sub>(8)</sub> · [long-video](long-video.md) <sub>(2)</sub> · [autonomous-driving-video](autonomous-driving-video.md) <sub>(5)</sub>

## 🌟 Spotlight

#### 🌟 [Anti-I2V: Safeguarding your photos from malicious image-to-video generation](https://arxiv.org/abs/2603.24570)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: image-to-video](https://img.shields.io/static/v1?label=Track&message=image-to-video&color=7C3AED&style=flat-square&labelColor=111827)

> A defensive method for protecting photos against misuse by malicious image-to-video generation systems.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.24570)

#### 🌟 [Faster Inference of Flow-Based Generative Models via Improved Data-Noise Coupling](https://arxiv.org/abs/2603.15279)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-video](https://img.shields.io/static/v1?label=Track&message=text-to-video&color=7C3AED&style=flat-square&labelColor=111827)

> A flow-based inference acceleration method with better data-noise coupling forl generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.15279)

#### 🌟 [Foveated Diffusion: Efficient Spatially Adaptive Image and Video Generation](https://arxiv.org/abs/2603.23491)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-video](https://img.shields.io/static/v1?label=Track&message=text-to-video&color=7C3AED&style=flat-square&labelColor=111827)

> A spatially adaptive generation framework that concentrates compute where perceptual detail matters most.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.23491)

## Full Catalog

**Legend:** 🟢 code publicly available · ⚪ code not (yet) public · ★ live GitHub stars (refreshed weekly)

### [text-to-video](text-to-video.md) · 20

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[Faster Inference of Flow-Based Generative Models via Improved Data-Noise Coupling](https://arxiv.org/abs/2603.15279)** | arXiv 2026 | A flow-based inference acceleration method with better data-noise coupling forl… | [📄 arXiv](https://arxiv.org/abs/2603.15279) |
| ⚪ **[Foveated Diffusion: Efficient Spatially Adaptive Image and Video Generation](https://arxiv.org/abs/2603.23491)** | arXiv 2026 | A spatially adaptive generation framework that concentrates compute where perceptual… | [📄 arXiv](https://arxiv.org/abs/2603.23491) |
| ⚪ **[LumosX: Relate Any Identities with Their Attributes for Personalized Video Generation](https://arxiv.org/abs/2603.20192)** | arXiv 2026 | A personalized video-generation framework that better binds identities to their… | [📄 arXiv](https://arxiv.org/abs/2603.20192) |
| ⚪ **[Spectrally-Guided Diffusion Noise Schedules](https://arxiv.org/abs/2603.19222)** | arXiv 2026 | Studies spectral properties of noise schedules to improve diffusion performance for image… | [📄 arXiv](https://arxiv.org/abs/2603.19222) |
| 🟢 **[Wan 2.1: Open-Source Video Foundation Model](https://arxiv.org/abs/2503.20314)** | arXiv 2025 | A strong open video foundation model supporting text-to-video, image-to-video, and… | [📄 arXiv](https://arxiv.org/abs/2503.20314) · [💻 Code ★16.5k](https://github.com/Wan-Video/Wan2.1) |
| 🟢 **[HunyuanVideo: A Systematic Framework for Large Video Generation Models](https://arxiv.org/abs/2412.03603)** | arXiv 2024 · since 2025 | A major open video backbone that remained highly active and widely reused throughout 2025. | [📄 arXiv](https://arxiv.org/abs/2412.03603) · [💻 Code ★12.3k](https://github.com/Tencent-Hunyuan/HunyuanVideo) |
| 🟢 **[HunyuanVideo 1.5 Technical Report](https://arxiv.org/abs/2511.18870)** | arXiv 2025 | HunyuanVideo 1.5 is Tencent Hunyuan’s lighter video generation release spanning… | [📄 arXiv](https://arxiv.org/abs/2511.18870) · [💻 Code ★4.5k](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5) |
| 🟢 **[Step-Video-T2V: A State-of-the-Art Text-to-Video Model](https://arxiv.org/abs/2502.10248)** | arXiv 2025 | A large-scale open T2V model combining video VAE and flow-matching DiT for strong motion… | [📄 arXiv](https://arxiv.org/abs/2502.10248) · [💻 Code ★3.2k](https://github.com/stepfun-ai/Step-Video-T2V) |
| 🟢 **[ConsisID: Identity-Preserving Text-to-Video Generation by Frequency Decomposition](https://arxiv.org/abs/2411.17440)** | CVPR 2025 | A frequency-aware DiT-based framework for preserving identity in personalized… | [📄 arXiv](https://arxiv.org/abs/2411.17440) · [💻 Code ★847](https://github.com/PKU-YuanGroup/ConsisID) · [🌐 Project](https://pku-yuangroup.github.io/ConsisID/) |
| 🟢 **[PhyT2V: LLM-Guided Iterative Self-Refinement for Physics-Grounded Text-to-Video Generation](https://arxiv.org/abs/2412.00596)** | CVPR 2025 | Uses LLM-guided iterative self-refinement to improve physical plausibility in generated… | [📄 arXiv](https://arxiv.org/abs/2412.00596) · [💻 Code ★68](https://github.com/pittisl/PhyT2V) |
| 🟢 **[ByTheWay: Boost Your Text-to-Video Generation Model to Higher Quality in a Training-free Way](https://openaccess.thecvf.com/content/CVPR2025/html/Bu_ByTheWay_Boost_Your_Text-to-Video_Generation_Model_to_Higher_Quality_in_CVPR_2025_paper.html)** | CVPR 2025 | A training-free enhancement method that improves temporal consistency and motion… | [📄 CVF](https://openaccess.thecvf.com/content/CVPR2025/html/Bu_ByTheWay_Boost_Your_Text-to-Video_Generation_Model_to_Higher_Quality_in_CVPR_2025_paper.html) · [💻 Code ★48](https://github.com/Bujiazi/ByTheWay) · [🌐 Project](https://bujiazi.github.io/bytheway.github.io/) |
| ⚪ **[BlobGEN-Vid: Compositional Text-to-Video Generation with Blob Video Representations](https://arxiv.org/abs/2501.07647)** | CVPR 2025 | Represents videos as blob primitives to enable more controllable multi-object video… | [📄 arXiv](https://arxiv.org/abs/2501.07647) |
| 🟢 **[CogVideoX: Text-to-Video Diffusion Models with An Expert Transformer](https://arxiv.org/abs/2408.06072)** | arXiv 2024 · since 2025 | An influential open T2V backbone that continued to be actively reused in 2025 research… | [📄 arXiv](https://arxiv.org/abs/2408.06072) · [💻 Code](https://github.com/THUDM/CogVideo) |
| ⚪ **[EIDT-V: Exploiting Intersections in Diffusion Trajectories for Model-Agnostic, Zero-Shot, Training-Free Text-to-Video Generation](https://arxiv.org/abs/2504.06861)** | CVPR 2025 | A model-agnostic training-free T2V method that exploits intersections in diffusion… | [📄 arXiv](https://arxiv.org/abs/2504.06861) |
| ⚪ **[InstanceCap: Improving Text-to-Video Generation via Instance-aware Structured Caption](https://arxiv.org/abs/2412.09283)** | CVPR 2025 | An instance-aware captioning and enhancement pipeline for improving object fidelity and… | [📄 arXiv](https://arxiv.org/abs/2412.09283) |
| ⚪ **[Kling: AI-Powered Video Generation Platform](https://klingai.com/)** | Technical Report 2025 | A production video platform known for strong motion realism, long clips, and… | [🌐 Project](https://klingai.com/) |
| ⚪ **[RAPO: The Devil is in the Prompts: Retrieval-Augmented Prompt Optimization for Text-to-Video Generation](https://arxiv.org/abs/2504.11739)** | CVPR 2025 | A retrieval-augmented prompt-optimization framework that improves both visual detail and… | [📄 arXiv](https://arxiv.org/abs/2504.11739) |
| ⚪ **[Seaweed-7B: Cost-Effective Training of Video Generation Foundation Model](https://arxiv.org/abs/2504.08685)** | arXiv 2025 | A 7B-scale video foundation model emphasizing lower training cost without giving up broad… | [📄 arXiv](https://arxiv.org/abs/2504.08685) · [🌐 Project](https://seaweed.video/) |
| ⚪ **[Seedance 1.0: Exploring the Boundaries of Video Generation Models](https://arxiv.org/abs/2506.18538)** | arXiv 2025 | A unified high-end video generator from ByteDance Seed focused on quality, multi-shot… | [📄 arXiv](https://arxiv.org/abs/2506.18538) · [🌐 Project](https://seed.bytedance.com/en/seedance) |
| ⚪ **[TransPixeler: Advancing Text-to-Video Generation with Transparency](https://arxiv.org/abs/2501.03006)** | CVPR 2025 | Extends text-to-video models to RGBA generation so transparent visual effects can be… | [📄 arXiv](https://arxiv.org/abs/2501.03006) |

### [image-to-video](image-to-video.md) · 9

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[Anti-I2V: Safeguarding your photos from malicious image-to-video generation](https://arxiv.org/abs/2603.24570)** | arXiv 2026 | A defensive method for protecting photos against misuse by malicious image-to-video… | [📄 arXiv](https://arxiv.org/abs/2603.24570) |
| ⚪ **[Search2Motion: Training-Free Object-Level Motion Control via Attention-Consensus Search](https://arxiv.org/abs/2603.16711)** | arXiv 2026 | A training-free object-level motion editing framework based on attention-consensus search. | [📄 arXiv](https://arxiv.org/abs/2603.16711) |
| 🟢 **[HunyuanVideo-I2V: A Customizable Image-to-Video Model based on HunyuanVideo](https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V)** | Technical Report 2025 | Tencent Hunyuan’s image-to-video extension builds on HunyuanVideo and targets… | [💻 Code ★1.8k](https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V) |
| ⚪ **[AnyI2V: Animating Any Conditional Image with Motion Control](https://arxiv.org/abs/2507.02857)** | ICCV 2025 | A training-free motion-control framework that animates diverse condition images… | [📄 arXiv](https://arxiv.org/abs/2507.02857) · [🌐 Project](https://henghuiding.com/AnyI2V/) |
| ⚪ **[MotionPro: A Precise Motion Controller for Image-to-Video Generation](https://arxiv.org/abs/2505.20287)** | CVPR 2025 | A precise trajectory- and mask-based motion controller for fine-grained I2V animation. | [📄 arXiv](https://arxiv.org/abs/2505.20287) · [🌐 Project](https://zhw-zhang.github.io/MotionPro-page/) |
| ⚪ **[MotionStone: Decoupled Motion Intensity Modulation with Diffusion Transformer for Image-to-Video Generation](https://arxiv.org/abs/2412.05848)** | CVPR 2025 | Decouples object motion and camera motion intensity to improve controllable I2V synthesis. | [📄 arXiv](https://arxiv.org/abs/2412.05848) |
| ⚪ **[Pyramidal Flow Matching for Efficient Video Generative Modeling](https://arxiv.org/abs/2410.05954)** | ICLR 2025 | A unified pyramidal flow-matching framework for efficient high-resolution video… | [📄 arXiv](https://arxiv.org/abs/2410.05954) · [🌐 Project](https://pyramid-flow.github.io/) |
| ⚪ **[SG-I2V: Self-Guided Trajectory Control in Image-to-Video Generation](https://arxiv.org/abs/2411.04989)** | ICLR 2025 | A zero-shot I2V control method that leverages the pretrained model’s own knowledge… | [📄 arXiv](https://arxiv.org/abs/2411.04989) |
| ⚪ **[Through-The-Mask: Mask-based Motion Trajectories for Image-to-Video Generation](https://arxiv.org/abs/2501.03059)** | CVPR 2025 | A compositional I2V pipeline using mask-based motion trajectories as explicit… | [📄 arXiv](https://arxiv.org/abs/2501.03059) · [🌐 Project](https://guyyariv.github.io/TTM/) |

### [video-editing](video-editing.md) · 7

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[P-Flow: Prompting Visual Effects Generation](https://arxiv.org/abs/2603.22091)** | arXiv 2026 | A prompting-based framework for generating controllable visual effects sequences in video. | [📄 arXiv](https://arxiv.org/abs/2603.22091) |
| ⚪ **[ViFeEdit: A Video-Free Tuner of Your Video Diffusion Transformer](https://arxiv.org/abs/2603.15478)** | arXiv 2026 | Tunes video diffusion transformers for editing tasks without requiring task-specific… | [📄 arXiv](https://arxiv.org/abs/2603.15478) |
| 🟢 **[VACE: All-in-One Video Creation and Editing](https://arxiv.org/abs/2503.07598)** | ICCV 2025 | A unified diffusion-transformer framework for reference-to-video, V2V editing, and masked… | [📄 arXiv](https://arxiv.org/abs/2503.07598) · [💻 Code ★3.9k](https://github.com/ali-vilab/VACE) · [🌐 Project](https://ali-vilab.github.io/VACE-Page/) |
| 🟢 **[h-Edit: Effective and Flexible Diffusion-Based Editing via Doob's h-Transform](https://arxiv.org/abs/2503.02187)** | CVPR 2025 | A general bridge-based editing framework that supports flexible composition of editing… | [📄 arXiv](https://arxiv.org/abs/2503.02187) · [💻 Code ★77](https://github.com/nktoan/h-edit) |
| ⚪ **[SketchVideo: Sketch-based Video Generation and Editing](https://arxiv.org/abs/2503.23284)** | CVPR 2025 | A sketch-conditioned video model supporting sparse keyframe control for both generation… | [📄 arXiv](https://arxiv.org/abs/2503.23284) |
| ⚪ **[VideoDirector: Precise Video Editing via Text-to-Video Models](https://arxiv.org/abs/2411.17592)** | CVPR 2025 | Brings inversion and attention-control ideas into native T2V models for more accurate… | [📄 arXiv](https://arxiv.org/abs/2411.17592) |
| ⚪ **[VideoMage: Multi-Subject and Motion Customization of Text-to-Video Diffusion Models](https://arxiv.org/abs/2503.21781)** | CVPR 2025 | Customizes both multiple identities and their interactive motions within one… | [📄 arXiv](https://arxiv.org/abs/2503.21781) |

### [human-animation](human-animation.md) · 8

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| 🟢 **[UniAnimate-DiT: Human Image Animation with Large-Scale Video Diffusion Transformer](https://arxiv.org/abs/2504.11289)** | arXiv 2025 | Builds high-fidelity human animation on top of a large open video backbone with…<br>`human-avatar` | [📄 arXiv](https://arxiv.org/abs/2504.11289) · [💻 Code ★852](https://github.com/ali-vilab/UniAnimate-DiT) |
| 🟢 **[X-Dyna: Expressive Dynamic Human Image Animation](https://arxiv.org/abs/2501.10021)** | CVPR 2025 | A ByteDance human animation system that strengthens dynamic details in both subject and…<br>`human-avatar` | [📄 arXiv](https://arxiv.org/abs/2501.10021) · [💻 Code ★269](https://github.com/bytedance/X-Dyna) |
| ⚪ **[Animate Anyone 2: High-Fidelity Character Image Animation with Environment Affordance](https://arxiv.org/abs/2502.06145)** | ICCV 2025 | Adds environment affordance and object interaction modeling to character image animation.<br>`human-avatar` | [📄 arXiv](https://arxiv.org/abs/2502.06145) |
| ⚪ **[Animate-X: Universal Character Image Animation with Enhanced Motion Representation](https://arxiv.org/abs/2410.10306)** | ICLR 2025 | A universal animation framework that extends beyond humans to anthropomorphic characters…<br>`human-avatar` | [📄 arXiv](https://arxiv.org/abs/2410.10306) |
| ⚪ **[DreamActor-M1: Holistic, Expressive and Robust Human Image Animation with Hybrid Guidance](https://arxiv.org/abs/2504.01724)** | ICCV 2025 | A DiT-based animation model combining face, head, and body guidance for robust…<br>`human-avatar` | [📄 arXiv](https://arxiv.org/abs/2504.01724) · [🌐 Project](https://grisoon.github.io/DreamActor-M1/) |
| ⚪ **[EgoControl: Controllable Egocentric Video Generation via 3D Full-Body Poses](https://arxiv.org/abs/2511.18173)** | arXiv 2025 | A pose-controllable egocentric video generator trained to follow articulated 3D body…<br>`human-avatar` | [📄 arXiv](https://arxiv.org/abs/2511.18173) |
| ⚪ **[OmniHuman-1: Rethinking the Scaling-Up of One-Stage Conditioned Human Animation Models](https://arxiv.org/abs/2502.01061)** | ICCV 2025 | A large one-stage conditioned human animation framework that scales across portraits…<br>`human-avatar` | [📄 arXiv](https://arxiv.org/abs/2502.01061) · [🌐 Project](https://omnihuman-lab.github.io/) |
| ⚪ **[StableAnimator: High-Quality Identity-Preserving Human Image Animation](https://arxiv.org/abs/2411.17697)** | CVPR 2025 | An end-to-end identity-preserving human animation model with strong facial consistency.<br>`human-avatar` | [📄 arXiv](https://arxiv.org/abs/2411.17697) |

### [long-video](long-video.md) · 2

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[Minute-Long Videos with Dual Parallelisms](https://arxiv.org/abs/2505.21070)** | AAAI 2026 | A distributed inference scheme that parallelizes both frames and layers for minute-long… | [📄 arXiv](https://arxiv.org/abs/2505.21070) |
| ⚪ **[LinGen: Towards High-Resolution Minute-Length Text-to-Video Generation with Linear Computational Complexity](https://arxiv.org/abs/2412.09856)** | CVPR 2025 | A linear-complexity architecture aimed at minute-length high-resolution T2V generation on… | [📄 arXiv](https://arxiv.org/abs/2412.09856) · [🌐 Project](https://lineargen.github.io/) |

### [autonomous-driving-video](autonomous-driving-video.md) · 5

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| 🟢 **[MagicDrive-V2: High-Resolution Long Video Generation for Autonomous Driving with Adaptive Control](https://arxiv.org/abs/2411.13807)** | ICCV 2025 | A high-resolution long-form multi-view driving video model with richer geometric and…<br>`autonomous-driving` | [📄 arXiv](https://arxiv.org/abs/2411.13807) · [💻 Code ★717](https://github.com/flymin/MagicDrive-V2) · [🌐 Project](https://magicdrive-v2.github.io/) |
| ⚪ **[CoGen: 3D Consistent Video Generation via Adaptive Conditioning for Autonomous Driving](https://arxiv.org/abs/2503.22231)** | arXiv 2025 | Improves 3D consistency in controllable driving video generation through spatially…<br>`autonomous-driving` | [📄 arXiv](https://arxiv.org/abs/2503.22231) · [🌐 Project](https://xiaomi-research.github.io/cogen/) |
| ⚪ **[DriveDreamer-2: LLM-Enhanced World Models for Diverse Driving Video Generation](https://arxiv.org/abs/2403.06845)** | AAAI 2025 | An LLM-enhanced driving video generator that converts user intent into trajectories…<br>`autonomous-driving` | [📄 arXiv](https://arxiv.org/abs/2403.06845) |
| ⚪ **[DriveScape: Towards High-Resolution Controllable Multi-View Driving Video Generation](https://arxiv.org/abs/2409.05463)** | ICCV 2025 | A high-resolution multi-view driving video generator with strong spatial-temporal…<br>`autonomous-driving` | [📄 arXiv](https://arxiv.org/abs/2409.05463) · [🌐 Project](https://metadrivescape.github.io/papers_project/drivescapev1/index.html) |
| ⚪ **[StreetCrafter: Street View Synthesis with Controllable Video Diffusion Models](https://arxiv.org/abs/2412.13188)** | CVPR 2025 | A controllable street-view synthesis model driven by LiDAR renderings for precise view…<br>`autonomous-driving` | [📄 arXiv](https://arxiv.org/abs/2412.13188) |
