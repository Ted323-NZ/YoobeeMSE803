"""Pydantic schemas used by the API layer."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    cv_text: str = Field(..., min_length=50, description="Plain text CV content")
    target_role: str = Field(default="Software Engineer", min_length=2)


class CVFeedback(BaseModel):
    target_role: str
    overall_score: int = Field(..., ge=0, le=100)
    summary: str
    strengths: list[str]
    improvement_areas: list[str]
    content_recommendations: list[str]
    structure_recommendations: list[str]
    presentation_recommendations: list[str]
    ats_keywords: list[str]
    revised_summary: str
    provider: str


class OptimizeRequest(BaseModel):
    cv_text: str = Field(..., min_length=50)
    target_role: str = Field(default="Software Engineer", min_length=2)


class OptimizeResponse(BaseModel):
    target_role: str
    optimized_cv_text: str
    changes_made: list[str]
    provider: str

