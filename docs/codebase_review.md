# Codebase Review

## Current Functionality
- **Automation CLI (`teho`)** orchestrates context validation, company scaffolding, signal collection, prompting, packaging, Supabase queue management, and outreach logging via Typer commands. It supports creating per-company folders, validating context completeness/recency, queueing requests (Supabase + CSV fallback), pulling and processing queued jobs (including attachment sync), generating executive/full reports with prompt templates, and packaging/uploading snapshot assets to Supabase storage. 【F:src/teho_automation/cli.py†L1-L205】【F:src/teho_automation/cli.py†L270-L375】
- **Context & source models** define the research schema (business info, headlines, contacts, sources) with helpers to surface missing fields, stale headlines, and load CSV sources for prompting. 【F:src/teho_automation/context.py†L1-L121】
- **Collectors + caching** fetch website overviews, recent headlines, and Trustpilot reviews with retry logic and a 7-day cache to avoid redundant calls; outputs are stored under each company’s `raw` folder. 【F:src/teho_automation/collector_runner.py†L1-L107】
- **Packaging & styling** render markdown reports into branded HTML/PDF assets using a shared palette and typography aligned with the landing site, with hooks for storage upload. 【F:src/teho_automation/packaging.py†L1-L85】
- **Operational docs** maintain an active task list capturing completed work (automation worker, portal/admin integrations, outreach logging) and upcoming priorities. 【F:docs/todo.md†L1-L57】

## Suggested Next Steps
- Integrate Companies House and enhanced news APIs to enrich `context.json` with financials/ownership and fresher headlines. 【F:docs/todo.md†L22-L33】
- Add contact enrichment (email heuristics + provider lookup) and confidence flags to improve outreach readiness before prompting. 【F:docs/todo.md†L23-L30】
- Stand up a scheduled runner (cron or GitHub Actions) for `teho process-queue`, with secrets documented, to keep automation flowing without manual triggers. 【F:docs/todo.md†L25-L27】
- Expand runbooks and compliance documentation (data retention, consent logging, secrets handling) so handover to other operators is safe and repeatable. 【F:docs/todo.md†L28-L33】
- Enhance PDF branding (cover/footer/page numbers) once final assets arrive to align client-facing exports with the landing aesthetic. 【F:docs/todo.md†L31-L33】
