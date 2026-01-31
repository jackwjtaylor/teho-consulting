"""Orchestrate data collectors and persist results (with caching + retries)."""

from __future__ import annotations

import asyncio
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional

from .collectors import (
    fetch_recent_headlines,
    fetch_site_overview,
    fetch_trustpilot_reviews,
    perform_web_search,
)
from .context import CompanyContext, load_context
from .openai_tools import summarise_market_signals
from .paths import CompanyPaths, get_company_paths
from tenacity import retry, stop_after_attempt, wait_exponential

CACHE_TTL_DAYS = int(os.getenv("COLLECTOR_CACHE_TTL_DAYS", "7"))


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _cache_path(paths: CompanyPaths) -> Path:
    return paths.raw_dir / "cache" / "automation_signals.json"


def _load_cached_payload(cache_path: Path) -> Optional[dict]:
    if not cache_path.exists():
        return None
    try:
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    fetched_at = cache.get("fetched_at")
    payload = cache.get("payload")
    if not fetched_at or payload is None:
        return None
    try:
        fetched_dt = datetime.fromisoformat(fetched_at)
    except ValueError:
        return None
    if datetime.utcnow() - fetched_dt > timedelta(days=CACHE_TTL_DAYS):
        return None
    return payload


def _save_cache(cache_path: Path, payload: dict) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_payload = {
        "fetched_at": datetime.utcnow().isoformat(),
        "payload": payload,
    }
    cache_path.write_text(json.dumps(cache_payload, indent=2), encoding="utf-8")


def gather_signals(
    slug: str,
    company_name: str,
    domain: str,
    site_fetcher: Callable[[str], Dict] = fetch_site_overview,
    news_fetcher: Callable[[str, int], List[Dict]] = fetch_recent_headlines,
    review_fetcher: Callable[[str, str, int], List[Dict]] = fetch_trustpilot_reviews,
    web_searcher: Callable[[str, int], List[Dict]] = perform_web_search,
    summary_builder: Callable[[str, List[Dict], List[Dict], List[Dict]], Dict] = summarise_market_signals,
    news_limit: int = 5,
    review_limit: int = 5,
    trustpilot_country: str = "uk",
) -> dict:
    """Fetch signals from web sources for the given company."""

    site_fetcher_retry = _make_retryable(site_fetcher, "site")
    news_fetcher_retry = _make_retryable(news_fetcher, "news")
    reviews_fetcher_retry = _make_retryable(review_fetcher, "reviews")

    site_info = site_fetcher_retry(f"https://{domain}" if not domain.startswith("http") else domain)
    headlines = news_fetcher_retry(company_name, limit=news_limit)
    reviews = reviews_fetcher_retry(domain, country=trustpilot_country, limit=review_limit)

    web_queries = {
        "automation": f"{company_name} automation initiative",
        "customer_experience": f"{company_name} customer complaints {trustpilot_country.upper()}",
        "regulation": f"{company_name} compliance enforcement",
        "competitors": f"{company_name} competitors AI strategy",
    }
    web_results: List[Dict] = []
    for tag, query in web_queries.items():
        try:
            results = web_searcher(query, limit=news_limit)
        except Exception:
            results = []
        for item in results:
            item = dict(item)
            item.setdefault("tag", tag)
            web_results.append(item)

    summaries: Dict = {}
    try:
        summaries = summary_builder(company_name, headlines, reviews, web_results)
    except Exception:
        summaries = {}

    return {
        "site_overview": site_info,
        "recent_headlines": headlines,
        "reviews": reviews,
        "web_results": web_results,
        "summaries": summaries,
    }


def collect_and_store(slug: str, domain: str) -> Path:
    """Run collectors and write results to disk, returning JSON path."""

    paths = get_company_paths(slug)
    context = load_context(str(paths.context_file))
    company_name = context.business_name or slug.replace("-", " ").title()

    cache_path = _cache_path(paths)
    cached = _load_cached_payload(cache_path)
    if cached is not None:
        _write_json(paths.raw_dir / "automation_signals.json", cached)
        return paths.raw_dir / "automation_signals.json"

    payload = gather_signals(slug, company_name, domain)
    output_path = paths.raw_dir / "automation_signals.json"
    _write_json(output_path, payload)
    _save_cache(cache_path, payload)
    return output_path


def _make_retryable(fetcher: Callable, name: str) -> Callable:
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=30), reraise=True)
    def wrapped(*args, **kwargs):
        return fetcher(*args, **kwargs)

    wrapped.__name__ = f"retryable_{name}"
    return wrapped
