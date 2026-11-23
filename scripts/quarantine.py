#!/usr/bin/env python3
"""Two-strike (24h apart) error tiering, auto-repair, and quarantine manager.

Error tiering rules:
- BLOCKING (candidate for quarantine):
    Deterministic error that reproduces twice in a row, at least 24 hours apart:
    * 404/410 still failing after 3 retries
    * normalized similarity between title and arXiv title < 0.90
    * repository README/About does not match paper title or arXiv ID
    * repository deleted (404/410)
- WARNING (never quarantined):
    403 / 429 / 5xx / timeout / DNS failure / stale star cache
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable

BLOCKING_CODES = {
    "network.paper.broken",
    "network.repo.broken",
    "network.homepage.broken",
    "semantic.paper_mismatch",
    "semantic.repo_mismatch",
}

WARNING_CODES = {
    "network.paper.unknown",
    "network.repo.unknown",
    "network.homepage.unknown",
    "semantic.paper_unverified",
    "source.arxiv_api",
    "repository.archived",
    "stats.stale_cache",
}

MIN_CONFIRMATION_HOURS = 24.0


def classify_error_tier(code: str, http_status: int | None = None) -> str:
    """Classify a validation finding into BLOCKING or WARNING."""
    if http_status is not None:
        if http_status in {404, 410}:
            return "BLOCKING"
        if http_status in {403, 408, 425, 429, 500, 502, 503, 504}:
            return "WARNING"
    if code in BLOCKING_CODES:
        return "BLOCKING"
    return "WARNING"


def load_quarantine_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "updated_at": "", "pending_strikes": {}, "entries": {}}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload.setdefault("version", 1)
        payload.setdefault("pending_strikes", {})
        payload.setdefault("entries", {})
        return payload
    except (OSError, json.JSONDecodeError):
        return {"version": 1, "updated_at": "", "pending_strikes": {}, "entries": {}}


def save_quarantine_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f".{path.name}.tmp")
    tmp.write_text(
        json.dumps(state, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def _parse_iso(ts: str) -> datetime | None:
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00"))
    except ValueError:
        return None


def update_quarantine_state(
    state: dict[str, Any],
    *,
    observed_blocking: dict[str, dict[str, Any]],
    now: datetime | None = None,
    min_hours: float = MIN_CONFIRMATION_HOURS,
    repair_fn: Callable[[str, dict[str, Any]], dict[str, Any] | None] | None = None,
) -> tuple[dict[str, Any], dict[str, list[str]]]:
    """Apply two-strike 24h confirmation to observed deterministic blocking errors.

    Parameters
    ----------
    state:
        Current quarantine index dict.
    observed_blocking:
        Mapping of entry_key (e.g. ``"video/seedance"``) ->
        ``{"reason_code": str, "message": str, "record": dict}``.
    now:
        Current UTC datetime.
    min_hours:
        Minimum hours between first and second observation before quarantining.
    repair_fn:
        Optional callback ``(entry_key, info) -> repaired_fields | None``.
        If it returns a non-empty dict, the entry is marked repaired instead
        of quarantined.

    Returns
    -------
    (new_state, actions) where actions has keys:
        ``first_strike``, ``repaired``, ``quarantined``, ``cleared``.
    """
    current = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    now_iso = current.strftime("%Y-%m-%dT%H:%M:%SZ")

    pending = dict(state.get("pending_strikes") or {})
    entries = dict(state.get("entries") or {})
    actions: dict[str, list[str]] = {
        "first_strike": [],
        "repaired": [],
        "quarantined": [],
        "cleared": [],
    }

    # Clear pending strikes for entries that passed this run
    for key in list(pending.keys()):
        if key not in observed_blocking:
            pending.pop(key, None)
            actions["cleared"].append(key)

    for key, info in observed_blocking.items():
        if key in entries:
            entries[key]["last_seen_at"] = now_iso
            continue

        existing = pending.get(key)
        if not existing:
            pending[key] = {
                "reason_code": info.get("reason_code", "blocking"),
                "message": info.get("message", ""),
                "first_detected_at": now_iso,
                "last_detected_at": now_iso,
                "strikes": 1,
            }
            actions["first_strike"].append(key)
            continue

        first_dt = _parse_iso(existing.get("first_detected_at", ""))
        elapsed = (current - first_dt) if first_dt else timedelta(0)
        if elapsed < timedelta(hours=min_hours):
            existing["last_detected_at"] = now_iso
            existing["strikes"] = int(existing.get("strikes", 1)) + 1
            pending[key] = existing
            continue

        # Confirmed twice >= 24h apart: attempt auto-repair first
        repaired = repair_fn(key, info) if repair_fn else None
        if repaired:
            pending.pop(key, None)
            actions["repaired"].append(key)
            continue

        # Cannot repair: move to quarantine
        pending.pop(key, None)
        entries[key] = {
            "id": key,
            "reason_code": info.get("reason_code", existing.get("reason_code", "blocking")),
            "message": info.get("message", existing.get("message", "")),
            "first_detected_at": existing.get("first_detected_at", now_iso),
            "quarantined_at": now_iso,
            "last_seen_at": now_iso,
        }
        actions["quarantined"].append(key)

    new_state = {
        "version": 1,
        "updated_at": now_iso,
        "pending_strikes": pending,
        "entries": entries,
    }
    return new_state, actions
