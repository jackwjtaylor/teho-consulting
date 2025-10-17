"""Collect short summaries of Trustpilot reviews."""

from __future__ import annotations

from typing import List

import httpx
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )
}


def parse_trustpilot_reviews(html: str, limit: int = 5) -> List[dict]:
    """Extract review highlights from Trustpilot HTML."""
    soup = BeautifulSoup(html, "html.parser")
    reviews: List[dict] = []

    for card in soup.select("article.review-card"):
        title_tag = card.select_one("h2, h3")
        paragraph = card.select_one("p")
        rating_tag = card.select_one("img[alt*='Rated']")
        title = title_tag.get_text(strip=True) if title_tag else ""
        summary = paragraph.get_text(strip=True) if paragraph else ""
        rating = rating_tag.get("alt", "") if rating_tag else ""
        if not (title or summary):
            continue
        reviews.append(
            {
                "title": title,
                "summary": summary,
                "rating": rating,
            }
        )
        if len(reviews) >= limit:
            break

    return reviews


def fetch_trustpilot_reviews(domain: str, country: str = "uk", limit: int = 5) -> List[dict]:
    """Fetch Trustpilot reviews for a given domain (best effort)."""
    base_url = f"https://{country}.trustpilot.com/review/{domain}"
    try:
        response = httpx.get(base_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except httpx.HTTPError:
        return []

    return parse_trustpilot_reviews(response.text, limit=limit)
