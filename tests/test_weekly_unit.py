from __future__ import annotations

import sys
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build as catalog_build  # noqa: E402
import catalog_common as common  # noqa: E402
import migrate_catalog as migrator  # noqa: E402
import quarantine as qmgr  # noqa: E402
import validate_data as validator  # noqa: E402
from weekly import score as wscore  # noqa: E402
from weekly import verify as wverify  # noqa: E402
from weekly import window as wwindow  # noqa: E402


class WindowTests(unittest.TestCase):
    def test_monday_morning_selects_previous_complete_week(self) -> None:
        now = datetime(2026, 11, 23, 2, 0, 0, tzinfo=timezone.utc)
        win = wwindow.previous_complete_week(now)
        self.assertEqual(win.week, "2026-W47")
        self.assertEqual(win.start.isoformat(), "2026-11-16")
        self.assertEqual(win.end.isoformat(), "2026-11-22")

    def test_sunday_235959_utc_does_not_close_current_week(self) -> None:
        now = datetime(2026, 11, 22, 23, 59, 59, tzinfo=timezone.utc)
        win = wwindow.previous_complete_week(now)
        self.assertEqual(win.week, "2026-W46")
        self.assertEqual(win.start.isoformat(), "2026-11-09")
        self.assertEqual(win.end.isoformat(), "2026-11-15")

    def test_year_spanning_iso_week(self) -> None:
        now = datetime(2026, 1, 5, 0, 0, 0, tzinfo=timezone.utc)
        win = wwindow.previous_complete_week(now)
        self.assertEqual(win.week, "2026-W01")
        self.assertEqual(win.start.isoformat(), "2025-12-29")
        self.assertEqual(win.end.isoformat(), "2026-01-04")
        self.assertTrue(wwindow.in_window("2025-12-29T00:00:00Z", win))
        self.assertTrue(wwindow.in_window("2026-01-04T23:59:59Z", win))
        self.assertFalse(wwindow.in_window("2025-12-28T23:59:59Z", win))
        self.assertFalse(wwindow.in_window("2026-01-05T00:00:00Z", win))


class ScoringAndSelectionTests(unittest.TestCase):
    def test_github_star_tier_boundaries(self) -> None:
        self.assertEqual(wscore.score_github_stars(0), 0)
        self.assertEqual(wscore.score_github_stars(29), 3)
        self.assertEqual(wscore.score_github_stars(30), 4)
        self.assertEqual(wscore.score_github_stars(99), 4)
        self.assertEqual(wscore.score_github_stars(100), 7)
        self.assertEqual(wscore.score_github_stars(299), 7)
        self.assertEqual(wscore.score_github_stars(300), 10)

    def test_anti_gaming_blocks_low_signals_plus_quality(self) -> None:
        self.assertFalse(wscore.is_eligible_for_selection({"signals": 10, "quality": 24}))
        self.assertTrue(wscore.is_eligible_for_selection({"signals": 15, "quality": 20}))

    def test_tiebreakers_and_no_padding(self) -> None:
        def make_item(iid: str, track: str, total: int, quality: int, openness: int, pub: str) -> dict:
            return {
                "id": iid,
                "title": iid,
                "track": track,
                "published_date": pub,
                "score": {
                    "total": total,
                    "signals": 20,
                    "quality": quality,
                    "openness": openness,
                    "institution": 10,
                    "fit": 8,
                    "evidence": [],
                },
            }

        items = [
            make_item("arxiv:2611.00001", "video", 80, 22, 18, "2026-11-18"),
            make_item("arxiv:2611.00002", "video", 80, 25, 15, "2026-11-17"),  # higher quality wins tie
            make_item("arxiv:2611.00003", "image-2d", 70, 20, 15, "2026-11-19"),  # notable (65-74)
        ]
        selected, honorable, empty_tracks, potw = wscore.select_weekly_picks(items)
        self.assertEqual(len(selected), 1)
        self.assertEqual(selected[0]["id"], "arxiv:2611.00002")
        self.assertEqual(potw, "arxiv:2611.00002")
        self.assertTrue(selected[0]["is_pick_of_the_week"])
        self.assertEqual(len(honorable), 1)
        self.assertEqual(honorable[0]["id"], "arxiv:2611.00003")
        self.assertEqual(set(empty_tracks), {"image-2d", "3d-object", "3d-scene", "4d-world"})


class NormalizationAndSimilarityTests(unittest.TestCase):
    def test_affiliation_normalization_from_orgs_yml(self) -> None:
        name, slug = common.normalize_org_name("Tencent-Hunyuan")
        self.assertEqual(name, "Tencent Hunyuan")
        self.assertEqual(slug, "tencent-hunyuan")

        name2, slug2 = common.normalize_org_name("MIT CSAIL")
        self.assertEqual(name2, "MIT")
        self.assertEqual(slug2, "mit")

    def test_title_similarity_threshold_090(self) -> None:
        ok, score = validator.title_matches(
            "Seedance 1.0: Exploring the Boundaries of Video Generation Models",
            "Seedance 1.0: Exploring the Boundaries of Video Generation Models",
        )
        self.assertTrue(ok)
        self.assertGreaterEqual(score, 0.90)

        ok_bad, score_bad = validator.title_matches(
            "Seedance 1.0: Exploring the Boundaries of Video Generation Models",
            "A Question Bank to Assess AI Inclusivity",
        )
        self.assertFalse(ok_bad)
        self.assertLess(score_bad, 0.90)


class ErrorTieringAndQuarantineTests(unittest.TestCase):
    def test_error_tiering(self) -> None:
        self.assertEqual(qmgr.classify_error_tier("network.paper.broken", 404), "BLOCKING")
        self.assertEqual(qmgr.classify_error_tier("network.repo.broken", 410), "BLOCKING")
        self.assertEqual(qmgr.classify_error_tier("network.paper.unknown", 403), "WARNING")
        self.assertEqual(qmgr.classify_error_tier("network.paper.unknown", 429), "WARNING")
        self.assertEqual(qmgr.classify_error_tier("network.paper.unknown", 503), "WARNING")

    def test_two_strike_24h_quarantine_and_repair(self) -> None:
        t0 = datetime(2026, 11, 20, 4, 0, tzinfo=timezone.utc)
        state = {"version": 1, "pending_strikes": {}, "entries": {}}
        obs = {"video/bad": {"reason_code": "network.paper.broken", "message": "HTTP 404"}}

        # Strike 1: goes to pending_strikes, NOT quarantined
        state, actions1 = qmgr.update_quarantine_state(state, observed_blocking=obs, now=t0)
        self.assertEqual(actions1["first_strike"], ["video/bad"])
        self.assertEqual(actions1["quarantined"], [])
        self.assertNotIn("video/bad", state["entries"])

        # Re-check 12h later (< 24h): still NOT quarantined
        state, actions2 = qmgr.update_quarantine_state(state, observed_blocking=obs, now=t0 + timedelta(hours=12))
        self.assertEqual(actions2["quarantined"], [])

        # Re-check 25h later (>= 24h) without repair: quarantined!
        state, actions3 = qmgr.update_quarantine_state(state, observed_blocking=obs, now=t0 + timedelta(hours=25))
        self.assertEqual(actions3["quarantined"], ["video/bad"])
        self.assertIn("video/bad", state["entries"])


class ReadmeIdempotencyAndMigrationTests(unittest.TestCase):
    def test_replace_weekly_block_is_idempotent(self) -> None:
        base = "Header\n<!-- WEEKLY:START -->\nold\n<!-- WEEKLY:END -->\nFooter\n"
        block = "<!-- WEEKLY:START -->\n## New Block\n<!-- WEEKLY:END -->"
        once = catalog_build.replace_weekly_block(base, block)
        twice = catalog_build.replace_weekly_block(once, block)
        self.assertEqual(once, twice)
        self.assertIn("Header\n", twice)
        self.assertIn("\nFooter\n", twice)

    def test_migration_backfills_verified_and_marks_unverified_without_fabricating(self) -> None:
        with_repo = {"id": "flux", "repo": "https://github.com/black-forest-labs/flux"}
        upd, changed = migrator.migrate_record(with_repo)
        self.assertTrue(changed)
        self.assertEqual(upd["orgs"], ["Black Forest Labs"])
        self.assertEqual(upd["affiliation_status"], "verified")

        # Idempotent on second run
        _, changed2 = migrator.migrate_record(upd)
        self.assertFalse(changed2)

        without_org = {"id": "unknown-paper", "paper": "https://arxiv.org/abs/2603.99999"}
        upd_u, changed_u = migrator.migrate_record(without_org)
        self.assertTrue(changed_u)
        self.assertNotIn("orgs", upd_u)
        self.assertEqual(upd_u["affiliation_status"], "unverified")


if __name__ == "__main__":
    unittest.main()
