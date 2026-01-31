"""Load and format research bundles for board-level reports."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .patterns import format_patterns


@dataclass
class ResearchBundle:
    raw: Dict[str, Any]

    @property
    def company_snapshot(self) -> List[str]:
        return _ensure_list(self.raw.get("company_snapshot", {}).get("bullets"))

    @property
    def scale_signals(self) -> List[str]:
        return _ensure_list(self.raw.get("scale_signals", {}).get("bullets"))

    @property
    def recent_developments(self) -> List[Dict[str, str]]:
        return _ensure_list_of_dicts(self.raw.get("recent_developments", {}).get("entries"))

    @property
    def peer_signals(self) -> List[Dict[str, Any]]:
        return _ensure_list_of_dicts(self.raw.get("peer_signals", {}).get("entries"))

    @property
    def sector_benchmarks(self) -> List[Dict[str, Any]]:
        return _ensure_list_of_dicts(self.raw.get("sector_benchmarks", {}).get("entries"))

    @property
    def value_chain(self) -> List[Dict[str, Any]]:
        return _ensure_list_of_dicts(self.raw.get("value_chain", {}).get("stages"))

    @property
    def opportunities(self) -> List[Dict[str, Any]]:
        return _ensure_list_of_dicts(self.raw.get("opportunities", {}).get("entries"))

    @property
    def prioritisation(self) -> Dict[str, Any]:
        entries = _ensure_list_of_dicts(self.raw.get("prioritisation", {}).get("entries"))
        return {
            "entries": entries,
            "quick_wins": _ensure_list(self.raw.get("prioritisation", {}).get("quick_wins")),
            "big_bets": _ensure_list(self.raw.get("prioritisation", {}).get("big_bets")),
            "fill_ins": _ensure_list(self.raw.get("prioritisation", {}).get("fill_ins")),
            "postpone": _ensure_list(self.raw.get("prioritisation", {}).get("postpone")),
        }

    @property
    def risks(self) -> List[Dict[str, Any]]:
        return _ensure_list_of_dicts(self.raw.get("risks", {}).get("entries"))

    @property
    def architecture(self) -> Dict[str, Any]:
        data = self.raw.get("architecture", {})
        return {
            "description": data.get("description", ""),
            "flows": _ensure_list(data.get("flows")),
        }

    @property
    def pilot_plan(self) -> List[Dict[str, Any]]:
        return _ensure_list_of_dicts(self.raw.get("pilot_plan", {}).get("phases"))

    @property
    def capability_heatmap(self) -> List[Dict[str, Any]]:
        return _ensure_list_of_dicts(self.raw.get("capability_heatmap", {}).get("entries"))

    @property
    def sources(self) -> List[Dict[str, str]]:
        return _ensure_list_of_dicts(self.raw.get("sources", {}).get("entries"))


def load_research_bundle(path: Path) -> ResearchBundle:
    if not path.exists():
        raise FileNotFoundError(f"Research bundle not found at {path}")
    content = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(content, dict):
        raise ValueError(f"Research bundle must be a mapping: {path}")
    return ResearchBundle(raw=content)


def init_research_bundle(path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"Research bundle already exists at {path}")

    template = {
        "company_snapshot": {
            "bullets": [
                "Legal name: (S1)",
                "Products / services: (S2)",
                "Brands: (S3)",
                "Customer segments: (S4)",
                "Regions: (S5)",
                "Leadership: CEO … (S6)",
                "Data & AI maturity signals: (S7)",
            ]
        },
        "scale_signals": {
            "bullets": [
                "Headcount: (estimate) (S8)",
                "Revenue: (Data gap)",
                "Growth direction: (S9)",
            ]
        },
        "recent_developments": {
            "entries": [
                {"title": "", "date": "", "summary": "", "source": "", "url": ""}
            ]
        },
        "peer_signals": {
            "entries": [
                {
                    "name": "",
                    "evidence": [""],
                    "source": "",
                    "url": "",
                }
            ]
        },
        "sector_benchmarks": {
            "entries": [
                {"metric": "", "unit": "", "range": "", "source": "", "notes": ""}
            ]
        },
        "value_chain": {
            "stages": [
                {
                    "name": "Acquire",
                    "sub_processes": [
                        {
                            "name": "",
                            "pain_points": [""],
                            "kpis": [""],
                        }
                    ],
                }
            ]
        },
        "opportunities": {
            "entries": [
                {
                    "title": "",
                    "category": "Cost-out",
                    "mechanism": "",
                    "impact": "High",
                    "effort": "Medium",
                    "roi": [""],
                    "data_prereqs": [""],
                    "integrations": [""],
                    "guardrails": [""],
                    "metrics": [""],
                }
            ]
        },
        "prioritisation": {
            "entries": [
                {
                    "title": "",
                    "impact": "High",
                    "confidence": "Medium",
                    "effort": "Medium",
                    "strategic_fit": "High",
                    "data_readiness": "Medium",
                    "compliance_risk": "Low",
                    "score": "",
                }
            ],
            "quick_wins": [""],
            "big_bets": [""],
            "fill_ins": [""],
            "postpone": [""],
        },
        "risks": {
            "entries": [
                {
                    "opportunity": "",
                    "risks": [""],
                    "mitigations": [""],
                    "controls": [""],
                    "owner": "",
                }
            ]
        },
        "architecture": {
            "description": "",
            "flows": [""],
        },
        "pilot_plan": {
            "phases": [
                {
                    "name": "Discovery & Data Readiness",
                    "objectives": [""],
                    "activities": [""],
                    "owner": "Head of Operations",
                    "exit_criteria": [""],
                }
            ]
        },
        "capability_heatmap": {
            "entries": [
                {"area": "Data", "rating": "Medium", "commentary": ""}
            ]
        },
        "sources": {
            "entries": [
                {"id": "S1", "title": "", "url": ""},
            ]
        },
    }

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(template, sort_keys=False, allow_unicode=True), encoding="utf-8")


def extract_yaml_payload(output: str) -> str:
    text = output.strip()
    if not text:
        return text
    match = re.search(r"```(?:yaml)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        text = match.group(1).strip()
    return text


def bundle_to_prompt_fields(bundle: ResearchBundle) -> Dict[str, str]:
    return {
        "COMPANY_SNAPSHOT": _format_bullets(bundle.company_snapshot),
        "SCALE_SIGNALS": _format_bullets(bundle.scale_signals),
        "RECENT_DEVELOPMENTS": _format_recent_developments(bundle.recent_developments),
        "PEER_SIGNALS": _format_peer_signals(bundle.peer_signals),
        "SECTOR_BENCHMARKS": _format_sector_benchmarks(bundle.sector_benchmarks),
        "VALUE_CHAIN": _format_value_chain(bundle.value_chain),
        "OPPORTUNITIES": _format_opportunities(bundle.opportunities),
        "PRIORITISATION": _format_prioritisation(bundle.prioritisation),
        "RISKS": _format_risks(bundle.risks),
        "ARCHITECTURE": _format_architecture(bundle.architecture),
        "PILOT_PLAN": _format_pilot_plan(bundle.pilot_plan),
        "CAPABILITY_HEATMAP": _format_capability_heatmap(bundle.capability_heatmap),
        "SOURCES_APPENDIX": _format_sources(bundle.sources),
        "SOURCE_CATALOG": _format_sources(bundle.sources),
        "SOURCE_IDS": ", ".join(
            entry.get("id", "") for entry in bundle.sources if entry.get("id")
        )
        or "None",
        "PATTERN_LIBRARY": format_patterns(),
    }


def _ensure_list(value: Optional[Any]) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    return [str(value)]


def _ensure_list_of_dicts(value: Optional[Any]) -> List[Dict[str, Any]]:
    if not value:
        return []
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def _format_bullets(items: List[str]) -> str:
    return "\n".join(f"- {item}" for item in items) if items else "- (Data gap)"


def _format_recent_developments(entries: List[Dict[str, str]]) -> str:
    if not entries:
        return "| Title | Date | Summary | Source |\n| --- | --- | --- | --- |\n| (Data gap) | | | |"
    lines = ["| Title | Date | Summary | Source |", "| --- | --- | --- | --- |"]
    for item in entries:
        lines.append(
            f"| {item.get('title', '') or '(Data gap)'} | {item.get('date', '')} | {item.get('summary', '')} | {item.get('source', '')} |"
        )
    return "\n".join(lines)


def _format_peer_signals(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "- (Data gap)"
    output = []
    for item in entries:
        lines = [f"- **{item.get('name', '(unknown)')}**"]
        evidence = _ensure_list(item.get('evidence'))
        if evidence:
            lines.extend([f"  - {note}" for note in evidence])
        if item.get('source'):
            lines.append(f"  - Source: {item['source']}")
        if item.get('url'):
            lines.append(f"  - Link: {item['url']}")
        output.append("\n".join(lines))
    return "\n".join(output)


def _format_sector_benchmarks(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "| KPI | Range | Unit | Source | Notes |\n| --- | --- | --- | --- | --- |\n| (Data gap) | | | | |"
    lines = ["| KPI | Range | Unit | Source | Notes |", "| --- | --- | --- | --- | --- |"]
    for item in entries:
        lines.append(
            f"| {item.get('metric', '')} | {item.get('range', '')} | {item.get('unit', '')} | {item.get('source', '')} | {item.get('notes', '')} |"
        )
    return "\n".join(lines)


def _format_value_chain(stages: List[Dict[str, Any]]) -> str:
    if not stages:
        return "- (Data gap)"
    blocks: List[str] = []
    for stage in stages:
        stage_name = stage.get('name', '(Stage)')
        blocks.append(f"#### {stage_name}")
        for sub in _ensure_list_of_dicts(stage.get('sub_processes')):
            blocks.append(f"- **{sub.get('name', '(Process)')}**")
            pains = _ensure_list(sub.get('pain_points'))
            if pains:
                blocks.append("  - Pain points:")
                blocks.extend([f"    - {item}" for item in pains])
            kpis = _ensure_list(sub.get('kpis'))
            if kpis:
                blocks.append("  - KPIs:")
                blocks.extend([f"    - {item}" for item in kpis])
    return "\n".join(blocks)


def _format_opportunities(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "| Title | Category | Mechanism | Pattern | Impact | Effort | ROI | Data | Integrations | Guardrails | Metrics | Practical example | Exec rebuttal |\n| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n| (Data gap) | | | | | | | | | | | | |"
    lines = [
        "| Title | Category | Mechanism | Pattern | Impact | Effort | ROI | Data | Integrations | Guardrails | Metrics | Practical example | Exec rebuttal |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in entries:
        lines.append(
            "| {title} | {category} | {mechanism} | {pattern} | {impact} | {effort} | {roi} | {data} | {integrations} | {guardrails} | {metrics} | {example} | {rebuttal} |".format(
                title=item.get('title', ''),
                category=item.get('category', ''),
                mechanism=item.get('mechanism', ''),
                pattern=item.get('pattern', ''),
                impact=item.get('impact', ''),
                effort=item.get('effort', ''),
                roi="; ".join(_ensure_list(item.get('roi'))),
                data="; ".join(_ensure_list(item.get('data_prereqs'))),
                integrations="; ".join(_ensure_list(item.get('integrations'))),
                guardrails="; ".join(_ensure_list(item.get('guardrails'))),
                metrics="; ".join(_ensure_list(item.get('metrics'))),
                example=item.get('practical_example', ''),
                rebuttal=item.get('exec_rebuttal', ''),
            )
        )
    return "\n".join(lines)


def _format_prioritisation(prior: Dict[str, Any]) -> str:
    entries = prior.get('entries') or []
    if not entries:
        table = "| Title | Impact | Confidence | Effort | Strategic Fit | Data Readiness | Compliance Risk | Score |\n| --- | --- | --- | --- | --- | --- | --- | --- |\n| (Data gap) | | | | | | | |"
    else:
        lines = [
            "| Title | Impact | Confidence | Effort | Strategic Fit | Data Readiness | Compliance Risk | Score |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for item in entries:
            lines.append(
                f"| {item.get('title', '')} | {item.get('impact', '')} | {item.get('confidence', '')} | {item.get('effort', '')} | {item.get('strategic_fit', '')} | {item.get('data_readiness', '')} | {item.get('compliance_risk', '')} | {item.get('score', '')} |"
            )
        table = "\n".join(lines)

    lists = []
    for heading in ("quick_wins", "big_bets", "fill_ins", "postpone"):
        items = _ensure_list(prior.get(heading))
        title = heading.replace('_', ' ').title()
        if items:
            lists.append(f"- **{title}**")
            lists.extend([f"  - {item}" for item in items])
        else:
            lists.append(f"- **{title}**\n  - (Data gap)")

    return f"{table}\n\n" + "\n".join(lists)


def _format_risks(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "- (Data gap)"
    blocks = []
    for item in entries:
        blocks.append(f"- **{item.get('opportunity', '')}**")
        blocks.append("  - Risks:")
        blocks.extend([f"    - {risk}" for risk in _ensure_list(item.get('risks'))] or ["    - (Data gap)"])
        blocks.append("  - Mitigations:")
        blocks.extend([f"    - {mit}" for mit in _ensure_list(item.get('mitigations'))] or ["    - (Data gap)"])
        blocks.append("  - Controls:")
        blocks.extend([f"    - {ctrl}" for ctrl in _ensure_list(item.get('controls'))] or ["    - (Data gap)"])
        if item.get('owner'):
            blocks.append(f"  - Owner: {item['owner']}")
    return "\n".join(blocks)


def _format_architecture(data: Dict[str, Any]) -> str:
    description = data.get('description') or '(Data gap)'
    flows = _ensure_list(data.get('flows'))
    flow_text = "\n".join(f"- {flow}" for flow in flows) if flows else "- (Data gap)"
    return f"{description}\n\n{flow_text}"


def _format_pilot_plan(phases: List[Dict[str, Any]]) -> str:
    if not phases:
        return "- (Data gap)"
    output = []
    for phase in phases:
        output.append(f"- **{phase.get('name', '')}**")
        output.append("  - Objectives:")
        output.extend([f"    - {item}" for item in _ensure_list(phase.get('objectives'))] or ["    - (Data gap)"])
        output.append("  - Activities:")
        output.extend([f"    - {item}" for item in _ensure_list(phase.get('activities'))] or ["    - (Data gap)"])
        if phase.get('owner'):
            output.append(f"  - Owner: {phase['owner']}")
        output.append("  - Exit criteria:")
        output.extend([f"    - {item}" for item in _ensure_list(phase.get('exit_criteria'))] or ["    - (Data gap)"])
    return "\n".join(output)


def _format_capability_heatmap(entries: List[Dict[str, Any]]) -> str:
    if not entries:
        return "| Area | Rating | Commentary |\n| --- | --- | --- |\n| (Data gap) | | |"
    lines = ["| Area | Rating | Commentary |", "| --- | --- | --- |"]
    for item in entries:
        lines.append(
            f"| {item.get('area', '')} | {item.get('rating', '')} | {item.get('commentary', '')} |"
        )
    return "\n".join(lines)


def _format_sources(entries: List[Dict[str, str]]) -> str:
    if not entries:
        return "- (Data gap)"
    lines = []
    for item in entries:
        identifier = item.get('id', '')
        title = item.get('title', '')
        url = item.get('url', '')
        lines.append(f"- ({identifier}) {title} — {url}")
    return "\n".join(lines)
