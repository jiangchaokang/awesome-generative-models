# 🖼️ Image 2D

> Final output is a single 2D image: text-to-image, controllable generation, safety, personalization, and efficient inference.

**Curated entries:** 56

[← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)

## Research Pattern

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

## Quick Navigation

[`text-to-image`](text-to-image.md) · [`controllable-generation`](controllable-generation.md) · [`model-efficiency`](model-efficiency.md) · [`alignment-safety`](alignment-safety.md) · [`personalization`](personalization.md)

## Selected Papers

### [Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation](https://arxiv.org/abs/2603.18627)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Uses agentic search over flow trajectories to improve spatial grounding for difficult compositional prompts.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.18627)

### [DAK-UCB: Diversity-Aware Prompt Routing for LLMs and Generative Models](https://arxiv.org/abs/2603.23140)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A routing strategy that allocates prompts across model choices to balance quality, diversity, and compute cost.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.23140)

### [DiffGraph: An Automated Agent-driven Model Merging Framework for In-the-Wild Text-to-Image Generation](https://arxiv.org/abs/2603.20470)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> An agentic model-merging system for assembling stronger in-the-wild T2I pipelines from community checkpoints.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.20470)

### [DTVI: Dual-Stage Textual and Visual Intervention for Safe Text-to-Image Generation](https://arxiv.org/abs/2603.22041)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: alignment-safety](https://img.shields.io/static/v1?label=Track&message=alignment-safety&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A two-stage safeguard that intervenes on both prompt and visual generation pathways for safer T2I outputs.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.22041)

## By Task

## [text-to-image](text-to-image.md)

**18 entries**

### [DiffGraph: An Automated Agent-driven Model Merging Framework for In-the-Wild Text-to-Image Generation](https://arxiv.org/abs/2603.20470)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> An agentic model-merging system for assembling stronger in-the-wild T2I pipelines from community checkpoints.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.20470)

### [LaDe: Unified Multi-Layered Graphic Media Generation and Decomposition](https://arxiv.org/abs/2603.17965)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A unified system for generating and decomposing layered editable graphic media rather than flat raster outputs only.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.17965)

### [SHARP: Spectrum-aware Highly-dynamic Adaptation for Resolution Promotion in Remote Sensing Synthesis](https://arxiv.org/abs/2603.21783)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A domain-oriented T2I adaptation framework targeting high-resolution remote-sensing synthesis with spectrum-aware tuning.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.21783)

### [UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation](https://arxiv.org/abs/2603.23500)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A policy-optimization view of reasoning-driven visual generation for stronger prompt following and planning.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.23500)

### [D-AR: Diffusion via Autoregressive Models](https://arxiv.org/abs/2505.23660)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Rewrites diffusion-style generation in an autoregressive form and studies the bridge between AR and diffusion paradigms.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2505.23660) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/showlab/D-AR)

### [Denoising Autoregressive Transformers for Scalable Text-to-Image Generation](https://openreview.net/forum?id=amDkNPVWcn)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> DART unifies autoregressive generation and denoising ideas for scalable image synthesis.

[![Paper: OpenReview](https://img.shields.io/static/v1?label=Paper&message=OpenReview&color=B31B1B&style=flat-square&labelColor=111827)](https://openreview.net/forum?id=amDkNPVWcn)

### [Fluid: Scaling Autoregressive Text-to-image Generative Models with Continuous Tokens](https://arxiv.org/abs/2410.13863)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A large-scale autoregressive T2I model built on continuous tokens and random-order generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2410.13863)

### [FLUX.1: Scalable Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206)

![Venue: arXiv 2024](https://img.shields.io/static/v1?label=Venue&message=arXiv+2024&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative) ![Legacy: Active since 2025](https://img.shields.io/static/v1?label=Legacy&message=Active+since+2025&color=F59E0B&style=flat-square&labelColor=111827)

> A highly influential rectified-flow image generator that remained one of the dominant open ecosystems throughout 2025.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2403.03206) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/black-forest-labs/flux)

_Scope note: Kept because the FLUX open ecosystem remained one of the most active image-generation backbones in 2025._

### [HunyuanImage 3.0 Technical Report](https://arxiv.org/abs/2509.23951)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative) ![Org: Tencent Hunyuan](https://img.shields.io/static/v1?label=Org&message=Tencent+Hunyuan&color=0064FF&style=flat-square&labelColor=111827&logo=tencentqq)

> HunyuanImage 3.0 is Tencent Hunyuan’s large native multimodal image model focused on strong text-image alignment, high visual quality, and industrial-scale text rendering.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2509.23951) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Tencent-Hunyuan/HunyuanImage-3.0)

### [Meissonic: Revitalizing Masked Generative Transformers for Efficient High-Resolution Text-to-Image Synthesis](https://arxiv.org/abs/2410.08261)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A masked generative transformer that closes much of the gap to diffusion while staying efficient at high resolution.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2410.08261)

### [One-Prompt-One-Story: Free-Lunch Consistent Text-to-Image Generation Using a Single Prompt](https://arxiv.org/abs/2501.13554)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A training-free method for identity-consistent image sequences by concatenating story prompts into one context.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2501.13554) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/byliutao/1Prompt1Story)

### [PixArt-Sigma: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation](https://arxiv.org/abs/2403.04692)

![Venue: ECCV 2024](https://img.shields.io/static/v1?label=Venue&message=ECCV+2024&color=2563EB&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative) ![Legacy: Active since 2025](https://img.shields.io/static/v1?label=Legacy&message=Active+since+2025&color=F59E0B&style=flat-square&labelColor=111827)

> An important open DiT baseline that continued to matter in 2025 as a widely reused high-resolution training recipe.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2403.04692) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/PixArt-alpha/PixArt-sigma)

_Scope note: Kept because PixArt-Sigma remained a strong open 4K DiT baseline actively reused in 2025._

### [Qwen-Image Technical Report](https://arxiv.org/abs/2508.02324)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative) ![Org: Alibaba](https://img.shields.io/static/v1?label=Org&message=Alibaba&color=FF6A00&style=flat-square&labelColor=111827&logo=alibabacloud)

> Qwen-Image is an open image-generation foundation model built for strong text rendering and high-consistency image editing, with a dual-encoding editing design on top of the Qwen stack.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2508.02324) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/QwenLM/Qwen-Image)

### [SANA 1.5: Efficient Scaling of Training-Time and Inference-Time Compute in Linear Diffusion Transformer](https://arxiv.org/abs/2501.18427)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A stronger SANA release focused on efficient scaling of both training-time and inference-time compute for high-resolution T2I.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2501.18427) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/NVlabs/Sana)

### [SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers](https://arxiv.org/abs/2410.10629)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A linear-attention DiT family that made high-resolution image generation substantially cheaper and faster.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2410.10629) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://nvlabs.github.io/Sana/)

### [Seedream 3.0 Technical Report](https://arxiv.org/abs/2504.11346)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827) ![Org: ByteDance Seed](https://img.shields.io/static/v1?label=Org&message=ByteDance+Seed&color=161823&style=flat-square&labelColor=111827&logo=bytedance)

> Seedream 3.0 is ByteDance Seed’s upgraded text-to-image system emphasizing typography, prompt following, and production-oriented image quality.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2504.11346) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://seed.bytedance.com/blog/seedream-3-0-%E6%96%87%E7%94%9F%E5%9B%BE%E6%A8%A1%E5%9E%8B%E6%8A%80%E6%9C%AF%E6%8A%A5%E5%91%8A%E5%8F%91%E5%B8%83)

### [Text-to-Image Rectified Flow as Plug-and-Play Priors](https://arxiv.org/abs/2406.03293)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Shows rectified-flow T2I models can act as plug-and-play priors beyond direct image synthesis.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2406.03293)

### [TIGeR: Unifying Text-to-Image Generation and Retrieval with Large Multimodal Models](https://arxiv.org/abs/2406.05814)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: text-to-image](https://img.shields.io/static/v1?label=Track&message=text-to-image&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Unifies generation and retrieval in a single multimodal model and lets the system choose the better response mode.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2406.05814)

## [controllable-generation](controllable-generation.md)

**14 entries**

### [Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation](https://arxiv.org/abs/2603.18627)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Uses agentic search over flow trajectories to improve spatial grounding for difficult compositional prompts.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.18627)

### [LGTM: Training-Free Light-Guided Text-to-Image Diffusion Model via Initial Noise Manipulation](https://arxiv.org/abs/2603.24086)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A training-free method that steers lighting effects by directly manipulating the initial diffusion noise.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.24086)

### [Relevance Feedback in Text-to-Image Diffusion: A Training-Free And Model-Agnostic Interactive Framework](https://arxiv.org/abs/2603.14936)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> An interactive relevance-feedback loop for refining generations without retraining the underlying diffusion model.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.14936)

### [SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation](https://arxiv.org/abs/2603.22228)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Introduces verifiable reward modeling for spatial relations to improve fine-grained layout consistency in T2I outputs.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.22228)

### [Compass Control: Multi Object Orientation Control for Text-to-Image Generation](https://arxiv.org/abs/2504.06752)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Introduces orientation-aware compass tokens for explicit multi-object pose control in text-to-image diffusion models.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2504.06752)

### [Focus-N-Fix: Region-Aware Fine-Tuning for Text-to-Image Generation](https://arxiv.org/abs/2501.06481)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A localized fine-tuning method that corrects only problematic regions while preserving the rest of the image behavior.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2501.06481)

### [Generative Photography: Scene-Consistent Camera Control for Realistic Text-to-Image Synthesis](https://arxiv.org/abs/2412.02168)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A physically grounded camera-control framework for scene-consistent changes in focal length and viewpoint during image synthesis.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2412.02168)

### [Make It Count: Text-to-Image Generation with an Accurate Number of Objects](https://arxiv.org/abs/2406.10210)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Targets count fidelity by detecting over- and under-generation during denoising and correcting missing instances.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2406.10210)

### [MCCD: Multi-Agent Collaboration-based Compositional Diffusion for Complex Text-to-Image Generation](https://arxiv.org/abs/2505.02648)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A training-free multi-agent prompting and regional refinement framework for complex compositional image generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2505.02648)

### [PreciseCam: Precise Camera Control for Text-to-Image Generation](https://arxiv.org/abs/2501.12910)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A camera-conditioned generation method that gives explicit control over extrinsics and intrinsics instead of relying on prompt hacks.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2501.12910) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://graphics.unizar.es/projects/PreciseCam2024)

### [Progressive Compositionality in Text-to-Image Generative Models](https://arxiv.org/abs/2410.16719)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Builds a hard-negative curriculum and contrastive learning pipeline to improve compositional reasoning in T2I models.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2410.16719)

### [ShapeWords: Guiding Text-to-Image Synthesis with 3D Shape-Aware Prompts](https://arxiv.org/abs/2412.02912)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Injects 3D shape information as specialized prompt tokens to improve geometry-aware image generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2412.02912)

### [SILMM: Self-Improving Large Multimodal Models for Compositional Text-to-Image Generation](https://arxiv.org/abs/2412.05818)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Uses scalable self-feedback and preference optimization to improve compositional text-image alignment in large multimodal models.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2412.05818)

### [Type-R: Automatically Retouching Typos for Text-to-Image Generation](https://arxiv.org/abs/2411.18159)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: controllable-generation](https://img.shields.io/static/v1?label=Track&message=controllable-generation&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A post-generation correction pipeline that detects, removes, and re-renders text regions to improve text spelling in generated images.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2411.18159)

## [model-efficiency](model-efficiency.md)

**13 entries**

### [DAK-UCB: Diversity-Aware Prompt Routing for LLMs and Generative Models](https://arxiv.org/abs/2603.23140)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A routing strategy that allocates prompts across model choices to balance quality, diversity, and compute cost.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.23140)

### [Generative Modeling via Drifting](https://arxiv.org/abs/2602.04770)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Introduces drifting as a native one-step generative paradigm with strong ImageNet performance in latent space.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.04770)

### [iFSQ: Improving FSQ for Image Generation with 1 Line of Code](https://arxiv.org/abs/2601.17124)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A simple quantization improvement that makes FSQ stronger for high-quality image generation with minimal code changes.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2601.17124) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Tencent-Hunyuan/iFSQ)

### [RPiAE: A Representation-Pivoted Autoencoder Enhancing Both Image Generation and Editing](https://arxiv.org/abs/2603.19206)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A representation-centered autoencoder design that improves both latent generation quality and editing robustness.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.19206)

### [TMPDiff: Temporal Mixed-Precision for Diffusion Models](https://arxiv.org/abs/2603.14062)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A mixed-precision inference strategy that adapts numerical precision over denoising time to reduce diffusion cost.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.14062)

### [Warm-Start Flow Matching for Guaranteed Fast Text/Image Generation](https://arxiv.org/abs/2603.19360)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A warm-start flow-matching method that targets provably faster conditional generation for text and image models.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.19360)

### [Accelerating Auto-regressive Text-to-Image Generation with Training-free Speculative Jacobi Decoding](https://arxiv.org/abs/2410.01699)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A training-free parallel decoding algorithm for accelerating autoregressive image generation without sacrificing diversity.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2410.01699)

### [Improved Mean Flows: On the Challenges of Fastforward Generative Models](https://arxiv.org/abs/2512.02012)

![Venue: arXiv 2025](https://img.shields.io/static/v1?label=Venue&message=arXiv+2025&color=B31B1B&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Revisits one-step mean-flow training and improves stability and conditional guidance quality for fast generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2512.02012)

### [Mean Flows for One-step Generative Modeling](https://arxiv.org/abs/2505.13447)

![Venue: NeurIPS 2025](https://img.shields.io/static/v1?label=Venue&message=NeurIPS+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A self-contained one-step generative framework based on average velocity instead of standard flow matching.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2505.13447) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Gsunshine/meanflow)

### [One-Way Ticket: Time-Independent Unified Encoder for Distilling Text-to-Image Diffusion Models](https://arxiv.org/abs/2505.21960)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A loop-free distilled design that shares encoder computation across denoising stages for faster T2I generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2505.21960)

### [PT-T2I/V: An Efficient Proxy-Tokenized Diffusion Transformer for Text-to-Image/Video-Task](https://openreview.net/forum?id=lTrrnNdkOX)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Uses sparse proxy tokens to reduce redundant global attention in diffusion transformers for image and video generation.

[![Paper: OpenReview](https://img.shields.io/static/v1?label=Paper&message=OpenReview&color=B31B1B&style=flat-square&labelColor=111827)](https://openreview.net/forum?id=lTrrnNdkOX)

### [Scaling Down Text Encoders of Text-to-Image Diffusion Models](https://arxiv.org/abs/2503.19897)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Shows that much smaller distilled text encoders can retain strong visual generation quality in large T2I systems.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2503.19897)

### [SnapGen: Taming High-Resolution Text-to-Image Models for Mobile Devices with Efficient Architectures and Training](https://arxiv.org/abs/2412.09619)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: model-efficiency](https://img.shields.io/static/v1?label=Track&message=model-efficiency&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A mobile-first T2I model that pushes 1024px generation to practical latency on edge hardware.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2412.09619)

## [alignment-safety](alignment-safety.md)

**7 entries**

### [DTVI: Dual-Stage Textual and Visual Intervention for Safe Text-to-Image Generation](https://arxiv.org/abs/2603.22041)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: alignment-safety](https://img.shields.io/static/v1?label=Track&message=alignment-safety&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A two-stage safeguard that intervenes on both prompt and visual generation pathways for safer T2I outputs.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.22041)

### [Self-Corrected Image Generation with Explainable Latent Rewards](https://arxiv.org/abs/2603.24965)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: alignment-safety](https://img.shields.io/static/v1?label=Track&message=alignment-safety&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A reward-driven self-correction method that edits latent trajectories using interpretable feedback signals.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.24965)

### [Improving Long-Text Alignment for Text-to-Image Diffusion Models](https://arxiv.org/abs/2410.11817)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: alignment-safety](https://img.shields.io/static/v1?label=Track&message=alignment-safety&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> A long-text encoding and decomposed preference-optimization framework for better alignment to lengthy prompts.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2410.11817) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/luping-liu/LongAlign)

### [Information Theoretic Text-to-Image Alignment](https://arxiv.org/abs/2405.20759)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: alignment-safety](https://img.shields.io/static/v1?label=Track&message=alignment-safety&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Improves T2I alignment by using mutual-information-based self-supervised fine-tuning without extra annotation pipelines.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2405.20759) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Chao0511/mitune)

### [Noise Diffusion for Enhancing Semantic Faithfulness in Text-to-Image Synthesis](https://arxiv.org/abs/2411.16503)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: alignment-safety](https://img.shields.io/static/v1?label=Track&message=alignment-safety&color=2563EB&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Optimizes the initial noisy latent with LVLM guidance to improve prompt-image semantic fidelity across diffusion models.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2411.16503) [![Code: GitHub](https://img.shields.io/static/v1?label=Code&message=GitHub&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Bomingmiao/NoiseDiffusion)

### [Plug-and-Play Interpretable Responsible Text-to-Image Generation via Dual-Space Multi-facet Concept Control](https://arxiv.org/abs/2503.18324)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: alignment-safety](https://img.shields.io/static/v1?label=Track&message=alignment-safety&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A plug-and-play responsible generation framework that jointly controls multiple safety and fairness facets with interpretable mechanisms.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2503.18324)

### [Text Embedding is Not All You Need: Attention Control for Text-to-Image Semantic Alignment with Text Self-Attention Maps](https://arxiv.org/abs/2411.15236)

![Venue: CVPR 2025](https://img.shields.io/static/v1?label=Venue&message=CVPR+2025&color=2563EB&style=flat-square&labelColor=111827) ![Track: alignment-safety](https://img.shields.io/static/v1?label=Track&message=alignment-safety&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Transfers syntactic relations from text self-attention to cross-attention to improve semantic binding and prompt faithfulness.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2411.15236)

## [personalization](personalization.md)

**4 entries**

### [MS-CustomNet: Controllable Multi-Subject Customization with Hierarchical Relational Semantics](https://arxiv.org/abs/2603.21136)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: personalization](https://img.shields.io/static/v1?label=Track&message=personalization&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A multi-subject customization framework that explicitly models relational semantics among personalized subjects.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.21136)

### [PersonalQ: Select, Quantize, and Serve Personalized Diffusion Models for Efficient Inference](https://arxiv.org/abs/2603.22943)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: personalization](https://img.shields.io/static/v1?label=Track&message=personalization&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A systems-oriented work on selecting and quantizing personalized diffusion checkpoints for practical serving.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.22943)

### [Premier: Personalized Preference Modulation with Learnable User Embedding in Text-to-Image Generation](https://arxiv.org/abs/2603.20725)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: personalization](https://img.shields.io/static/v1?label=Track&message=personalization&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> Models user preference as a learnable embedding to steer T2I outputs toward individual taste.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.20725)

### [PaRa: Personalizing Text-to-Image Diffusion via Parameter Rank Reduction](https://arxiv.org/abs/2406.05641)

![Venue: ICLR 2025](https://img.shields.io/static/v1?label=Venue&message=ICLR+2025&color=7C3AED&style=flat-square&labelColor=111827) ![Track: personalization](https://img.shields.io/static/v1?label=Track&message=personalization&color=2563EB&style=flat-square&labelColor=111827) ![Source: Closed](https://img.shields.io/static/v1?label=Source&message=Closed&color=6B7280&style=flat-square&labelColor=111827)

> A rank-reduction personalization method that improves subject fidelity while preserving editability and parameter efficiency.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2406.05641)

## Compact Index

<details>
<summary><b>Open compact index</b></summary>

| Title | Task | Venue | Links |
|:--|:--|:--|:--|
| **[Agentic Flow Steering and Parallel Rollout Search for Spatially Grounded Text-to-Image Generation](https://arxiv.org/abs/2603.18627)** | controllable-generation | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.18627) |
| **[DAK-UCB: Diversity-Aware Prompt Routing for LLMs and Generative Models](https://arxiv.org/abs/2603.23140)** | model-efficiency | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.23140) |
| **[DiffGraph: An Automated Agent-driven Model Merging Framework for In-the-Wild Text-to-Image Generation](https://arxiv.org/abs/2603.20470)** | text-to-image | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.20470) |
| **[DTVI: Dual-Stage Textual and Visual Intervention for Safe Text-to-Image Generation](https://arxiv.org/abs/2603.22041)** | alignment-safety | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.22041) |
| **[Generative Modeling via Drifting](https://arxiv.org/abs/2602.04770)** | model-efficiency | arXiv 2026 | [Paper](https://arxiv.org/abs/2602.04770) |
| **[iFSQ: Improving FSQ for Image Generation with 1 Line of Code](https://arxiv.org/abs/2601.17124)** | model-efficiency | arXiv 2026 | [Paper](https://arxiv.org/abs/2601.17124) / [Code](https://github.com/Tencent-Hunyuan/iFSQ) |
| **[LaDe: Unified Multi-Layered Graphic Media Generation and Decomposition](https://arxiv.org/abs/2603.17965)** | text-to-image | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.17965) |
| **[LGTM: Training-Free Light-Guided Text-to-Image Diffusion Model via Initial Noise Manipulation](https://arxiv.org/abs/2603.24086)** | controllable-generation | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.24086) |
| **[MS-CustomNet: Controllable Multi-Subject Customization with Hierarchical Relational Semantics](https://arxiv.org/abs/2603.21136)** | personalization | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.21136) |
| **[PersonalQ: Select, Quantize, and Serve Personalized Diffusion Models for Efficient Inference](https://arxiv.org/abs/2603.22943)** | personalization | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.22943) |
| **[Premier: Personalized Preference Modulation with Learnable User Embedding in Text-to-Image Generation](https://arxiv.org/abs/2603.20725)** | personalization | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.20725) |
| **[Relevance Feedback in Text-to-Image Diffusion: A Training-Free And Model-Agnostic Interactive Framework](https://arxiv.org/abs/2603.14936)** | controllable-generation | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.14936) |
| **[RPiAE: A Representation-Pivoted Autoencoder Enhancing Both Image Generation and Editing](https://arxiv.org/abs/2603.19206)** | model-efficiency | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.19206) |
| **[Self-Corrected Image Generation with Explainable Latent Rewards](https://arxiv.org/abs/2603.24965)** | alignment-safety | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.24965) |
| **[SHARP: Spectrum-aware Highly-dynamic Adaptation for Resolution Promotion in Remote Sensing Synthesis](https://arxiv.org/abs/2603.21783)** | text-to-image | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.21783) |
| **[SpatialReward: Verifiable Spatial Reward Modeling for Fine-Grained Spatial Consistency in Text-to-Image Generation](https://arxiv.org/abs/2603.22228)** | controllable-generation | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.22228) |
| **[TMPDiff: Temporal Mixed-Precision for Diffusion Models](https://arxiv.org/abs/2603.14062)** | model-efficiency | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.14062) |
| **[UniGRPO: Unified Policy Optimization for Reasoning-Driven Visual Generation](https://arxiv.org/abs/2603.23500)** | text-to-image | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.23500) |
| **[Warm-Start Flow Matching for Guaranteed Fast Text/Image Generation](https://arxiv.org/abs/2603.19360)** | model-efficiency | arXiv 2026 | [Paper](https://arxiv.org/abs/2603.19360) |
| **[Accelerating Auto-regressive Text-to-Image Generation with Training-free Speculative Jacobi Decoding](https://arxiv.org/abs/2410.01699)** | model-efficiency | ICLR 2025 | [Paper](https://arxiv.org/abs/2410.01699) |
| **[Compass Control: Multi Object Orientation Control for Text-to-Image Generation](https://arxiv.org/abs/2504.06752)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2504.06752) |
| **[D-AR: Diffusion via Autoregressive Models](https://arxiv.org/abs/2505.23660)** | text-to-image | arXiv 2025 | [Paper](https://arxiv.org/abs/2505.23660) / [Code](https://github.com/showlab/D-AR) |
| **[Denoising Autoregressive Transformers for Scalable Text-to-Image Generation](https://openreview.net/forum?id=amDkNPVWcn)** | text-to-image | ICLR 2025 | [Paper](https://openreview.net/forum?id=amDkNPVWcn) |
| **[Fluid: Scaling Autoregressive Text-to-image Generative Models with Continuous Tokens](https://arxiv.org/abs/2410.13863)** | text-to-image | ICLR 2025 | [Paper](https://arxiv.org/abs/2410.13863) |
| **[FLUX.1: Scalable Rectified Flow Transformers for High-Resolution Image Synthesis](https://arxiv.org/abs/2403.03206)** | text-to-image | arXiv 2024 | [Paper](https://arxiv.org/abs/2403.03206) / [Code](https://github.com/black-forest-labs/flux) |
| **[Focus-N-Fix: Region-Aware Fine-Tuning for Text-to-Image Generation](https://arxiv.org/abs/2501.06481)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2501.06481) |
| **[Generative Photography: Scene-Consistent Camera Control for Realistic Text-to-Image Synthesis](https://arxiv.org/abs/2412.02168)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2412.02168) |
| **[HunyuanImage 3.0 Technical Report](https://arxiv.org/abs/2509.23951)** | text-to-image | arXiv 2025 | [Paper](https://arxiv.org/abs/2509.23951) / [Code](https://github.com/Tencent-Hunyuan/HunyuanImage-3.0) |
| **[Improved Mean Flows: On the Challenges of Fastforward Generative Models](https://arxiv.org/abs/2512.02012)** | model-efficiency | arXiv 2025 | [Paper](https://arxiv.org/abs/2512.02012) |
| **[Improving Long-Text Alignment for Text-to-Image Diffusion Models](https://arxiv.org/abs/2410.11817)** | alignment-safety | ICLR 2025 | [Paper](https://arxiv.org/abs/2410.11817) / [Code](https://github.com/luping-liu/LongAlign) |
| **[Information Theoretic Text-to-Image Alignment](https://arxiv.org/abs/2405.20759)** | alignment-safety | ICLR 2025 | [Paper](https://arxiv.org/abs/2405.20759) / [Code](https://github.com/Chao0511/mitune) |
| **[Make It Count: Text-to-Image Generation with an Accurate Number of Objects](https://arxiv.org/abs/2406.10210)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2406.10210) |
| **[MCCD: Multi-Agent Collaboration-based Compositional Diffusion for Complex Text-to-Image Generation](https://arxiv.org/abs/2505.02648)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2505.02648) |
| **[Mean Flows for One-step Generative Modeling](https://arxiv.org/abs/2505.13447)** | model-efficiency | NeurIPS 2025 | [Paper](https://arxiv.org/abs/2505.13447) / [Code](https://github.com/Gsunshine/meanflow) |
| **[Meissonic: Revitalizing Masked Generative Transformers for Efficient High-Resolution Text-to-Image Synthesis](https://arxiv.org/abs/2410.08261)** | text-to-image | ICLR 2025 | [Paper](https://arxiv.org/abs/2410.08261) |
| **[Noise Diffusion for Enhancing Semantic Faithfulness in Text-to-Image Synthesis](https://arxiv.org/abs/2411.16503)** | alignment-safety | CVPR 2025 | [Paper](https://arxiv.org/abs/2411.16503) / [Code](https://github.com/Bomingmiao/NoiseDiffusion) |
| **[One-Prompt-One-Story: Free-Lunch Consistent Text-to-Image Generation Using a Single Prompt](https://arxiv.org/abs/2501.13554)** | text-to-image | ICLR 2025 | [Paper](https://arxiv.org/abs/2501.13554) / [Code](https://github.com/byliutao/1Prompt1Story) |
| **[One-Way Ticket: Time-Independent Unified Encoder for Distilling Text-to-Image Diffusion Models](https://arxiv.org/abs/2505.21960)** | model-efficiency | CVPR 2025 | [Paper](https://arxiv.org/abs/2505.21960) |
| **[PaRa: Personalizing Text-to-Image Diffusion via Parameter Rank Reduction](https://arxiv.org/abs/2406.05641)** | personalization | ICLR 2025 | [Paper](https://arxiv.org/abs/2406.05641) |
| **[PixArt-Sigma: Weak-to-Strong Training of Diffusion Transformer for 4K Text-to-Image Generation](https://arxiv.org/abs/2403.04692)** | text-to-image | ECCV 2024 | [Paper](https://arxiv.org/abs/2403.04692) / [Code](https://github.com/PixArt-alpha/PixArt-sigma) |
| **[Plug-and-Play Interpretable Responsible Text-to-Image Generation via Dual-Space Multi-facet Concept Control](https://arxiv.org/abs/2503.18324)** | alignment-safety | CVPR 2025 | [Paper](https://arxiv.org/abs/2503.18324) |
| **[PreciseCam: Precise Camera Control for Text-to-Image Generation](https://arxiv.org/abs/2501.12910)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2501.12910) / [Project](https://graphics.unizar.es/projects/PreciseCam2024) |
| **[Progressive Compositionality in Text-to-Image Generative Models](https://arxiv.org/abs/2410.16719)** | controllable-generation | ICLR 2025 | [Paper](https://arxiv.org/abs/2410.16719) |
| **[PT-T2I/V: An Efficient Proxy-Tokenized Diffusion Transformer for Text-to-Image/Video-Task](https://openreview.net/forum?id=lTrrnNdkOX)** | model-efficiency | ICLR 2025 | [Paper](https://openreview.net/forum?id=lTrrnNdkOX) |
| **[Qwen-Image Technical Report](https://arxiv.org/abs/2508.02324)** | text-to-image | arXiv 2025 | [Paper](https://arxiv.org/abs/2508.02324) / [Code](https://github.com/QwenLM/Qwen-Image) |
| **[SANA 1.5: Efficient Scaling of Training-Time and Inference-Time Compute in Linear Diffusion Transformer](https://arxiv.org/abs/2501.18427)** | text-to-image | arXiv 2025 | [Paper](https://arxiv.org/abs/2501.18427) / [Code](https://github.com/NVlabs/Sana) |
| **[SANA: Efficient High-Resolution Image Synthesis with Linear Diffusion Transformers](https://arxiv.org/abs/2410.10629)** | text-to-image | ICLR 2025 | [Paper](https://arxiv.org/abs/2410.10629) / [Project](https://nvlabs.github.io/Sana/) |
| **[Scaling Down Text Encoders of Text-to-Image Diffusion Models](https://arxiv.org/abs/2503.19897)** | model-efficiency | CVPR 2025 | [Paper](https://arxiv.org/abs/2503.19897) |
| **[Seedream 3.0 Technical Report](https://arxiv.org/abs/2504.11346)** | text-to-image | arXiv 2025 | [Paper](https://arxiv.org/abs/2504.11346) / [Project](https://seed.bytedance.com/blog/seedream-3-0-%E6%96%87%E7%94%9F%E5%9B%BE%E6%A8%A1%E5%9E%8B%E6%8A%80%E6%9C%AF%E6%8A%A5%E5%91%8A%E5%8F%91%E5%B8%83) |
| **[ShapeWords: Guiding Text-to-Image Synthesis with 3D Shape-Aware Prompts](https://arxiv.org/abs/2412.02912)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2412.02912) |
| **[SILMM: Self-Improving Large Multimodal Models for Compositional Text-to-Image Generation](https://arxiv.org/abs/2412.05818)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2412.05818) |
| **[SnapGen: Taming High-Resolution Text-to-Image Models for Mobile Devices with Efficient Architectures and Training](https://arxiv.org/abs/2412.09619)** | model-efficiency | CVPR 2025 | [Paper](https://arxiv.org/abs/2412.09619) |
| **[Text Embedding is Not All You Need: Attention Control for Text-to-Image Semantic Alignment with Text Self-Attention Maps](https://arxiv.org/abs/2411.15236)** | alignment-safety | CVPR 2025 | [Paper](https://arxiv.org/abs/2411.15236) |
| **[Text-to-Image Rectified Flow as Plug-and-Play Priors](https://arxiv.org/abs/2406.03293)** | text-to-image | ICLR 2025 | [Paper](https://arxiv.org/abs/2406.03293) |
| **[TIGeR: Unifying Text-to-Image Generation and Retrieval with Large Multimodal Models](https://arxiv.org/abs/2406.05814)** | text-to-image | ICLR 2025 | [Paper](https://arxiv.org/abs/2406.05814) |
| **[Type-R: Automatically Retouching Typos for Text-to-Image Generation](https://arxiv.org/abs/2411.18159)** | controllable-generation | CVPR 2025 | [Paper](https://arxiv.org/abs/2411.18159) |

</details>
