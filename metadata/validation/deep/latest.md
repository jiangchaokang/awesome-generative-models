# Validation Report — Deep

- Status: **FAIL**
- Generated: `2026-09-21 08:59:53 UTC`
- Commit: `382f068cbe1c`
- Records checked: **207**
- Blocking errors: **5**
- Warnings: **19**
- Notices: **3**

## Blocking Errors

- `semantic.paper_mismatch` — 10-image-2d/relevance-feedback-t2i (image_2d.jsonl:15): Paper title mismatch. Expected `Relevance Feedback in Text-to-Image Diffusion: A Training-Free And Model-Agnostic Interactive Framework`; arXiv API returned `Bridging the Intention-Expression Gap: Aligning Multi-Dimensional Preferences via Hierarchical Relevance Feedback in Text-to-Image Diffusion` (score=0.56).
- `semantic.paper_mismatch` — 20-video/seedance (video.jsonl:15): Paper title mismatch. Expected `Seedance 1.0: Exploring the Boundaries of Video Generation Models`; arXiv API returned `A Question Bank to Assess AI Inclusivity: Mapping out the Journey from Diversity Errors to Inclusion Excellence` (score=0.38).
- `semantic.paper_mismatch` — 20-video/step-video (video.jsonl:18): Paper title mismatch. Expected `Step-Video-T2V: A State-of-the-Art Text-to-Video Model`; arXiv API returned `Step-Video-T2V Technical Report: The Practice, Challenges, and Future of Video Foundation Model` (score=0.55).
- `semantic.paper_mismatch` — 20-video/wan2.1 (video.jsonl:10): Paper title mismatch. Expected `Wan 2.1: Open-Source Video Foundation Model`; arXiv API returned `Wan: Open and Advanced Large-Scale Video Generative Models` (score=0.59).
- `semantic.paper_mismatch` — 40-3d-scene/respace (scene_3d.jsonl:13): Paper title mismatch. Expected `ReSpace: Text-Driven 3D Scene Synthesis and Editing with Preference Alignment`; arXiv API returned `ReSpace: Text-Driven Autoregressive 3D Indoor Scene Synthesis and Editing` (score=0.75).

## Warnings

- `semantic.paper_unverified` — 10-image-2d/denoising-autoregressive-transformers (image_2d.jsonl:53): Paper title could not be verified because the remote site returned a bot-challenge or generic page.
- `metadata.organization` — 10-image-2d/flux (image_2d.jsonl:49): Repository owner suggests organization `Black Forest Labs`.
- `metadata.organization` — 10-image-2d/ifsq (image_2d.jsonl:38): Repository owner suggests organization `Tencent Hunyuan`.
- `semantic.paper_unverified` — 10-image-2d/pt-t2iv (image_2d.jsonl:37): Paper title could not be verified because the remote site returned a bot-challenge or generic page.
- `metadata.organization` — 10-image-2d/sana-1.5 (image_2d.jsonl:48): Repository owner suggests organization `NVLabs`.
- `metadata.organization` — 20-video/cogvideox (video.jsonl:16): Repository owner suggests organization `THUDM`.
- `metadata.missing_paper` — 20-video/hunyuanvideo-i2v (video.jsonl:12): Missing `paper` link.
- `metadata.missing_paper` — 20-video/kling (video.jsonl:17): Missing `paper` link.
- `metadata.organization` — 20-video/unianimate-dit (video.jsonl:51): Repository owner suggests organization `Alibaba VILab`.
- `network.repo.unknown` — 20-video/unianimate-dit (video.jsonl:51): `repo` could not be conclusively verified: GitHub API unavailable: <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1016)>.
- `metadata.organization` — 20-video/vace (video.jsonl:39): Repository owner suggests organization `Alibaba VILab`.
- `metadata.organization` — 20-video/wan2.1 (video.jsonl:10): Repository owner suggests organization `Alibaba Wan`.
- `metadata.missing_paper` — 30-3d-object-asset/hunyuan3d-2.1 (object_3d.jsonl:27): Missing `paper` link.
- `metadata.organization` — 30-3d-object-asset/instantmesh (object_3d.jsonl:31): Repository owner suggests organization `Tencent ARC`.
- `metadata.organization` — 50-4d-dynamic-scene-world/hy-worldplay (world_4d.jsonl:19): Repository owner suggests organization `Tencent Hunyuan`.
- `metadata.organization` — 50-4d-dynamic-scene-world/nvidia-cosmos (world_4d.jsonl:20): Repository owner suggests organization `NVIDIA`.
- `metadata.organization` — 50-4d-dynamic-scene-world/waymax (world_4d.jsonl:22): Repository owner suggests organization `Waymo`.
- `date.precision` — catalog: 207 records do not have `published_at`; day-level freshness cannot be guaranteed until they are backfilled.
- `source.arxiv_api` — catalog: arXiv API was partially unavailable; 200 title checks were skipped.

<details>
<summary>Notices (3)</summary>

- `semantic.repo_weak_match` — 10-image-2d/flux (image_2d.jsonl:49): Repository name/description weakly matches the catalog title (score=0.14).
- `semantic.homepage_weak_match` — 10-image-2d/seedream-3.0 (image_2d.jsonl:64): Homepage title weakly matches the catalog title: `Seed News - ByteDance Seed Team` (score=0.24).
- `semantic.homepage_weak_match` — 50-4d-dynamic-scene-world/hy-worldplay (world_4d.jsonl:19): Homepage title weakly matches the catalog title: `腾讯混元3D` (score=0.02).

</details>

## Refreshed GitHub Repository Stats

| Repository | Stars | Last push | Archived | License |
|:--|--:|:--|:--:|:--|
| `black-forest-labs/flux` | 25973 | 2025-07-31 | No | Apache-2.0 |
| `Wan-Video/Wan2.1` | 17015 | 2026-03-05 | No | Apache-2.0 |
| `Tencent-Hunyuan/Hunyuan3D-2` | 14924 | 2025-10-28 | No | NOASSERTION |
| `microsoft/TRELLIS` | 13684 | 2026-06-26 | No | MIT |
| `zai-org/CogVideo` | 13032 | 2025-11-04 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo` | 12550 | 2026-06-29 | No | NOASSERTION |
| `NVIDIA/cosmos` | 11874 | 2026-09-21 | No | NOASSERTION |
| `NVlabs/Sana` | 9124 | 2026-09-21 | No | Apache-2.0 |
| `QwenLM/Qwen-Image` | 8349 | 2026-02-10 | No | Apache-2.0 |
| `VAST-AI-Research/TripoSR` | 6967 | 2026-06-04 | No | MIT |
| `Tencent-Hunyuan/HunyuanVideo-1.5` | 4555 | 2026-04-10 | No | NOASSERTION |
| `TencentARC/InstantMesh` | 4534 | 2025-01-03 | No | Apache-2.0 |
| `Tencent-Hunyuan/Hunyuan3D-2.1` | 4049 | 2025-10-17 | No | NOASSERTION |
| `ali-vilab/VACE` | 3952 | 2025-10-17 | No | Apache-2.0 |
| `AiuniAI/Unique3D` | 3590 | 2025-07-17 | No | MIT |
| `Tencent-Hunyuan/HunyuanImage-3.0` | 3268 | 2026-06-23 | No | NOASSERTION |
| `stepfun-ai/Step-Video-T2V` | 3186 | 2025-03-17 | No | MIT |
| `Tencent-Hunyuan/HunyuanWorld-1.0` | 2936 | 2026-04-15 | No | NOASSERTION |
| `SkyworkAI/Matrix-Game` | 2336 | 2026-03-30 | No | MIT |
| `PixArt-alpha/PixArt-sigma` | 1941 | 2024-10-31 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo-I2V` | 1843 | 2026-04-07 | No | NOASSERTION |
| `Tencent-Hunyuan/HY-WorldPlay` | 1604 | 2026-06-10 | No | NOASSERTION |
| `Tencent-Hunyuan/HunyuanWorld-Voyager` | 1597 | 2026-04-15 | No | NOASSERTION |
| `lizhihao6/Sparc3D` | 1359 | 2025-06-16 | No | — |
| `waymo-research/waymax` | 1102 | 2025-10-23 | No | NOASSERTION |
| `PKU-YuanGroup/ConsisID` | 857 | 2026-04-14 | No | Apache-2.0 |
| `KovenYu/WonderWorld` | 743 | 2025-04-14 | No | — |
| `flymin/MagicDrive-V2` | 728 | 2025-06-26 | No | AGPL-3.0 |
| `pengHTYX/Era3D` | 645 | 2024-12-09 | No | AGPL-3.0 |
| `Gsunshine/meanflow` | 613 | 2026-03-13 | No | MIT |
| `Kevin-thu/Epona` | 388 | 2025-07-22 | No | MIT |
| `Tencent-Hunyuan/FlashVDM` | 335 | 2026-03-13 | No | NOASSERTION |
| `byliutao/1Prompt1Story` | 321 | 2025-10-20 | No | MIT |
| `bytedance/X-Dyna` | 268 | 2025-01-30 | No | Apache-2.0 |
| `LMD0311/HERMES` | 264 | 2026-05-12 | No | Apache-2.0 |
| `octree-nn/octfusion` | 231 | 2025-07-02 | No | — |
| `InternRobotics/Infinite-Mobility` | 196 | 2025-07-25 | No | BSD-3-Clause |
| `showlab/D-AR` | 138 | 2026-01-29 | No | MIT |
| `liulin815/DriveWorld-VLA` | 127 | 2026-07-08 | No | — |
| `ucaszyp/World4Drive` | 109 | 2025-12-31 | No | Apache-2.0 |
| `Tencent-Hunyuan/iFSQ` | 106 | 2026-01-27 | No | NOASSERTION |
| `luping-liu/LongAlign` | 83 | 2025-04-23 | No | Apache-2.0 |
| `nktoan/h-edit` | 81 | 2025-06-11 | No | Apache-2.0 |
| `pittisl/PhyT2V` | 67 | 2025-07-31 | No | — |
| `Bujiazi/ByTheWay` | 48 | 2025-10-10 | No | — |
| `Advocate99/AssetFormer` | 41 | 2026-02-13 | No | — |
| `jiangchaokang/VectorWorld` | 36 | 2026-06-23 | No | — |
| `xiaolul2/DynFlowDrive` | 25 | 2026-03-23 | No | — |
| `Bomingmiao/NoiseDiffusion` | 15 | 2025-11-08 | No | MIT |
| `Zechao-Guan/TopoDiT-3D` | 15 | 2025-05-13 | No | — |
| `ZhenglinZhou/ITS3D` | 11 | 2026-07-30 | No | Apache-2.0 |
| `Chao0511/mitune` | 6 | 2025-03-23 | No | MIT |
