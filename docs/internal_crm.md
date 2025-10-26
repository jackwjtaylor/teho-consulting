# Internal CRM & Ops Dashboard

The briefing queue and analytics now live inside the Next.js portal at `/admin`. This view replaces the old `landing/admin` page and lets you add companies, update statuses, and monitor funnel + engagement metrics in one place.

## 1. Environment Prerequisites

1. Supabase tables/policies: follow `docs/intake_pipeline.md` and `docs/supabase_reports.md` so `briefing_requests`, `reports`, `report_events`, and `outreach_events` exist with the right RLS policies.  
2. Portal secrets: in `teho-portal/.env.local` (or your hosting provider), set
   ```env
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_SERVICE_KEY=service_role_key
   NEXT_PUBLIC_SUPABASE_URL=...
   NEXT_PUBLIC_SUPABASE_ANON_KEY=...
   ```
   The `/admin` route queries Supabase with the service key on the server, so no additional login is required. Keep the deployed site behind a trusted network or SSO if you need stronger controls.

## 2. Accessing the Dashboard

1. Run the portal locally (`npm run dev` in `teho-portal/`) or open your deployed site.  
2. Visit `http://localhost:3000/admin` (or `<your-domain>/admin`).  
3. The page loads the latest queue plus KPI cards automatically; no extra configuration is needed once env vars are set.

## 3. Features

- **Add a company** – Form mirrors `teho queue-request`: enter company name, domain, persona, contacts, and optional notes. Submissions land in `briefing_requests` with `status = queued`.  
- **Filter & update status** – Use the status dropdown at the top-right to filter the queue. Each row includes a status select + save button that writes back to Supabase immediately. Automation (`teho process-queue`) watches the same table.  
- **Request automation runs** – Buttons in the queue and dedicated Automation card create entries in `public.automation_runs` (e.g., “generate summary”, “package snapshot”, “process queue”). The `teho automation-worker` command now polls this table continuously, flips jobs to `in_progress`, and records `succeeded` / `failed` along with the latest result/error payload so operators see the outcome inside `/admin`.  
- **Direct automation triggers** – Additional buttons call `/api/automation/run-process-queue` and `/api/automation/generate-report`, which spawn the local CLI (`teho`) immediately (configure `TEHO_CLI_PATH` / `TEHO_AUTOMATION_CWD` on the portal server).  
- **Research health & notes** – Each queue row now surfaces context gaps (missing domain/contact/email plus any `payload.missing_fields` data). Expandable panels show the latest `briefing_notes`, and you can append new notes inline without leaving the portal.  
- **QA checklist** – Inline form persists checklist progress into `public.qa_reviews`, highlights whether QA is “in progress” or “approved”, and records the reviewer email.  
- **Attachments** – Upload PDFs/screenshots per request; files go into the private `briefing-uploads` bucket and metadata in `public.briefing_attachments`, so the automation worker can fetch supporting docs before prompting.  
- **Report assets & overrides** – Dedicated card lists each `reports` entry, provides signed HTML/PDF links via `/api/report-link`, and lets you override stored paths (e.g., when uploading a bespoke PDF). Useful when packaging manually or after editing files locally.  
- **Outreach composer** – Dedicated card lets you enter `client_slug`, contact email, subject, and message. Submitting the form sends the teaser via Postmark (server action) and automatically logs a `sent` event in `outreach_events` with the subject/body stored in `metadata`. Set `POSTMARK_SERVER_TOKEN`, `POSTMARK_FROM_EMAIL`, and (optionally) `POSTMARK_MESSAGE_STREAM` in `teho-portal/.env.local`.  
- **Follow-up radar** – Highlights companies whose last outreach event is older than ~3 days, plus a manual event form so you can log follow-ups, replies, meetings, etc. into `outreach_events` directly from `/admin`.  
- **Pipeline lenses** – “Active pipeline”, “Needs QA”, and “Ready to send” cards surface the current workload based on `briefing_requests.status`.  
- **Engagement metrics** – Overview cards plus “Latest report interactions” and “Outreach signals” read from `report_events` and `outreach_events`. Anything logged via `teho log-outreach` or the portal download/view buttons will appear here.  
- **Client health** – The account health card aggregates report counts, last send date, and view/download tallies per `client_slug` to help prioritise follow-ups.

## 4. Operational Notes

- The service key is only used server-side; never expose it in client bundles or `landing/` assets.  
- If you prefer to keep `/admin` behind authentication, add an allowlist check before rendering (e.g., verify Supabase session email) or wrap the route with middleware.  
- Continue using `teho assign-portal-user` to control what clients see on `/dashboard`; staff access to `/admin` no longer depends on that metadata.  
- When adding more team members, share the `/admin` URL privately and rotate the service key if you suspect it leaked.
