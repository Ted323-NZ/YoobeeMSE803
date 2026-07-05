"""Generate assignment feedback and optimized CV using configured provider."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import get_settings
from app.services.cv_document import write_cv_docx
from app.services.cv_feedback import CVFeedbackService


async def main() -> None:
    sample_path = ROOT / "examples" / "sample_cv.txt"
    output_dir = ROOT / "output"
    output_dir.mkdir(exist_ok=True)

    settings = get_settings()
    service = CVFeedbackService(settings)
    cv_text = sample_path.read_text(encoding="utf-8")

    feedback = await service.analyze(cv_text, "Software Engineer")
    optimized = await service.optimize(cv_text, "Software Engineer")
    provider = optimized.get("provider", settings.llm_mode)

    feedback_path = output_dir / f"submission_feedback_{provider}.json"
    markdown_path = output_dir / f"optimized_cv_{provider}.md"
    docx_path = output_dir / f"optimized_cv_{provider}.docx"

    feedback_path.write_text(json.dumps(feedback, indent=2), encoding="utf-8")
    markdown_path.write_text(optimized["optimized_cv_text"], encoding="utf-8")
    write_cv_docx(optimized["optimized_cv_text"], docx_path)

    print(f"Provider: {provider}")
    print(feedback_path)
    print(markdown_path)
    print(docx_path)


if __name__ == "__main__":
    asyncio.run(main())

