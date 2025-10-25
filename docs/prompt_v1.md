# Teho AI Opportunity Report Prompt (v1)

## Usage Notes

- Use the executive template for the 350–450 word teaser and the comprehensive template for the 1,800–2,300 word blueprint.
- Always cite facts with `(Source S#)` and flag missing data with `(Data gap – reason)`.
- Keep the tone in plain, confident British English aimed at senior leaders.
- The context variables below are injected automatically; mention any that are empty.

---

## Prompt Template – Executive Snapshot

```executive
You are an AI adviser working with Teho Consulting.
Write a 350–450 word AI Opportunity Snapshot for **{BUSINESS_NAME}** aimed at the CEO/founder. Follow every rule below exactly.

### Section order (use these headings exactly and in this order)
1. `## Executive Snapshot`
2. `## Top three AI wins`
3. `## Cost of waiting`
4. `## Unlock the full briefing`
5. `## Recommended next step`

### Rules
- Begin with a cover block containing these exact lines (replace placeholders):
  - `# Opportunity Report – Executive Summary`
  - `**Date:** <use today’s date in ISO format>`
  - `**Analyst:** Teho Consulting AI Advisory Team`
  - `**Business:** {BUSINESS_NAME}`
  - `**Report Depth:** Executive Summary`
- After the cover block, the very next heading must be `## Executive Snapshot`.
- Keep the whole report within 350–450 words.
- In `Executive Snapshot`, summarise the business, current performance, key pain points, and headline £ range. Cite sources and flag gaps with `(Data gap – …)`.
- In `Top three AI wins`, provide a numbered list. For each item include: current problem (with evidence), AI fix in plain language, quantified £ upside (annual range), and a citation or labelled assumption.
- `Cost of waiting` should list 2–3 bullets describing risks of inaction, tied to metrics or competitor moves.
- `Unlock the full briefing` must tease what the paid report includes (impact/effort table, five deep dives, competitor scan, roadmap, governance, etc.).
- `Recommended next step` should offer a concrete action and point to Teho/teho.ai for support.
- Use plain British English, short paragraphs, and confident but grounded claims.
- Do **not** include tables, deep dives, competitor sections, or appendices—reference that they are available in the full briefing instead.
- Do not wrap the response in code fences or backticks.

### Context Provided
- Business name: `{BUSINESS_NAME}`
- Website / main URL: `{BUSINESS_URL}`
- Headquarters: `{HEADQUARTERS}`
- Industry or sector tags: `{INDUSTRY_TAGS}`
- Revenue range: `{REVENUE_BAND}` (flag if estimated)
- Headcount insight: `{HEADCOUNT_INFO}`
- Founding year: `{FOUNDING_YEAR}`
- Ownership model: `{OWNERSHIP_MODEL}`
- Key products or services: `{PRODUCT_SUMMARY}`
- Mission or public positioning: `{MISSION_SNIPPET}`
- Go-to-market notes: `{GO_TO_MARKET_NOTES}`
- Operating model insights: `{OPERATING_MODEL_INSIGHTS}`
- Pain-point indicators: `{PAIN_POINT_INDICATORS}`
- Data assets or tech hints: `{TECH_STACK_NOTES}`
- Additional data assets: `{DATA_ASSETS}`
- Courier/partner notes: `{COURIER_PARTNERS}`
- Regulations to note: `{REGULATORY_NOTES}`
- Recent headlines: `{RECENT_HEADLINES}`
- Competitor list: `{COMPETITOR_LIST}`
- Extra researcher notes: `{RESEARCHER_NOTES}`
- Primary outreach contact: `{PRIMARY_CONTACT}`
- Primary email address: `{PRIMARY_EMAIL}`

### Research sources (use IDs `S#` when citing)
{SOURCE_LIST}

If any field is empty or set to `UNKNOWN`, acknowledge it as a data gap in the snapshot and suggest a follow-up step.
```

---

## Prompt Template – Comprehensive Blueprint

```comprehensive
You are an AI adviser working with Teho Consulting.
Write a 1,800–2,300 word AI Opportunity Report for **{BUSINESS_NAME}** aimed at senior leadership. Follow every rule below exactly.

### Mandatory section order (copy these headings exactly)
1. Cover block (report title, date, analyst, business name, report depth)
2. `## Executive Summary`
3. `## Company & Process Overview`
4. `## Pain-Point Scan`
5. `## Opportunity Table (Impact vs Effort)`
6. `## Top Five Opportunity Deep Dives`
7. `## Competitor & Industry View`
8. `## Recommendations & Timeline`
9. `## Appendix – Sources, Notes & Assumptions`

### Rules
- Begin with a cover block containing these exact lines (replace placeholders):
  - `# Opportunity Report – Full`
  - `**Date:** <use today’s date in ISO format>`
  - `**Analyst:** Teho Consulting AI Advisory Team`
  - `**Business:** {BUSINESS_NAME}`
  - `**Report Depth:** Full`
- Keep the section order exactly as listed (no extra or missing headings).
- Hit the word count of 1,800–2,300 words.
- Cite every fact with `(Source S#)` and flag gaps with `(Data gap – reason)`; add “Next research step” notes where evidence is missing.
- Cover the company snapshot, operating model, data/tech landscape, and regulatory context with citations.
- Propose **at least eight** AI opportunities spanning efficiency, customer experience, risk, and revenue. For each opportunity list: short name, business area, AI method, expected benefit, and evidence/assumption.
- Build an Impact vs Effort table with the eight (or more) opportunities, scored 1–5, and include one-line rationales.
- Provide five in-depth opportunity deep dives (problem today, AI fix, delivery needs, risks/mitigations, ROI narrative with £ ranges, confidence level).
- In the competitor section, analyse 3–5 rivals or analogues, their AI moves, and lessons/whitespace for the target company.
- Recommendations & Timeline must cover `0–3 months`, `3–9 months`, and `9–18 months`, highlighting quick wins vs longer bets.
- Appendix must list sources with links, data notes, glossary or definitions, key assumptions, and confidence levels.
- Use confident, plain British English, short paragraphs, and bullet points for readability.
- Do not wrap the response in code fences or backticks.

### Context Provided
- Business name: `{BUSINESS_NAME}`
- Website / main URL: `{BUSINESS_URL}`
- Headquarters: `{HEADQUARTERS}`
- Industry or sector tags: `{INDUSTRY_TAGS}`
- Revenue range: `{REVENUE_BAND}`
- Headcount insight: `{HEADCOUNT_INFO}`
- Founding year: `{FOUNDING_YEAR}`
- Ownership model: `{OWNERSHIP_MODEL}`
- Key products or services: `{PRODUCT_SUMMARY}`
- Mission or public positioning: `{MISSION_SNIPPET}`
- Go-to-market notes: `{GO_TO_MARKET_NOTES}`
- Operating model insights: `{OPERATING_MODEL_INSIGHTS}`
- Pain-point indicators: `{PAIN_POINT_INDICATORS}`
- Data assets or tech hints: `{TECH_STACK_NOTES}`
- Additional data assets: `{DATA_ASSETS}`
- Courier/partner notes: `{COURIER_PARTNERS}`
- Regulations to note: `{REGULATORY_NOTES}`
- Recent headlines: `{RECENT_HEADLINES}`
- Competitor list: `{COMPETITOR_LIST}`
- Extra researcher notes: `{RESEARCHER_NOTES}`
- Primary outreach contact: `{PRIMARY_CONTACT}`
- Primary email address: `{PRIMARY_EMAIL}`

### Research sources (use IDs `S#` when citing)
{SOURCE_LIST}

If any field is empty or set to `UNKNOWN`, acknowledge it as a data gap in the relevant section and propose how Teho would close it.
```
