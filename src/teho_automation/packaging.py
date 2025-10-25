"""Utilities for packaging reports (HTML, PDF, email drafts)."""

from __future__ import annotations

import re
import textwrap
from pathlib import Path
from typing import Optional
from datetime import datetime

from markdown_it import MarkdownIt

from .context import CompanyContext

PALETTE = {
    "bg": "#e8e7e1",
    "surface": "#f4f2ed",
    "surface_alt": "#ffffff",
    "border": "#d7d3c6",
    "text": "#1f201e",
    "muted": "#596152",
    "primary": "#2b3625",
    "primary_light": "#3e4739",
    "accent": "#78957a",
}

FULL_DISPLAY_NAME = "Opportunity Report – Full"
FULL_DEPTH_LABEL = "Full"
SUMMARY_DISPLAY_NAME = "Opportunity Report – Executive Summary"
SUMMARY_DEPTH_LABEL = "Executive Summary"
REPORT_STORAGE_FOLDER = "opportunity-report"

CSS_STYLES = f"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {{
  color-scheme: light;
  --bg: {PALETTE['bg']};
  --surface: {PALETTE['surface']};
  --surface-alt: {PALETTE['surface_alt']};
  --border: {PALETTE['border']};
  --text: {PALETTE['text']};
  --muted: {PALETTE['muted']};
  --primary: {PALETTE['primary']};
  --primary-light: {PALETTE['primary_light']};
  --accent: {PALETTE['accent']};
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

* {{
  box-sizing: border-box;
}}

body {{
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg);
  color: var(--text);
  margin: 0;
  padding: 56px 0;
  line-height: 1.7;
}}

.report-page {{
  margin: 0 auto;
  max-width: 920px;
  padding: 0 28px 72px;
}}

.report-card {{
  background: var(--surface-alt);
  border-radius: 28px;
  box-shadow: 0 28px 55px rgba(21, 25, 19, 0.16);
  overflow: hidden;
  border: 1px solid rgba(27, 30, 25, 0.08);
}}

.report-hero {{
  background: linear-gradient(125deg, rgba(43, 54, 37, 0.92), rgba(120, 149, 122, 0.62));
  color: #f8f7f3;
  padding: 54px 56px 48px;
  display: grid;
  gap: 32px;
}}

.report-hero__brand {{
  font-size: 18px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  font-weight: 600;
  opacity: 0.78;
}}

.report-hero__client {{
  font-size: 20px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 600;
  opacity: 0.9;
}}

.report-hero__title {{
  font-size: clamp(2.4rem, 4vw, 2.9rem);
  font-weight: 700;
  letter-spacing: 0.015em;
  line-height: 1.1;
}}

.report-hero__meta {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 18px 32px;
}}

.report-hero__meta-item {{
  display: flex;
  flex-direction: column;
  gap: 6px;
}}

.report-hero__meta-label {{
  font-size: 11px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  opacity: 0.8;
}}

.report-hero__meta-value {{
  font-size: 18px;
  font-weight: 600;
  color: #fefbf6;
}}

.report-body {{
  padding: 48px 56px 60px;
  display: grid;
  gap: 32px;
  font-size: 1.05rem;
}}

.report-body h1 {{
  display: none;
}}

.report-body h2 {{
  font-size: 1.6rem;
  margin: 12px 0 6px;
  padding: 18px 0 12px;
  border-bottom: 2px solid rgba(43, 54, 37, 0.14);
}}

.report-body h3 {{
  font-size: 1.25rem;
  margin: 20px 0 8px;
  color: var(--primary);
}}

.report-body p {{
  margin: 0;
  line-height: 1.78;
}}

.report-body strong {{
  color: var(--primary);
}}

.report-body a {{
  color: var(--primary);
  font-weight: 600;
  text-decoration: none;
  border-bottom: 1px solid rgba(43, 54, 37, 0.35);
}}

.report-body a:hover {{
  border-bottom-color: rgba(43, 54, 37, 0.65);
}}

.report-body ul,
.report-body ol {{
  margin: 0;
  padding-left: 28px;
  display: grid;
  gap: 10px;
}}

.report-body li {{
  line-height: 1.72;
}}

.report-body table {{
  border-collapse: separate;
  border-spacing: 0;
  width: 100%;
  margin: 20px 0;
  font-size: 0.98rem;
  overflow-x: auto;
  overflow: hidden;
  border-radius: 16px;
  border: 1px solid rgba(43, 54, 37, 0.1);
}}

.report-body thead {{
  background: rgba(43, 54, 37, 0.08);
}}

.report-body th,
.report-body td {{
  padding: 14px 18px;
  text-align: left;
  border-bottom: 1px solid rgba(43, 54, 37, 0.08);
}}

.report-body tbody tr:nth-child(even) {{
  background: rgba(232, 231, 225, 0.35);
}}

.report-body tbody tr:last-child td {{
  border-bottom: none;
}}

.report-body blockquote {{
  background: rgba(39, 50, 34, 0.08);
  border-left: 4px solid rgba(43, 54, 37, 0.45);
  padding: 18px 24px;
  font-style: italic;
  color: var(--primary);
}}

.report-body hr {{
  border: none;
  height: 1px;
  background: rgba(43, 54, 37, 0.12);
  margin: 12px 0 4px;
}}

.summary-callout {{
  margin: 8px 0 12px;
  padding: 24px 26px;
  border-radius: 24px;
  background: rgba(232, 231, 225, 0.75);
  border: 1px solid rgba(43, 54, 37, 0.12);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.45);
}}

.summary-callout h3 {{
  margin: 0 0 12px;
}}

.cta-banner {{
  margin-top: 8px;
  padding: 24px 26px;
  border-radius: 24px;
  background: linear-gradient(120deg, rgba(43, 54, 37, 0.9), rgba(120, 149, 122, 0.58));
  color: #f9f8f4;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  flex-wrap: wrap;
}}

.cta-banner a {{
  color: #f9f8f4;
  font-weight: 600;
  text-decoration: none;
}}

.cta-banner__action {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.25);
  border-radius: 999px;
  padding: 11px 20px;
}}

@media (max-width: 780px) {{
  body {{
    padding: 32px 0;
  }}
  .report-page {{
    padding: 0 18px 48px;
  }}
  .report-hero {{
    padding: 40px 28px;
  }}
  .report-body {{
    padding: 36px 28px 44px;
    font-size: 1rem;
  }}
}}

@media print {{
  @page {{
    margin: 18mm 15mm 22mm;
  }}
  body {{
    background: #ffffff;
    padding: 0;
  }}
  .report-page {{
    max-width: 100%;
    padding: 0 15mm 20mm;
  }}
  .report-card {{
    border: none;
    box-shadow: none;
    border-radius: 0;
  }}
  .report-hero {{
    padding: 28px 28px 24px;
  }}
  .report-body {{
    padding: 32px 28px 40px;
    font-size: 11pt;
  }}
  .report-body h2 {{
    page-break-after: avoid;
  }}
  .report-body table {{
    table-layout: fixed;
    width: 100%;
    font-size: 10pt;
  }}
  .report-body th,
  .report-body td {{
    word-break: break-word;
    white-space: normal;
  }}
  table {{
    page-break-inside: auto;
  }}
  tr {{
    page-break-inside: avoid;
    page-break-after: auto;
  }}
}}
"""


def parse_markdown_sections(markdown_text: str) -> tuple[str, dict[str, str], str]:
    lines = markdown_text.splitlines()
    heading = ""
    idx = 0
    if lines and lines[0].startswith("#"):
        heading = lines[0].lstrip("# ").strip()
        idx = 1

    meta: dict[str, str] = {}
    while idx < len(lines):
        stripped = lines[idx].strip()
        if not stripped:
            idx += 1
            continue
        if stripped.startswith("**") and "**" in stripped[2:]:
            label, rest = stripped[2:].split("**", 1)
            label = label.rstrip(": ").strip()
            value = rest.strip().lstrip(":").strip().strip("*").strip()
            meta[label] = value
            idx += 1
        else:
            break
    body_markdown = "\n".join(lines[idx:]).lstrip()
    return heading, meta, body_markdown


def render_markdown_html(
    body_markdown: str,
    title: str,
    meta: dict[str, str],
    client_name: str,
) -> str:
    md = MarkdownIt("commonmark").enable("table")
    body_html = md.render(body_markdown)

    hero_meta_html = "".join(
        f'<div class="report-hero__meta-item"><span class="report-hero__meta-label">{label}</span>'
        f'<span class="report-hero__meta-value">{meta.get(label, "—")}</span></div>'
        for label in ("Date", "Analyst", "Business", "Report Depth")
    )

    html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
      <head>
        <meta charset=\"utf-8\" />
        <title>{title}</title>
        <style>{CSS_STYLES}</style>
      </head>
      <body>
        <div class=\"report-page\">
          <div class=\"report-card\">
            <header class=\"report-hero\">
              <div class=\"report-hero__brand\">Teho Consulting</div>
              <div class=\"report-hero__client\">{client_name}</div>
              <div class=\"report-hero__title\">{title}</div>
              <div class=\"report-hero__meta\">{hero_meta_html}</div>
            </header>
            <section class=\"report-body\">
              {body_html}
            </section>
          </div>
        </div>
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


def rewrite_markdown_intro(markdown_text: str, title: str, depth_label: str) -> str:
    lines = markdown_text.splitlines()
    if lines and lines[0].startswith("#"):
        lines[0] = f"# {title}  "
    for idx, line in enumerate(lines):
        if line.lower().startswith("**report depth"):
            lines[idx] = f"**Report Depth:** {depth_label}  "
            break
    return "\n".join(lines).strip()



def build_email_draft(
    context: CompanyContext,
    slug: str,
    snapshot_summary: str,
    briefing_url: str = "https://teho.ai/{slug}-brief",
    calendly_url: str = "https://calendly.com/teho-jack/{slug}",
) -> str:
    """Return teaser email text personalised for the company."""
    contact_name = context.primary_contact or "there"
    contact_name = contact_name.split("—")[0].strip()
    company = context.business_name or slug.replace("-", " ").title()
    briefing = briefing_url.format(slug=slug)
    calendly = calendly_url.format(slug=slug)

    # Try to pull a £ headline from the summary bullets to power the subject.
    value_phrase = "your next AI wins"
    amount_matches = re.findall(r"£[\d,]+(?:\.\d+)?(?:\s*(?:–|-)\s*£?[\d,]+(?:\.\d+)?)*(?:m|bn)?", snapshot_summary, flags=re.IGNORECASE)

    def _to_numeric(match: str) -> float:
        clean = match.lower().replace("£", "").replace(",", "")
        multiplier = 1.0
        if clean.endswith("bn"):
            multiplier = 1_000.0
            clean = clean[:-2]
        elif clean.endswith("m"):
            multiplier = 1.0
            clean = clean[:-1]
        clean = clean.strip()
        if "–" in clean or "-" in clean:
            parts = re.split(r"[–-]", clean)
            try:
                return float(parts[-1]) * multiplier
            except ValueError:
                return 0.0
        try:
            return float(clean) * multiplier
        except ValueError:
            return 0.0

    if amount_matches:
        best_match = max(amount_matches, key=_to_numeric)
        value_phrase = best_match

    subject = f"{company}: unlock {value_phrase}"

    body = f"""
Subject: {subject}

Hi {contact_name},

I’m Jack, founder at Teho Consulting. We’ve just wrapped a short AI briefing for {company} and the numbers look promising:
{snapshot_summary}

The full opportunity report lays out the rollout steps, data checks, and risk plan for each move.

Pick what works best:
• Unlock the full briefing → {briefing}
• Prefer a chat? Grab a 30-minute slot → {calendly}

Thanks,
Jack Taylor
Founder, Teho Consulting
"""
    return textwrap.dedent(body).strip()


def summarise_snapshot(markdown_text: str, bullet_count: int = 3) -> str:
    """Return first few bullet points from the snapshot to drop into an email."""
    lines = markdown_text.splitlines()
    numbered = []
    idx = 0
    while idx < len(lines):
        stripped = lines[idx].strip()
        handled = False
        for num in range(1, bullet_count + 6):
            prefix = f"{num}."
            if stripped.startswith(prefix):
                title = stripped[len(prefix):].strip()
                j = idx + 1
                upside = ""
                while j < len(lines) and lines[j].strip():
                    candidate = lines[j].strip()
                    if "£" in candidate and "upside" in candidate.lower():
                        upside = candidate.split(":", 1)[-1].strip().lstrip("* ")
                        break
                    j += 1
                numbered.append((title, upside))
                idx = j
                handled = True
                break
        if len(numbered) >= bullet_count:
            break
        idx += 1 if not handled else 1

    if numbered:
        formatted = []
        for title, upside in numbered[:bullet_count]:
            summary = title
            if upside:
                summary = f"{summary} – {upside}"
            formatted.append(f"• {summary}")
        return "\n".join(formatted)

    bullets = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("-"):
            continue
        if stripped in {"-", "--", "---"}:
            continue
        bullets.append(stripped.lstrip("- ").strip())
    selected = bullets[:bullet_count] if bullets else ["AI moves ready to deploy"]
    return "\n".join(f"• {item}" for item in selected)


def create_report_assets(
    markdown_text: str,
    title: str,
    output_dir: Path,
    basename: str,
    context: CompanyContext,
    depth_label: str,
    generate_pdf: bool = True,
) -> dict:
    """Create HTML and optional PDF assets for a given markdown string."""
    _, meta, body_markdown = parse_markdown_sections(markdown_text)
    meta.setdefault("Business", context.business_name or context.business_url or title)
    meta.setdefault("Analyst", "Teho Consulting AI Advisory Team")
    meta.setdefault("Date", datetime.utcnow().strftime("%Y-%m-%d"))
    meta["Report Depth"] = depth_label

    html = render_markdown_html(
        body_markdown,
        title=title,
        meta=meta,
        client_name=context.business_name or title,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    html_path = output_dir / f"{basename}.html"
    html_path.write_text(html, encoding="utf-8")

    pdf_path = None
    if generate_pdf:
        pdf_path = maybe_render_pdf(html, html_path)

    return {"html": html_path, "pdf": pdf_path}


def package_snapshot(
    slug: str,
    snapshot_markdown: Path,
    output_dir: Path,
    context: CompanyContext,
    generate_pdf: bool = True,
) -> dict:
    """Create HTML (and optional PDF) snapshot plus email draft."""

    markdown_text = snapshot_markdown.read_text(encoding="utf-8")
    summary_text = rewrite_markdown_intro(
        markdown_text,
        title=SUMMARY_DISPLAY_NAME,
        depth_label=SUMMARY_DEPTH_LABEL,
    )
    snapshot_markdown.write_text(summary_text, encoding="utf-8")
    assets = create_report_assets(
        summary_text,
        title=f"{context.business_name} – {SUMMARY_DISPLAY_NAME}",
        output_dir=output_dir,
        basename="snapshot",
        context=context,
        depth_label=SUMMARY_DEPTH_LABEL,
        generate_pdf=generate_pdf,
    )

    summary = summarise_snapshot(summary_text)
    email_text = build_email_draft(context, slug=slug, snapshot_summary=summary)
    email_path = output_dir / "email_draft.txt"
    email_path.write_text(email_text, encoding="utf-8")

    return {**assets, "email": email_path}
