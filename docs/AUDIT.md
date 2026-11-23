# Repository Audit Report

> Audit date: `2026-11-23`  
> Audited commit: `089fccf01a46` (branch `main` prior to `refactor/weekly-top-picks`)

---

## 1. Existing Architecture Summary

### 1.1 Workflows (`.github/workflows/`)

| Workflow | Trigger | Schedule | Permissions | Key Actions | Issues Found |
|:--|:--|:--|:--|:--|:--|
| `ci.yml` | `pull_request`, `push` (`main`/`master`) | None | `contents: read` | `compileall`, `unittest`, `validate_data.py --mode fast`, `build.py`, `check_internal_links.py`, `git diff --check` | Does **not** run `git diff --exit-code` after `build.py` (only checks whitespace); no pinned `requirements.txt` / pip cache; runs on bot pushes too. |
| `daily.yml` | `workflow_dispatch`, `push`, `schedule` | `25 1 * * *` (daily 01:25 UTC) | `contents: write`, `issues: write` | `unittest`, `fetch_candidates.py --days 14 --issue`, `validate_data.py --mode fast`, `build.py`, `check_internal_links.py`, `build_explorer.py`, `git commit && git push` | No `git pull --rebase` or push retry; commit message lacks `[skip ci]`; rebuilds README daily with `Updated: <today>` even when zero papers changed; scheduled failures turn Actions red. |
| `weekly-link-check.yml` | `workflow_dispatch`, `schedule` | `15 3 * * 1` (Monday 03:15 UTC) | `contents: write` | `unittest`, `build_explorer.py`, `validate_data.py --mode deep --write-cache`, `build.py`, `check_internal_links.py`, `git push`, final step `exit 1` on `status != 0` | Collides with Monday UTC arXiv announcement window and weekly picks; **explicitly exits 1 on scheduled runs** when blocking errors exist; no Issue deduplication/reporting; no `git pull --rebase` / push retry; no `issues: write` permission. |

### 1.2 Scripts (`scripts/`) & Tests (`tests/`)

- `scripts/catalog_common.py`: Taxonomy constants (`FILE_ARTIFACT`, `ARTIFACT_META`, `ARTIFACT_TASK_ORDER`, `DOMAIN_VOCAB`, `REPRESENTATION_VOCAB`, `METHOD_VOCAB`, `CONDITIONING_VOCAB`), hard-coded `WATCH_ORGS`, `ORG_BADGE_META`, `REPO_OWNER_TO_ORG`, and JSONL loader `load_records()`.
- `scripts/validate_data.py`: Fast (schema/vocab/dedupe/scope) and Deep (HTTP probes, arXiv/OpenReview title matching, GitHub repo stats). Uses `urllib.request`, `ThreadPoolExecutor(8)`, 24h TTL cache (`metadata/cache/network_cache_v2.json`).
- `scripts/build.py`: Renders `README.md`, `00-surveys-and-foundations/README.md`, `10-image-2d/`..`50-4d-dynamic-scene-world/`, `90-topics/`, `91-organizations/`.
- `scripts/fetch_candidates.py`: Harvests arXiv (via unencrypted `http://export.arxiv.org`, no retries, no rate-limit sleep) and GitHub org repos into `metadata/candidates/YYYY-MM-DD/`.
- `scripts/check_internal_links.py`: Verifies relative Markdown/HTML links across all `.md` files.
- `scripts/build_explorer.py`: Builds `docs/explorer/` static explorer.
- `tests/test_validate_data.py`: Only 7 minimal unit tests covering `is_unreliable_title`, `title_matches`, `classify_http_status`, and `canonical_paper_key`. Zero tests for `build.py`, deduplication, window calculation, scoring, or integration scenarios.

### 1.3 Data Schema (`data/*.jsonl`) & Metadata

- 5 JSONL files (`image_2d.jsonl`, `video.jsonl`, `object_3d.jsonl`, `scene_3d.jsonl`, `world_4d.jsonl`), **207 total entries**.
- Required fields per `CONTRIBUTING.md`: `id`, `title`, `venue`, `task`, `summary`, plus at least one of `paper` / `repo` / `homepage`.
- Optional fields: `domain`, `representation`, `method`, `conditioning`, `orgs`, `open_source`, `featured`, `active_since`, `scope_note`, `venue_url`, `stars`, `published_at`.
- `metadata/candidates/`: Daily dated directories (`2026-10-23` through `2026-11-22`), each with `candidates.json`, `report.md`, `watched_repos.json`, plus `seen_index.json`, `latest.json`, `latest.md`.
- `metadata/validation/fast/latest.md`: PASS (0 blocking errors, 15 warnings, 0 notices).
- `metadata/validation/deep/latest.md`: **FAIL** (6 blocking errors, 17 warnings, 3 notices).

---

## 2. Local Reproduction & Analysis of the 6 Deep-Validation Blocking Errors

### Local Reproduction Results
- `python scripts/validate_data.py --skip-network`: **PASS** (`records=207 errors=0 warnings=15 notices=0`).
- `python -m unittest discover -s tests -p "test_*.py" -v`: **7 tests OK**.
- External API endpoint probe (verified on `2026-11-23`):
  - `https://huggingface.co/api/daily_papers`: **HTTP 200 OK**
  - `https://huggingface.co/api/papers/{id}`: **HTTP 200 OK**
  - `https://api.github.com/repos/{owner}/{repo}`: **HTTP 200 OK**
  - `https://api.openalex.org/works`: **HTTP 200 OK** (note: shared daily budget without API key / polite email)
  - `https://export.arxiv.org/api/query`: **HTTP 429** under shared-IP burst without ≥3s spacing (must enforce ≥3s rate limit + exponential backoff + graceful degradation)
  - `https://api.semanticscholar.org/graph/v1/...`: **HTTP 429** without API key (must degrade gracefully)
  - `https://api2.openreview.net/notes`: **HTTP 403** bot protection (must degrade gracefully)

### The 6 Blocking Errors in `metadata/validation/deep/latest.md`

| # | Entry ID & Location | Error Type | Evidence | Root-Cause Classification | Resolution |
|---:|:--|:--|:--|:--|:--|
| 1 | `10-image-2d/relevance-feedback-t2i` (`data/image_2d.jsonl:15`) | `semantic.paper_mismatch` | Catalog title: `Relevance Feedback in Text-to-Image Diffusion: A Training-Free And Model-Agnostic Interactive Framework`; arXiv API (`2603.14936`) returned: `Bridging the Intention-Expression Gap: Aligning Multi-Dimensional Preferences via Hierarchical Relevance Feedback in Text-to-Image Diffusion` (score=0.56). | **(a) Deterministic error** — stale v1 title; authors renamed paper on arXiv in a later version. | **Fixed**: Update catalog title to exact canonical arXiv title for `2603.14936`. |
| 2 | `20-video/seedance` (`data/video.jsonl:15`) | `semantic.paper_mismatch` | Catalog title: `Seedance 1.0: Exploring the Boundaries of Video Generation Models`; linked arXiv `2506.18538` is actually `A Question Bank to Assess AI Inclusivity: Mapping out the Journey from Diversity Errors to Inclusion Excellence` (score=0.38). Verified via HF Papers API that Seedance 1.0's real arXiv ID is `2506.09113` (published `2025-06-10`). | **(a) Deterministic error** — wrong arXiv ID linked to an unrelated paper. | **Fixed**: Replace `https://arxiv.org/abs/2506.18538` with verified `https://arxiv.org/abs/2506.09113` (and set `published_at: "2025-06-10"`, `orgs: ["ByteDance Seed"]`). |
| 3 | `20-video/step-video` (`data/video.jsonl:18`) | `semantic.paper_mismatch` | Catalog title: `Step-Video-T2V: A State-of-the-Art Text-to-Video Model`; arXiv API & HF Papers API (`2502.10248`) returned: `Step-Video-T2V Technical Report: The Practice, Challenges, and Future of Video Foundation Model` (score=0.55). | **(a) Deterministic error** — paraphrased/marketing title in catalog instead of exact arXiv title. | **Fixed**: Update catalog title to exact canonical arXiv title (and set `published_at: "2025-02-14"`). |
| 4 | `20-video/wan2.1` (`data/video.jsonl:10`) | `semantic.paper_mismatch` | Catalog title: `Wan 2.1: Open-Source Video Foundation Model`; arXiv API & HF Papers API (`2503.20314`) returned: `Wan: Open and Advanced Large-Scale Video Generative Models` (score=0.59). | **(a) Deterministic error** — paraphrased/shortened title in catalog instead of exact arXiv title. | **Fixed**: Update catalog title to exact canonical arXiv title (and set `published_at: "2025-03-26"`, `orgs: ["Alibaba Wan"]`). |
| 5 | `30-3d-object-asset/squeeze3d` (`data/object_3d.jsonl:12`) | `semantic.paper_mismatch` | Catalog title: `Squeeze3D: Your 3D Generation Model is Secretly an Extreme Neural Compressor` (original v1 title); arXiv API (`2506.07932`) returned: `Squeeze3D: Extreme Neural Compression with Latent Space Bridging` (score=0.51). | **(a) Deterministic error** — stale v1 title after authors renamed paper on arXiv. | **Fixed**: Update catalog title to exact canonical arXiv title (and set `published_at: "2025-06-09"`). |
| 6 | `40-3d-scene/respace` (`data/scene_3d.jsonl:13`) | `semantic.paper_mismatch` | Catalog title: `ReSpace: Text-Driven 3D Scene Synthesis and Editing with Preference Alignment` (original v1 title); arXiv API (`2506.02459`) returned: `ReSpace: Text-Driven Autoregressive 3D Indoor Scene Synthesis and Editing` (score=0.75). | **(a) Deterministic error** — stale v1 title after authors renamed paper on arXiv. | **Fixed**: Update catalog title to exact canonical arXiv title (and set `published_at: "2025-06-03"`). |

---

## 3. Root Causes of Frequent CI / Scheduled Job Failures

1. **Network checks directly deciding scheduled CI exit code**: `weekly-link-check.yml` ends with `exit 1` whenever `validate_data.py --mode deep` finds any blocking error, turning the repository's Actions tab red on scheduled runs.
2. **Insufficient retry / backoff / rate limiting**:
   - `validate_data.py` uses only 2 retries with `min(2**attempt, 3)` (capped at 3s), no arXiv ≥3s request spacing, and no `ETag` / `If-Modified-Since` conditional caching.
   - `fetch_candidates.py` uses unencrypted `http://export.arxiv.org` with zero retries, zero backoff, and no inter-request delay.
3. **No two-pass confirmation (24h apart) or quarantine workflow**: A single deep validation run immediately treats any semantic/404 failure as fatal instead of confirming determinism across ≥24h, attempting auto-repair, and quarantining unresolved entries.
4. **Unpinned dependencies & missing pip cache**: No `requirements.txt` with pinned versions; workflows rely on whatever preinstalled packages exist on `ubuntu-latest`.
5. **Git push race conditions & trigger loops**: `daily.yml` and `weekly-link-check.yml` run `git commit && git push` directly without `git pull --rebase` or retry logic, and without `[skip ci]` on bot commits.
6. **Cron timing collision**: `weekly-link-check.yml` runs Monday 03:15 UTC, colliding with arXiv's Sunday/Monday UTC batch announcements and with Monday's weekly curation window.
7. **Generated-file drift undetected in `ci.yml`**: `ci.yml` runs `build.py` and then only `git diff --check` (whitespace check), NOT `git diff --exit-code`. Out-of-sync generated files can be merged without failing PR CI.
8. **Missing `GITHUB_TOKEN` / User-Agent consistency**: `fetch_candidates.py` and `validate_data.py` use inconsistent User-Agents (`3.0` vs `5.0`) and `validate_data.py` only reads `GH_TOKEN` (not falling back to `GITHUB_TOKEN`).
9. **60-day inactivity risk**: GitHub automatically disables scheduled (`cron`) workflows in repositories with no commits for 60 consecutive days; this was undocumented.

---

## 4. Known Content & Metadata Problems Identified

1. **Stale static "Editor's Picks"**:
   - The 5 homepage Editor's Picks (`iFSQ` 2026-01, `AssetFormer` 2026-02, `Anti-I2V` 2026-03, `FlowScene` 2026-03, `VectorWorld` 2026-03) are 8–10 months old, display no publication dates, and 4 of 5 lack organization metadata.
   - **Plan**: Remove static Editor's Picks from `README.md`, archive them to `weekly/hall-of-fame.md` with original dates, and replace the top of `README.md` with the auto-generated `<!-- WEEKLY:START --> ... <!-- WEEKLY:END -->` block.
2. **Misleading "Updated" badge**:
   - `scripts/build.py` sets `Updated` to `datetime.now(timezone.utc).strftime("%Y-%m-%d")` (build time), so the badge says `2026-11-22` even when homepage picks are from March 2026.
   - **Plan**: Set `Updated` badge to the latest weekly issue's `window.end` (real content date), use shields.io dynamic badge for repository stars, and add `freshness-watchdog.yml` to open/update a `stale-homepage` issue if `window.end` is >8 days old.
3. **Severe affiliation & date metadata gap**:
   - Only **12 / 207 (5.8%)** entries have `orgs` populated; **0 / 207 (0%)** have `published_at`.
   - Hard-coded org maps (`WATCH_ORGS`, `ORG_BADGE_META`, `REPO_OWNER_TO_ORG`) live inside `scripts/catalog_common.py` instead of a data file.
   - **Plan**: Move org normalization to `data/orgs.yml` and tiers to `data/org_tiers.yml`. Backfill verifiable orgs from exact repo owners (matching existing warnings) and mark remaining historical entries without verified orgs with `"affiliation_status": "unverified"` via a tested migration script — never fabricating affiliations.
