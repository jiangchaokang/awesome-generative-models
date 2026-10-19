# Validation Report — Deep

- Status: **FAIL**
- Generated: `2026-10-19 08:55:59 UTC`
- Commit: `4c54803fb753`
- Records checked: **207**
- Blocking errors: **6**
- Warnings: **18**
- Notices: **3**

## Blocking Errors

- `semantic.paper_mismatch` — 10-image-2d/relevance-feedback-t2i (image_2d.jsonl:15): Paper title mismatch. Expected `Relevance Feedback in Text-to-Image Diffusion: A Training-Free And Model-Agnostic Interactive Framework`; arXiv API returned `Bridging the Intention-Expression Gap: Aligning Multi-Dimensional Preferences via Hierarchical Relevance Feedback in Text-to-Image Diffusion` (score=0.56).
- `semantic.paper_mismatch` — 20-video/seedance (video.jsonl:15): Paper title mismatch. Expected `Seedance 1.0: Exploring the Boundaries of Video Generation Models`; arXiv API returned `A Question Bank to Assess AI Inclusivity: Mapping out the Journey from Diversity Errors to Inclusion Excellence` (score=0.38).
- `semantic.paper_mismatch` — 20-video/step-video (video.jsonl:18): Paper title mismatch. Expected `Step-Video-T2V: A State-of-the-Art Text-to-Video Model`; arXiv API returned `Step-Video-T2V Technical Report: The Practice, Challenges, and Future of Video Foundation Model` (score=0.55).
- `semantic.paper_mismatch` — 20-video/wan2.1 (video.jsonl:10): Paper title mismatch. Expected `Wan 2.1: Open-Source Video Foundation Model`; arXiv API returned `Wan: Open and Advanced Large-Scale Video Generative Models` (score=0.59).
- `semantic.paper_mismatch` — 30-3d-object-asset/squeeze3d (object_3d.jsonl:12): Paper title mismatch. Expected `Squeeze3D: Your 3D Generation Model is Secretly an Extreme Neural Compressor`; arXiv API returned `Squeeze3D: Extreme Neural Compression with Latent Space Bridging` (score=0.51).
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
- `metadata.organization` — 20-video/vace (video.jsonl:39): Repository owner suggests organization `Alibaba VILab`.
- `metadata.organization` — 20-video/wan2.1 (video.jsonl:10): Repository owner suggests organization `Alibaba Wan`.
- `metadata.missing_paper` — 30-3d-object-asset/hunyuan3d-2.1 (object_3d.jsonl:27): Missing `paper` link.
- `metadata.organization` — 30-3d-object-asset/instantmesh (object_3d.jsonl:31): Repository owner suggests organization `Tencent ARC`.
- `network.repo.unknown` — 50-4d-dynamic-scene-world/hunyuanworld-voyager (world_4d.jsonl:11): `repo` could not be conclusively verified: GitHub API unavailable: <urlopen error EOF occurred in violation of protocol (_ssl.c:2437)>.
- `metadata.organization` — 50-4d-dynamic-scene-world/hy-worldplay (world_4d.jsonl:19): Repository owner suggests organization `Tencent Hunyuan`.
- `metadata.organization` — 50-4d-dynamic-scene-world/nvidia-cosmos (world_4d.jsonl:20): Repository owner suggests organization `NVIDIA`.
- `metadata.organization` — 50-4d-dynamic-scene-world/waymax (world_4d.jsonl:22): Repository owner suggests organization `Waymo`.
- `date.precision` — catalog: 207 records do not have `published_at`; day-level freshness cannot be guaranteed until they are backfilled.

<details>
<summary>Notices (3)</summary>

- `semantic.repo_weak_match` — 10-image-2d/flux (image_2d.jsonl:49): Repository name/description weakly matches the catalog title (score=0.14).
- `semantic.homepage_weak_match` — 10-image-2d/seedream-3.0 (image_2d.jsonl:64): Homepage title weakly matches the catalog title: `Seed News - ByteDance Seed Team` (score=0.24).
- `semantic.homepage_weak_match` — 50-4d-dynamic-scene-world/hy-worldplay (world_4d.jsonl:19): Homepage title weakly matches the catalog title: `腾讯混元3D` (score=0.02).

</details>

## Refreshed GitHub Repository Stats

| Repository | Stars | Last push | Archived | License |
|:--|--:|:--|:--:|:--|
| `black-forest-labs/flux` | 26025 | 2025-07-31 | No | Apache-2.0 |
| `Wan-Video/Wan2.1` | 17241 | 2026-03-05 | No | Apache-2.0 |
| `Tencent-Hunyuan/Hunyuan3D-2` | 15158 | 2025-10-28 | No | NOASSERTION |
| `microsoft/TRELLIS` | 14009 | 2026-06-26 | No | MIT |
| `zai-org/CogVideo` | 13086 | 2025-11-04 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo` | 12634 | 2026-10-08 | No | NOASSERTION |
| `NVIDIA/cosmos` | 12064 | 2026-10-16 | No | NOASSERTION |
| `NVlabs/Sana` | 9398 | 2026-10-19 | No | Apache-2.0 |
| `QwenLM/Qwen-Image` | 8411 | 2026-02-10 | No | Apache-2.0 |
| `VAST-AI-Research/TripoSR` | 7103 | 2026-06-04 | No | MIT |
| `TencentARC/InstantMesh` | 4574 | 2025-01-03 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo-1.5` | 4570 | 2026-04-10 | No | NOASSERTION |
| `Tencent-Hunyuan/Hunyuan3D-2.1` | 4232 | 2025-10-17 | No | NOASSERTION |
| `ali-vilab/VACE` | 3983 | 2025-10-17 | No | Apache-2.0 |
| `AiuniAI/Unique3D` | 3596 | 2025-07-17 | No | MIT |
| `Tencent-Hunyuan/HunyuanImage-3.0` | 3289 | 2026-06-23 | No | NOASSERTION |
| `stepfun-ai/Step-Video-T2V` | 3187 | 2025-03-17 | No | MIT |
| `Tencent-Hunyuan/HunyuanWorld-1.0` | 2952 | 2026-04-15 | No | NOASSERTION |
| `SkyworkAI/Matrix-Game` | 2618 | 2026-10-16 | No | MIT |
| `PixArt-alpha/PixArt-sigma` | 1941 | 2024-10-31 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo-I2V` | 1849 | 2026-04-07 | No | NOASSERTION |
| `Tencent-Hunyuan/HY-WorldPlay` | 1618 | 2026-06-10 | No | NOASSERTION |
| `lizhihao6/Sparc3D` | 1359 | 2025-06-16 | No | — |
| `waymo-research/waymax` | 1110 | 2025-10-23 | No | NOASSERTION |
| `PKU-YuanGroup/ConsisID` | 863 | 2026-04-14 | No | Apache-2.0 |
| `ali-vilab/UniAnimate-DiT` | 854 | 2025-04-27 | No | — |
| `KovenYu/WonderWorld` | 746 | 2025-04-14 | No | — |
| `flymin/MagicDrive-V2` | 724 | 2025-06-26 | No | AGPL-3.0 |
| `pengHTYX/Era3D` | 647 | 2024-12-09 | No | AGPL-3.0 |
| `Gsunshine/meanflow` | 622 | 2026-03-13 | No | MIT |
| `Kevin-thu/Epona` | 391 | 2025-07-22 | No | MIT |
| `Tencent-Hunyuan/FlashVDM` | 336 | 2026-03-13 | No | NOASSERTION |
| `byliutao/1Prompt1Story` | 322 | 2025-10-20 | No | MIT |
| `bytedance/X-Dyna` | 268 | 2025-01-30 | No | Apache-2.0 |
| `LMD0311/HERMES` | 264 | 2026-05-12 | No | Apache-2.0 |
| `octree-nn/octfusion` | 232 | 2025-07-02 | No | — |
| `InternRobotics/Infinite-Mobility` | 196 | 2025-07-25 | No | BSD-3-Clause |
| `showlab/D-AR` | 138 | 2026-01-29 | No | MIT |
| `liulin815/DriveWorld-VLA` | 128 | 2026-07-08 | No | — |
| `ucaszyp/World4Drive` | 115 | 2025-12-31 | No | Apache-2.0 |
| `Tencent-Hunyuan/iFSQ` | 107 | 2026-01-27 | No | NOASSERTION |
| `luping-liu/LongAlign` | 83 | 2025-04-23 | No | Apache-2.0 |
| `nktoan/h-edit` | 80 | 2025-06-11 | No | Apache-2.0 |
| `pittisl/PhyT2V` | 67 | 2025-07-31 | No | — |
| `Bujiazi/ByTheWay` | 48 | 2025-10-10 | No | — |
| `Advocate99/AssetFormer` | 41 | 2026-02-13 | No | — |
| `jiangchaokang/VectorWorld` | 36 | 2026-06-23 | No | — |
| `xiaolul2/DynFlowDrive` | 26 | 2026-03-23 | No | — |
| `Bomingmiao/NoiseDiffusion` | 15 | 2025-11-08 | No | MIT |
| `Zechao-Guan/TopoDiT-3D` | 15 | 2025-05-13 | No | — |
| `ZhenglinZhou/ITS3D` | 11 | 2026-07-30 | No | Apache-2.0 |
| `Chao0511/mitune` | 6 | 2025-03-23 | No | MIT |
