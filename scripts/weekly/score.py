#!/usr/bin/env python3
"""100-point rubric scoring, anti-gaming rules, LLM boundary, and weekly selection.

Scoring rubric (100 points total; >= 75 => Top Pick; 65-74 => Honorable Mention / Notable):
- External signals (0-30):
    * HF upvote percentile for the week: 0-10
    * GitHub star growth within one week: >=300 -> 10, 100-299 -> 7, 30-99 -> 4, else linear 0-3
    * Third-party adoption / official blog / top-conference oral/spotlight: 0-10
- Research quality (0-30):
    * Novelty (0-10) + Experimental thoroughness (0-10) + Quantified gains (0-10)
    * LLM rubric scoring MUST cite verbatim source evidence (<=25 words); missing evidence => 0.
    * When LLM is unavailable/times out/unconfigured: deterministic heuristic fallback
      marked `quality_mode: "heuristic"`. Pipeline never fails.
- Openness (0-20):
    * Code open-sourced and non-empty repo: 8
    * Weights/checkpoints available: 6
    * Project page or demo: 3
    * Explicit license: 3
- Institution (0-10):
    * Loaded from `data/org_tiers.yml` (Tier1=10, Tier2=6, other=3, independent=3). Capped at 10.
- Scope & impact (0-10):
    * Direct contribution to the 5 tracks + transferability.

Anti-gaming rules:
- `signals + quality < 35` => NEVER selected, regardless of institution tier.
- Tiebreakers: (quality, openness, published_date) descending.
- Weekly selection: <=1 Pick of the Week (highest overall) + <=1 per track. No padding.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Callable
from urllib.request import Request, urlopen

import yaml

from catalog_common import ROOT, normalize_whitespace
from weekly.verify import TRACK_ORDER, truncate_quote

TOP_PICK_THRESHOLD = 75
NOTABLE_THRESHOLD = 65
MIN_SIGNALS_PLUS_QUALITY = 35
MAX_HIGHLIGHT_WORDS = 30

NOVELTY_PATTERNS = (
    "first",
    "novel",
    "new paradigm",
    "unified framework",
    "introduce",
    "propose",
)
EXPERIMENT_PATTERNS = (
    "benchmark",
    "ablation",
    "extensive experiments",
    "outperforms",
    "baselines",
    "state-of-the-art",
    "sota",
)
QUANTIFIED_GAIN_RE = re.compile(
    r"(?:\b\d+(?:\.\d+)?\s*(?:%|x|×|fps|ms|db|fid|fvd|psnr|ssim)\b|\b\d+(?:\.\d+)?\s*times\s+faster\b)",
    re.IGNORECASE,
)


def load_org_tiers(root: Path = ROOT) -> dict[str, Any]:
    path = root / "data" / "org_tiers.yml"
    if not path.exists():
        return {"points": {"tier1": 10, "tier2": 6, "other": 3, "independent": 3}, "tier1": [], "tier2": [], "independent": []}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def score_github_stars(stars: int) -> int:
    s = max(0, int(stars or 0))
    if s >= 300:
        return 10
    if s >= 100:
        return 7
    if s >= 30:
        return 4
    return min(3, round(4.0 * s / 30.0))


def score_hf_upvotes_percentile(upvotes: int, all_upvotes: list[int]) -> int:
    u = max(0, int(upvotes or 0))
    if u == 0 or not all_upvotes:
        return 0
    positive = [x for x in all_upvotes if x > 0]
    if not positive:
        return 0
    if len(positive) == 1:
        return 10 if u >= 30 else min(9, max(2, round(10 * u / 30.0)))
    below_or_eq = sum(1 for x in positive if x <= u)
    pct = below_or_eq / len(positive)
    return min(10, max(1, round(pct * 10)))


def score_adoption_and_venue(candidate: dict[str, Any]) -> tuple[int, list[dict[str, str]]]:
    points = 0
    evidence: list[dict[str, str]] = []
    venue = str(candidate.get("venue") or "")
    paper_url = (candidate.get("links") or {}).get("paper") or "https://arxiv.org"
    venue_lower = venue.lower()
    if any(k in venue_lower for k in ("oral", "best paper")):
        points += 6
        evidence.append({"url": paper_url, "quote": truncate_quote(f"Venue recognition: {venue}")})
    elif "spotlight" in venue_lower:
        points += 4
        evidence.append({"url": paper_url, "quote": truncate_quote(f"Venue recognition: {venue}")})
    elif any(k in venue_lower for k in ("cvpr", "iccv", "eccv", "iclr", "neurips", "icml", "siggraph")):
        points += 3
        evidence.append({"url": paper_url, "quote": truncate_quote(f"Accepted at venue: {venue}")})

    if candidate.get("official_blog_url"):
        points += 4
        evidence.append({"url": str(candidate["official_blog_url"]), "quote": "Official research blog announcement"})
    if candidate.get("third_party_adoption"):
        points += 4
        evidence.append({"url": paper_url, "quote": truncate_quote(str(candidate["third_party_adoption"]))})

    return min(10, points), evidence


def score_openness(candidate: dict[str, Any]) -> tuple[int, list[dict[str, str]]]:
    links = candidate.get("links") or {}
    gh = candidate.get("github_meta") or {}
    abstract_lower = str(candidate.get("abstract") or "").lower()
    readme_lower = str(gh.get("readme") or "").lower()
    points = 0
    evidence: list[dict[str, str]] = []

    code_url = links.get("code")
    if code_url and int(gh.get("size", 1) or 0) > 0:
        points += 8
        evidence.append({"url": code_url, "quote": "Public non-empty code repository verified"})

    has_weights = (
        bool(candidate.get("has_weights"))
        or any(k in readme_lower for k in ("huggingface.co", "checkpoint", "weights", "pretrained model"))
        or any(k in abstract_lower for k in ("pretrained weights", "checkpoints", "model weights"))
    )
    if has_weights:
        points += 6
        evidence.append({"url": code_url or links.get("paper") or "https://arxiv.org", "quote": "Pretrained weights or checkpoints referenced"})

    if links.get("project") or links.get("hf"):
        points += 3
        evidence.append({"url": links.get("project") or links.get("hf"), "quote": "Project page or interactive demo link available"})

    lic = str(gh.get("license") or candidate.get("license") or "").strip()
    if lic and lic.upper() != "NOASSERTION":
        points += 3
        evidence.append({"url": code_url or links.get("paper") or "https://arxiv.org", "quote": f"Explicit license: {lic}"})

    return min(20, points), evidence


def score_institution(affiliations: list[dict[str, Any]], tiers: dict[str, Any]) -> int:
    pts_cfg = tiers.get("points") or {"tier1": 10, "tier2": 6, "other": 3, "independent": 3}
    t1 = set(tiers.get("tier1") or [])
    t2 = set(tiers.get("tier2") or [])
    indep = set(tiers.get("independent") or ["independent"])

    best = 0
    for aff in affiliations:
        slug = str(aff.get("normalized") or "").lower()
        if slug in t1:
            best = max(best, int(pts_cfg.get("tier1", 10)))
        elif slug in t2:
            best = max(best, int(pts_cfg.get("tier2", 6)))
        elif slug in indep:
            best = max(best, int(pts_cfg.get("independent", 3)))
        elif slug:
            best = max(best, int(pts_cfg.get("other", 3)))
    return min(10, best)


def score_fit(candidate: dict[str, Any], track: str) -> int:
    if track not in TRACK_ORDER:
        return 0
    combined = f"{candidate.get('title', '')} {candidate.get('abstract', '')}".lower()
    points = 6
    if any(k in combined for k in ("foundation model", "scalable", "generalizable", "open-source", "real-time", "interactive", "closed-loop")):
        points += 2
    if any(k in combined for k in ("zero-shot", "unified", "controllable", "long-horizon", "high-resolution")):
        points += 2
    return min(10, points)


def _find_sentence_with(text: str, matcher: Callable[[str], bool]) -> str:
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", normalize_whitespace(text)) if s.strip()]
    for sent in sentences:
        if matcher(sent):
            return truncate_quote(sent)
    return ""


def heuristic_quality_score(candidate: dict[str, Any]) -> tuple[int, list[dict[str, str]], str]:
    """Deterministic fallback when LLM is unavailable. Always attaches verbatim quotes."""
    abstract = normalize_whitespace(str(candidate.get("abstract") or ""))
    paper_url = (candidate.get("links") or {}).get("paper") or "https://arxiv.org"
    evidence: list[dict[str, str]] = []

    # Novelty (0-10)
    nov_quote = _find_sentence_with(abstract, lambda s: any(p in s.lower() for p in NOVELTY_PATTERNS))
    novelty = 7 if nov_quote else 0
    if nov_quote:
        evidence.append({"url": paper_url, "quote": nov_quote})

    # Experimental thoroughness (0-10)
    exp_quote = _find_sentence_with(abstract, lambda s: any(p in s.lower() for p in EXPERIMENT_PATTERNS))
    experiments = 8 if exp_quote else 0
    if exp_quote:
        evidence.append({"url": paper_url, "quote": exp_quote})

    # Quantified gains (0-10)
    gain_quote = _find_sentence_with(abstract, lambda s: bool(QUANTIFIED_GAIN_RE.search(s)))
    gains = 8 if gain_quote else 0
    if gain_quote:
        evidence.append({"url": paper_url, "quote": gain_quote})

    return min(30, novelty + experiments + gains), evidence, "heuristic"


def extractive_highlight(abstract: str, max_words: int = MAX_HIGHLIGHT_WORDS) -> str:
    cleaned = normalize_whitespace(abstract)
    if not cleaned:
        return "Generative modeling work verified from primary arXiv submission."
    first_sentence = re.split(r"(?<=[.!?])\s+", cleaned)[0].strip()
    words = first_sentence.split()
    if len(words) <= max_words:
        return first_sentence
    return " ".join(words[:max_words]).rstrip(",;:") + "…"


def llm_quality_and_highlight(
    candidate: dict[str, Any],
    *,
    llm_caller: Callable[[str], dict[str, Any]] | None = None,
) -> tuple[int, list[dict[str, str]], str, str]:
    """Call LLM ONLY for rubric quality scoring (with mandatory quoted evidence)
    and <=30-word highlight. Falls back cleanly to deterministic heuristic on any error."""
    abstract = normalize_whitespace(str(candidate.get("abstract") or ""))
    paper_url = (candidate.get("links") or {}).get("paper") or "https://arxiv.org"

    api_key = os.environ.get("LLM_API_KEY", "").strip() or os.environ.get("OPENAI_API_KEY", "").strip()
    if llm_caller is None and not api_key:
        q_score, q_ev, q_mode = heuristic_quality_score(candidate)
        return q_score, q_ev, q_mode, extractive_highlight(abstract)

    prompt = (
        "Score this paper's research quality on three 0-10 axes (novelty, experiments, gains) "
        "ONLY from the provided abstract. Each axis MUST include a verbatim quote (<=25 words) "
        "from the abstract. Also write a <=30-word extractive highlight. "
        "Return JSON: {novelty:{score,quote}, experiments:{score,quote}, gains:{score,quote}, highlight}."
        f"\nTitle: {candidate.get('title', '')}\nAbstract: {abstract}"
    )

    try:
        if llm_caller is not None:
            parsed = llm_caller(prompt)
        else:
            endpoint = os.environ.get("LLM_API_BASE", "https://api.openai.com/v1").rstrip("/") + "/chat/completions"
            model = os.environ.get("LLM_MODEL", "gpt-4o-mini")
            body = json.dumps(
                {
                    "model": model,
                    "temperature": 0,
                    "response_format": {"type": "json_object"},
                    "messages": [{"role": "user", "content": prompt}],
                }
            ).encode("utf-8")
            req = Request(
                endpoint,
                data=body,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
            with urlopen(req, timeout=15) as resp:
                raw = json.loads(resp.read().decode("utf-8"))
            content = raw["choices"][0]["message"]["content"]
            parsed = json.loads(content)

        if not isinstance(parsed, dict):
            raise ValueError("LLM response is not a JSON object")

        total_q = 0
        evidence: list[dict[str, str]] = []
        abs_lower = abstract.lower()
        for axis in ("novelty", "experiments", "gains"):
            sub = parsed.get(axis) or {}
            quote = truncate_quote(str(sub.get("quote") or ""))
            # Hard rule: missing or ungrounded evidence => 0 points for this axis
            if not quote or quote.lower()[:20] not in abs_lower:
                continue
            pts = max(0, min(10, int(sub.get("score", 0) or 0)))
            total_q += pts
            evidence.append({"url": paper_url, "quote": quote})

        hl = normalize_whitespace(str(parsed.get("highlight") or ""))
        if not hl or len(hl.split()) > MAX_HIGHLIGHT_WORDS:
            hl = extractive_highlight(abstract)
        return min(30, total_q), evidence, "llm", hl

    except Exception:
        q_score, q_ev, q_mode = heuristic_quality_score(candidate)
        return q_score, q_ev, q_mode, extractive_highlight(abstract)


def score_candidate(
    candidate: dict[str, Any],
    *,
    track: str,
    affiliations: list[dict[str, Any]],
    all_hf_upvotes: list[int],
    org_tiers: dict[str, Any],
    llm_caller: Callable[[str], dict[str, Any]] | None = None,
) -> tuple[dict[str, Any], str]:
    """Compute full 100-point score breakdown and highlight for a verified candidate."""
    gh_stars = int((candidate.get("github_meta") or {}).get("stars", candidate.get("github_stars", 0)) or 0)
    hf_upvotes = int(candidate.get("hf_upvotes", 0) or 0)

    hf_pts = score_hf_upvotes_percentile(hf_upvotes, all_hf_upvotes)
    star_pts = score_github_stars(gh_stars)
    adopt_pts, adopt_ev = score_adoption_and_venue(candidate)
    signals = min(30, hf_pts + star_pts + adopt_pts)

    quality, quality_ev, quality_mode, highlight = llm_quality_and_highlight(
        candidate,
        llm_caller=llm_caller,
    )
    openness, openness_ev = score_openness(candidate)
    institution = score_institution(affiliations, org_tiers)
    fit = score_fit(candidate, track)

    total = signals + quality + openness + institution + fit
    evidence = [*adopt_ev, *quality_ev, *openness_ev]

    score_obj = {
        "total": total,
        "signals": signals,
        "quality": quality,
        "openness": openness,
        "institution": institution,
        "fit": fit,
        "quality_mode": quality_mode,
        "evidence": evidence,
    }
    return score_obj, highlight


def is_eligible_for_selection(score_obj: dict[str, Any]) -> bool:
    """Anti-gaming gate: signals + quality must be >= 35."""
    return (score_obj["signals"] + score_obj["quality"]) >= MIN_SIGNALS_PLUS_QUALITY


def select_weekly_picks(
    scored_items: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], str | None]:
    """Select Top Picks (>=75) and Honorable Mentions (65-74) with anti-gaming & tiebreakers.

    Rules:
    - Anti-gaming: `signals + quality < 35` -> never selected.
    - Tiebreakers: (total, quality, openness, published_date) descending.
    - At most 1 Pick of the Week (highest overall) + at most 1 per track.
    - No padding for tracks without a >=75 pick.
    Returns (selected_items, honorable_mentions, empty_tracks, pick_of_the_week_id).
    """
    eligible = [item for item in scored_items if is_eligible_for_selection(item["score"])]

    def sort_key(item: dict[str, Any]) -> tuple[Any, ...]:
        sc = item["score"]
        return (-sc["total"], -sc["quality"], -sc["openness"], item.get("published_date", ""), item.get("id", ""))

    # Sort descending (for published_date we invert properly using reverse=True on tuple)
    eligible.sort(
        key=lambda item: (
            item["score"]["total"],
            item["score"]["quality"],
            item["score"]["openness"],
            item.get("published_date", ""),
        ),
        reverse=True,
    )

    top_pool = [item for item in eligible if item["score"]["total"] >= TOP_PICK_THRESHOLD]
    notable_pool = [
        item
        for item in eligible
        if NOTABLE_THRESHOLD <= item["score"]["total"] < TOP_PICK_THRESHOLD
    ]

    selected_by_track: dict[str, dict[str, Any]] = {}
    for item in top_pool:
        track = item["track"]
        if track not in selected_by_track:
            chosen = dict(item)
            chosen["tier"] = "top-pick"
            chosen["is_pick_of_the_week"] = False
            selected_by_track[track] = chosen

    selected_items = list(selected_by_track.values())
    selected_items.sort(
        key=lambda item: (
            item["score"]["total"],
            item["score"]["quality"],
            item["score"]["openness"],
            item.get("published_date", ""),
        ),
        reverse=True,
    )

    pick_of_the_week_id: str | None = None
    if selected_items:
        selected_items[0]["is_pick_of_the_week"] = True
        pick_of_the_week_id = selected_items[0]["id"]

    empty_tracks = [t for t in TRACK_ORDER if t not in selected_by_track]

    honorable: list[dict[str, Any]] = []
    for item in notable_pool[:10]:
        hm = dict(item)
        hm["tier"] = "notable"
        hm["is_pick_of_the_week"] = False
        honorable.append(hm)

    return selected_items, honorable, empty_tracks, pick_of_the_week_id
