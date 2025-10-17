"""Helpers for loading and filling prompt templates."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable

from .context import CompanyContext

DEFAULT_TEMPLATE_PATH = Path("docs/prompt_v1.md")


def load_prompt_template(path: Path | None = None) -> str:
    """Return the raw template string inside the markdown code block."""
    target = path or DEFAULT_TEMPLATE_PATH
    text = Path(target).read_text(encoding="utf-8")
    captured: list[str] = []
    in_block = False
    for line in text.splitlines():
        if line.strip().startswith("````"):
            in_block = not in_block
            continue
        if in_block:
            captured.append(line)
    if not captured:
        raise ValueError(f"No code block prompt found in {target}")
    return "\n".join(captured)


def _format_list(values: Iterable[str]) -> str:
    cleaned = [value.strip() for value in values if value and value.strip()]
    return "; ".join(cleaned) if cleaned else "UNKNOWN"


def build_prompt(template: str, context: CompanyContext, report_depth: str) -> str:
    """Fill the prompt template with context values."""
    data: Dict[str, str] = {
        "REPORT_DEPTH": report_depth,
        "BUSINESS_NAME": context.business_name or "UNKNOWN",
        "BUSINESS_URL": str(context.business_url) if context.business_url else "UNKNOWN",
        "HEADQUARTERS": context.headquarters or "UNKNOWN",
        "INDUSTRY_TAGS": _format_list(context.industry_tags),
        "REVENUE_BAND": context.revenue_band or "UNKNOWN",
        "HEADCOUNT_INFO": context.headcount_info or "UNKNOWN",
        "RECENT_HEADLINES": _format_list(
            f"{headline.title} ({headline.date})" if headline.date else headline.title
            for headline in context.recent_headlines
        ),
        "PRODUCT_SUMMARY": _format_list(context.product_summary),
        "MISSION_SNIPPET": context.mission_snippet or "UNKNOWN",
        "TECH_STACK_NOTES": _format_list(context.tech_stack_notes),
        "COMPETITOR_LIST": _format_list(context.competitor_list),
        "REGULATORY_NOTES": _format_list(context.regulatory_notes),
        "RESEARCHER_NOTES": context.researcher_notes or "None",
        "GO_TO_MARKET_NOTES": _format_list(context.go_to_market_notes),
        "OPERATING_MODEL_INSIGHTS": _format_list(context.operating_model_insights),
        "PAIN_POINT_INDICATORS": _format_list(context.pain_point_indicators),
        "DATA_ASSETS": _format_list(context.data_assets),
        "COURIER_PARTNERS": _format_list(context.courier_partners),
        "OWNERSHIP_MODEL": context.ownership_model or "UNKNOWN",
        "FOUNDING_YEAR": context.founding_year or "UNKNOWN",
        "PRIMARY_CONTACT": context.primary_contact or "UNKNOWN",
        "PRIMARY_EMAIL": context.primary_email or "UNKNOWN",
    }

    try:
        return template.format_map(data)
    except KeyError as exc:
        missing_key = exc.args[0]
        raise ValueError(f"Template requires missing key: {missing_key}") from exc
