# Validation Report — Deep

- Status: **FAIL**
- Generated: `2026-11-25 13:57:15 UTC`
- Commit: `5f8914e343fd`
- Records checked: **207**
- Blocking errors: **2**
- Warnings: **6**
- Notices: **3**

## Blocking Errors

- `semantic.paper_mismatch` — 30-3d-object-asset/pointcloud-ar-upsampling (object_3d.jsonl:17): Paper title mismatch. Expected `3D Point Cloud Generation via Autoregressive Up-sampling`; arXiv API returned `PointNSP: Autoregressive 3D Point Cloud Generation with Next-Scale Level-of-Detail Prediction` (score=0.80).
- `semantic.paper_mismatch` — 50-4d-dynamic-scene-world/hy-worldplay (world_4d.jsonl:19): Paper title mismatch. Expected `HY-World 1.5 (WorldPlay): A Systematic Framework for Interactive World Modeling with Real-Time Latency and Geometric Consistency`; arXiv API returned `WorldPlay: Towards Long-Term Geometric Consistency for Real-Time Interactive World Modeling` (score=0.80).

## Warnings

- `semantic.paper_unverified` — 10-image-2d/denoising-autoregressive-transformers (image_2d.jsonl:53): Paper title could not be verified because the remote site returned a bot-challenge or generic page.
- `semantic.paper_unverified` — 10-image-2d/pt-t2iv (image_2d.jsonl:37): Paper title could not be verified because the remote site returned a bot-challenge or generic page.
- `metadata.missing_paper` — 20-video/hunyuanvideo-i2v (video.jsonl:12): Missing `paper` link.
- `metadata.missing_paper` — 20-video/kling (video.jsonl:17): Missing `paper` link.
- `metadata.missing_paper` — 30-3d-object-asset/hunyuan3d-2.1 (object_3d.jsonl:27): Missing `paper` link.
- `date.precision` — catalog: 202 records do not have `published_at`; day-level freshness cannot be guaranteed until they are backfilled.

<details>
<summary>Notices (3)</summary>

- `semantic.repo_weak_match` — 10-image-2d/flux (image_2d.jsonl:49): Repository name/description weakly matches the catalog title (score=0.14).
- `semantic.homepage_weak_match` — 10-image-2d/seedream-3.0 (image_2d.jsonl:64): Homepage title weakly matches the catalog title: `Seed News - ByteDance Seed Team` (score=0.24).
- `semantic.homepage_weak_match` — 50-4d-dynamic-scene-world/hy-worldplay (world_4d.jsonl:19): Homepage title weakly matches the catalog title: `腾讯混元3D` (score=0.02).

</details>

## Refreshed GitHub Repository Stats

| Repository | Stars | Last push | Archived | License |
|:--|--:|:--|:--:|:--|
| `black-forest-labs/flux` | 26083 | 2025-07-31 | No | Apache-2.0 |
| `Wan-Video/Wan2.1` | 17492 | 2026-03-05 | No | Apache-2.0 |
| `Tencent-Hunyuan/Hunyuan3D-2` | 15564 | 2025-10-28 | No | NOASSERTION |
| `microsoft/TRELLIS` | 14400 | 2026-10-27 | No | MIT |
| `zai-org/CogVideo` | 13230 | 2025-11-04 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo` | 12832 | 2026-10-08 | No | NOASSERTION |
| `NVIDIA/cosmos` | 12459 | 2026-11-19 | No | NOASSERTION |
| `NVlabs/Sana` | 9896 | 2026-11-25 | No | Apache-2.0 |
| `QwenLM/Qwen-Image` | 8498 | 2026-02-10 | No | Apache-2.0 |
| `VAST-AI-Research/TripoSR` | 7471 | 2026-06-04 | No | MIT |
| `TencentARC/InstantMesh` | 4630 | 2025-01-03 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo-1.5` | 4618 | 2026-04-10 | No | NOASSERTION |
| `Tencent-Hunyuan/Hunyuan3D-2.1` | 4553 | 2025-10-17 | No | NOASSERTION |
| `ali-vilab/VACE` | 4078 | 2025-10-17 | No | Apache-2.0 |
| `AiuniAI/Unique3D` | 3599 | 2025-07-17 | No | MIT |
| `Tencent-Hunyuan/HunyuanImage-3.0` | 3310 | 2026-06-23 | No | NOASSERTION |
| `stepfun-ai/Step-Video-T2V` | 3187 | 2025-03-17 | No | MIT |
| `Tencent-Hunyuan/HunyuanWorld-1.0` | 2994 | 2026-04-15 | No | NOASSERTION |
| `SkyworkAI/Matrix-Game` | 2992 | 2026-10-29 | No | MIT |
| `PixArt-alpha/PixArt-sigma` | 1944 | 2024-10-31 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo-I2V` | 1859 | 2026-04-07 | No | NOASSERTION |
| `Tencent-Hunyuan/HY-WorldPlay` | 1637 | 2026-11-25 | No | NOASSERTION |
| `Tencent-Hunyuan/HunyuanWorld-Voyager` | 1611 | 2026-11-25 | No | NOASSERTION |
| `lizhihao6/Sparc3D` | 1365 | 2025-06-16 | No | — |
| `waymo-research/waymax` | 1117 | 2025-10-23 | No | NOASSERTION |
| `PKU-YuanGroup/ConsisID` | 866 | 2026-04-14 | No | Apache-2.0 |
| `ali-vilab/UniAnimate-DiT` | 857 | 2025-04-27 | No | — |
| `KovenYu/WonderWorld` | 748 | 2025-04-14 | No | — |
| `flymin/MagicDrive-V2` | 726 | 2025-06-26 | No | AGPL-3.0 |
| `pengHTYX/Era3D` | 648 | 2024-12-09 | No | AGPL-3.0 |
| `Gsunshine/meanflow` | 624 | 2026-03-13 | No | MIT |
| `Kevin-thu/Epona` | 393 | 2025-07-22 | No | MIT |
| `Tencent-Hunyuan/FlashVDM` | 340 | 2026-03-13 | No | NOASSERTION |
| `byliutao/1Prompt1Story` | 321 | 2025-10-20 | No | MIT |
| `bytedance/X-Dyna` | 268 | 2025-01-30 | No | Apache-2.0 |
| `LMD0311/HERMES` | 265 | 2026-11-08 | No | Apache-2.0 |
| `octree-nn/octfusion` | 236 | 2025-07-02 | No | — |
| `Sage-PhysicalAI/Infinite-Mobility` | 196 | 2025-07-25 | No | BSD-3-Clause |
| `showlab/D-AR` | 137 | 2026-01-29 | No | MIT |
| `liulin815/DriveWorld-VLA` | 129 | 2026-07-08 | No | — |
| `ucaszyp/World4Drive` | 115 | 2025-12-31 | No | Apache-2.0 |
| `Tencent-Hunyuan/iFSQ` | 108 | 2026-01-27 | No | NOASSERTION |
| `luping-liu/LongAlign` | 83 | 2025-04-23 | No | Apache-2.0 |
| `nktoan/h-edit` | 80 | 2025-06-11 | No | Apache-2.0 |
| `pittisl/PhyT2V` | 67 | 2025-07-31 | No | — |
| `Bujiazi/ByTheWay` | 48 | 2025-10-10 | No | — |
| `Advocate99/AssetFormer` | 41 | 2026-02-13 | No | — |
| `jiangchaokang/VectorWorld` | 39 | 2026-06-23 | No | — |
| `xiaolul2/DynFlowDrive` | 26 | 2026-03-23 | No | — |
| `Bomingmiao/NoiseDiffusion` | 15 | 2025-11-08 | No | MIT |
| `Zechao-Guan/TopoDiT-3D` | 15 | 2025-05-13 | No | — |
| `ZhenglinZhou/ITS3D` | 12 | 2026-07-30 | No | Apache-2.0 |
| `Chao0511/mitune` | 6 | 2025-03-23 | No | MIT |
