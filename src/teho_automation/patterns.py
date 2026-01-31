"""Load reusable opportunity patterns to guide report generation."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List

PATTERN_FILE = Path("docs/pattern_library.json")


@lru_cache(maxsize=1)
def load_patterns() -> List[Dict[str, Any]]:
    if not PATTERN_FILE.exists():
        return []
    try:
        data = json.loads(PATTERN_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def format_patterns() -> str:
    patterns = load_patterns()
    if not patterns:
        return "No pattern library available yet."
    lines = []
    for item in patterns:
        lines.append(
            "- {name} ({stage}): when to use – {when}; mechanism – {mechanism}; proof – {evidence}; key metrics – {metrics}".format(
                name=item.get("name", "Pattern"),
                stage=item.get("process_stage", ""),
                when=item.get("when_to_use", ""),
                mechanism=item.get("mechanism", ""),
                evidence=item.get("evidence", ""),
                metrics=", ".join(item.get("metrics", []) or []),
            )
        )
    return "\n".join(lines)
