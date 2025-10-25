"""Run prompts against the OpenAI API and validate the output."""

from __future__ import annotations

import os
from dataclasses import dataclass
import re
from typing import Iterable, List, Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore

REQUIRED_HEADINGS = [
    "Company & Process Overview",
    "Pain-Point Scan",
    "Opportunity Table",
    "Top Five Opportunity Deep Dives",
    "Competitor & Industry View",
    "Recommendations & Timeline",
    "Appendix",
]


def validate_report_structure(markdown: str) -> List[str]:
    """Return missing headings that should appear in the report."""
    missing = []
    for heading in REQUIRED_HEADINGS:
        escaped = re.escape(heading)
        pattern = rf"^##\s*(?:\d+\.\s*)?{escaped}"
        if re.search(pattern, markdown, flags=re.IGNORECASE | re.MULTILINE) is None:
            missing.append(f"## {heading}")
    return missing


@dataclass
class PromptRunner:
    """Wrapper around OpenAI responses API with basic defaults."""

    model: str = "gpt-4.1-mini"
    temperature: float = 0.2
    client: Optional[OpenAI] = None

    def __post_init__(self) -> None:
        if self.client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise RuntimeError(
                    "OPENAI_API_KEY not set. Export it or provide a configured OpenAI client."
                )
            if OpenAI is None:
                raise RuntimeError(
                    "openai package not installed. Install with `pip install openai`."
                )
            self.client = OpenAI(api_key=api_key)

    def run(self, prompt: str) -> str:
        """Call the OpenAI Responses API and return plain text."""
        assert self.client is not None  # for mypy
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
            temperature=self.temperature,
        )
        return _extract_response_text(response)


def _extract_response_text(response: object) -> str:
    """Extract text from OpenAI responses API."""
    output_text = getattr(response, "output_text", None)
    if output_text:
        text = str(output_text).strip()
        if text:
            return text
    # response output schema reference: https://platform.openai.com/docs/api-reference/responses/object
    if hasattr(response, "output"):
        chunks: Iterable[object] = getattr(response, "output")
        parts: List[str] = []
        for chunk in chunks:
            if getattr(chunk, "type", "") == "output_text":
                parts.append(getattr(chunk, "text", ""))
        combined = "\n".join(parts).strip()
        if combined:
            return combined
    # Fallback for older/alternative structures
    text = getattr(response, "text", None)
    if text:
        return str(text)
    raise ValueError("Could not extract text from response object")
