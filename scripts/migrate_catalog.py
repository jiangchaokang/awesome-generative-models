#!/usr/bin/env python3
"""Idempotent migration script for historical data/*.jsonl records.

Responsibilities:
1. Backfill verifiable `orgs` ONLY from exact canonical GitHub repository owners
   defined in `data/orgs.yml` (never fabricating affiliations).
2. Normalize existing `orgs` entries via `data/orgs.yml`.
3. Set `affiliation_status` to `"verified"` if `orgs` is non-empty, or
   `"unverified"` if no verifiable affiliation exists.
4. Preserve blank lines, comments, and record ordering in `data/*.jsonl`.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from catalog_common import (
    FILE_ARTIFACT,
    ROOT,
    normalize_org_name,
    suggested_org_from_repo,
)


def migrate_record(
    record: dict[str, Any],
    *,
    orgs_path: Path | None = None,
) -> tuple[dict[str, Any], bool]:
    """Return (updated_record, changed)."""
    updated = dict(record)
    changed = False

    raw_orgs = updated.get("orgs")
    orgs_list: list[str] = []
    if isinstance(raw_orgs, list):
        orgs_list = [str(o).strip() for o in raw_orgs if str(o).strip()]
    elif isinstance(raw_orgs, str) and raw_orgs.strip():
        orgs_list = [raw_orgs.strip()]

    # Normalize existing org names via data/orgs.yml
    normalized_orgs: list[str] = []
    seen_slugs: set[str] = set()
    for org in orgs_list:
        canonical, slug = normalize_org_name(org, orgs_path=orgs_path)
        if canonical and slug not in seen_slugs:
            normalized_orgs.append(canonical)
            seen_slugs.add(slug)

    # Backfill from exact canonical GitHub repository owner if verifiable
    repo_url = str(updated.get("repo") or "").strip()
    if repo_url:
        suggested = suggested_org_from_repo(repo_url, orgs_path=orgs_path)
        if suggested:
            canonical, slug = normalize_org_name(suggested, orgs_path=orgs_path)
            if canonical and slug not in seen_slugs:
                normalized_orgs.append(canonical)
                seen_slugs.add(slug)

    if normalized_orgs:
        if updated.get("orgs") != normalized_orgs:
            updated["orgs"] = normalized_orgs
            changed = True
        if updated.get("affiliation_status") != "verified":
            updated["affiliation_status"] = "verified"
            changed = True
    else:
        if updated.get("affiliation_status") != "unverified":
            updated["affiliation_status"] = "unverified"
            changed = True

    return updated, changed


def migrate_jsonl_file(
    path: Path,
    *,
    orgs_path: Path | None = None,
    dry_run: bool = False,
) -> dict[str, int]:
    """Migrate a single JSONL file in-place (unless dry_run=True)."""
    stats = {"total": 0, "changed": 0, "verified": 0, "unverified": 0}
    if not path.exists():
        return stats

    out_lines: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            out_lines.append(line)
            continue

        record = json.loads(stripped)
        stats["total"] += 1
        updated, changed = migrate_record(record, orgs_path=orgs_path)
        if changed:
            stats["changed"] += 1
        if updated.get("affiliation_status") == "verified":
            stats["verified"] += 1
        else:
            stats["unverified"] += 1
        out_lines.append(json.dumps(updated, ensure_ascii=False, separators=(",", ":")))

    if not dry_run and stats["changed"] > 0:
        tmp = path.with_name(f".{path.name}.tmp")
        tmp.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
        tmp.replace(path)

    return stats


def migrate_all(
    root: Path | None = None,
    *,
    dry_run: bool = False,
) -> dict[str, dict[str, int]]:
    repo_root = root or ROOT
    data_dir = repo_root / "data"
    orgs_path = data_dir / "orgs.yml"
    summary: dict[str, dict[str, int]] = {}
    for file_name in FILE_ARTIFACT:
        summary[file_name] = migrate_jsonl_file(
            data_dir / file_name,
            orgs_path=orgs_path,
            dry_run=dry_run,
        )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Migrate historical data/*.jsonl metadata.")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files.")
    args = parser.parse_args()

    summary = migrate_all(dry_run=args.dry_run)
    total = sum(s["total"] for s in summary.values())
    changed = sum(s["changed"] for s in summary.values())
    verified = sum(s["verified"] for s in summary.values())
    unverified = sum(s["unverified"] for s in summary.values())
    mode = "DRY-RUN" if args.dry_run else "APPLIED"
    print(
        f"[migrate:{mode}] total={total} changed={changed} "
        f"verified={verified} unverified={unverified}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
