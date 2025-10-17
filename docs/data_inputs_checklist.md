# Lead Gen Data Checklist

## Why we use this

Before we run `prompt_v1`, we gather the facts in this list so the report feels grounded, fair, and honest about any gaps.

## Company basics to capture

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
| `PRIMARY_CONTACT` | Decision maker + role | Leadership page, LinkedIn | Format “Name — Role” |
| `PRIMARY_EMAIL` | Best outreach email | Press contact, email pattern tools | Confirm manually before send |

## How the business runs

| Field | What we need | Where to look | Tips |
| --- | --- | --- | --- |
| `GO_TO_MARKET_NOTES` | How they sell and to whom | Sales pages, webinars | Note partners or channels |
| `OPERATING_MODEL_INSIGHTS` | Key steps in their workflow | Careers posts, help centre | Relate to value chain if possible |
| `PAIN_POINT_INDICATORS` | Signs of issues or friction | Customer reviews, forums, news | Group by function (e.g. delivery, support) |
| `TECH_STACK_NOTES` | Tools, platforms, AI hints | Job ads, engineering blog, StackShare | Add confidence level (high/medium/low) |
| `DATA_ASSETS` | Data they likely hold | Product copy, privacy policy | Flag guesses as assumptions |
| `REGULATORY_NOTES` | Rules they must follow | Industry sites, legal briefings | Mention region-specific rules |
| `RECENT_HEADLINES` | 3–5 news items from last 24 months | Google News, newsroom | Include ISO date and mark anything older as “Data gap – refresh”. |
| `COMPETITOR_LIST` | 3–5 main rivals | Analyst notes, “alternatives” pages | Split by segment if needed |

## Handy reference numbers

| Metric | Why it helps | Possible sources |
| --- | --- | --- |
| Revenue per employee | Benchmark efficiency | Industry reports, listed peers |
| Typical salary bands | Size cost/time savings | Payscale, Glassdoor, ONS data |
| Customer count clues | Judge scale of impact | Case studies, testimonials, filings |
| Average cycle times | Compare speed of service | Trade articles, ops blogs |

## Suggested workflow

1. **Initial search** – Combine the company name with words like “overview”, “funding”, “AI”, “customer story”.  
2. **Website skim** – Capture facts from About, Products, Careers, Blog, and News pages.  
3. **People signals** – Scan LinkedIn and job boards for team size, hiring focus, and tech clues.  
4. **Filings and databases** – Review Companies House, SEC, or trusted directories for finances and ownership.  
5. **Customer and staff feedback** – Read reviews on Trustpilot, G2, Glassdoor, and relevant forums.  
6. **Competitor check** – Note rival claims from comparison pages, rankings, and analyst write-ups.  
7. **Regulation** – List any licences, data rules, or safety standards that shape how they can use AI.

Tag every source with a unique ID, save the quote with its link and date, and store the notes in JSON, a spreadsheet, or our shared workspace so the prompt can cite everything clearly.
