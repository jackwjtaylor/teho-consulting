# Teho Consulting – Task List

## Doing now

- [x] Regenerate Gousto executive + summary assets with the new split prompt, modern styling, and Supabase upload.  
- [x] Tighten Supabase RLS so report rows are only visible to matched `client_slug`/`client_id` users (remove `policy = true`).  
- [x] Document how portal users get mapped to `client_slug` (admin workflow + Supabase metadata) and automate the sync.  
- [x] Polish portal UI (list view, buttons, inline viewer) to mirror the refreshed report styling.  
- [x] Update automation runbooks (data collection, QA, packaging) with portal/publishing steps.
- [x] Portal `/admin` can log automation requests (generate/package/process) via `automation_runs`.
- [x] Python automation worker consumes `automation_runs`, executes CLI actions, and writes back status/results.

## Lined up next

- [ ] Implement caching + retry layer for collectors (JSON/SQLite TTL 7 days, tenacity retries, asyncio parallelism).  
- [ ] Integrate Companies House API (filings, revenue, ownership) and evaluate News/headline APIs; wire results into context schema.  
- [ ] Add contact enrichment workflow (email pattern heuristics + first API provider such as Hunter/Clearbit) with confidence flags in `context.json`.  
- [ ] Create a GitHub Action/cron job to run `teho process-queue` (document secrets setup).  
- [ ] Choose interim orchestration (cron vs GitHub Actions) and document upgrade triggers for Prefect/Temporal.  
- [x] Implement outreach metrics pipeline (webhooks, Supabase tables, dashboard logging).  
- [ ] Outline runbooks so others can handle data collection, QA, outreach (extend from draft).  
- [ ] Define compliance/infosec measures (consent logging, data retention, secrets management).  
- [ ] Map process for refreshing financial data every quarter across all target companies.  
- [ ] Define pricing & payment flow for full briefing unlocks and advisory services (invoice, Stripe, etc.).  
- [ ] Draft customer-facing email templates (snapshot delivery, full briefing upsell, call follow-up).
- [ ] Invest in richer PDF branding (cover page, footer, page numbers once logo/brand kit lands).

## Already done

- [x] Created the main prompt (`prompt_v1`).  
- [x] Wrote the data collection checklist.  
- [x] Chosen the first pilot companies.  
- [x] Set up the `/data/raw` folder and saved the first company profile.  
- [x] Generated Gousto executive and full reports with the prompt.  
- [x] Produced board snapshot and teaser email assets in plain English.  
- [x] Documented workflow/RACI and data storage standards.  
- [x] Created automation project skeleton (pyproject, CLI scaffold, tests).  
- [x] Added initial automated collectors for website and news signals.  
- [x] Delivered prompt runner CLI with output validation.  
- [x] Created QA checklist and change-log template.  
- [x] Added Trustpilot/news/site signal aggregator and CLI command.  
- [x] Automated packaging (HTML/email draft with optional PDF support).  
- [x] Designed outreach metrics dashboard plan.  
- [x] Completed Bloom & Wild data pack (context, sources, reports) with outstanding data gaps flagged.
- [x] Rebuilt teho.ai marketing site with new product ladder and value-focused messaging.
- [x] Wired form + CLI queue into Supabase-ready workflow and added automation runner (`teho process-queue`).
- [x] Hooked public form + admin dashboard into Supabase via `config.js`, verified live submissions, and improved diagnostics.
- [x] Added automated Supabase storage uploads for generated reports and snapshots (with CLI flag + ensure-storage command).
- [x] Scaffolded `teho-portal` Next.js app with Supabase integration (login, dashboard shell, snapshot viewer).
- [x] Refreshed report HTML/CSS to match landing-page brand, regenerated Bloom & Wild assets, and uploaded HTML/PDF into Supabase.
