from teho_automation.collectors.reviews import parse_trustpilot_reviews


def test_parse_trustpilot_reviews_extracts_basic_fields() -> None:
    html = """
    <html>
      <body>
        <article class="review-card">
          <h2>Great service</h2>
          <p>Boxes always arrived on time.</p>
          <img alt="Rated 5 out of 5 stars" />
        </article>
        <article class="review-card">
          <h3>Needs work</h3>
          <p>Delivery late last week.</p>
          <img alt="Rated 2 out of 5 stars" />
        </article>
      </body>
    </html>
    """
    reviews = parse_trustpilot_reviews(html, limit=5)
    assert len(reviews) == 2
    assert reviews[0]["title"] == "Great service"
    assert "Boxes" in reviews[0]["summary"]
    assert reviews[0]["rating"] == "Rated 5 out of 5 stars"
