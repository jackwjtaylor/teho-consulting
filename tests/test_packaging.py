from pathlib import Path

from teho_automation.context import CompanyContext
from teho_automation.packaging import build_email_draft, package_snapshot, render_markdown_html


def test_render_markdown_html_wraps_markdown() -> None:
    html = render_markdown_html(
        "# Title",
        "Demo Report",
        {"Date": "2025-01-01", "Analyst": "Teho"},
        "Demo Co",
    )
    assert "<h1>Title</h1>" in html
    assert "Demo Report" in html


def test_package_snapshot_creates_outputs(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot.md"
    snapshot.write_text("# Snapshot\n- Point one\n- Point two", encoding="utf-8")

    context = CompanyContext(
        business_name="Demo Co",
        industry_tags=[],
        product_summary=[],
        primary_contact="Alex Smith — CEO",
    )

    result = package_snapshot(
        slug="demo-co",
        snapshot_markdown=snapshot,
        output_dir=tmp_path,
        context=context,
        generate_pdf=False,
    )

    assert result["html"].exists()
    assert result["email"].exists()
    email_text = result["email"].read_text(encoding="utf-8")
    assert "Demo Co" in email_text
    assert "Point one" in email_text


def test_build_email_draft_uses_contact_and_links() -> None:
    context = CompanyContext(
        business_name="Demo Co",
        industry_tags=[],
        product_summary=[],
        primary_contact="Alex Smith — CEO",
    )
    email = build_email_draft(context, slug="demo-co", snapshot_summary="Point")
    assert "Alex Smith" in email
    assert "demo-co" in email
