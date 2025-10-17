"""Orchestrate data collectors and persist results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional

from .collectors import (
    fetch_recent_headlines,
    fetch_site_overview,
    fetch_trustpilot_reviews,
)
from .context import CompanyContext, load_context
from .paths import get_company_paths


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def gather_signals(
    slug: str,
    company_name: str,
    domain: str,
    site_fetcher: Callable[[str], Dict] = fetch_site_overview,
    news_fetcher: Callable[[str, int], List[Dict]] = fetch_recent_headlines,
    review_fetcher: Callable[[str, str, int], List[Dict]] = fetch_trustpilot_reviews,
    news_limit: int = 5,
    review_limit: int = 5,
    trustpilot_country: str = "uk",
) -> dict:
    """Fetch signals from web sources for the given company."""

    site_info = site_fetcher(f"https://{domain}" if not domain.startswith("http") else domain)
    headlines = news_fetcher(company_name, limit=news_limit)
    reviews = review_fetcher(domain, country=trustpilot_country, limit=review_limit)

    return {
        "site_overview": site_info,
        "recent_headlines": headlines,
        "reviews": reviews,
    }


def collect_and_store(slug: str, domain: str) -> Path:
    """Run collectors and write results to disk, returning JSON path."""

    paths = get_company_paths(slug)
    context = load_context(str(paths.context_file))
    company_name = context.business_name or slug.replace("-", " ").title()

    payload = gather_signals(slug, company_name, domain)
    output_path = paths.raw_dir / "automation_signals.json"
    _write_json(output_path, payload)
    return output_path
