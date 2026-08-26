from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_data as validator  # noqa: E402


class ValidationTests(unittest.TestCase):
    def test_openreview_challenge_is_unreliable(self) -> None:
        self.assertTrue(
            validator.is_unreliable_title(
                "Verifying your browser | OpenReview"
            )
        )

    def test_real_title_is_reliable(self) -> None:
        self.assertFalse(
            validator.is_unreliable_title(
                "Denoising Autoregressive Transformers for "
                "Scalable Text-to-Image Generation"
            )
        )

    def test_equivalent_titles_match(self) -> None:
        matched, score = validator.title_matches(
            "PT-T2I/V: An Efficient Proxy-Tokenized Diffusion Transformer "
            "for Text-to-Image/Video-Task",
            "PT-T2I/V: An Efficient Proxy-Tokenized Diffusion Transformer "
            "for Text-to-Image/Video-Task",
        )
        self.assertTrue(matched)
        self.assertEqual(score, 1.0)

    def test_http_404_is_broken(self) -> None:
        self.assertEqual(
            validator.classify_http_status(404),
            "broken",
        )

    def test_http_403_is_unknown(self) -> None:
        self.assertEqual(
            validator.classify_http_status(403),
            "unknown",
        )

    def test_http_503_is_unknown(self) -> None:
        self.assertEqual(
            validator.classify_http_status(503),
            "unknown",
        )

    def test_arxiv_versions_share_identity(self) -> None:
        first = validator.canonical_paper_key(
            "https://arxiv.org/abs/2603.12345v1"
        )
        second = validator.canonical_paper_key(
            "https://arxiv.org/pdf/2603.12345v2"
        )
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()