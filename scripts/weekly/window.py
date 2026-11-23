#!/usr/bin/env python3
"""Calendar week window calculation (Monday 00:00:00 to Sunday 23:59:59 UTC)."""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

WEEK_ID_RE = re.compile(r"^([0-9]{4})-W(0[1-9]|[1-4][0-9]|5[0-3])$")


@dataclass(frozen=True)
class WeekWindow:
    week: str
    start: date  # Monday UTC
    end: date    # Sunday UTC

    @property
    def start_dt(self) -> datetime:
        return datetime.combine(self.start, time(0, 0, 0), tzinfo=timezone.utc)

    @property
    def end_dt(self) -> datetime:
        return datetime.combine(self.end, time(23, 59, 59), tzinfo=timezone.utc)

    def to_dict(self) -> dict[str, str]:
        return {
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "tz": "UTC",
        }


def week_id_for_monday(monday: date) -> str:
    iso_year, iso_week, _ = monday.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def parse_week_id(week_id: str) -> WeekWindow:
    """Parse an ISO week string like '2026-W47' into its Monday..Sunday UTC window."""
    match = WEEK_ID_RE.fullmatch((week_id or "").strip())
    if not match:
        raise ValueError(f"Invalid ISO week identifier: {week_id!r} (expected YYYY-Www)")
    iso_year = int(match.group(1))
    iso_week = int(match.group(2))
    monday = date.fromisocalendar(iso_year, iso_week, 1)
    sunday = monday + timedelta(days=6)
    return WeekWindow(week=f"{iso_year}-W{iso_week:02d}", start=monday, end=sunday)


def previous_complete_week(now_utc: datetime | None = None) -> WeekWindow:
    """Return the previous complete calendar week (Monday 00:00 to Sunday 23:59:59 UTC).

    Examples:
    - Monday 2026-11-23 02:00 UTC -> 2026-W47 (2026-11-16 .. 2026-11-22)
    - Sunday 2026-11-22 23:59:59 UTC -> 2026-W46 (2026-11-09 .. 2026-11-15)
      because 2026-W47 has not yet ended!
    - Monday 2026-01-05 00:00:00 UTC -> 2026-W01 (2025-12-29 .. 2026-01-04)
      (year-spanning ISO week).
    """
    current = (now_utc or datetime.now(timezone.utc)).astimezone(timezone.utc)
    today = current.date()
    current_monday = today - timedelta(days=today.weekday())
    prev_monday = current_monday - timedelta(days=7)
    prev_sunday = prev_monday + timedelta(days=6)
    return WeekWindow(
        week=week_id_for_monday(prev_monday),
        start=prev_monday,
        end=prev_sunday,
    )


def parse_utc_datetime(value: str | date | datetime) -> datetime | None:
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, date):
        return datetime.combine(value, time(12, 0, 0), tzinfo=timezone.utc)
    text = (value or "").strip()
    if not text:
        return None
    if re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", text):
        return datetime.combine(date.fromisoformat(text), time(12, 0, 0), tzinfo=timezone.utc)
    try:
        dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def in_window(published_at: str | date | datetime, window: WeekWindow) -> bool:
    """True iff the v1 publication timestamp falls within [start 00:00:00, end 23:59:59] UTC."""
    dt = parse_utc_datetime(published_at)
    if dt is None:
        return False
    return window.start_dt <= dt <= window.end_dt
