"""Small REST client for the Gemini Interactions API."""

from __future__ import annotations

from typing import Any


class GeminiClient:
    def __init__(self, api_key: str, model: str, endpoint: str) -> None:
        self.api_key = api_key
        self.model = model
        self.endpoint = endpoint

    async def generate_text(
        self,
        prompt: str,
        system_instruction: str,
        temperature: float = 0.2,
    ) -> str:
        import httpx

        payload = {
            "model": self.model,
            "system_instruction": system_instruction,
            "input": prompt,
            "generation_config": {
                "temperature": temperature,
                "thinking_level": "low",
            },
        }
        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(self.endpoint, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
        return self._extract_output_text(data)

    @staticmethod
    def _extract_output_text(data: dict[str, Any]) -> str:
        if isinstance(data.get("output_text"), str):
            return data["output_text"]

        fragments: list[str] = []
        for step in data.get("steps", []) or []:
            for item in step.get("content", []) or []:
                if isinstance(item, dict) and item.get("type") == "text":
                    fragments.append(str(item.get("text", "")))
            for item in step.get("output", []) or []:
                if isinstance(item, dict) and item.get("type") == "text":
                    fragments.append(str(item.get("text", "")))
        if fragments:
            return "\n".join(fragment for fragment in fragments if fragment).strip()

        raise ValueError("Gemini response did not include text output.")
