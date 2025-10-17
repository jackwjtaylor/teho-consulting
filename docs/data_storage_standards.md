# Data Storage & Validation Standards

## Folder Structure

```
data/
  raw/
    {company_slug}/
      context.json            # structured prompt inputs
      sources.csv             # id,title,url,retrieved,notes
      research_notes.md       # optional human summary
      attachments/            # cached HTML, PDFs if allowed
reports/
  {company_slug}/
    executive.md
    comprehensive.md
    snapshot.md
    snapshot.pdf
logs/
  qa/
    {company_slug}.md
  outreach/
    activity.csv
```

Use lowercase slugified company names (e.g. `gousto`, `bloom-and-wild`). Keep supporting assets (screenshots, exports) in `attachments/` with descriptive filenames.

## File Naming Rules

- Dates use ISO format: `2025-10-07`.  
- Include version suffixes when iterating (`executive_v2.md`). Keep latest version without suffix once approved.  
- Source IDs follow `S1`, `S2`, etc., matching the source catalogue.

## Company Basics to Capture

| Field | What we need | Where to look | Tips |
| --- | --- | --- | --- |
| `BUSINESS_NAME` | Full company name (and legal name if different) | Company site, Companies House | Note common short names |
| `BUSINESS_URL` | Main website address | Google, press releases | Double-check for redirects |
| `HEADQUARTERS` | Town/city, region, country | About page, LinkedIn | Mention extra hubs if relevant |
| `FOUNDING_YEAR` | Year the firm started trading | About page, news archive | Mark “est.” if unsure |
| `OWNERSHIP_MODEL` | Private, public, PE-backed, etc. | Press releases, filings | Mention latest funding if known |
| `INDUSTRY_TAGS` | Plain English description of sector | Website copy, directories | Keep to 2–3 simple tags |
| `REVENUE_BAND` | Estimated annual revenue range | Public filings, trade press | State the source or basis |
| `HEADCOUNT_INFO` | Staff numbers or range | LinkedIn, job boards | Flag if growing or shrinking |
| `PRODUCT_SUMMARY` | Main products or services | Product pages, case studies | Use bullet points |
| `MISSION_SNIPPET` | Short mission or promise | About page, CEO letter | Quote with attribution |
| `PRIMARY_CONTACT` | Decision-maker name + role | Leadership page, LinkedIn | Store as “Name — Role” |
| `PRIMARY_EMAIL` | Best outreach email | PR contact, email finder | Confirm before sending |

## context.json Schema

```json
{
  "business_name": "",
  "business_url": "",
  "headquarters": "",
  "industry_tags": [],
  "revenue_band": "",
  "headcount_info": "",
  "founding_year": "",
  "ownership_model": "",
  "product_summary": [],
  "mission_snippet": "",
  "courier_partners": [],
  "go_to_market_notes": [],
  "operating_model_insights": [],
  "pain_point_indicators": [],
  "tech_stack_notes": [],
  "data_assets": [],
  "regulatory_notes": [],
  "recent_headlines": [],
  "competitor_list": [],
  "researcher_notes": "",
  "primary_contact": "",
  "primary_email": ""
}
```

Save arrays even if only one item is known, to keep the structure stable. Leave missing fields as `"UNKNOWN"` or empty lists and explain the gap in reports.

## Source Catalogue Fields

| Column | Description |
| --- | --- |
| `id` | Matches references in reports (`S1`, `S2`, ...). |
| `title` | Page or document title. |
| `url` | Direct link. |
| `retrieved` | Date fetched (ISO). |
| `summary` | One-line note on what the source supports. |
| `confidence` | High / Medium / Low assessment of reliability. |
| `notes` | Optional: context, access limits, or follow-up actions. |

## Validation Checklist (run before prompting)

1. **Schema check:** `context.json` validates against schema (script to confirm required keys present).  
2. **Empty fields:** All `"UNKNOWN"` entries have a research note explaining why.  
3. **Date freshness:** Headline and financial data older than 24 months flagged as refresh required.  
4. **Source mapping:** Every data point has a source ID; `sources.csv` has matching entries.  
4. **File paths:** Required files exist (`context.json`, `sources.csv`, at least one note file).  
5. **Sensitive data:** Ensure no personal data or paywalled content stored if licensing forbids.  
6. **Attachments:** Large files stored in `attachments/` with clear names; note any licensing restrictions.

## Future Automation Ideas

- Add a Python script (`scripts/validate_context.py`) to enforce schema, flag missing sources, and highlight stale headlines.  
- Consider using JSON Schema + `ajv`/`pydantic` for validation once the data pipeline grows.  
- Log validation results in `logs/validation/{company}.json` for audit trail.
