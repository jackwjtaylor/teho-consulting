"""Utilities for packaging reports (HTML snapshot, email drafts, optional PDF)."""

from __future__ import annotations

import textwrap
from pathlib import Path
from typing import Optional

from markdown_it import MarkdownIt

from .context import CompanyContext

CSS_STYLES = """
body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #1f1f1f; margin: 40px; }
h1, h2, h3 { color: #12304a; }
h1 { font-size: 28px; margin-bottom: 16px; }
h2 { font-size: 20px; margin-top: 32px; border-bottom: 1px solid #e3e3e3; padding-bottom: 4px; }
ul { padding-left: 20px; }
table { border-collapse: collapse; width: 100%; margin: 16px 0; }
table, th, td { border: 1px solid #d7d7d7; }
th, td { padding: 8px; text-align: left; }
blockquote { border-left: 4px solid #d7d7d7; padding-left: 16px; color: #555; }
code { background-color: #f5f5f5; padding: 2px 4px; }
"""


def render_snapshot_html(markdown_text: str, title: str) -> str:
    """Convert snapshot markdown to styled HTML document."""
    md = MarkdownIt("commonmark").enable("table")
    body_html = md.render(markdown_text)
    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\" />
        <title>{title}</title>
        <style>
        {CSS_STYLES}
        </style>
      </head>
      <body>
        {body_html}
      </body>
    </html>
    """
    return textwrap.dedent(html).strip()


def maybe_render_pdf(html: str, output_path: Path) -> Optional[Path]:
    """Render HTML to PDF if WeasyPrint is available. Return PDF path or None."""
    try:
        from weasyprint import HTML  # type: ignore
    except Exception:  # pragma: no cover - optional dependency
        return None

    pdf_path = output_path.with_suffix(".pdf")
    HTML(string=html).write_pdf(str(pdf_path))
    return pdf_path


def build_email_draft(
    context: CompanyContext,
    slug: str,
    snapshot_summary: str,
    briefing_url: str = "https://teho.ai/{slug}-brief",
    calendly_url: str = "https://calendly.com/teho-jack/{slug}",
) -> str:
    """Return teaser email text personalised for the company."""
    contact_name = context.primary_contact or "there"
    company = context.business_name or slug.replace("-", " ").title()
    briefing = briefing_url.format(slug=slug)
    calendly = calendly_url.format(slug=slug)

    body = f"""
    Hi {contact_name.split('—')[0].strip() if '—' in contact_name else contact_name},

    I’m Jack, founder at Teho Consulting. We help UK teams squeeze more value from the automation they already have.

    We’ve mapped a short AI opportunity note for {company}. Highlights:
    {snapshot_summary}

    If that’s useful, feel free to:
    • View the fuller briefing here → {briefing}
    • Or pick a time for a quick chat → {calendly}

    Thanks,
    Jack Taylor
    Founder, Teho Consulting
    """
    return textwrap.dedent(body).strip()


def summarise_snapshot(snapshot_path: Path, bullet_count: int = 3) -> str:
    """Return first few bullet points from the snapshot to drop into an email."""
    lines = snapshot_path.read_text(encoding="utf-8").splitlines()
    bullets = [line.strip("- ") for line in lines if line.strip().startswith("-")]
    selected = bullets[:bullet_count] if bullets else ["AI moves ready to deploy"]
    return "\n    • ".join(selected)


def package_snapshot(
    slug: str,
    snapshot_markdown: Path,
    output_dir: Path,
    context: CompanyContext,
    generate_pdf: bool = True,
) -> dict:
    """Create HTML (and optional PDF) snapshot plus email draft."""

    markdown_text = snapshot_markdown.read_text(encoding="utf-8")
    html = render_snapshot_html(markdown_text, title=f"{context.business_name} – AI Snapshot")

    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / "snapshot.html"
    html_path.write_text(html, encoding="utf-8")

    pdf_path = None
    if generate_pdf:
        pdf_path = maybe_render_pdf(html, html_path)

    summary = summarise_snapshot(snapshot_markdown)
    email_text = build_email_draft(context, slug=slug, snapshot_summary=summary)
    email_path = output_dir / "email_draft.txt"
    email_path.write_text(email_text, encoding="utf-8")

    return {
        "html": html_path,
        "pdf": pdf_path,
        "email": email_path,
    }
