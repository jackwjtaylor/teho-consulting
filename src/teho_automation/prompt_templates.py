"""Helpers for loading and filling prompt templates."""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .context import CompanyContext, SourceEntry

DEFAULT_TEMPLATE_PATH = Path("docs/prompt_v1.md")


def load_prompt_templates(path: Path | None = None) -> Dict[str, str]:
    """Return a dictionary of prompt templates keyed by code block label."""
    target = path or DEFAULT_TEMPLATE_PATH
    text = Path(target).read_text(encoding="utf-8")
    templates: Dict[str, List[str]] = {}
    current_label: Optional[str] = None

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            label = stripped[3:].strip().lower()
            if current_label is None:
                current_label = label or "default"
                templates[current_label] = []
            else:
                current_label = None
            continue
        if current_label is not None:
            templates[current_label].append(line)

    flattened = {label: "\n".join(lines).strip() for label, lines in templates.items() if lines}
    if not flattened:
        raise ValueError(f"No prompt code blocks found in {target}")
    return flattened


def _format_list(values: Iterable[str]) -> str:
    cleaned = [value.strip() for value in values if value and value.strip()]
    return "; ".join(cleaned) if cleaned else "UNKNOWN"


def _format_sources(sources: Iterable[SourceEntry]) -> str:
    items: List[str] = []
    for source in sources:
        title = source.title or "Untitled"
        retrieved = source.retrieved or "unknown date"
        confidence = source.confidence or "medium"
        summary = source.summary or ""
        entry = f"{source.id} – {title} (retrieved {retrieved}, confidence {confidence})"
        if summary:
            entry += f" — {summary}"
        entry += f" — {source.url}"
        items.append(entry)
    return "\n".join(items) if items else "None provided"


def build_prompt(
    template: str,
    context: CompanyContext,
    report_depth: str,
    sources: Optional[Iterable[SourceEntry]] = None,
) -> str:
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
        "SOURCE_LIST": _format_sources(sources or []),
    }

    try:
        return template.format_map(data)
    except KeyError as exc:
        missing_key = exc.args[0]
        raise ValueError(f"Template requires missing key: {missing_key}") from exc
