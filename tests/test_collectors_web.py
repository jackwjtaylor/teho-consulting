from teho_automation.collectors.web import parse_site_overview


def test_parse_site_overview_extracts_title_description_and_headings() -> None:
    html = """
    <html>
      <head>
        <title>Example Company</title>
        <meta name="description" content="We help customers cook better meals." />
      </head>
      <body>
        <h1>Fresh recipe kits</h1>
        <h2>How it works</h2>
        <h2>Customer stories</h2>
      </body>
    </html>
    """
    result = parse_site_overview(html)
    assert result["title"] == "Example Company"
    assert result["description"] == "We help customers cook better meals."
    assert result["headings"] == ["Fresh recipe kits", "How it works", "Customer stories"]
