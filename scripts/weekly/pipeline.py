#!/usr/bin/env python3
"""End-to-end Weekly Top Picks pipeline.

Flow:
  harvest -> verify (H1-H8) -> score (100pt rubric) -> select
  -> write to temp dir -> fast validate -> atomic replace (unless --dry-run).

On any unexpected error, preserves previous issue unchanged and exits cleanly
when --safe-exit is set (for scheduled workflow reliability).
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

# Ensure `scripts/` is on sys.path when invoked as `python scripts/weekly/pipeline.py`
SCRIPTS_DIR = Path(__file__).resolve().parents[1]
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from catalog_common import ROOT, normalize_whitespace
from validate_data import validate_weekly_issue_payload
from weekly.harvest import HttpClient, harvest_week, load_vocab
from weekly.score import load_org_tiers, score_candidate, select_weekly_picks
from weekly.verify import (
    TRACK_ORDER,
    load_existing_dedupe_keys,
    load_retracted_ids,
    verify_candidate,
)
from weekly.window import WeekWindow, parse_week_id, previous_complete_week

PENDING_MAX_WEEKS = 2


def load_pending(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return list(payload.get("entries") or [])
    except (OSError, json.JSONDecodeError):
        return []


def update_pending_entries(
    existing_pending: list[dict[str, Any]],
    new_pending: list[dict[str, Any]],
    *,
    now: datetime,
) -> list[dict[str, Any]]:
    """Keep unverified-affiliation candidates for at most 2 weeks (PENDING_MAX_WEEKS)."""
    cutoff = now - timedelta(weeks=PENDING_MAX_WEEKS)
    by_id: dict[str, dict[str, Any]] = {}

    for item in existing_pending:
        aid = str(item.get("arxiv_id") or "")
        first_seen = str(item.get("first_seen_at") or "")
        try:
            dt = datetime.fromisoformat(first_seen.replace("Z", "+00:00"))
        except ValueError:
            dt = now
        if aid and dt >= cutoff:
            by_id[aid] = item

    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    for item in new_pending:
        aid = str(item.get("arxiv_id") or "")
        if not aid:
            continue
        if aid in by_id:
            by_id[aid]["retries"] = int(by_id[aid].get("retries", 0)) + 1
            by_id[aid]["last_checked_at"] = now_iso
        else:
            by_id[aid] = {
                "arxiv_id": aid,
                "title": item.get("title", ""),
                "published_date": item.get("published_date", ""),
                "first_seen_at": now_iso,
                "last_checked_at": now_iso,
                "retries": 0,
                "reason_code": "H4_AFFILIATION_UNVERIFIED",
            }
    return sorted(by_id.values(), key=lambda x: x["arxiv_id"])


def build_weekly_issue(
    window: WeekWindow,
    candidates: list[dict[str, Any]],
    *,
    root: Path = ROOT,
    harvest_errors: list[str] | None = None,
    llm_caller: Callable[[str], dict[str, Any]] | None = None,
    now: datetime | None = None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    """Run verify -> score -> select over candidates and produce a schema-valid issue dict.

    Returns (issue_payload, pending_affiliation_candidates, rejected_log).
    """
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    now_iso = current.strftime("%Y-%m-%dT%H:%M:%SZ")

    vocab = load_vocab(root)
    org_tiers = load_org_tiers(root)
    orgs_path = root / "data" / "orgs.yml"
    existing_keys = load_existing_dedupe_keys(root)
    retracted_ids = load_retracted_ids(root)

    passed: list[tuple[dict[str, Any], dict[str, Any]]] = []
    pending_aff: list[dict[str, Any]] = []
    rejected_log: list[dict[str, Any]] = []

    for cand in candidates:
        res = verify_candidate(
            cand,
            window=window,
            vocab=vocab,
            existing_keys=existing_keys,
            retracted_ids=retracted_ids,
            orgs_path=orgs_path,
            checked_at=now_iso,
        )
        if res["status"] == "pass":
            passed.append((cand, res))
        elif res["status"] == "pending_affiliation":
            pending_aff.append(cand)
            rejected_log.append(
                {"arxiv_id": cand.get("arxiv_id"), "title": cand.get("title"), "reason_codes": res["reason_codes"]}
            )
        else:
            rejected_log.append(
                {"arxiv_id": cand.get("arxiv_id"), "title": cand.get("title"), "reason_codes": res["reason_codes"]}
            )

    all_hf_upvotes = [int(c.get("hf_upvotes", 0) or 0) for c, _ in passed]

    scored_items: list[dict[str, Any]] = []
    for cand, ver in passed:
        score_obj, highlight = score_candidate(
            cand,
            track=ver["track"],
            affiliations=ver["affiliations"],
            all_hf_upvotes=all_hf_upvotes,
            org_tiers=org_tiers,
            llm_caller=llm_caller,
        )
        links = cand.get("links") or {}
        gh = cand.get("github_meta") or {}
        authors = [normalize_whitespace(a) for a in (cand.get("authors") or []) if normalize_whitespace(a)]
        if not authors:
            authors = ["Unknown"]

        scored_items.append(
            {
                "id": f"arxiv:{cand['arxiv_id']}",
                "title": normalize_whitespace(str(cand.get("arxiv_api_title") or cand.get("title") or "")),
                "published_date": str(cand.get("published_date") or window.start.isoformat())[:10],
                "authors": authors,
                "affiliations": ver["affiliations"],
                "track": ver["track"],
                "links": {
                    "paper": links.get("paper") or f"https://arxiv.org/abs/{cand['arxiv_id']}",
                    "code": links.get("code") or None,
                    "project": links.get("project") or None,
                    "hf": links.get("hf") or None,
                },
                "stats": {
                    "github_stars": int(gh.get("stars", cand.get("github_stars", 0)) or 0),
                    "hf_upvotes": int(cand.get("hf_upvotes", 0) or 0),
                    "fetched_at": now_iso,
                },
                "venue": normalize_whitespace(str(cand.get("venue") or "arXiv")),
                "score": score_obj,
                "highlight": highlight,
                "verification": ver["verification"],
            }
        )

    selected_items, honorable, empty_tracks, pick_of_week_id = select_weekly_picks(scored_items)

    if not selected_items:
        status = "empty"
        reason_parts = [
            f"Evaluated {len(candidates)} candidate(s) in {window.start.isoformat()}..{window.end.isoformat()} UTC; "
            f"{len(passed)} passed hard gates H1-H8, {len(pending_aff)} pending affiliation verification."
        ]
        if harvest_errors:
            reason_parts.append("Degraded sources: " + "; ".join(harvest_errors) + ".")
        if honorable:
            reason_parts.append(f"{len(honorable)} notable work(s) scored 65-74 (below the 75 Top Pick bar).")
        else:
            reason_parts.append("No candidate cleared the ≥75 Top Pick threshold; tracks are not padded.")
        notes = " ".join(reason_parts)
    elif len(empty_tracks) > 0:
        status = "partial"
        notes = (
            f"Selected {len(selected_items)} Top Pick(s) across {len(TRACK_ORDER) - len(empty_tracks)}/5 tracks. "
            f"No qualifying pick (>=75) for: {', '.join(empty_tracks)}."
        )
        if harvest_errors:
            notes += " Degraded sources: " + "; ".join(harvest_errors) + "."
    else:
        status = "ok"
        notes = f"Selected {len(selected_items)} Top Picks across all 5 tracks."

    issue = {
        "week": window.week,
        "window": window.to_dict(),
        "generated_at": now_iso,
        "status": status,
        "pick_of_the_week_id": pick_of_week_id,
        "empty_tracks": empty_tracks,
        "items": selected_items,
        "honorable_mentions": honorable,
        "notes": notes,
    }
    return issue, pending_aff, rejected_log


def run_pipeline(
    *,
    week_id: str | None = None,
    dry_run: bool = False,
    offline: bool = False,
    root: Path = ROOT,
    client: HttpClient | None = None,
    llm_caller: Callable[[str], dict[str, Any]] | None = None,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Execute the complete weekly pipeline with temp-dir validation and atomic commit."""
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    window = parse_week_id(week_id) if week_id else previous_complete_week(current)

    candidates, harvest_errors = harvest_week(window, client=client, root=root, offline=offline)
    issue, pending_aff, rejected_log = build_weekly_issue(
        window,
        candidates,
        root=root,
        harvest_errors=harvest_errors,
        llm_caller=llm_caller,
        now=current,
    )

    # Validate in a temp directory before touching any repository files
    schema_path = root / "data" / "weekly" / "schema.json"
    with tempfile.TemporaryDirectory(prefix="weekly-picks-") as tmpdir:
        tmp_issue_path = Path(tmpdir) / f"{window.week}.json"
        serialized = json.dumps(issue, indent=2, ensure_ascii=False) + "\n"
        tmp_issue_path.write_text(serialized, encoding="utf-8")

        findings = validate_weekly_issue_payload(
            json.loads(tmp_issue_path.read_text(encoding="utf-8")),
            f"data/weekly/{window.week}.json",
            schema_path=schema_path,
        )
        errors = [f for f in findings if f.severity == "error"]
        if errors:
            raise RuntimeError(
                "Generated weekly issue failed schema validation: "
                + "; ".join(f.message for f in errors)
            )

        if not dry_run:
            weekly_dir = root / "data" / "weekly"
            weekly_dir.mkdir(parents=True, exist_ok=True)
            target_issue = weekly_dir / f"{window.week}.json"
            tmp_target = weekly_dir / f".{window.week}.json.tmp"
            tmp_target.write_text(serialized, encoding="utf-8")
            tmp_target.replace(target_issue)

            pending_path = weekly_dir / "pending.json"
            updated_pending = update_pending_entries(
                load_pending(pending_path),
                pending_aff,
                now=current,
            )
            tmp_pending = weekly_dir / ".pending.json.tmp"
            tmp_pending.write_text(
                json.dumps(
                    {
                        "version": 1,
                        "updated_at": current.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "max_retry_weeks": PENDING_MAX_WEEKS,
                        "entries": updated_pending,
                    },
                    indent=2,
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            tmp_pending.replace(pending_path)

    return {
        "issue": issue,
        "candidates_total": len(candidates),
        "pending_affiliation": len(pending_aff),
        "rejected": rejected_log,
        "harvest_errors": harvest_errors,
        "dry_run": dry_run,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Weekly Top Picks issue.")
    parser.add_argument("--week", default="", help="ISO week ID, e.g. 2026-W47 (default: previous complete week).")
    parser.add_argument("--dry-run", action="store_true", help="Do not write repository files; print JSON summary.")
    parser.add_argument("--offline", action="store_true", help="Use only local candidate inbox without network calls.")
    parser.add_argument("--output-summary", type=Path, default=None, help="Optional path to write JSON run summary.")
    args = parser.parse_args()

    result = run_pipeline(
        week_id=args.week or None,
        dry_run=args.dry_run,
        offline=args.offline,
    )
    issue = result["issue"]
    print(
        f"[weekly] week={issue['week']} status={issue['status']} "
        f"items={len(issue['items'])} honorable={len(issue['honorable_mentions'])} "
        f"candidates={result['candidates_total']} pending={result['pending_affiliation']} "
        f"dry_run={args.dry_run}"
    )
    if args.output_summary:
        args.output_summary.parent.mkdir(parents=True, exist_ok=True)
        args.output_summary.write_text(
            json.dumps(result, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    if args.dry_run:
        print(json.dumps(issue, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
