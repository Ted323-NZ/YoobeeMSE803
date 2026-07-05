"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


@dataclass(frozen=True)
class Settings:
    app_name: str
    gemini_api_key: str | None
    gemini_model: str
    gemini_endpoint: str

    @property
    def llm_mode(self) -> str:
        return "gemini" if self.gemini_api_key else "demo"


def get_settings() -> Settings:
    api_key = os.getenv("GEMINI_API_KEY", "").strip() or None
    return Settings(
        app_name=os.getenv("APP_NAME", "LLM CV Feedback API"),
        gemini_api_key=api_key,
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-3.5-flash"),
        gemini_endpoint=os.getenv(
            "GEMINI_ENDPOINT",
            "https://generativelanguage.googleapis.com/v1beta/interactions",
        ),
    )

