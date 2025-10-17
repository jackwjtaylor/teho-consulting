"""Fetch recent headlines using Google News RSS."""

from __future__ import annotations

import datetime as dt
import xml.etree.ElementTree as ET
from typing import List, Optional

import httpx

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search"


def parse_google_news_feed(xml_text: str, limit: int = 5) -> List[dict]:
    """Parse Google News RSS XML into headline dictionaries."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    headlines: List[dict] = []
    for item in root.findall(".//item"):
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        pub_date = item.findtext("pubDate") or ""
        try:
            parsed_date = dt.datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S %Z")
            iso_date = parsed_date.date().isoformat()
        except (ValueError, TypeError):
            iso_date = ""
        headlines.append(
            {
                "title": title.strip(),
                "url": link.strip(),
                "date": iso_date,
                "summary": "",
                "confidence": "medium",
            }
        )
        if len(headlines) >= limit:
            break
    return headlines


def fetch_recent_headlines(query: str, limit: int = 5) -> List[dict]:
    """Retrieve recent news headlines for a query."""
    params = {
        "q": query,
        "hl": "en-GB",
        "gl": "GB",
        "ceid": "GB:en",
    }
    try:
        response = httpx.get(GOOGLE_NEWS_RSS, params=params, timeout=10)
        response.raise_for_status()
    except httpx.HTTPError:
        return []

    return parse_google_news_feed(response.text, limit=limit)
