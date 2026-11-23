# Operations & Troubleshooting Manual

This document explains how to operate, debug, and customize the self-healing Weekly Top Picks pipeline.

---

## 1. Workflow Architecture (4 Workflows)

| Workflow | Schedule / Trigger | Can Turn Red? | Purpose |
|:--|:--|:--:|:--|
| `ci.yml` | `pull_request`, non-bot `push` to `main` | **Yes (only workflow allowed to turn red)** | Offline unit + integration tests, `validate_data.py --skip-network`, `build.py`, internal link check, `git diff --exit-code` |
| `weekly-picks.yml` | Monday `02:00 UTC` + `workflow_dispatch` | **No** (alerts via `pipeline-failure` Issue) | Harvest → verify → score → select → temp-dir validate → atomic commit & push |
| `deep-validate.yml` | Wednesday `04:00 UTC` + `workflow_dispatch` | **No** (reports via `deep-validation` Issue + `$GITHUB_STEP_SUMMARY`) | Live link check, title similarity ≥ 0.90, 24h two-strike quarantine, GitHub star refresh |
| `freshness-watchdog.yml` | Daily `06:00 UTC` + `workflow_dispatch` | **No** (alerts via `stale-homepage` Issue) | Checks `window.end` age ≤ 8 days and README `WEEKLY` block consistency |

> **Important GitHub Actions Note (60-day inactivity rule):**  
> GitHub automatically disables `schedule` (`cron`) workflows in repositories with no commits for **60 consecutive days**. Because `weekly-picks.yml` and `deep-validate.yml` commit weekly updates, an active repository stays alive automatically. If a repository ever goes quiet for 60 days (e.g., all issues empty with no commits), re-enable scheduled workflows under **Actions → Select workflow → Enable workflow**, or trigger `weekly-picks.yml` via `workflow_dispatch`.

> **Important `GITHUB_TOKEN` Note:**  
> Commits pushed using `GITHUB_TOKEN` intentionally do **not** trigger `ci.yml` (GitHub's anti-loop protection). Therefore `weekly-picks.yml` runs unit tests, `validate_data.py --skip-network`, `build.py`, and `check_internal_links.py` **inside the same job** before committing.

---

## 2. How to Manually Re-Run Weekly Top Picks

### Via GitHub Actions UI
1. Open **Actions → `weekly-picks` → Run workflow**.
2. Optional inputs:
   - `week`: ISO week ID such as `2026-W47` (leave blank for previous complete calendar week).
   - `dry_run`: Set to `true` to inspect output in logs without committing.

### Locally
```bash
# Dry-run for a specific week (no files modified)
python scripts/weekly/pipeline.py --week 2026-W47 --dry-run

# Offline dry-run using only metadata/candidates/
python scripts/weekly/pipeline.py --week 2026-W47 --dry-run --offline

# Generate and rebuild pages locally
python scripts/weekly/pipeline.py --week 2026-W47
python scripts/build.py
python scripts/validate_data.py --skip-network
python scripts/check_internal_links.py
```

---

## 3. How Quarantine Works & How to Release an Entry

### How an Entry Enters Quarantine
1. `deep-validate.yml` runs every Wednesday with `--update-quarantine`.
2. Transient errors (`403`, `429`, `5xx`, timeout, DNS failure) are classified as **WARNING** and **never** quarantined.
3. Deterministic errors (`404`/`410` after 3 retries, arXiv title similarity `< 0.90`, repo README mismatch, deleted repo) are classified as **BLOCKING**:
   - **First observation**: Recorded in `metadata/quarantine/index.json` under `pending_strikes` with `first_detected_at`. Entry stays live.
   - **Second consecutive observation ≥ 24h later**: Pipeline attempts auto-repair; if still unresolved, entry moves to `entries` in `metadata/quarantine/index.json` with `reason_code`, `first_detected_at`, and `quarantined_at`.
   - `scripts/build.py` automatically excludes quarantined entries from `README.md` and track pages (`load_records(include_quarantined=False)`). No data is silently deleted from `data/*.jsonl`.

### How to Release an Entry from Quarantine
1. Fix the underlying root cause in `data/*.jsonl` (e.g., update dead URL or canonical arXiv title).
2. Remove the entry's key from `entries` (and `pending_strikes` if present) in `metadata/quarantine/index.json`.
3. Rebuild and validate:
   ```bash
   python scripts/validate_data.py --skip-network
   python scripts/build.py
   python scripts/check_internal_links.py
   ```
4. Open a PR; `ci.yml` will verify everything deterministically.

---

## 4. How to Adjust Thresholds, Organizations, and Tiers

- **Organization aliases & GitHub owner mapping**: Edit `data/orgs.yml` (never hard-code in Python).
- **Institution scoring tiers**: Edit `data/org_tiers.yml` (`tier1: 10`, `tier2: 6`, `other: 3`, `independent: 3`).
- **Track keywords & arXiv categories**: Edit `data/vocab.yml`.
- **Scoring thresholds**: Defined as constants at the top of `scripts/weekly/score.py`:
  - `TOP_PICK_THRESHOLD = 75`
  - `NOTABLE_THRESHOLD = 65`
  - `MIN_SIGNALS_PLUS_QUALITY = 35`
- **Freshness watchdog threshold**: Default `8` days in `.github/workflows/freshness-watchdog.yml` (`--max-stale-days 8`).

---

## 5. Secrets & Optional Configuration

| Secret / Variable | Required? | Purpose |
|:--|:--:|:--|
| `GITHUB_TOKEN` | Built-in | GitHub API rate limits, committing weekly updates, upserting deduplicated Issues |
| `LLM_API_KEY` (Secret) | Optional | Enables LLM rubric quality scoring & highlight generation (degrades to `heuristic` mode cleanly if absent) |
| `LLM_API_BASE` (Variable) | Optional | OpenAI-compatible base URL (defaults to `https://api.openai.com/v1`) |
| `LLM_MODEL` (Variable) | Optional | Model identifier (defaults to `gpt-4o-mini`) |
