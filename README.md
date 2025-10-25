# Teho Consulting

## About the Project

Teho Consulting is building simple AI-led services for UK businesses. Our first focus is a lead generation workflow that creates tailored AI opportunity briefings for decision makers. This repository holds the prompts, research guides, reports, portal, and plans we are using while the offer takes shape.

## Useful Files

- `docs/prompt_v1.md` – main prompt used to generate the reports.
- `docs/data_inputs_checklist.md` – guide to the information we gather before running a prompt.
- `docs/pilot_companies.md` – current list of pilot companies we are testing with.
- `docs/intake_pipeline.md` – Supabase queue + intake workflow for the website and automation runner.
- `reports/` – working reports and one-page snapshots.
- `docs/todo.md` – running task list.
- `landing/config.example.js` – copy to `landing/config.js` with your Supabase URL + anon key for the public form and admin dashboard.
- `teho-portal/` – Next.js + Supabase client portal (magic-link auth, inline HTML viewer, PDF downloads).
- `/admin` inside `teho-portal` – consolidated queue + analytics dashboard (see `docs/internal_crm.md`).
- `docs/supabase_reports.md` – RLS + metadata setup so the portal only shows reports for the right client.

## Report Workflow & Storage

- Generate or refresh assets with:
  ```bash
  .venv/bin/teho generate <slug> --report executive --report comprehensive --report snapshot
  .venv/bin/teho package <slug>
  ```
- Track outreach/activity with:
  ```bash
  .venv/bin/teho log-outreach --client-slug <slug> --contact-email <email> --event-type sent
  ```
- This produces `reports/<slug>/summary.*` for the executive teaser and `reports/<slug>/full.*` for the comprehensive briefing, alongside the packaged HTML/PDF/email assets.
- By default the CLI now creates/uses a Supabase Storage bucket called `reports` and uploads the generated Markdown, branded HTML, PDF (if WeasyPrint is installed), and email draft. Use `--no-upload` on either command to skip this step.
- To (re)create the storage bucket manually run:
  ```bash
  .venv/bin/teho ensure-storage
  ```
- All files are stored at `reports/<slug>/opportunity-report/...` inside Supabase Storage, ready to be surfaced in the client portal.
- Regenerated assets now use the landing-page palette and Inter font so the inline viewer and PDFs share a consistent brand.

## Getting Involved

Review `docs/todo.md` for the current priorities, or open the `reports/` folder to see the latest output.

### Portal quick start

```bash
cd ../teho-portal
npm install
npm run dev
```

Set `SUPABASE_URL`, `SUPABASE_ANON_KEY`, and `NEXT_PUBLIC_SUPABASE_URL`/`NEXT_PUBLIC_SUPABASE_ANON_KEY` in `teho-portal/.env.local`. Portal users need a `client_slug` in Supabase auth metadata that matches the `client_slug` column in `reports`.

Assign metadata quickly with:

```bash
.venv/bin/teho assign-portal-user client@example.com acme-co
```

Use `http://localhost:3000/admin` for the internal CRM + analytics view (see `docs/internal_crm.md` for env requirements) and `/dashboard` for the client-facing report list.
