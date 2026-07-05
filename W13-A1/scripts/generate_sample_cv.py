"""Generate sample feedback and an optimized DOCX CV without requiring Gemini."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.services.cv_document import write_cv_docx
from app.services.rule_based_cv import analyze_cv, generate_optimized_cv_text


def main() -> None:
    sample_path = ROOT / "examples" / "sample_cv.txt"
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)

    cv_text = sample_path.read_text(encoding="utf-8")
    feedback = analyze_cv(cv_text, "Software Engineer")
    optimized = generate_optimized_cv_text(cv_text, "Software Engineer")

    (output_dir / "sample_feedback.json").write_text(
        json.dumps(feedback, indent=2),
        encoding="utf-8",
    )
    (output_dir / "optimized_cv_sample.md").write_text(
        optimized["optimized_cv_text"],
        encoding="utf-8",
    )
    write_cv_docx(
        optimized["optimized_cv_text"],
        output_dir / "optimized_cv_sample.docx",
    )

    print("Generated:")
    print(output_dir / "sample_feedback.json")
    print(output_dir / "optimized_cv_sample.md")
    print(output_dir / "optimized_cv_sample.docx")


if __name__ == "__main__":
    main()

