"""Higher-level helpers for using OpenAI Responses API (web search + summarisation)."""

from __future__ import annotations

import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - optional dependency
    OpenAI = None  # type: ignore

WEB_MODEL = os.getenv("OPENAI_WEB_MODEL", "gpt-4.1-mini")
SUMMARY_MODEL = os.getenv("OPENAI_SUMMARY_MODEL", "gpt-4.1-mini")
MAX_AGE_DAYS = int(os.getenv("OPENAI_WEB_MAX_AGE_DAYS", "365"))


def _build_client() -> Optional[OpenAI]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or OpenAI is None:
        return None
    return OpenAI(api_key=api_key)


def perform_web_search(query: str, max_results: int = 6) -> List[Dict[str, Any]]:
    """Use OpenAI web_search tool to gather recent links for the query."""
    client = _build_client()
    if client is None:
        return []

    schema = {
        "name": "WebSearchResults",
        "schema": {
            "type": "object",
            "properties": {
                "results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"},
                            "snippet": {"type": "string"},
                            "published": {"type": "string"},
                            "source": {"type": "string"},
                        },
                        "required": ["title", "url"],
                    },
                }
            },
            "required": ["results"],
        },
    }

    try:
        response = client.responses.create(
            model=WEB_MODEL,
            input=[
                {
                    "role": "system",
                    "content": "You perform factual web reconnaissance. Return concise results with publication dates when available.",
                },
                {
                    "role": "user",
                    "content": f"Search the web for the latest 10 items about: {query}",
                },
            ],
            tools=[{"type": "web_search"}],
            response_format={"type": "json_schema", "json_schema": schema},
        )
    except Exception:
        return []

    try:
        data = json.loads(response.output[0].content[0].text)  # type: ignore[attr-defined]
    except Exception:
        try:
            data = json.loads(response.output_text)  # type: ignore[attr-defined]
        except Exception:
            return []

    results = data.get("results", [])
    if not isinstance(results, list):
        return []
    trimmed: List[Dict[str, Any]] = []
    cutoff = datetime.utcnow() - timedelta(days=MAX_AGE_DAYS)

    def _parse_published(value: Any) -> Optional[datetime]:
        if not value or not isinstance(value, str):
            return None
        text = value.strip()
        if not text:
            return None
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z"):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None

    for item in results:
        published = item.get("published")
        parsed_date = _parse_published(published)
        if parsed_date and parsed_date < cutoff:
            continue
        item.setdefault("snippet", "")
        item.setdefault("source", "")
        item.setdefault("published", parsed_date.isoformat() if parsed_date else published or "")
        trimmed.append(item)
        if len(trimmed) >= max_results:
            break
    return trimmed


def summarise_market_signals(
    company_name: str,
    headlines: List[Dict[str, Any]],
    reviews: List[Dict[str, Any]],
    web_results: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Summarise raw signals into actionable insight buckets using OpenAI."""
    client = _build_client()
    if client is None:
        return {}

    scaffold = {
        "name": "SignalSummary",
        "schema": {
            "type": "object",
            "properties": {
                "spotlight": {"type": "string"},
                "operational_risks": {"type": "array", "items": {"type": "string"}},
                "customer_voice": {"type": "array", "items": {"type": "string"}},
                "competitor_moves": {"type": "array", "items": {"type": "string"}},
                "regulatory_flags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["spotlight"],
        },
    }

    payload = json.dumps(
        {
            "company": company_name,
            "headlines": headlines,
            "reviews": reviews,
            "web_results": web_results,
        },
        ensure_ascii=False,
    )

    try:
        response = client.responses.create(
            model=SUMMARY_MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "You are an analyst preparing AI opportunity research. "
                        "Condense the provided signals into concise, factual bullets."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Summarise these signals for {company_name}. Return JSON.\n{payload}",
                },
            ],
            response_format={"type": "json_schema", "json_schema": scaffold},
        )
    except Exception:
        return {}

    try:
        data = json.loads(response.output[0].content[0].text)  # type: ignore[attr-defined]
    except Exception:
        try:
            data = json.loads(response.output_text)  # type: ignore[attr-defined]
        except Exception:
            return {}
    return data if isinstance(data, dict) else {}
