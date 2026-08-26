# Validation Report — Deep

- Status: **FAIL**
- Generated: `2026-08-26 09:30:36 UTC`
- Commit: `local`
- Records checked: **207**
- Blocking errors: **5**
- Warnings: **48**
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
- `network.repo.unknown` — 10-image-2d/improving-long-text-alignment (image_2d.jsonl:21): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 10-image-2d/information-theoretic-t2i-alignment (image_2d.jsonl:22): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 10-image-2d/meanflow (image_2d.jsonl:39): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 10-image-2d/noise-diffusion (image_2d.jsonl:20): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 10-image-2d/one-prompt-one-story (image_2d.jsonl:54): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 10-image-2d/pixart-sigma (image_2d.jsonl:50): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `semantic.paper_unverified` — 10-image-2d/pt-t2iv (image_2d.jsonl:37): Paper title could not be verified because the remote site returned a bot-challenge or generic page.
- `network.repo.unknown` — 10-image-2d/qwen-image (image_2d.jsonl:62): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.organization` — 10-image-2d/sana-1.5 (image_2d.jsonl:48): Repository owner suggests organization `NVLabs`.
- `network.repo.unknown` — 10-image-2d/sana-1.5 (image_2d.jsonl:48): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.organization` — 20-video/cogvideox (video.jsonl:16): Repository owner suggests organization `THUDM`.
- `metadata.missing_paper` — 20-video/hunyuanvideo-i2v (video.jsonl:12): Missing `paper` link.
- `metadata.missing_paper` — 20-video/kling (video.jsonl:17): Missing `paper` link.
- `network.repo.unknown` — 20-video/magicdrive-v2 (video.jsonl:61): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 20-video/phyt2v (video.jsonl:7): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 20-video/step-video (video.jsonl:18): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.organization` — 20-video/unianimate-dit (video.jsonl:51): Repository owner suggests organization `Alibaba VILab`.
- `network.repo.unknown` — 20-video/unianimate-dit (video.jsonl:51): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.organization` — 20-video/vace (video.jsonl:39): Repository owner suggests organization `Alibaba VILab`.
- `network.repo.unknown` — 20-video/vace (video.jsonl:39): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.organization` — 20-video/wan2.1 (video.jsonl:10): Repository owner suggests organization `Alibaba Wan`.
- `network.repo.unknown` — 20-video/wan2.1 (video.jsonl:10): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 20-video/x-dyna (video.jsonl:44): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 30-3d-object-asset/flashvdm (object_3d.jsonl:28): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.missing_paper` — 30-3d-object-asset/hunyuan3d-2.1 (object_3d.jsonl:27): Missing `paper` link.
- `network.repo.unknown` — 30-3d-object-asset/infinite-mobility (object_3d.jsonl:44): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.organization` — 30-3d-object-asset/instantmesh (object_3d.jsonl:31): Repository owner suggests organization `Tencent ARC`.
- `network.repo.unknown` — 30-3d-object-asset/instantmesh (object_3d.jsonl:31): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 30-3d-object-asset/its3d (object_3d.jsonl:36): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 30-3d-object-asset/octfusion (object_3d.jsonl:11): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 30-3d-object-asset/sparc3d (object_3d.jsonl:8): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 30-3d-object-asset/topodit-3d (object_3d.jsonl:16): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 30-3d-object-asset/trellis (object_3d.jsonl:2): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 30-3d-object-asset/triposr (object_3d.jsonl:30): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 30-3d-object-asset/unique3d (object_3d.jsonl:32): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 40-3d-scene/wonderworld (scene_3d.jsonl:32): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 50-4d-dynamic-scene-world/hunyuanworld-1.0 (world_4d.jsonl:12): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 50-4d-dynamic-scene-world/hunyuanworld-voyager (world_4d.jsonl:11): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.organization` — 50-4d-dynamic-scene-world/hy-worldplay (world_4d.jsonl:19): Repository owner suggests organization `Tencent Hunyuan`.
- `network.repo.unknown` — 50-4d-dynamic-scene-world/matrix-game (world_4d.jsonl:28): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `metadata.organization` — 50-4d-dynamic-scene-world/nvidia-cosmos (world_4d.jsonl:20): Repository owner suggests organization `NVIDIA`.
- `metadata.organization` — 50-4d-dynamic-scene-world/waymax (world_4d.jsonl:22): Repository owner suggests organization `Waymo`.
- `network.repo.unknown` — 50-4d-dynamic-scene-world/waymax (world_4d.jsonl:22): `repo` could not be conclusively verified: GitHub API HTTP 403.
- `network.repo.unknown` — 50-4d-dynamic-scene-world/world4drive (world_4d.jsonl:4): `repo` could not be conclusively verified: GitHub API HTTP 403.
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
| `black-forest-labs/flux` | 25911 | 2025-07-31 | No | Apache-2.0 |
| `Tencent-Hunyuan/Hunyuan3D-2` | 14623 | 2025-10-28 | No | NOASSERTION |
| `zai-org/CogVideo` | 12977 | 2025-11-04 | No | Apache-2.0 |
| `Tencent-Hunyuan/HunyuanVideo` | 12472 | 2026-06-29 | No | NOASSERTION |
| `NVIDIA/cosmos` | 11631 | 2026-08-25 | No | NOASSERTION |
| `Tencent-Hunyuan/HunyuanVideo-1.5` | 4534 | 2026-04-10 | No | NOASSERTION |
| `Tencent-Hunyuan/Hunyuan3D-2.1` | 3913 | 2025-10-17 | No | NOASSERTION |
| `Tencent-Hunyuan/HunyuanImage-3.0` | 3253 | 2026-06-23 | No | NOASSERTION |
| `Tencent-Hunyuan/HunyuanVideo-I2V` | 1839 | 2026-04-07 | No | NOASSERTION |
| `Tencent-Hunyuan/HY-WorldPlay` | 1586 | 2026-06-10 | No | NOASSERTION |
| `PKU-YuanGroup/ConsisID` | 855 | 2026-04-14 | No | Apache-2.0 |
| `pengHTYX/Era3D` | 645 | 2024-12-09 | No | AGPL-3.0 |
| `Kevin-thu/Epona` | 384 | 2025-07-22 | No | MIT |
| `LMD0311/HERMES` | 260 | 2026-05-12 | No | Apache-2.0 |
| `showlab/D-AR` | 138 | 2026-01-29 | No | MIT |
| `liulin815/DriveWorld-VLA` | 122 | 2026-07-08 | No | — |
| `Tencent-Hunyuan/iFSQ` | 106 | 2026-01-27 | No | NOASSERTION |
| `nktoan/h-edit` | 79 | 2025-06-11 | No | Apache-2.0 |
| `Bujiazi/ByTheWay` | 48 | 2025-10-10 | No | — |
| `Advocate99/AssetFormer` | 39 | 2026-02-13 | No | — |
| `jiangchaokang/VectorWorld` | 35 | 2026-06-23 | No | — |
| `xiaolul2/DynFlowDrive` | 24 | 2026-03-23 | No | — |
