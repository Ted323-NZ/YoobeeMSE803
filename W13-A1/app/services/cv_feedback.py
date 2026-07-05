"""CV feedback orchestration for Gemini and demo mode."""

from __future__ import annotations

import json
import re

from app.config import Settings
from app.services.gemini_client import GeminiClient
from app.services.rule_based_cv import analyze_cv as demo_analyze_cv
from app.services.rule_based_cv import generate_optimized_cv_text as demo_optimize_cv


FEEDBACK_SYSTEM_INSTRUCTION = (
    "You are a constructive CV reviewer for entry-level technology roles. "
    "Give specific, professional, ethical feedback. Do not invent real employment history. "
    "Return only valid JSON matching the requested schema."
)

OPTIMIZE_SYSTEM_INSTRUCTION = (
    "You are a CV optimization assistant. Improve clarity, structure, ATS alignment, and presentation. "
    "Do not invent unverifiable companies, degrees, or certifications. You may reframe provided evidence "
    "and add clearly generic project descriptions only when the input is a sample CV. "
    "Return only valid JSON matching the requested schema."
)


class CVFeedbackService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = (
            GeminiClient(
                api_key=settings.gemini_api_key,
                model=settings.gemini_model,
                endpoint=settings.gemini_endpoint,
            )
            if settings.gemini_api_key
            else None
        )

    async def analyze(self, cv_text: str, target_role: str) -> dict:
        if not self.client:
            return demo_analyze_cv(cv_text, target_role)

        prompt = f"""
Analyze this CV for the target role: {target_role}

Return JSON with this exact schema:
{{
  "target_role": "{target_role}",
  "overall_score": 0,
  "summary": "",
  "strengths": [],
  "improvement_areas": [],
  "content_recommendations": [],
  "structure_recommendations": [],
  "presentation_recommendations": [],
  "ats_keywords": [],
  "revised_summary": "",
  "provider": "gemini"
}}

CV:
{cv_text}
"""
        raw = await self.client.generate_text(prompt, FEEDBACK_SYSTEM_INSTRUCTION)
        data = _loads_json_object(raw)
        data["provider"] = "gemini"
        data["target_role"] = target_role
        return data

    async def optimize(self, cv_text: str, target_role: str) -> dict:
        if not self.client:
            return demo_optimize_cv(cv_text, target_role)

        prompt = f"""
Optimize this CV for the target role: {target_role}

Return JSON with this exact schema:
{{
  "target_role": "{target_role}",
  "optimized_cv_text": "",
  "changes_made": [],
  "provider": "gemini"
}}

        The optimized_cv_text should be a concise one-page CV using uppercase section headings.
        Keep it under 450 words. Prefer fewer, stronger bullets over long descriptions.
        Keep it truthful and avoid inventing specific employers or credentials.

CV:
{cv_text}
"""
        raw = await self.client.generate_text(prompt, OPTIMIZE_SYSTEM_INSTRUCTION)
        data = _loads_json_object(raw)
        data["provider"] = "gemini"
        data["target_role"] = target_role
        return data


def _loads_json_object(raw_text: str) -> dict:
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise
        return json.loads(cleaned[start : end + 1])
