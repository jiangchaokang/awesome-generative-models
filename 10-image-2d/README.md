# 🖼️ Image 2D

> Final output is a single 2D image: text-to-image, controllable generation, safety, personalization, and efficient inference.

**56 curated papers** · [← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)

<details>
<summary><b>📐 How this pipeline works</b></summary>

```text
Prompt / control / reference
        ↓
Text / multimodal encoder
        ↓
Latent generator (Diffusion / Flow / AR / VQ)
        ↓
Decoder / upsampler / reward correction
        ↓
Single 2D image
```

</details>

## Tasks in this category

[text-to-image](text-to-image.md) <sub>(18)</sub> · [controllable-generation](controllable-generation.md) <sub>(14)</sub> · [model-efficiency](model-efficiency.md) <sub>(13)</sub> · [alignment-safety](alignment-safety.md) <sub>(7)</sub> · [personalization](personalization.md) <sub>(4)</sub>

## 🌟 Spotlight

#### 🌟 [iFSQ: Improving FSQ for Image Generation with 1 Line of Code](https://arxiv.org/abs/2601.17124)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A simple quantization improvement that makes FSQ stronger for high-quality image generation with minimal code changes.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2601.17124) [![Code: GitHub ★ 101](https://img.shields.io/static/v1?label=Code&message=GitHub+%E2%98%85+101&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Tencent-Hunyuan/iFSQ)

#### 🌟 [Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation](https://arxiv.org/abs/2603.18627)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827)

> Uses agentic search over flow trajectories to improve spatial grounding for difficult compositional prompts.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.18627)

#### 🌟 [DAK-UCB: Diversity-Aware Prompt Routing for LLMs and Generative Models](https://arxiv.org/abs/2603.23140)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827)

> A routing strategy that allocates prompts across model choices to balance quality, diversity, and compute cost.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.23140)

## Full Catalog

**Legend:** 🟢 code publicly available · ⚪ code not (yet) public · ★ live GitHub stars (refreshed weekly)

### [text-to-image](text-to-image.md) · 18

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[DiffGraph: An Automated Agent-driven Model Merging Framework for In-the-Wild Text-to-Image Generation](https://arxiv.org/abs/2603.20470)** | arXiv 2026 | An agentic model-merging system for assembling stronger in-the-wild T2I pipelines from… | [📄 arXiv](https://arxiv.org/abs/2603.20470) |
| ⚪ **[LaDe: Unified Multi-Layered Graphic Media Generation and Decomposition](https://arxiv.org/abs/2603.17965)** | arXiv 2026 | A unified system for generating and decomposing layered editable graphic media rather… | [📄 arXiv](https://arxiv.org/abs/2603.17965) |
| ⚪ **[SHARP: Spectrum-aware Highly-dynamic Adaptation for Resolution Promotion in Remote Sensing Synthesis](https://arxiv.org/abs/2603.21783)** | arXiv 2026 | A domain-oriented T2I adaptation framework targeting high-resolution remote-sensing… | [📄 arXiv](https://arxiv.org/abs/2603.21783) |
| ⚪ **[UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation](https://arxiv.org/abs/2603.23500)** | arXiv 2026 | A policy-optimization view of reasoning-driven visual generation for stronger prompt… | [📄 arXiv](https://arxiv.org/abs/2603.23500) |
| 🟢 **[FLUX.1: Scalable Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206)** | arXiv 2024 · since 2025 | A highly influential rectified-flow image generator that remained one of the dominant… | [📄 arXiv](https://arxiv.org/abs/2403.03206) · [💻 Code ★25.7k](https://github.com/black-forest-labs/flux) |
| 🟢 **[SANA 1.5: Efficient Scaling of Training-Time and Inference-Time Compute in Linear Diffusion Transformer](https://arxiv.org/abs/2501.18427)** | arXiv 2025 | A stronger SANA release focused on efficient scaling of both training-time and… | [📄 arXiv](https://arxiv.org/abs/2501.18427) · [💻 Code ★8.5k](https://github.com/NVlabs/Sana) |
| 🟢 **[Qwen-Image Technical Report](https://arxiv.org/abs/2508.02324)** | arXiv 2025 | Qwen-Image is an open image-generation foundation model built for strong text rendering… | [📄 arXiv](https://arxiv.org/abs/2508.02324) · [💻 Code ★8.1k](https://github.com/QwenLM/Qwen-Image) |
| 🟢 **[HunyuanImage 3.0 Technical Report](https://arxiv.org/abs/2509.23951)** | arXiv 2025 | HunyuanImage 3.0 is Tencent Hunyuan’s large native multimodal image model focused on… | [📄 arXiv](https://arxiv.org/abs/2509.23951) · [💻 Code ★3.2k](https://github.com/Tencent-Hunyuan/HunyuanImage-3.0) |
| 🟢 **[PixArt-Sigma: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation](https://arxiv.org/abs/2403.04692)** | ECCV 2024 · since 2025 | An important open DiT baseline that continued to matter in 2025 as a widely reused… | [📄 arXiv](https://arxiv.org/abs/2403.04692) · [💻 Code ★1.9k](https://github.com/PixArt-alpha/PixArt-sigma) |
| 🟢 **[One-Prompt-One-Story: Free-Lunch Consistent Text-to-Image Generation Using a Single Prompt](https://arxiv.org/abs/2501.13554)** | ICLR 2025 | A training-free method for identity-consistent image sequences by concatenating story… | [📄 arXiv](https://arxiv.org/abs/2501.13554) · [💻 Code ★318](https://github.com/byliutao/1Prompt1Story) |
| 🟢 **[D-AR: Diffusion via Autoregressive Models](https://arxiv.org/abs/2505.23660)** | arXiv 2025 | Rewrites diffusion-style generation in an autoregressive form and studies the bridge… | [📄 arXiv](https://arxiv.org/abs/2505.23660) · [💻 Code ★138](https://github.com/showlab/D-AR) |
| ⚪ **[Denoising Autoregressive Transformers for Scalable Text-to-Image Generation](https://openreview.net/forum?id=amDkNPVWcn)** | ICLR 2025 | DART unifies autoregressive generation and denoising ideas for scalable image synthesis. | [📄 OpenReview](https://openreview.net/forum?id=amDkNPVWcn) |
| ⚪ **[Fluid: Scaling Autoregressive Text-to-image Generative Models with Continuous Tokens](https://arxiv.org/abs/2410.13863)** | ICLR 2025 | A large-scale autoregressive T2I model built on continuous tokens and random-order… | [📄 arXiv](https://arxiv.org/abs/2410.13863) |
| ⚪ **[Meissonic: Revitalizing Masked Generative Transformers for Efficient High-Resolution Text-to-Image Synthesis](https://arxiv.org/abs/2410.08261)** | ICLR 2025 | A masked generative transformer that closes much of the gap to diffusion while staying… | [📄 arXiv](https://arxiv.org/abs/2410.08261) |
| ⚪ **[SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers](https://arxiv.org/abs/2410.10629)** | ICLR 2025 | A linear-attention DiT family that made high-resolution image generation substantially… | [📄 arXiv](https://arxiv.org/abs/2410.10629) · [🌐 Project](https://nvlabs.github.io/Sana/) |
| ⚪ **[Seedream 3.0 Technical Report](https://arxiv.org/abs/2504.11346)** | arXiv 2025 | Seedream 3.0 is ByteDance Seed’s upgraded text-to-image system emphasizing typography… | [📄 arXiv](https://arxiv.org/abs/2504.11346) · [🌐 Project](https://seed.bytedance.com/blog/seedream-3-0-%E6%96%87%E7%94%9F%E5%9B%BE%E6%A8%A1%E5%9E%8B%E6%8A%80%E6%9C%AF%E6%8A%A5%E5%91%8A%E5%8F%91%E5%B8%83) |
| ⚪ **[Text-to-Image Rectified Flow as Plug-and-Play Priors](https://arxiv.org/abs/2406.03293)** | ICLR 2025 | Shows rectified-flow T2I models can act as plug-and-play priors beyond direct image… | [📄 arXiv](https://arxiv.org/abs/2406.03293) |
| ⚪ **[TIGeR: Unifying Text-to-Image Generation and Retrieval with Large Multimodal Models](https://arxiv.org/abs/2406.05814)** | ICLR 2025 | Unifies generation and retrieval in a single multimodal model and lets the system choose… | [📄 arXiv](https://arxiv.org/abs/2406.05814) |

### [controllable-generation](controllable-generation.md) · 14

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation](https://arxiv.org/abs/2603.18627)** | arXiv 2026 | Uses agentic search over flow trajectories to improve spatial grounding for difficult… | [📄 arXiv](https://arxiv.org/abs/2603.18627) |
| ⚪ **[LGTM: Training-Free Light-Guided Text-to-Image Diffusion Model via Initial Noise Manipulation](https://arxiv.org/abs/2603.24086)** | arXiv 2026 | A training-free method that steers lighting effects by directly manipulating the initial… | [📄 arXiv](https://arxiv.org/abs/2603.24086) |
| ⚪ **[Relevance Feedback in Text-to-Image Diffusion: A Training-Free And Model-Agnostic Interactive Framework](https://arxiv.org/abs/2603.14936)** | arXiv 2026 | An interactive relevance-feedback loop for refining generations without retraining the… | [📄 arXiv](https://arxiv.org/abs/2603.14936) |
| ⚪ **[SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation](https://arxiv.org/abs/2603.22228)** | arXiv 2026 | Introduces verifiable reward modeling for spatial relations to improve fine-grained… | [📄 arXiv](https://arxiv.org/abs/2603.22228) |
| ⚪ **[Compass Control: Multi Object Orientation Control for Text-to-Image Generation](https://arxiv.org/abs/2504.06752)** | CVPR 2025 | Introduces orientation-aware compass tokens for explicit multi-object pose control in… | [📄 arXiv](https://arxiv.org/abs/2504.06752) |
| ⚪ **[Focus-N-Fix: Region-Aware Fine-Tuning for Text-to-Image Generation](https://arxiv.org/abs/2501.06481)** | CVPR 2025 | A localized fine-tuning method that corrects only problematic regions while preserving… | [📄 arXiv](https://arxiv.org/abs/2501.06481) |
| ⚪ **[Generative Photography: Scene-Consistent Camera Control for Realistic Text-to-Image Synthesis](https://arxiv.org/abs/2412.02168)** | CVPR 2025 | A physically grounded camera-control framework for scene-consistent changes in focal… | [📄 arXiv](https://arxiv.org/abs/2412.02168) |
| ⚪ **[Make It Count: Text-to-Image Generation with an Accurate Number of Objects](https://arxiv.org/abs/2406.10210)** | CVPR 2025 | Targets count fidelity by detecting over- and under-generation during denoising and… | [📄 arXiv](https://arxiv.org/abs/2406.10210) |
| ⚪ **[MCCD: Multi-Agent Collaboration-based Compositional Diffusion for Complex Text-to-Image Generation](https://arxiv.org/abs/2505.02648)** | CVPR 2025 | A training-free multi-agent prompting and regional refinement framework for complex… | [📄 arXiv](https://arxiv.org/abs/2505.02648) |
| ⚪ **[PreciseCam: Precise Camera Control for Text-to-Image Generation](https://arxiv.org/abs/2501.12910)** | CVPR 2025 | A camera-conditioned generation method that gives explicit control over extrinsics and… | [📄 arXiv](https://arxiv.org/abs/2501.12910) · [🌐 Project](https://graphics.unizar.es/projects/PreciseCam2024) |
| ⚪ **[Progressive Compositionality in Text-to-Image Generative Models](https://arxiv.org/abs/2410.16719)** | ICLR 2025 | Builds a hard-negative curriculum and contrastive learning pipeline to improve… | [📄 arXiv](https://arxiv.org/abs/2410.16719) |
| ⚪ **[ShapeWords: Guiding Text-to-Image Synthesis with 3D Shape-Aware Prompts](https://arxiv.org/abs/2412.02912)** | CVPR 2025 | Injects 3D shape information as specialized prompt tokens to improve geometry-aware image… | [📄 arXiv](https://arxiv.org/abs/2412.02912) |
| ⚪ **[SILMM: Self-Improving Large Multimodal Models for Compositional Text-to-Image Generation](https://arxiv.org/abs/2412.05818)** | CVPR 2025 | Uses scalable self-feedback and preference optimization to improve compositional… | [📄 arXiv](https://arxiv.org/abs/2412.05818) |
| ⚪ **[Type-R: Automatically Retouching Typos for Text-to-Image Generation](https://arxiv.org/abs/2411.18159)** | CVPR 2025 | A post-generation correction pipeline that detects, removes, and re-renders text regions… | [📄 arXiv](https://arxiv.org/abs/2411.18159) |

### [model-efficiency](model-efficiency.md) · 13

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| 🟢 **[iFSQ: Improving FSQ for Image Generation with 1 Line of Code](https://arxiv.org/abs/2601.17124)** | arXiv 2026 | A simple quantization improvement that makes FSQ stronger for high-quality image… | [📄 arXiv](https://arxiv.org/abs/2601.17124) · [💻 Code ★101](https://github.com/Tencent-Hunyuan/iFSQ) |
| ⚪ **[DAK-UCB: Diversity-Aware Prompt Routing for LLMs and Generative Models](https://arxiv.org/abs/2603.23140)** | arXiv 2026 | A routing strategy that allocates prompts across model choices to balance quality… | [📄 arXiv](https://arxiv.org/abs/2603.23140) |
| ⚪ **[Generative Modeling via Drifting](https://arxiv.org/abs/2602.04770)** | arXiv 2026 | Introduces drifting as a native one-step generative paradigm with strong ImageNet… | [📄 arXiv](https://arxiv.org/abs/2602.04770) |
| ⚪ **[RPiAE: A Representation-Pivoted Autoencoder Enhancing Both Image Generation and Editing](https://arxiv.org/abs/2603.19206)** | arXiv 2026 | A representation-centered autoencoder design that improves both latent generation quality… | [📄 arXiv](https://arxiv.org/abs/2603.19206) |
| ⚪ **[TMPDiff: Temporal Mixed-Precision for Diffusion Models](https://arxiv.org/abs/2603.14062)** | arXiv 2026 | A mixed-precision inference strategy that adapts numerical precision over denoising time… | [📄 arXiv](https://arxiv.org/abs/2603.14062) |
| ⚪ **[Warm-Start Flow Matching for Guaranteed Fast Text/Image Generation](https://arxiv.org/abs/2603.19360)** | arXiv 2026 | A warm-start flow-matching method that targets provably faster conditional generation for… | [📄 arXiv](https://arxiv.org/abs/2603.19360) |
| 🟢 **[Mean Flows for One-step Generative Modeling](https://arxiv.org/abs/2505.13447)** | NeurIPS 2025 | A self-contained one-step generative framework based on average velocity instead of… | [📄 arXiv](https://arxiv.org/abs/2505.13447) · [💻 Code ★599](https://github.com/Gsunshine/meanflow) |
| ⚪ **[Accelerating Auto-regressive Text-to-Image Generation with Training-free Speculative Jacobi Decoding](https://arxiv.org/abs/2410.01699)** | ICLR 2025 | A training-free parallel decoding algorithm for accelerating autoregressive image… | [📄 arXiv](https://arxiv.org/abs/2410.01699) |
| ⚪ **[Improved Mean Flows: On the Challenges of Fastforward Generative Models](https://arxiv.org/abs/2512.02012)** | arXiv 2025 | Revisits one-step mean-flow training and improves stability and conditional guidance… | [📄 arXiv](https://arxiv.org/abs/2512.02012) |
| ⚪ **[One-Way Ticket: Time-Independent Unified Encoder for Distilling Text-to-Image Diffusion Models](https://arxiv.org/abs/2505.21960)** | CVPR 2025 | A loop-free distilled design that shares encoder computation across denoising stages for… | [📄 arXiv](https://arxiv.org/abs/2505.21960) |
| ⚪ **[PT-T2I/V: An Efficient Proxy-Tokenized Diffusion Transformer for Text-to-Image/Video-Task](https://openreview.net/forum?id=lTrrnNdkOX)** | ICLR 2025 | Uses sparse proxy tokens to reduce redundant global attention in diffusion transformers… | [📄 OpenReview](https://openreview.net/forum?id=lTrrnNdkOX) |
| ⚪ **[Scaling Down Text Encoders of Text-to-Image Diffusion Models](https://arxiv.org/abs/2503.19897)** | CVPR 2025 | Shows that much smaller distilled text encoders can retain strong visual generation… | [📄 arXiv](https://arxiv.org/abs/2503.19897) |
| ⚪ **[SnapGen: Taming High-Resolution Text-to-Image Models for Mobile Devices with Efficient Architectures and Training](https://arxiv.org/abs/2412.09619)** | CVPR 2025 | A mobile-first T2I model that pushes 1024px generation to practical latency on edge… | [📄 arXiv](https://arxiv.org/abs/2412.09619) |

### [alignment-safety](alignment-safety.md) · 7

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[DTVI: Dual-Stage Textual and Visual Intervention for Safe Text-to-Image Generation](https://arxiv.org/abs/2603.22041)** | arXiv 2026 | A two-stage safeguard that intervenes on both prompt and visual generation pathways for… | [📄 arXiv](https://arxiv.org/abs/2603.22041) |
| ⚪ **[Self-Corrected Image Generation with Explainable Latent Rewards](https://arxiv.org/abs/2603.24965)** | arXiv 2026 | A reward-driven self-correction method that edits latent trajectories using interpretable… | [📄 arXiv](https://arxiv.org/abs/2603.24965) |
| 🟢 **[Improving Long-Text Alignment for Text-to-Image Diffusion Models](https://arxiv.org/abs/2410.11817)** | ICLR 2025 | A long-text encoding and decomposed preference-optimization framework for better… | [📄 arXiv](https://arxiv.org/abs/2410.11817) · [💻 Code ★83](https://github.com/luping-liu/LongAlign) |
| 🟢 **[Noise Diffusion for Enhancing Semantic Faithfulness in Text-to-Image Synthesis](https://arxiv.org/abs/2411.16503)** | CVPR 2025 | Optimizes the initial noisy latent with LVLM guidance to improve prompt-image semantic… | [📄 arXiv](https://arxiv.org/abs/2411.16503) · [💻 Code ★16](https://github.com/Bomingmiao/NoiseDiffusion) |
| 🟢 **[Information Theoretic Text-to-Image Alignment](https://arxiv.org/abs/2405.20759)** | ICLR 2025 | Improves T2I alignment by using mutual-information-based self-supervised fine-tuning… | [📄 arXiv](https://arxiv.org/abs/2405.20759) · [💻 Code ★6](https://github.com/Chao0511/mitune) |
| ⚪ **[Plug-and-Play Interpretable Responsible Text-to-Image Generation via Dual-Space Multi-facet Concept Control](https://arxiv.org/abs/2503.18324)** | CVPR 2025 | A plug-and-play responsible generation framework that jointly controls multiple safety… | [📄 arXiv](https://arxiv.org/abs/2503.18324) |
| ⚪ **[Text Embedding is Not All You Need: Attention Control for Text-to-Image Semantic Alignment with Text Self-Attention Maps](https://arxiv.org/abs/2411.15236)** | CVPR 2025 | Transfers syntactic relations from text self-attention to cross-attention to improve… | [📄 arXiv](https://arxiv.org/abs/2411.15236) |

### [personalization](personalization.md) · 4

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[MS-CustomNet: Controllable Multi-Subject Customization with Hierarchical Relational Semantics](https://arxiv.org/abs/2603.21136)** | arXiv 2026 | A multi-subject customization framework that explicitly models relational semantics among… | [📄 arXiv](https://arxiv.org/abs/2603.21136) |
| ⚪ **[PersonalQ: Select, Quantize, and Serve Personalized Diffusion Models for Efficient Inference](https://arxiv.org/abs/2603.22943)** | arXiv 2026 | A systems-oriented work on selecting and quantizing personalized diffusion checkpoints… | [📄 arXiv](https://arxiv.org/abs/2603.22943) |
| ⚪ **[Premier: Personalized Preference Modulation with Learnable User Embedding in Text-to-Image Generation](https://arxiv.org/abs/2603.20725)** | arXiv 2026 | Models user preference as a learnable embedding to steer T2I outputs toward individual… | [📄 arXiv](https://arxiv.org/abs/2603.20725) |
| ⚪ **[PaRa: Personalizing Text-to-Image Diffusion via Parameter Rank Reduction](https://arxiv.org/abs/2406.05641)** | ICLR 2025 | A rank-reduction personalization method that improves subject fidelity while preserving… | [📄 arXiv](https://arxiv.org/abs/2406.05641) |
