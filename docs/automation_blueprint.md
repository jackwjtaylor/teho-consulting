# Automation Blueprint

Goal: run the end-to-end lead-gen workflow with minimal manual effort so a single operator can manage volume and scale to £1m revenue. Human touchpoints remain only where judgement is crucial (company selection, QA sign-off, high-value conversations).

## Architecture at a Glance

- **Trigger layer:** Web form / API intake lands in Supabase `briefing_requests` (CLI can fall back to CSV locally).  
- **Orchestration:** Lightweight scheduler (GitHub Actions or cron) calls Python workflow; migrate to Prefect/Temporal once volume >10 companies/week.  
- **Data gathering:** Python scripts use requests/BeautifulSoup/APIs to fetch company info, filings, reviews, news. Results stored in structured JSON per schema. Portal uploads (screenshots, PDFs) sync automatically into `data/raw/{slug}/attachments` so manual research files ride along with each run.
- **Contact enrichment:** Automation drafts primary contact suggestions (leadership names + guessed emails) and flags them for manual confirmation before outreach.
- **LLM runner:** Script calls OpenAI (or self-hosted model) with `prompt_v1`, generating `summary.md` (teaser), `full.md` (comprehensive), and snapshot markdown. Handles retries, temperature, and automatic “data gap” tags.  
- **Storage:** Repo folder structure per `docs/data_storage_standards.md` plus Supabase `public.reports` + storage bucket for HTML/PDF assets. Consider S3/Blob storage if you outgrow Supabase.  
- **Packaging:** Script renders snapshot to branded PDF, creates the teaser email, and uploads summary/full HTML/PDF to Supabase (signed URLs for portal).  
- **Outreach automation:** Postmark/Sendgrid automation triggers send with personalised tokens (including Supabase-hosted links); integrates with CRM (HubSpot/Pipedrive).
- **Worker service:** `teho automation-worker` polls `automation_runs`, executes CLI actions (generate/package/process), and marks each job `in_progress` → `succeeded/failed` in Supabase so `/admin` reflects the latest result.
- **Analytics:** Webhook logs events (opens/clicks) into a central sheet or database. Dashboard built with Looker Studio or Retool.  
- **Monitoring:** Slack/Email alerts on job failures, schema validation errors, or responses needing human follow-up.

## Automation Steps

1. **Company intake job**  
   - Validate inputs (country, size).  
   - If approved, create `data/raw/{company}` folder and seed `context.json` template.

2. **Data enrichment job**  
   - Crawl website sections, fetch Companies House filing summaries, pull latest headlines (news API), scrape Trustpilot/Glassdoor summaries.  
   - Cache outputs (JSON/SQLite) with 7-day TTL and retry failed fetches with backoff.  
   - Tag each snippet with source ID, confidence, and refresh timestamp.  
   - Run schema validator; if critical fields missing, send task to manual queue.

3. **Prompt generation job**  
   - Combine `context.json` and `sources.csv`.  
   - Generate executive summary (`summary.md`), comprehensive blueprint (`full.md`), and snapshot markdown with depth-specific prompt blocks.  
   - Compare full output to required section list; auto-flag missing sections.  
   - Save to `/reports/{slug}` and log Supabase payload (client_slug + report_key).  

4. **Automated QA pre-checks**  
   - Lint Markdown (headings, tables).  
   - Confirm each source ID referenced exists.  
   - Ensure “Data gap” appears for empty fields.  
   - Generate summary of assumptions for human reviewer.

5. **Human QA gate**  
   - Reviewer scans the summary, spot-checks high-risk sections, approves or edits.  
   - Edits logged and fed back into prompts/settings.

6. **Packaging & publishing job**  
   - Render snapshot PDF with template (e.g. Jinja + WeasyPrint).  
   - Merge quantified bullets into teaser email HTML and verify CTA links.  
   - Upload summary/full HTML + PDF to Supabase storage and upsert `public.reports` with signed paths, model info, and `client_slug`.  
   - Attach Supabase asset references (or signed URLs) to CRM/outreach records.  

7. **Send & track job**  
   - Schedule initial email and follow-up.  
   - Confirm portal user metadata exists (`teho assign-portal-user`) so recipients can unlock reports securely.  
   - Capture sends/opens/clicks via webhook or CLI (`teho log-outreach`) into `outreach_events`.  
   - Auto-create tasks when replies arrive or links clicked multiple times.  

8. **Feedback loop job**  
   - Weekly script compiles metrics: response rates, meetings booked, prompt issues.  
   - Generates report for founder review; backlog items created automatically.

## Tech Stack Suggestions

- **Language:** Python 3.11 for scripts; Node optional for landing page automation.  
- **Storage:** Git for versioned artefacts, S3 for large files, Postgres/SQLite for logs.  
- **Caching:** SQLite/JSON store with TTL to reduce scraping/API calls; tenacity for retries.  
- **Scheduling:** GitHub Actions + cron for MVP; Prefect Cloud or Temporal for scale.  
- **Validation:** Pydantic for schema, pytest for unit tests on scrapers.  
- **PDF/Email:** Pandoc/WeasyPrint for PDF, Resend/Postmark for transactional email.  
- **Dashboard:** Google Sheets + Looker Studio or Retool for quick setup.  
- **Alerts:** Slack webhook via Zapier, or Opsgenie if needed later.

## Manual Review Points

- **Weekly intake review:** sanity-check queued companies.  
- **Report QA:** brief review of executive summary, top opportunities, and ROI figures.  
- **High-value lead interactions:** personal replies or call prep.  
- Everything else runs unattended, with alerts for failure.

## Scaling Notes

- **Parallelism:** run multiple companies in parallel once scripts are idempotent and API limits allow.  
- **Caching:** store scraped data with timestamps to avoid hitting rate limits; only refresh stale entries.  
- **Fallback modes:** if an automation step fails (e.g. news API), log the gap and proceed; do not block entire pipeline.  
- **Security:** keep API keys in `.env` or secrets manager; encrypt PII if stored.  
- **Cost control:** monitor OpenAI usage per report; consider caching embeddings or switching to cheaper models when feasible.

## Next Build Tasks

- [ ] Layer caching + retries across collectors (JSON/SQLite TTL 7 days, tenacity, asyncio).  
- [ ] Integrate Companies House API for financials/ownership and evaluate headline/news APIs.  
- [ ] Add contact enrichment helper (pattern detection + Hunter/Clearbit integration with confidence scoring).  
- [ ] Create QA summary generator (auto highlights assumptions, missing fields).  
- [ ] Automate PDF/email packaging and integrate with send service.  
- [ ] Wire landing page + gated access workflow.  
- [ ] Set up tracking dashboard + alerting.  
- [ ] Document recovery steps for failed jobs.  
- [ ] Implement optional filings/job-posting scrapers for deeper insight.
