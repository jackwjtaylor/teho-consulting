"""Data models for company research context."""

from __future__ import annotations

import datetime as dt
import csv
from pathlib import Path
from typing import Iterable, List, Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, ValidationError

from .utils import parse_iso_date


class Headline(BaseModel):
    title: str = Field(..., description="Headline title")
    summary: str = Field(..., description="One-line takeaway")
    url: HttpUrl = Field(..., description="Source URL")
    date: str = Field(..., description="ISO formatted date e.g. 2025-10-07")
    confidence: str = Field("medium", description="Confidence level: high/medium/low")


class ListItem(BaseModel):
    text: str
    confidence: str = Field("medium", description="Confidence level")


class SourceEntry(BaseModel):
    id: str
    title: str
    url: HttpUrl
    retrieved: str
    summary: Optional[str] = None
    confidence: str = Field("medium", description="Confidence level")


class CompanyContext(BaseModel):
    model_config = ConfigDict(extra="allow")

    business_name: str
    business_url: Optional[HttpUrl] = None
    headquarters: Optional[str] = None
    industry_tags: List[str] = Field(default_factory=list)
    revenue_band: Optional[str] = None
    headcount_info: Optional[str] = None
    founding_year: Optional[str] = None
    ownership_model: Optional[str] = None
    product_summary: List[str] = Field(default_factory=list)
    mission_snippet: Optional[str] = None
    courier_partners: List[str] = Field(default_factory=list)
    go_to_market_notes: List[str] = Field(default_factory=list)
    operating_model_insights: List[str] = Field(default_factory=list)
    pain_point_indicators: List[str] = Field(default_factory=list)
    tech_stack_notes: List[str] = Field(default_factory=list)
    data_assets: List[str] = Field(default_factory=list)
    regulatory_notes: List[str] = Field(default_factory=list)
    recent_headlines: List[Headline] = Field(default_factory=list)
    competitor_list: List[str] = Field(default_factory=list)
    researcher_notes: Optional[str] = None
    primary_contact: Optional[str] = None
    primary_email: Optional[str] = None
    persona_focus: Optional[str] = None
    engagement_goal: Optional[str] = None
    market_spotlight: Optional[str] = None
    customer_voice_highlights: List[str] = Field(default_factory=list)
    competitor_signals: List[str] = Field(default_factory=list)
    regulatory_watch: List[str] = Field(default_factory=list)

    def missing_fields(self) -> List[str]:
        """Return context keys that are empty or None."""
        missing = []
        for field_name, value in self.__dict__.items():
            if isinstance(value, list) and not value:
                missing.append(field_name)
            elif value in (None, "", "UNKNOWN"):
                missing.append(field_name)
        return missing

    def stale_headlines(self, max_age_years: int = 2) -> List[str]:
        """Return headline titles older than the threshold."""
        stale: List[str] = []
        cutoff = dt.date.today() - dt.timedelta(days=365 * max_age_years)
        for headline in self.recent_headlines:
            if not headline.date:
                continue
            parsed = parse_iso_date(headline.date)
            if parsed and parsed < cutoff:
                stale.append(f"{headline.title} ({headline.date})")
        return stale


def load_context(path: str) -> CompanyContext:
    """Load a context JSON file and validate against CompanyContext."""
    import json

    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    try:
        return CompanyContext.model_validate(raw)
    except ValidationError as exc:
        raise ValueError(f"Context validation failed for {path}") from exc


def load_sources(path: str) -> List[SourceEntry]:
    """Load sources from CSV (id,title,url,retrieved,summary,confidence)."""
    file_path = Path(path)
    if not file_path.exists():
        return []

    entries: List[SourceEntry] = []
    with file_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if not row:
                continue
            try:
                entry = SourceEntry(
                    id=row.get("id", "").strip(),
                    title=row.get("title", "").strip(),
                    url=row.get("url", "").strip(),
                    retrieved=row.get("retrieved", "").strip(),
                    summary=(row.get("summary") or "").strip() or None,
                    confidence=(row.get("confidence") or "medium").strip(),
                )
            except ValidationError:
                continue
            entries.append(entry)
    return entries


def save_context(path: str, context: CompanyContext) -> None:
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(context.model_dump_json(indent=2), encoding="utf-8")


def append_sources(path: str, entries: Iterable[SourceEntry]) -> None:
    file_path = Path(path)
    existing = load_sources(str(file_path))
    existing_ids = {entry.id for entry in existing}
    new_entries = [entry for entry in entries if entry.id and entry.id not in existing_ids]
    if not new_entries:
        return
    combined = existing + new_entries
    _write_sources(file_path, combined)


def _write_sources(path: Path, entries: List[SourceEntry]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        fieldnames = ["id", "title", "url", "retrieved", "summary", "confidence"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(
                {
                    "id": entry.id,
                    "title": entry.title,
                    "url": str(entry.url),
                    "retrieved": entry.retrieved,
                    "summary": entry.summary or "",
                    "confidence": entry.confidence,
                }
            )
