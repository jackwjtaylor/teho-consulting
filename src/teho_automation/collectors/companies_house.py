"""Company profile enrichment via Companies House."""

from __future__ import annotations

import os
import json
from datetime import datetime
from typing import Dict, Optional

import requests

from ..context import CompanyContext, SourceEntry, append_sources, save_context
from ..paths import CompanyPaths

API_BASE = "https://api.company-information.service.gov.uk"


def _build_session(api_key: str) -> requests.Session:
    session = requests.Session()
    session.auth = (api_key, "")  # API key as username, blank password
    session.headers.update({"Accept": "application/json"})
    return session


def _search_company(session: requests.Session, name: str) -> Optional[str]:
    try:
        response = session.get(f"{API_BASE}/search/companies", params={"q": name, "items_per_page": 1})
        response.raise_for_status()
        payload = response.json()
    except Exception:
        return None
    items = payload.get("items") or []
    if not items:
        return None
    return items[0].get("company_number")


def _fetch_profile(session: requests.Session, company_number: str) -> Optional[Dict]:
    try:
        response = session.get(f"{API_BASE}/company/{company_number}")
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def _fetch_account_filings(session: requests.Session, company_number: str) -> Optional[Dict]:
    try:
        response = session.get(
            f"{API_BASE}/company/{company_number}/filing-history",
            params={"category": "accounts", "items_per_page": 5},
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def enrich_companies_house(
    paths: CompanyPaths,
    context: CompanyContext,
    *,
    company_name: str,
    company_number: Optional[str] = None,
) -> tuple[bool, str | None]:
    api_key = os.getenv("COMPANIES_HOUSE_API_KEY")
    if not api_key:
        return False, "COMPANIES_HOUSE_API_KEY not configured"

    session = _build_session(api_key)
    number = company_number or _search_company(session, company_name)
    if not number:
        return False, "No Companies House match found"

    profile = _fetch_profile(session, number)
    if profile is None:
        return False, "Companies House profile unavailable"
    filings = _fetch_account_filings(session, number) or {}

    payload = {
        "company_number": number,
        "company_name": profile.get("company_name"),
        "company_status": profile.get("company_status"),
        "date_of_creation": profile.get("date_of_creation"),
        "registered_office_address": profile.get("registered_office_address"),
        "sic_codes": profile.get("sic_codes", []),
        "accounts": profile.get("accounts", {}),
        "filing_history": filings.get("items", []),
        "retrieved_at": datetime.utcnow().isoformat(),
        "source": "Companies House",
    }

    output_path = paths.raw_dir / "companies_house.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    _update_context_from_profile(context, payload)
    save_context(str(paths.context_file), context)

    source_entry = SourceEntry(
        id=f"S-CH-{number}",
        title=f"Companies House profile for {payload.get('company_name', company_name)}",
        url=f"https://find-and-update.company-information.service.gov.uk/company/{number}",
        retrieved=datetime.utcnow().date().isoformat(),
        summary="Official company profile (status, accounts metadata) from Companies House",
        confidence="high",
    )
    sources_path = paths.raw_dir / "sources.csv"
    append_sources(str(sources_path), [source_entry])
    return True, None


def _update_context_from_profile(context: CompanyContext, payload: Dict) -> None:
    sic_codes = payload.get("sic_codes") or []
    for code in sic_codes:
        if code not in context.industry_tags:
            context.industry_tags.append(code)

    date_of_creation = payload.get("date_of_creation")
    if date_of_creation and not context.founding_year:
        context.founding_year = date_of_creation.split("-")[0]

    status = payload.get("company_status")
    if status:
        note = f"Companies House status: {status}"
        if note not in context.regulatory_notes:
            context.regulatory_notes.append(note)

    accounts = payload.get("accounts") or {}
    last_accounts = accounts.get("last_accounts") or {}
    if last_accounts:
        period_end = last_accounts.get("period_end_on")
        if period_end:
            context.operating_model_insights.append(
                f"Last accounts filed for period ending {period_end} (Companies House)."
            )

    registered_office = payload.get("registered_office_address") or {}
    address_line = ", ".join(str(value) for value in registered_office.values() if value)
    if address_line and not context.headquarters:
        context.headquarters = address_line
