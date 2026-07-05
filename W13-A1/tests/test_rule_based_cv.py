from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.rule_based_cv import analyze_cv, generate_optimized_cv_text


class RuleBasedCVTests(unittest.TestCase):
    def setUp(self) -> None:
        self.cv_text = (ROOT / "examples" / "sample_cv.txt").read_text(encoding="utf-8")

    def test_analyze_cv_returns_structured_feedback(self) -> None:
        result = analyze_cv(self.cv_text, "Software Engineer")

        self.assertEqual(result["target_role"], "Software Engineer")
        self.assertGreaterEqual(result["overall_score"], 0)
        self.assertLessEqual(result["overall_score"], 100)
        self.assertIn("ats_keywords", result)
        self.assertIn("FastAPI", result["ats_keywords"])

    def test_optimize_cv_returns_cv_sections(self) -> None:
        result = generate_optimized_cv_text(self.cv_text, "Software Engineer")
        optimized_text = result["optimized_cv_text"]

        self.assertIn("PROFESSIONAL SUMMARY", optimized_text)
        self.assertIn("TECHNICAL SKILLS", optimized_text)
        self.assertIn("PROJECTS", optimized_text)
        self.assertGreater(len(result["changes_made"]), 2)


if __name__ == "__main__":
    unittest.main()

