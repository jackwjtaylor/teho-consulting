"""Utilities for managing source citations (S#/N#/B#) in generated reports."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence

from .context import SourceEntry

CATEGORY_PATTERN = re.compile(r"^(S|N|B)[\s_-]*([0-9]+)?", re.IGNORECASE)


def _infer_category(entry: SourceEntry) -> str:
    """Infer a citation category (S/N/B) for the given source."""
    identifier = (entry.id or "").strip()
    if identifier:
        match = CATEGORY_PATTERN.match(identifier)
        if match:
            return match.group(1).upper()

    url = entry.url.lower()
    summary = (entry.summary or "").lower()

    if any(keyword in url for keyword in ("press", "news", "article", "blog")):
        return "N"
    if any(keyword in summary for keyword in ("benchmark", "industry", "sector", "market share")):
        return "B"
    if any(keyword in summary for keyword in ("regulator", "statutory", "government", "filing")):
        return "S"
    return "S"


@dataclass(frozen=True)
class CitationItem:
    label: str
    category: str
    number: int
    source: SourceEntry

    def render_line(self) -> str:
        """Represent the citation in a human-readable string."""
        title = self.source.title or "Untitled"
        retrieved = self.source.retrieved or "unknown date"
        confidence = self.source.confidence or "medium"
        summary = (self.source.summary or "").strip()
        original_id = self.source.id or ""

        parts = [
            f"{self.label} — {title}",
            f"retrieved {retrieved}",
            f"confidence {confidence}",
        ]
        if summary:
            parts.append(summary)
        if original_id and original_id.upper() != self.label:
            parts.append(f"original id {original_id}")
        parts.append(self.source.url)
        return " — ".join(parts)


class CitationCatalog:
    """Ordered catalogue of citations used for prompting and validation."""

    def __init__(self, items: Sequence[CitationItem]):
        self._items: List[CitationItem] = list(items)
        self._index: Dict[str, CitationItem] = {item.label: item for item in self._items}

    @property
    def items(self) -> List[CitationItem]:
        return list(self._items)

    @property
    def labels(self) -> List[str]:
        return [item.label for item in self._items]

    def get(self, label: str) -> CitationItem | None:
        return self._index.get(label)

    def render_catalog(self) -> str:
        if not self._items:
            return "No sources captured. Mark data gaps explicitly."
        return "\n".join(item.render_line() for item in self._items)


def create_citation_catalog(sources: Iterable[SourceEntry]) -> CitationCatalog:
    """Assign stable S#/N#/B# labels to the provided sources."""
    counters = {"S": 0, "N": 0, "B": 0}
    items: List[CitationItem] = []
    for entry in sources:
        category = _infer_category(entry)
        counters[category] += 1
        number = counters[category]
        label = f"{category}{number}"
        items.append(CitationItem(label=label, category=category, number=number, source=entry))
    return CitationCatalog(items)


@dataclass
class CitationValidationResult:
    ok: bool
    missing: bool
    unknown_labels: List[str]

    def message(self) -> str:
        if self.ok:
            return "Citations validated."
        parts: List[str] = []
        if self.missing:
            parts.append("No S#/N#/B# citations found in output.")
        if self.unknown_labels:
            parts.append(f"Unknown citation labels referenced: {', '.join(sorted(self.unknown_labels))}.")
        return " ".join(parts) if parts else "Citation validation failed."


def validate_citations(text: str, catalog: CitationCatalog) -> CitationValidationResult:
    """Ensure the output references only known citations."""
    allowed = set(catalog.labels)
    if not allowed:
        # Nothing to validate; treat as ok (data gaps should be marked manually).
        return CitationValidationResult(ok=True, missing=False, unknown_labels=[])

    full_matches = set(re.findall(r"(?:S|N|B)\d+", text))
    if not full_matches:
        return CitationValidationResult(ok=False, missing=True, unknown_labels=[])

    unknown = sorted(full_matches - allowed)
    ok = not unknown
    return CitationValidationResult(ok=ok, missing=False, unknown_labels=unknown)
