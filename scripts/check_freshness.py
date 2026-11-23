#!/usr/bin/env python3
"""Freshness watchdog for Weekly Top Picks and README consistency.

Checks:
1. Whether the latest weekly issue's `window.end` is more than 8 days old.
2. Whether README.md's <!-- WEEKLY:START --> ... <!-- WEEKLY:END --> block is
   consistent with the latest file in data/weekly/.

Always exits 0 (scheduled watchdog must stay green; alerts go via GitHub Issue).
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from build import (
    WEEKLY_BLOCK_RE,
    load_weekly_issues,
    render_weekly_block,
)
from catalog_common import ROOT

DEFAULT_MAX_STALE_DAYS = 8


def check_freshness(
    *,
    root: Path = ROOT,
    today_utc: date | None = None,
    max_stale_days: int = DEFAULT_MAX_STALE_DAYS,
) -> dict[str, object]:
    today = today_utc or datetime.now(timezone.utc).date()
    issues = load_weekly_issues(root / "data" / "weekly")

    if not issues:
        return {
            "has_issue": False,
            "latest_week": "",
            "week_end": "",
            "days_since_end": 999,
            "is_stale": True,
            "readme_consistent": False,
            "reason": "No weekly issue found in data/weekly/.",
        }

    latest = issues[0]
    previous = issues[1] if len(issues) > 1 else None
    week_end = date.fromisoformat(latest["window"]["end"])
    days_since = (today - week_end).days
    is_stale = days_since > max_stale_days

    readme_path = root / "README.md"
    readme_text = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""
    expected_block = render_weekly_block(latest, previous)
    match = WEEKLY_BLOCK_RE.search(readme_text)
    readme_consistent = bool(match and match.group(0).strip() == expected_block.strip())

    reasons: list[str] = []
    if is_stale:
        reasons.append(
            f"Latest issue {latest['week']} ended on {week_end.isoformat()} ({days_since} days ago > {max_stale_days} days)."
        )
    if not readme_consistent:
        reasons.append(
            f"README.md WEEKLY block does not match data/weekly/{latest['week']}.json."
        )

    return {
        "has_issue": True,
        "latest_week": latest["week"],
        "week_end": week_end.isoformat(),
        "days_since_end": days_since,
        "is_stale": is_stale,
        "readme_consistent": readme_consistent,
        "reason": " ".join(reasons) if reasons else "Homepage is fresh and consistent.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Weekly Top Picks freshness and README consistency.")
    parser.add_argument("--max-stale-days", type=int, default=DEFAULT_MAX_STALE_DAYS)
    args = parser.parse_args()

    result = check_freshness(max_stale_days=args.max_stale_days)
    needs_alert = bool(result["is_stale"] or not result["readme_consistent"])

    output_file = os.environ.get("GITHUB_OUTPUT", "")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as fh:
            fh.write(f"needs_alert={'true' if needs_alert else 'false'}\n")
            fh.write(f"is_stale={'true' if result['is_stale'] else 'false'}\n")
            fh.write(f"readme_consistent={'true' if result['readme_consistent'] else 'false'}\n")
            fh.write(f"latest_week={result['latest_week']}\n")
            fh.write(f"week_end={result['week_end']}\n")
            fh.write(f"days_since_end={result['days_since_end']}\n")
            fh.write(f"reason={result['reason']}\n")

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as fh:
            fh.write("## Freshness Watchdog\n\n")
            fh.write(f"- Latest issue: `{result['latest_week'] or 'none'}` (end: `{result['week_end'] or '—'}`)\n")
            fh.write(f"- Days since `window.end`: **{result['days_since_end']}**\n")
            fh.write(f"- Stale (> {args.max_stale_days}d): **{result['is_stale']}**\n")
            fh.write(f"- README consistent: **{result['readme_consistent']}**\n")
            fh.write(f"- Status: {result['reason']}\n")

    print(f"[watchdog] needs_alert={needs_alert} | {result['reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
