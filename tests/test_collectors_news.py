from teho_automation.collectors.news import parse_google_news_feed


def test_parse_google_news_feed_handles_basic_items() -> None:
    xml = """
    <rss xmlns:media="http://search.yahoo.com/mrss/">
      <channel>
        <item>
          <title>Gousto hits record profit</title>
          <link>https://example.com/gousto-profit</link>
          <pubDate>Tue, 07 Oct 2025 10:00:00 GMT</pubDate>
        </item>
        <item>
          <title>Meal kit trends in UK</title>
          <link>https://example.com/meal-kits</link>
          <pubDate>Mon, 06 Oct 2025 08:00:00 GMT</pubDate>
        </item>
      </channel>
    </rss>
    """
    headlines = parse_google_news_feed(xml, limit=5)
    assert len(headlines) == 2
    assert headlines[0]["title"] == "Gousto hits record profit"
    assert headlines[0]["url"] == "https://example.com/gousto-profit"
    assert headlines[0]["date"] == "2025-10-07"
