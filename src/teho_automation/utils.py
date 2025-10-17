"""Shared utilities."""

from __future__ import annotations

import datetime as dt
from typing import Optional


def parse_iso_date(value: str) -> Optional[dt.date]:
    """Parse an ISO date string (YYYY-MM-DD) into date object."""
    try:
        return dt.date.fromisoformat(value)
    except Exception:  # pragma: no cover - defensive
        return None
