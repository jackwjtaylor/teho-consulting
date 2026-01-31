"""Wrapper exposing OpenAI-powered web search to the collector runner."""

from __future__ import annotations

from typing import Any, Dict, List

from ..openai_tools import perform_web_search as _perform_web_search


def perform_web_search(query: str, limit: int = 6) -> List[Dict[str, Any]]:
    """Return recent web results for a query using OpenAI's web_search tool."""
    results = _perform_web_search(query, max_results=limit)
    return results
