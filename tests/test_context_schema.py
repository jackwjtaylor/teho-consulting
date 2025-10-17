from pathlib import Path

from teho_automation.context import CompanyContext


def test_missing_fields_detection(tmp_path: Path) -> None:
    sample = {
        "business_name": "Acme Ltd",
        "industry_tags": [],
        "product_summary": [],
        "recent_headlines": [
            {"title": "Old news", "summary": "", "url": "https://example.com", "date": "2020-01-01"}
        ],
    }
    context = CompanyContext.model_validate(sample)
    missing = set(context.missing_fields())
    assert "industry_tags" in missing
    assert "product_summary" in missing
    assert "recent_headlines" not in missing
    stale = context.stale_headlines(max_age_years=2)
    assert stale
    assert "primary_contact" in missing
    assert "primary_email" in missing
