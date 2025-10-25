"""Helpers for managing workspace paths."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class CompanyPaths:
    slug: str
    base_dir: Path

    @property
    def raw_dir(self) -> Path:
        return self.base_dir / "data" / "raw" / self.slug

    @property
    def reports_dir(self) -> Path:
        return self.base_dir / "reports" / self.slug

    @property
    def context_file(self) -> Path:
        return self.raw_dir / "context.json"

    @property
    def sources_file(self) -> Path:
        return self.raw_dir / "sources.csv"

    @property
    def qa_log(self) -> Path:
        return self.base_dir / "logs" / "qa" / f"{self.slug}.md"

    @property
    def attachments_dir(self) -> Path:
        return self.raw_dir / "attachments"

def get_company_paths(slug: str, base_dir: Path | None = None) -> CompanyPaths:
    """Return helpful Path objects for a given company slug."""
    base = base_dir or Path.cwd()
    return CompanyPaths(slug=slug, base_dir=base)
