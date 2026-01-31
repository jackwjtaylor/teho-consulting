# Agent Guide – Teho Consulting

## 1. Mission Snapshot
- **Business**: Teho Consulting delivers remote-first AI opportunity strategy for UK SMB/Mid-market leaders.  
- **Lead product**: Hyper-tailored AI opportunity ladder – starts with a free “Opportunity Snapshot”, upsells to paid briefings, exec Q&A, blueprints, and quarterly advisory.  
- **Vision**: Operate as a one-person, automation-heavy revenue engine. Humans step in only for judgement-heavy tasks (company selection, QA, client conversations).

## 2. Repo Tour
- `docs/` – strategy collateral: prompt (`prompt_v1.md`), workflow/automation plans, QA checklist, dashboard blueprint, data standards, pilot list, TODO.
- `reports/` – generated assets (e.g. Gousto, Bloom & Wild). Each company keeps `summary.md`, `full.md`, and packaged HTML/PDF/email files.
- `data/raw/{slug}/` – context JSON per schema (`docs/data_storage_standards.md`), `sources.csv`, `automation_signals.json`, QA logs.
- `src/teho_automation/` – Python package powering automation (CLI commands, collectors, prompt runner, packaging).
- `landing/teho/` – hand-coded marketing site (HTML/CSS) reflecting the new product ladder and used for public lead capture.
- `../teho-portal/` – Next.js + Supabase client portal (magic-link auth, briefing list, inline HTML viewer, PDF download).

## 3. Automation Stack & Commands
- Environment: Python 3.11+, optional `.venv`. Install with `pip install -e .[dev]`.
- Tests: `pytest`.
- CLI entrypoint: `teho` (Typer). Key commands:
  - `teho init-company <slug>` – scaffold folders.
- `teho collect-signals <slug> --domain example.com` – run web/news/review collectors.
- `teho validate-context data/raw/<slug>/context.json` – schema + recency check (flags headlines older than 24 months).
- `teho generate <slug> --report executive --report comprehensive` – call OpenAI using `OPENAI_API_KEY`; add `--dry-run` to inspect prompts without hitting the API.
- `teho package <slug>` – convert snapshot markdown to branded HTML/PDF and produce teaser email copy.
- `teho init-research <slug>` – scaffold the YAML research bundle required for the board-grade report; fill it with sourced bullets, tables, and opportunity data before generation.
- `teho generate <slug> --report board` – run the master prompt to create the McKinsey/Bain-style automation deck (requires the research bundle + context). Saves Markdown/HTML/PDF + email draft.
- `teho run-job <slug>` – end-to-end pipeline: initialise folders, collect web/news signals, pull Companies House filings (when `COMPANIES_HOUSE_API_KEY` is set), build the research bundle, generate full + summary + board reports, package the snapshot, and upload HTML/PDF/email assets to Supabase.
- `teho queue-request "Company" --domain example.com [...]` – append to `data/company_queue.csv` for manual/internal triggers.
- `teho list-requests [--status queued]` – inspect Supabase queue (falls back to CSV locally).
- `teho process-queue --limit 1 --generate --package` – pull queued requests, initialise folders, optionally generate reports and package assets.
- `teho assign-portal-user <email> <client-slug>` – attach client metadata to a Supabase auth user so the portal RLS works.
- `teho log-outreach --client-slug <slug> --contact-email <email> --event-type <sent|opened|clicked|replied>` – capture outreach signals for analytics.
- `teho automation-worker --poll 30` – optional background loop; the portal now runs `teho run-job <slug>` inline when you click “Run full job”.
- Automation design notes live in `docs/automation_blueprint.md` & `docs/workflow_map.md`.
- Intake specifics & Supabase schema live in `docs/intake_pipeline.md`.
- Internal CRM + analytics live at `/admin` in the portal (service-key powered queue + dashboard).
- Portal rendering pulls HTML/PDF from Supabase storage; ensure assets are uploaded when running `teho generate`/`teho package`.

## 4. Product Ladder (Client-Facing)
1. **Opportunity Snapshot** – free one-page teaser sent by email.
2. **Full Opportunity Briefing Unlock (£300–£500)** – full report delivered digitally; includes optional complimentary debrief call.
3. **Executive AI Q&A Session (£600 each / bundles)** – remote 60-minute sessions for leadership teams.
4. **Opportunity Blueprint (£3k–£5k each)** – detailed delivery plan, metrics, stakeholder map; Teho hands over execution.
5. **Leadership Readiness Workshop (£1.5k–£2k)** – remote alignment session + memo.
6. **Quarterly Advisory Subscription (£4k–£6k/quarter)** – refreshed briefings, competitor watch, exec roundtable.
7. **Add-ons** – vendor shortlist/RFP pack, internal comms kit, investor briefing.

## 5. Current Status (Oct 2025)
- **Reports**: Solar Wines & PHMG run end-to-end through the new “Run full job” button (collect → full + summary → packaged snapshot → email draft). Gousto still needs regeneration with the new flow.
- **Prompt**: `docs/prompt_v1.md` is being upgraded to the master McKinsey/Bain-style instruction (see plan in TODO). Current outputs still reference the older structure.
- **Automation**: collectors for website, news, Trustpilot; Companies House enrichment drops structured filings into each context when the API key is present; prompt runner validates output sections; packaging outputs branded HTML/PDF/email and stores them in Supabase, now writing `email_draft.txt` for the portal to reuse.
- **Portal**: `/admin` runs the CLI inline, displays QA assets via a styled viewer, auto-populates outreach drafts, logs events in Supabase, and now includes a “Clear completed” automation queue button plus smarter QA links that always pick the latest upload. Requires Supabase auth metadata to match `client_slug`.
- **Landing site**: `landing/teho/` marketing pages with updated palette. Public form posts into Supabase + CLI queue.

## 6. Active Work & Priorities
- Consult `docs/todo.md` (kept current). Highlights:
  - Regenerate Gousto (and future clients) using the new full-job flow.
  - Build the research pipeline to meet the master AI consulting instruction: source-backed snapshot, sector benchmarks, peer signals, and opportunity scoring.
  - Add citation tooling (S#/N#/B#) and value-model validation before reports ship.
  - Continue compliance, outreach metrics, and pricing track once report quality is locked in.

## 7. Key Considerations
- **Data recency**: Reports must cite sources ≤24 months old. Validation flags stale entries; update `sources.csv` before sending.
- **Citations**: The CLI builds an S#/N#/B# catalogue from `sources.csv` and fails generation if citations are missing or reference unknown IDs—keep the sources list clean.
- **Tone**: All copy and reports use plain, friendly British English. Avoid jargon and exposing internal automation mechanics to clients.
- **Manual gates**: QA checklist (`docs/qa_checklist.md`) is mandatory before shipping any report; log findings under `logs/qa/{company}.md`.
- **Secrets**: Store API keys (OpenAI, future data sources) in `.env` and never commit. Add guardrails before wiring to the web form.
- **Landing form**: On production integration, POST to a secure endpoint that writes to the queue (and triggers `teho` workflows). Add analytics hooks once backend is ready.

## 8. Quick Start for New Agent
1. `python -m venv .venv && source .venv/bin/activate`  
   `pip install -e .[dev]`
2. `pytest` to ensure baseline passes.
3. Review `docs/todo.md` and `data/company_queue.csv` (plus Supabase requests) to pick your next action.
4. If working on a company:
   - `.venv/bin/teho run-job <slug>` mirrors the portal pipeline (collectors, Companies House enrichment, research bundle, full + summary + board generation, packaging, uploads). Use the manual steps below only when you need to re-run a specific stage.
   - `teho validate-context data/raw/<slug>/context.json`
   - Refresh sources/headlines as needed.
   - (Optional) `teho research <slug>` to regenerate the research bundle manually; the portal runs this (plus Companies House enrichment) automatically when you click “Run full job”.
   - `teho generate <slug> --report executive --report snapshot` (use `--dry-run` first if needed).
   - QA via checklist, then `teho package <slug>` to create/upload snapshot assets.
   - Regenerate full reports with `.venv/bin/teho generate <slug> --report executive --report comprehensive --upload` when data is ready.
   - When the research pack is complete (either via automation or manual edits), run `.venv/bin/teho generate <slug> --report board --upload` to produce the board-level briefing.
5. For landing/ops tasks, edit under `landing/teho/` or `../teho-portal/`, keeping design aligned with the current palette, then run `npm run dev` inside the portal for local testing.

## 9. Contact & Handover Notes
- Founder: Jack Taylor – handles outreach conversations and strategic decisions.
- Communications: Use `reports/*/snapshot.md` as basis for outreach emails until automated templates are finalised.
- Landing previews: `python3 -m http.server 8000` (or `/usr/bin/python3 ...`) then visit `/landing/teho/index.html`.
- Before leaving a session, update `docs/todo.md`, QA logs, and commit with meaningful messages.

This guide should keep future agents aligned on the current state, assets, and immediate priorities. Update it whenever significant process or product changes land.
