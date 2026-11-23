# Weekly Top Picks Selection Rubric

> Implementation: `scripts/weekly/harvest.py`, `scripts/weekly/verify.py`, `scripts/weekly/score.py`, `scripts/weekly/pipeline.py`  
> Configuration: `data/vocab.yml`, `data/orgs.yml`, `data/org_tiers.yml`, `data/weekly/schema.json`

---

## 1. Window Definition

Each weekly issue covers strictly the **previous complete calendar week in UTC**:

- Start: **Monday 00:00:00 UTC**
- End: **Sunday 23:59:59 UTC**
- Qualifying date: **arXiv v1 submission date** (`published_date`), i.e., when the work was first made public — never v2 updates and never conference acceptance dates.
- Year-spanning ISO weeks (e.g., `2026-W01`: `2025-12-29 → 2026-01-04`) are handled via ISO-8601 calendar arithmetic (`scripts/weekly/window.py`).

---

## 2. Multi-Source Candidate Harvesting (Redundant & Degradable)

Failure of any single external source degrades gracefully and never aborts the pipeline:

| Source | Purpose | Tested Status (2026-11-23) | Degradation Behavior |
|:--|:--|:--|:--|
| `metadata/candidates/YYYY-MM-DD/` | Local daily candidate inbox (reused, not re-fetched) | Local disk (always available) | Always loaded first |
| arXiv API (`https://export.arxiv.org/api/query`) | Primary v1 date, exact title, authors, abstract (`cs.CV/GR/LG/AI/RO`, `data/vocab.yml`) | Enforces ≥3s spacing; 429 on bursty shared IP | ≥3.1s inter-request spacing + 3 retries w/ backoff; degrades to inbox + HF |
| Hugging Face Daily Papers (`https://huggingface.co/api/daily_papers`) | Upvotes, verified repo/project links, organization | **HTTP 200 OK** | Skipped with warning logged if unavailable |
| GitHub API (`https://api.github.com/repos/{owner}/{repo}`) | Stars, license, repo size, README for H6 identity | **HTTP 200 OK** (uses `GITHUB_TOKEN`) | Skipped if rate-limited; stars default to 0 |
| OpenAlex (`https://api.openalex.org/works`) | Auxiliary author affiliations | **HTTP 200 OK** (shared free daily budget) | Auxiliary only; skipped on error |
| Semantic Scholar / OpenReview | Auxiliary affiliations / venue status | **429 / 403** without key / bot challenge | Auxiliary only; never blocks pipeline |

---

## 3. Hard Gates (H1–H8)

Every candidate must pass **all 8 gates**. Failing any gate eliminates the candidate with an explicit `reason_code`:

| Gate | Rule | Reason Code |
|:--|:--|:--|
| **H1** | arXiv v1 submission timestamp is within `[window.start 00:00:00, window.end 23:59:59]` UTC | `H1_OUT_OF_WINDOW` |
| **H2** | Belongs to one of the 5 tracks (`image-2d`, `video`, `3d-object`, `3d-scene`, `4d-world`) and core contribution is a generative model (pure surveys/benchmarks/analyses excluded) | `H2_NON_GENERATIVE` |
| **H3** | arXiv ID is resolvable and normalized title similarity vs arXiv API title is **≥ 0.90** | `H3_TITLE_MISMATCH` |
| **H4** | Affiliation verified: consistent across **≥ 2 independent sources**, OR directly locatable in the paper's first-page text with evidence (`url` + verbatim `quote` ≤ 25 words). Candidates failing **only H4** go to `data/weekly/pending.json` (retried up to 2 weeks) and are not shown on the homepage. | `H4_AFFILIATION_UNVERIFIED` |
| **H5** | At least one verifiable primary-source link (official code / project page / official technical report page) | `H5_NO_PRIMARY_LINK` |
| **H6** | If a code link exists, it must pass identity verification: appears on arXiv abstract / paper body / HF paper page, OR repository README/description contains paper title or arXiv ID | `H6_CODE_IDENTITY_FAIL` |
| **H7** | Not a duplicate of any existing entry in `data/*.jsonl` or prior `data/weekly/*.json` (by arXiv ID, normalized title, or canonical repo URL) | `H7_DUPLICATE` |
| **H8** | Not on the retraction / security-issue list (`metadata/retracted.json`) and not withdrawn on arXiv | `H8_RETRACTED` |

---

## 4. 100-Point Scoring Rubric

Threshold: **≥ 75 = Top Pick** · **65–74 = Honorable Mention (`Notable`)** · **< 65 = Not listed**. Every scored item carries verifiable evidence (`url` + verbatim `quote` ≤ 25 words).

| Dimension | Max | Rules |
|:--|:--:|:--|
| **External signals** (`signals`) | 30 | Weekly HF upvote percentile (0–10) + GitHub star growth within 1 week (`≥300 → 10`, `100–299 → 7`, `30–99 → 4`, else linear 0–3) + third-party adoption / official blog / top-conference oral·spotlight (0–10) |
| **Research quality** (`quality`) | 30 | Novelty (0–10) + Experimental thoroughness (0–10) + Quantified gains (0–10). Scored by LLM per rubric with mandatory verbatim quotes; **missing or ungrounded evidence = 0 points** |
| **Openness** (`openness`) | 20 | Open-source non-empty repo (8) + pretrained weights/checkpoints (6) + project page or demo (3) + explicit license (3) |
| **Institution** (`institution`) | 10 | Configurable in `data/org_tiers.yml`: Tier1 = 10, Tier2 = 6, other = 3, independent = 3. Capped at 10 |
| **Scope & impact** (`fit`) | 10 | Direct contribution to the 5 tracks and transferability |

### Anti-Gaming & Selection Rules

1. **No prestige bypass**: If `signals + quality < 35`, the work is **never selected**, regardless of institution tier.
2. **Tiebreakers** (in order): `quality` → `openness` → more recent `published_date`.
3. **No padding**: At most **1 Pick of the Week** (🏆, highest score across all tracks) + at most **1 Top Pick per track**. Tracks with no candidate scoring ≥ 75 are explicitly marked `"No qualifying pick this week"`.
4. **Empty week honesty**: If all 5 tracks are empty, `status: "empty"` is recorded; the homepage shows the current week's heading, explains why, and links to the previous issue instead of silently displaying stale content.

---

## 5. LLM Usage Boundaries & Degradation

- **Allowed**: Rubric quality scoring (with verbatim quoted evidence ≤ 25 words from fetched source text) and writing the ≤ 30-word highlight from the abstract.
- **Forbidden**: The LLM must **never** generate or guess dates, authors, affiliations, links, star counts, or conference acceptance status.
- **Fallback**: If `LLM_API_KEY` is unset, times out, or returns invalid JSON, the pipeline automatically degrades to an extractive highlight (first sentence of abstract, ≤ 30 words) + deterministic heuristic quality estimation marked `quality_mode: "heuristic"`. The pipeline never fails due to LLM unavailability.
