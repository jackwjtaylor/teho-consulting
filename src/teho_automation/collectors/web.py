"""Utilities for gathering basic company website context."""

from __future__ import annotations

from typing import Dict, List

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    )
}


def parse_site_overview(html: str) -> Dict[str, List[str] | str]:
    """Extract title, description, and key headings from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    description = ""
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content"):
        description = meta["content"].strip()

    headings: List[str] = []
    for tag in soup.find_all(["h1", "h2"]):
        text = tag.get_text(strip=True)
        if text and text not in headings:
            headings.append(text)
        if len(headings) >= 6:
            break

    return {
        "title": title,
        "description": description,
        "headings": headings,
    }


def fetch_site_overview(url: str, timeout: int = 10) -> Dict[str, List[str] | str]:
    """Fetch HTML from a site and parse basic overview details."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException as exc:
        return {"title": "", "description": "", "headings": [], "error": str(exc)}

    return parse_site_overview(response.text)
