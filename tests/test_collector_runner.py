from pathlib import Path

from teho_automation.collector_runner import gather_signals


def test_gather_signals_uses_provided_fetchers(tmp_path: Path) -> None:
    def fake_site(url: str):
        return {"title": "Demo"}

    def fake_news(query: str, limit: int):
        return [{"title": "Headline", "url": "https://example.com", "date": "2025-10-07"}]

    def fake_reviews(domain: str, country: str, limit: int):
        return [{"title": "Great", "summary": "Helpful", "rating": "5"}]

    payload = gather_signals(
        slug="demo-co",
        company_name="Demo Co",
        domain="demo.com",
        site_fetcher=fake_site,
        news_fetcher=fake_news,
        review_fetcher=fake_reviews,
    )

    assert payload["site_overview"]["title"] == "Demo"
    assert len(payload["recent_headlines"]) == 1
    assert len(payload["reviews"]) == 1
