# 🧊 3D Object / Asset

> Reusable 3D objects, assets, avatars, articulated assets, and part-aware generation.

**40 curated papers** · [← Root](../README.md) · [Taxonomy](../docs/taxonomy.md) · [Candidate Inbox](../metadata/candidates/latest.md)

<details>
<summary><b>📐 How this pipeline works</b></summary>

```text
Text / image / multiview / structure prior
        ↓
Asset encoder + 3D latent generator
        ↓
Geometry head (mesh / point / triplane / octree)
        ↓
Texture / material / articulation head
        ↓
Reusable 3D object / asset / avatar
```

</details>

## Tasks in this category

[3d-shape-generation](3d-shape-generation.md) <sub>(19)</sub> · [image-to-3d](image-to-3d.md) <sub>(7)</sub> · [text-to-3d](text-to-3d.md) <sub>(3)</sub> · [part-aware-generation](part-aware-generation.md) <sub>(6)</sub> · [articulated-asset](articulated-asset.md) <sub>(4)</sub> · [human-avatar](human-avatar.md) <sub>(1)</sub>

## 🌟 Spotlight

#### 🌟 [AssetFormer: Modular 3D Assets Generation with Autoregressive Transformer](https://arxiv.org/abs/2602.12100)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: text-to-3d](https://img.shields.io/static/v1?label=Track&message=text-to-3d&color=0D9488&style=flat-square&labelColor=111827) ![Source: Open](https://img.shields.io/static/v1?label=Source&message=Open&color=16A34A&style=flat-square&labelColor=111827&logo=opensourceinitiative)

> Targets modular assets directly with autoregressive generation over part-aware structures.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.12100) [![Code: GitHub ★ 37](https://img.shields.io/static/v1?label=Code&message=GitHub+%E2%98%85+37&color=181717&style=flat-square&labelColor=111827&logo=github)](https://github.com/Advocate99/AssetFormer)

#### 🌟 [DreamPartGen: Semantically Grounded Part-Level 3D Generation via Collaborative Latent Denoising](https://arxiv.org/abs/2603.19216)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: part-aware-generation](https://img.shields.io/static/v1?label=Track&message=part-aware-generation&color=0D9488&style=flat-square&labelColor=111827)

> A collaborative latent-denoising framework for semantically grounded part-level 3D object generation.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2603.19216)

#### 🌟 [Fuse3D: Generating 3D Assets Controlled by Multi-Image Fusion](https://arxiv.org/abs/2602.17040)

![Venue: arXiv 2026](https://img.shields.io/static/v1?label=Venue&message=arXiv+2026&color=B31B1B&style=flat-square&labelColor=111827) ![Track: image-to-3d](https://img.shields.io/static/v1?label=Track&message=image-to-3d&color=0D9488&style=flat-square&labelColor=111827)

> A multi-image control framework for generating one fused 3D asset with region-level guidance.

[![Paper: arXiv](https://img.shields.io/static/v1?label=Paper&message=arXiv&color=B31B1B&style=flat-square&labelColor=111827&logo=arxiv)](https://arxiv.org/abs/2602.17040) [![Project: Site](https://img.shields.io/static/v1?label=Project&message=Site&color=0EA5E9&style=flat-square&labelColor=111827&logo=googlechrome)](https://jinnmnm.github.io/Fuse3d.github.io/)

## Full Catalog

**Legend:** 🟢 code publicly available · ⚪ code not (yet) public · ★ live GitHub stars (refreshed weekly)

### [3d-shape-generation](3d-shape-generation.md) · 19

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[SLAT-Phys: Fast Material Property Field Prediction from Structured 3D Latents](https://arxiv.org/abs/2603.23973)** | arXiv 2026 | Extends structured 3D latents from geometry toward material-property prediction for… | [📄 arXiv](https://arxiv.org/abs/2603.23973) |
| 🟢 **[Hunyuan3D 2.0: Scaling Diffusion Models for High Resolution Textured 3D Assets Generation](https://arxiv.org/abs/2501.12202)** | arXiv 2025 | A strong open 3D asset system combining large-scale shape generation and texture… | [📄 arXiv](https://arxiv.org/abs/2501.12202) · [💻 Code ★14.3k](https://github.com/Tencent-Hunyuan/Hunyuan3D-2) |
| 🟢 **[TRELLIS: Structured 3D Latents for Scalable and Versatile 3D Generation](https://arxiv.org/abs/2412.01506)** | CVPR 2025 | A large-scale unified latent representation for text- and image-conditioned 3D asset… | [📄 arXiv](https://arxiv.org/abs/2412.01506) · [💻 Code ★13.2k](https://github.com/microsoft/TRELLIS) · [🌐 Project](https://microsoft.github.io/TRELLIS/) |
| 🟢 **[Sparc3D: Sparse Representation and Construction for High-Resolution 3D Shapes Modeling](https://arxiv.org/abs/2505.14521)** | NeurIPS 2025 | A sparse deformable marching-cubes representation plus sparse-conv VAE for near-lossless… | [📄 arXiv](https://arxiv.org/abs/2505.14521) · [💻 Code ★1.3k](https://github.com/lizhihao6/Sparc3D) · [🌐 Project](https://lizhihao6.github.io/Sparc3D) |
| 🟢 **[Unleashing Vecset Diffusion Model for Fast Shape Generation](https://arxiv.org/abs/2503.16302)** | ICCV 2025 | FlashVDM introduces progressive flow distillation and engineering optimizations to cut… | [📄 arXiv](https://arxiv.org/abs/2503.16302) · [💻 Code ★332](https://github.com/Tencent-Hunyuan/FlashVDM) |
| 🟢 **[OctFusion: Octree-based Diffusion Models for 3D Shape Generation](https://arxiv.org/abs/2408.14732)** | SGP 2025 | An octree latent representation plus unified multi-scale diffusion model for fast… | [📄 arXiv](https://arxiv.org/abs/2408.14732) · [💻 Code ★231](https://github.com/octree-nn/octfusion) |
| 🟢 **[TopoDiT-3D: Topology-Aware Diffusion Transformer with Bottleneck Structure for 3D Point Cloud Generation](https://arxiv.org/abs/2505.09140)** | arXiv 2025 | Injects persistent-homology topology cues into diffusion transformers for better… | [📄 arXiv](https://arxiv.org/abs/2505.09140) · [💻 Code ★15](https://github.com/Zechao-Guan/TopoDiT-3D) |
| ⚪ **[3D Point Cloud Generation via Autoregressive Up-sampling](https://arxiv.org/abs/2503.08594)** | arXiv 2025 | Treats point-cloud generation as progressive next-scale up-sampling rather than… | [📄 arXiv](https://arxiv.org/abs/2503.08594) |
| ⚪ **[EAGLE: Contextual Point Cloud Generation via Adaptive Continuous Normalizing Flow with Self-Attention](https://arxiv.org/abs/2503.13479)** | arXiv 2025 | A flow-based point-cloud generator that augments continuous normalizing flows with global… | [📄 arXiv](https://arxiv.org/abs/2503.13479) |
| ⚪ **[Hunyuan3D 2.5: Towards High-Fidelity 3D Assets Generation with Ultimate Details](https://arxiv.org/abs/2506.16504)** | arXiv 2025 | A 2.5-generation upgrade emphasizing finer geometry, stronger textures, and better asset… | [📄 arXiv](https://arxiv.org/abs/2506.16504) |
| ⚪ **[LaGeM: A Large Geometry Model for 3D Representation Learning and Diffusion](https://arxiv.org/abs/2410.01295)** | ICLR 2025 | A hierarchical geometry autoencoder and cascaded diffusion pipeline for scalable… | [📄 arXiv](https://arxiv.org/abs/2410.01295) |
| ⚪ **[LATTICE: Democratize High-Fidelity 3D Generation at Scale](https://arxiv.org/abs/2512.03052)** | arXiv 2025 | A scalable two-stage 3D asset generator built on structured voxel-set latents and… | [📄 arXiv](https://arxiv.org/abs/2512.03052) |
| ⚪ **[Not-So-Optimal Transport Flows for 3D Point Cloud Generation](https://arxiv.org/abs/2502.12456)** | arXiv 2025 | An approximate-OT flow model designed to scale better and train more easily on large… | [📄 arXiv](https://arxiv.org/abs/2502.12456) |
| ⚪ **[OctGPT: Octree-based Multiscale Autoregressive Models for 3D Shape Generation](https://arxiv.org/abs/2504.09975)** | SIGGRAPH 2025 | A multiscale octree autoregressive model that makes high-resolution 3D generation far… | [📄 arXiv](https://arxiv.org/abs/2504.09975) |
| ⚪ **[SparseFlex: High-Resolution and Arbitrary-Topology 3D Shape Modeling](https://arxiv.org/abs/2503.21732)** | arXiv 2025 | A sparse-structured differentiable mesh representation that supports arbitrary topology… | [📄 arXiv](https://arxiv.org/abs/2503.21732) |
| ⚪ **[Squeeze3D: Your 3D Generation Model is Secretly an Extreme Neural Compressor](https://arxiv.org/abs/2506.07932)** | arXiv 2025 | Repurposes pretrained 3D generators as powerful implicit compressors for meshes, point… | [📄 arXiv](https://arxiv.org/abs/2506.07932) |
| ⚪ **[Ultra3D: Efficient and High-Fidelity 3D Generation with Part Attention](https://arxiv.org/abs/2507.17745)** | arXiv 2025 | Introduces geometry-aware part attention for faster high-resolution 3D generation without… | [📄 arXiv](https://arxiv.org/abs/2507.17745) |
| ⚪ **[UltraShape 1.0: High-Fidelity 3D Shape Generation via Scalable Geometric Refinement](https://arxiv.org/abs/2512.21185)** | arXiv 2025 | A two-stage geometry generation pipeline emphasizing high-resolution local refinement and… | [📄 arXiv](https://arxiv.org/abs/2512.21185) |
| ⚪ **[UniLat3D: Geometry-Appearance Unified Latents for Single-Stage 3D Generation](https://arxiv.org/abs/2509.25079)** | arXiv 2025 | Unifies geometry and appearance in one latent space so 3D assets can be generated in a… | [📄 arXiv](https://arxiv.org/abs/2509.25079) |

### [image-to-3d](image-to-3d.md) · 7

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[Fuse3D: Generating 3D Assets Controlled by Multi-Image Fusion](https://arxiv.org/abs/2602.17040)** | arXiv 2026 | A multi-image control framework for generating one fused 3D asset with region-level… | [📄 arXiv](https://arxiv.org/abs/2602.17040) · [🌐 Project](https://jinnmnm.github.io/Fuse3d.github.io/) |
| 🟢 **[TripoSR: Fast 3D Object Reconstruction from a Single Image](https://arxiv.org/abs/2403.02151)** | arXiv 2024 · since 2025 | A fast feed-forward single-image 3D reconstruction model that remained actively used in… | [📄 arXiv](https://arxiv.org/abs/2403.02151) · [💻 Code ★6.7k](https://github.com/VAST-AI-Research/TripoSR) |
| 🟢 **[InstantMesh: Efficient 3D Mesh Generation from a Single Image with Sparse-view Large Reconstruction Models](https://arxiv.org/abs/2404.07191)** | arXiv 2024 · since 2025 | A highly practical single-image mesh generator that continued to be heavily used in 2025… | [📄 arXiv](https://arxiv.org/abs/2404.07191) · [💻 Code ★4.5k](https://github.com/TencentARC/InstantMesh) |
| 🟢 **[Hunyuan3D 2.1: From Images to High-Fidelity 3D Assets with Production-Ready PBR Material](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1)** | Technical Report 2025 | Hunyuan3D 2.1 upgrades the Hunyuan 3D asset stack with production-ready PBR material… | [💻 Code ★3.7k](https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1) |
| 🟢 **[Unique3D: High-Quality and Efficient 3D Mesh Generation from a Single Image](https://arxiv.org/abs/2405.20343)** | arXiv 2024 · since 2025 | A strong multi-level diffusion image-to-3D mesh baseline that stayed active in 2025 open… | [📄 arXiv](https://arxiv.org/abs/2405.20343) · [💻 Code ★3.6k](https://github.com/AiuniAI/Unique3D) |
| 🟢 **[Era3D: High-Resolution Multiview Diffusion using Efficient Row-wise Attention](https://arxiv.org/abs/2405.11616)** | NeurIPS 2024 · since 2025 | A multiview generation model that remained relevant in 2025 for single-image 3D asset… | [📄 arXiv](https://arxiv.org/abs/2405.11616) · [💻 Code ★643](https://github.com/pengHTYX/Era3D) |
| ⚪ **[RGB2Point: 3D Point Cloud Generation from Single RGB Images](https://arxiv.org/abs/2407.14979)** | ACM MM 2024 · since 2025 | A transformer-based single-image point-cloud generator that stayed useful in 2025 as a… | [📄 arXiv](https://arxiv.org/abs/2407.14979) |

### [text-to-3d](text-to-3d.md) · 3

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| 🟢 **[AssetFormer: Modular 3D Assets Generation with Autoregressive Transformer](https://arxiv.org/abs/2602.12100)** | arXiv 2026 | Targets modular assets directly with autoregressive generation over part-aware structures. | [📄 arXiv](https://arxiv.org/abs/2602.12100) · [💻 Code ★37](https://github.com/Advocate99/AssetFormer) |
| ⚪ **[Text-Image Conditioned 3D Generation](https://arxiv.org/abs/2603.21295)** | arXiv 2026 | A joint text-and-image conditioned 3D generation framework aimed at stronger… | [📄 arXiv](https://arxiv.org/abs/2603.21295) |
| 🟢 **[ITS3D: Inference-Time Scaling for Text-Guided 3D Diffusion Models](https://arxiv.org/abs/2511.22456)** | arXiv 2025 | Brings inference-time scaling into text-guided 3D diffusion to improve asset quality at… | [📄 arXiv](https://arxiv.org/abs/2511.22456) · [💻 Code ★10](https://github.com/ZhenglinZhou/ITS3D) |

### [part-aware-generation](part-aware-generation.md) · 6

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[DreamPartGen: Semantically Grounded Part-Level 3D Generation via Collaborative Latent Denoising](https://arxiv.org/abs/2603.19216)** | arXiv 2026 | A collaborative latent-denoising framework for semantically grounded part-level 3D object… | [📄 arXiv](https://arxiv.org/abs/2603.19216) |
| ⚪ **[Assembler: Scalable 3D Part Assembly via Anchor Point Diffusion](https://arxiv.org/abs/2506.17074)** | arXiv 2025 | Recasts part assembly as a generative diffusion problem over sparse anchor points rather… | [📄 arXiv](https://arxiv.org/abs/2506.17074) · [🌐 Project](https://assembler3d.github.io) |
| ⚪ **[From One to More: Contextual Part Latents for 3D Generation](https://arxiv.org/abs/2507.08772)** | ICCV 2025 | Decomposes objects into contextual part latents for coherent part-aware generation and… | [📄 arXiv](https://arxiv.org/abs/2507.08772) |
| ⚪ **[FullPart: Generating each 3D Part at Full Resolution](https://arxiv.org/abs/2510.26140)** | arXiv 2025 | Generates each semantic part in its own full-resolution grid instead of sharing a… | [📄 arXiv](https://arxiv.org/abs/2510.26140) |
| ⚪ **[OmniPart: Part-Aware 3D Generation with Semantic Decoupling and Structural Cohesion](https://arxiv.org/abs/2507.06165)** | arXiv 2025 | A two-stage part planning and part synthesis framework for editable and controllable 3D… | [📄 arXiv](https://arxiv.org/abs/2507.06165) |
| ⚪ **[PartCrafter: Structured 3D Mesh Generation via Compositional Latent Diffusion Transformers](https://arxiv.org/abs/2506.05573)** | arXiv 2025 | A compositional latent DiT that jointly denoises multiple semantic parts into… | [📄 arXiv](https://arxiv.org/abs/2506.05573) |

### [articulated-asset](articulated-asset.md) · 4

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[Articulate AnyMesh: Open-Vocabulary 3D Articulated Objects Modeling](https://arxiv.org/abs/2502.02590)** | arXiv 2025 | Converts rigid meshes into articulated open-vocabulary assets by combining VLM semantics… | [📄 arXiv](https://arxiv.org/abs/2502.02590) · [🌐 Project](https://articulate-anymesh.github.io) |
| 🟢 **[Infinite Mobility: Scalable High-Fidelity Synthesis of Articulated Objects via Procedural Generation](https://arxiv.org/abs/2503.13424)** | arXiv 2025 | A procedural articulated-object synthesis pipeline built for scale, fidelity, and… | [📄 arXiv](https://arxiv.org/abs/2503.13424) · [💻 Code](https://github.com/Intern-Nexus/Infinite-Mobility) |
| ⚪ **[MeshArt: Generating Articulated Meshes with Structure-guided Transformers](https://arxiv.org/abs/2412.11596)** | CVPR 2025 | A hierarchical transformer that generates articulated meshes part by part with explicit… | [📄 arXiv](https://arxiv.org/abs/2412.11596) |
| ⚪ **[PrimitiveAnything: Human-Crafted 3D Primitive Assembly Generation with Auto-Regressive Transformer](https://arxiv.org/abs/2505.04622)** | SIGGRAPH 2025 | Learns human-like primitive abstractions and assemblies for editable structured 3D assets. | [📄 arXiv](https://arxiv.org/abs/2505.04622) · [🌐 Project](https://primitiveanything.github.io) |

### [human-avatar](human-avatar.md) · 1

| Title | Venue | What it does | Links |
|:--|:--|:--|:--|
| ⚪ **[AdaHuman: Animatable Detailed 3D Human Generation with Compositional Multiview Diffusion](https://arxiv.org/abs/2505.24877)** | ICCV 2025 | A single-image avatar generator that targets animation-ready humans with strong local… | [📄 arXiv](https://arxiv.org/abs/2505.24877) |
