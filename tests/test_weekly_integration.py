from __future__ import annotations

import json
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build as catalog_build  # noqa: E402
import validate_data as validator  # noqa: E402
from weekly.harvest import HttpClient, HttpResponse  # noqa: E402
from weekly.pipeline import run_pipeline  # noqa: E402


def _make_workspace(tmpdir: Path) -> Path:
    """Create an isolated mini-workspace with real orgs/tiers/vocab/schema."""
    (tmpdir / "data" / "weekly").mkdir(parents=True)
    (tmpdir / "metadata" / "candidates").mkdir(parents=True)
    for fname in ("orgs.yml", "org_tiers.yml", "vocab.yml"):
        (tmpdir / "data" / fname).write_text(
            (ROOT / "data" / fname).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
    (tmpdir / "data" / "weekly" / "schema.json").write_text(
        (ROOT / "data" / "weekly" / "schema.json").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    # Seed one existing paper for duplicate test (Scenario 7)
    (tmpdir / "data" / "video.jsonl").write_text(
        json.dumps(
            {
                "id": "existing-vid",
                "title": "Existing Video Generator",
                "venue": "arXiv 2026",
                "task": "text-to-video",
                "summary": "An existing video generation model in the catalog.",
                "paper": "https://arxiv.org/abs/2611.99999",
                "repo": "https://github.com/Tencent-Hunyuan/ExistingVid",
                "open_source": True,
            }
        )
        + "\n",
        encoding="utf-8",
    )
    (tmpdir / "README.md").write_text(
        "# Title\n\n<!-- WEEKLY:START -->\nold\n<!-- WEEKLY:END -->\n\n## Footer\n",
        encoding="utf-8",
    )
    return tmpdir


def _arxiv_atom(entries: list[dict]) -> bytes:
    parts = ['<?xml version="1.0" encoding="UTF-8"?><feed xmlns="http://www.w3.org/2005/Atom">']
    for e in entries:
        authors_xml = "".join(f"<author><name>{a}</name></author>" for a in e["authors"])
        parts.append(
            f"<entry><id>https://arxiv.org/abs/{e['id']}v1</id>"
            f"<published>{e['published']}</published>"
            f"<title>{e['title']}</title>"
            f"<summary>{e['abstract']}</summary>{authors_xml}</entry>"
        )
    parts.append("</feed>")
    return "".join(parts).encode("utf-8")


class WeeklyIntegrationTests(unittest.TestCase):
    """7 required offline integration scenarios using recorded HTTP fixtures."""

    def _run_and_assert_valid(
        self,
        ws: Path,
        client: HttpClient,
        *,
        llm_caller=None,
    ) -> dict:
        res = run_pipeline(
            week_id="2026-W47",
            dry_run=False,
            offline=False,
            root=ws,
            client=client,
            llm_caller=llm_caller,
            now=datetime(2026, 11, 23, 2, 0, tzinfo=timezone.utc),
        )
        issue = res["issue"]
        findings = validator.validate_weekly_issue_payload(
            issue,
            "data/weekly/2026-W47.json",
            schema_path=ws / "data" / "weekly" / "schema.json",
        )
        self.assertEqual([f for f in findings if f.severity == "error"], [])

        # Verify README block replacement does not corrupt README
        block = catalog_build.render_weekly_block(issue)
        readme = (ws / "README.md").read_text(encoding="utf-8")
        updated = catalog_build.replace_weekly_block(readme, block)
        self.assertIn("<!-- WEEKLY:START -->", updated)
        self.assertIn("<!-- WEEKLY:END -->", updated)
        self.assertIn("## Footer", updated)
        return res

    def test_01_normal_week(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = _make_workspace(Path(td))
            arxiv_xml = _arxiv_atom(
                [
                    {
                        "id": "2611.12345",
                        "published": "2026-11-19T12:00:00Z",
                        "title": "FlowWorld: Scalable 4D World Model via Rectified Flow",
                        "abstract": (
                            "We propose a novel unified framework for interactive 4D world model generation. "
                            "Extensive experiments and ablation studies on 4 benchmarks show 2.4x faster synthesis "
                            "and 18.5% better FVD over state-of-the-art baselines. "
                            "Code and pretrained weights: https://github.com/Tencent-Hunyuan/FlowWorld "
                            "Project: https://flowworld.github.io"
                        ),
                        "authors": ["Alice Chen", "Bob Li", "Carol Wang"],
                    }
                ]
            )
            hf_json = json.dumps(
                [
                    {
                        "paper": {
                            "id": "2611.12345",
                            "publishedAt": "2026-11-19T12:00:00Z",
                            "title": "FlowWorld: Scalable 4D World Model via Rectified Flow",
                            "summary": "We propose a novel unified framework for interactive 4D world model generation.",
                            "authors": [{"name": "Alice Chen"}, {"name": "Bob Li"}, {"name": "Carol Wang"}],
                            "organization": {"fullname": "Tencent Hunyuan"},
                            "githubRepo": "https://github.com/Tencent-Hunyuan/FlowWorld",
                            "projectPage": "https://flowworld.github.io",
                            "upvotes": 85,
                        }
                    }
                ]
            ).encode("utf-8")
            gh_meta = json.dumps(
                {
                    "full_name": "Tencent-Hunyuan/FlowWorld",
                    "stargazers_count": 420,
                    "created_at": "2026-11-18T10:00:00Z",
                    "size": 1200,
                    "archived": False,
                    "license": {"spdx_id": "Apache-2.0"},
                    "description": "Official repo for FlowWorld (arXiv:2611.12345)",
                }
            ).encode("utf-8")
            gh_readme = b"# FlowWorld: Scalable 4D World Model via Rectified Flow\nPaper: https://arxiv.org/abs/2611.12345\nCheckpoints on huggingface.co\n"

            def fetcher(url: str, headers: dict, timeout: int) -> HttpResponse:
                if "export.arxiv.org" in url:
                    return HttpResponse(200, arxiv_xml)
                if "huggingface.co/api/daily_papers" in url:
                    return HttpResponse(200, hf_json)
                if "api.github.com/repos/Tencent-Hunyuan/FlowWorld/readme" in url:
                    return HttpResponse(200, gh_readme)
                if "api.github.com/repos/Tencent-Hunyuan/FlowWorld" in url:
                    return HttpResponse(200, gh_meta)
                return HttpResponse(200, b'{"results": []}')

            client = HttpClient(fetcher=fetcher, sleep_fn=lambda _: None)
            res = self._run_and_assert_valid(ws, client)
            issue = res["issue"]
            self.assertEqual(issue["status"], "partial")
            self.assertEqual(len(issue["items"]), 1)
            self.assertEqual(issue["items"][0]["id"], "arxiv:2611.12345")
            self.assertTrue(issue["items"][0]["is_pick_of_the_week"])
            self.assertGreaterEqual(issue["items"][0]["score"]["total"], 75)

    def test_02_empty_week(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = _make_workspace(Path(td))
            client = HttpClient(
                fetcher=lambda u, h, t: HttpResponse(200, _arxiv_atom([]) if "arxiv" in u else b"[]"),
                sleep_fn=lambda _: None,
            )
            res = self._run_and_assert_valid(ws, client)
            self.assertEqual(res["issue"]["status"], "empty")
            self.assertEqual(res["issue"]["items"], [])
            self.assertEqual(len(res["issue"]["empty_tracks"]), 5)

    def test_03_source_returns_500_degrades_gracefully(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = _make_workspace(Path(td))

            def fetcher(url: str, headers: dict, timeout: int) -> HttpResponse:
                if "export.arxiv.org" in url:
                    return HttpResponse(500, b"Internal Server Error")
                return HttpResponse(200, b"[]")

            client = HttpClient(fetcher=fetcher, retries=1, sleep_fn=lambda _: None)
            res = self._run_and_assert_valid(ws, client)
            self.assertEqual(res["issue"]["status"], "empty")
            self.assertTrue(any("arxiv_api" in e for e in res["harvest_errors"]))

    def test_04_llm_unavailable_falls_back_to_heuristic(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = _make_workspace(Path(td))
            arxiv_xml = _arxiv_atom(
                [
                    {
                        "id": "2611.12346",
                        "published": "2026-11-20T08:00:00Z",
                        "title": "VidFlow: Real-Time Text-to-Video Diffusion Model",
                        "abstract": (
                            "We propose a novel text-to-video diffusion framework with flow matching. "
                            "Extensive experiments and ablation studies on 3 benchmarks achieve 3.1x speedup "
                            "over state-of-the-art baselines. Code: https://github.com/NVlabs/VidFlow"
                        ),
                        "authors": ["Dan Wu", "Eve Xu"],
                    }
                ]
            )
            hf_json = json.dumps(
                [
                    {
                        "paper": {
                            "id": "2611.12346",
                            "publishedAt": "2026-11-20T08:00:00Z",
                            "title": "VidFlow: Real-Time Text-to-Video Diffusion Model",
                            "summary": "We propose a novel text-to-video diffusion framework.",
                            "authors": [{"name": "Dan Wu"}, {"name": "Eve Xu"}],
                            "organization": {"fullname": "NVLabs"},
                            "githubRepo": "https://github.com/NVlabs/VidFlow",
                            "upvotes": 60,
                        }
                    }
                ]
            ).encode("utf-8")
            gh_meta = json.dumps(
                {
                    "full_name": "NVlabs/VidFlow",
                    "stargazers_count": 350,
                    "size": 500,
                    "license": {"spdx_id": "MIT"},
                    "description": "VidFlow arXiv:2611.12346",
                }
            ).encode("utf-8")

            def fetcher(url: str, headers: dict, timeout: int) -> HttpResponse:
                if "export.arxiv.org" in url:
                    return HttpResponse(200, arxiv_xml)
                if "huggingface.co" in url:
                    return HttpResponse(200, hf_json)
                if "readme" in url:
                    return HttpResponse(200, b"# VidFlow\n2611.12346\nweights on huggingface.co\n")
                if "api.github.com" in url:
                    return HttpResponse(200, gh_meta)
                return HttpResponse(200, b'{"results": []}')

            def failing_llm(_prompt: str) -> dict:
                raise TimeoutError("LLM endpoint timed out")

            client = HttpClient(fetcher=fetcher, sleep_fn=lambda _: None)
            res = self._run_and_assert_valid(ws, client, llm_caller=failing_llm)
            self.assertEqual(len(res["issue"]["items"]), 1)
            self.assertEqual(res["issue"]["items"][0]["score"]["quality_mode"], "heuristic")

    def test_05_missing_affiliation_goes_to_pending_not_homepage(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = _make_workspace(Path(td))
            arxiv_xml = _arxiv_atom(
                [
                    {
                        "id": "2611.22222",
                        "published": "2026-11-18T10:00:00Z",
                        "title": "MeshGen: Fast 3D Asset Generation with Diffusion",
                        "abstract": (
                            "We introduce MeshGen for text-to-3D asset generation. "
                            "Project page: https://meshgen-anon.github.io"
                        ),
                        "authors": ["Anon One"],
                    }
                ]
            )
            client = HttpClient(
                fetcher=lambda u, h, t: HttpResponse(200, arxiv_xml if "arxiv" in u else (b"[]" if "huggingface" in u else b'{"results": []}')),
                sleep_fn=lambda _: None,
            )
            res = self._run_and_assert_valid(ws, client)
            self.assertEqual(res["issue"]["items"], [])
            self.assertEqual(res["pending_affiliation"], 1)
            pending = json.loads((ws / "data" / "weekly" / "pending.json").read_text(encoding="utf-8"))
            self.assertEqual(pending["entries"][0]["arxiv_id"], "2611.22222")

    def test_06_code_repo_points_to_wrong_paper_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = _make_workspace(Path(td))
            hf_json = json.dumps(
                [
                    {
                        "paper": {
                            "id": "2611.33333",
                            "publishedAt": "2026-11-19T09:00:00Z",
                            "title": "SceneDiff: 3D Indoor Scene Generation with Diffusion",
                            "summary": "We propose SceneDiff for indoor 3D scene generation.",
                            "authors": [{"name": "Jane Doe"}],
                            "organization": {"fullname": "NVIDIA"},
                            "githubRepo": "https://github.com/someone/unrelated-crypto-bot",
                            "upvotes": 40,
                        }
                    }
                ]
            ).encode("utf-8")
            gh_meta = json.dumps(
                {
                    "full_name": "someone/unrelated-crypto-bot",
                    "stargazers_count": 500,
                    "size": 100,
                    "description": "Trading bot for cryptocurrencies",
                }
            ).encode("utf-8")

            def fetcher(url: str, headers: dict, timeout: int) -> HttpResponse:
                if "export.arxiv.org" in url:
                    return HttpResponse(200, _arxiv_atom([]))
                if "huggingface.co" in url:
                    return HttpResponse(200, hf_json)
                if "readme" in url:
                    return HttpResponse(200, b"# Crypto Bot\nAutomated trading script.\n")
                if "api.github.com" in url:
                    return HttpResponse(200, gh_meta)
                return HttpResponse(200, b'{"results": []}')

            client = HttpClient(fetcher=fetcher, sleep_fn=lambda _: None)
            res = self._run_and_assert_valid(ws, client)
            self.assertEqual(res["issue"]["items"], [])
            self.assertTrue(
                any("H6_CODE_IDENTITY_FAIL" in r["reason_codes"] for r in res["rejected"])
            )

    def test_07_duplicate_entry_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            ws = _make_workspace(Path(td))
            arxiv_xml = _arxiv_atom(
                [
                    {
                        "id": "2611.99999",
                        "published": "2026-11-20T09:00:00Z",
                        "title": "Existing Video Generator",
                        "abstract": "We propose a text-to-video diffusion model. Code: https://github.com/Tencent-Hunyuan/ExistingVid",
                        "authors": ["Test Author"],
                    }
                ]
            )
            client = HttpClient(
                fetcher=lambda u, h, t: HttpResponse(200, arxiv_xml if "arxiv" in u else (b"[]" if "huggingface" in u else b'{"results": []}')),
                sleep_fn=lambda _: None,
            )
            res = self._run_and_assert_valid(ws, client)
            self.assertEqual(res["issue"]["items"], [])
            self.assertTrue(
                any("H7_DUPLICATE" in r["reason_codes"] for r in res["rejected"])
            )


if __name__ == "__main__":
    unittest.main()
