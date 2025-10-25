# Supabase Reports Table & Access Control

This guide secures the report catalogue that the client portal reads. Complete these steps after the `briefing_requests` setup from `docs/intake_pipeline.md`.

## 1. Create/Update the `reports` Table

Run the following SQL in the Supabase SQL editor. Adjust schema/extension install if needed.

```sql
create table if not exists public.reports (
  id uuid primary key default uuid_generate_v4(),
  client_slug text not null,
  report_key text not null,
  display_name text not null,
  html_path text,
  pdf_path text,
  generated_at timestamptz default now(),
  model text,
  notes text,
  created_at timestamptz default now()
);

create unique index if not exists reports_slug_key_idx
  on public.reports (client_slug, report_key);
```

> The automation automatically upserts using `client_slug` + `report_key` and stores the storage paths created during `teho generate` / `teho package`.

## 2. Enable Row-Level Security

```sql
alter table public.reports enable row level security;
```

## 3. Add RLS Policies

Allow the automation (service key) to read/write everything, and restrict authenticated users to rows where their JWT metadata contains the matching `client_slug`. Add additional staff e-mails if you need broader access.

```sql
-- Remove existing policies if you created placeholders earlier
drop policy if exists "reports service" on public.reports;
drop policy if exists "reports client access" on public.reports;
drop policy if exists "reports staff access" on public.reports;

-- Automation / CLI (service role) – full access
create policy "reports service"
  on public.reports
  for all
  to service_role
  using (true)
  with check (true);

-- Portal users – read-only, scoped to their client_slug metadata
create policy "reports client access"
  on public.reports
  for select
  to authenticated
  using (
    coalesce(auth.jwt() -> 'user_metadata' ->> 'client_slug', '') = client_slug
  );

-- Optional: internal staff (replace e-mails)
create policy "reports staff access"
  on public.reports
  for select
  to authenticated
  using (auth.email() = any (array['jack@teho.ai']))
  with check (true);
```

If staff need to edit rows manually, add an `update` policy mirroring `reports staff access`.

## 4. Attach `client_slug` Metadata to Portal Users

Portal sign-in uses magic links with the public anon key. To ensure users only see their own reports, add a `client_slug` claim to their auth metadata. The CLI now ships a helper command that uses the service key to update metadata:

```bash
.venv/bin/teho assign-portal-user user@example.com acme-co
```

This stores `client_slug` (and optionally `client_id`) on the Supabase auth record, so the JWT contains `user_metadata.client_slug` for RLS. Re-run the command if you need to reassign access.

You can verify the metadata under **Auth → Users → (select user)** in the Supabase dashboard.

## 5. Storage Bucket Permissions

The automation uploads HTML/PDF files to the private `reports` storage bucket. Keep the bucket `private` and use signed URLs in the portal when presenting download links. Only the service role (automation) should have write access; the Next.js portal should request signed URLs via the authenticated Supabase client so that RLS protects the metadata lookup before storage access.

## 6. Operational Checklist

- [ ] Run the SQL above (table + policies).
- [ ] Update each portal user with `teho assign-portal-user <email> <client-slug>`.
- [ ] Confirm that the portal list view only shows entries for the linked slug.
- [ ] Document any staff accounts added to the RLS whitelist for auditing.

## 7. (Optional) Report Events Table for Portal Analytics

Create a lightweight table to capture portal interactions so you can see when clients view or download their briefings. Example schema:

```sql
create table if not exists public.report_events (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid not null,
  client_slug text not null,
  report_id uuid,
  report_key text not null,
  storage_path text not null,
  event_type text not null check (event_type in ('view', 'download')),
  created_at timestamptz default now()
);

alter table public.report_events enable row level security;

drop policy if exists "report_events service" on public.report_events;
drop policy if exists "report_events client" on public.report_events;

create policy "report_events service"
  on public.report_events
  for all
  to service_role
  using (true)
  with check (true);

create policy "report_events client"
  on public.report_events
  for insert
  to authenticated
  with check (
    coalesce(auth.jwt() -> 'user_metadata' ->> 'client_slug', '') = client_slug
  );

create policy "report_events client read"
  on public.report_events
  for select
  to authenticated
  using (
    coalesce(auth.jwt() -> 'user_metadata' ->> 'client_slug', '') = client_slug
  );

create policy "report_events staff"
  on public.report_events
  for select
  to authenticated
  using (auth.email() = any (array['jack@teho.ai']));
```

The portal uses `POST /api/report-events` to log view/download actions before issuing a fresh signed URL. Because the policy ties `client_slug` to the JWT claim, clients can only see their own event history if you choose to expose it later.

## 8. Outreach Events Table (sends/opens/clicks/replies)

Record the broader communication funnel so the admin dashboard can surface outreach alongside engagement:

```sql
create table if not exists public.outreach_events (
  id uuid primary key default uuid_generate_v4(),
  client_slug text not null,
  contact_email text not null,
  event_type text not null check (event_type in ('sent', 'opened', 'clicked', 'replied')),
  channel text not null default 'email',
  report_key text,
  notes text,
  metadata jsonb,
  created_at timestamptz default now()
);

alter table public.outreach_events enable row level security;

drop policy if exists "outreach service" on public.outreach_events;
drop policy if exists "outreach staff" on public.outreach_events;

create policy "outreach service"
  on public.outreach_events
  for all
  to service_role
  using (true)
  with check (true);

create policy "outreach staff"
  on public.outreach_events
  for select
  to authenticated
  using (auth.email() = any (array['jack@teho.ai']));
```

Use the CLI helper to log events:

```bash
.venv/bin/teho log-outreach \
  --client-slug bloom-and-wild \
  --contact-email ceo@bloomandwild.com \
  --event-type sent \
  --report-key opportunity-report-summary \
  --notes "Sent teaser email"
```

Future webhooks (Postmark/Sendgrid) can call the same endpoint or CLI to keep this table fresh.

## 9. Automation Runs Table (portal-triggered jobs)

The admin portal now records automation requests (generate/package/process) so the Python runner can pick them up. Create the table and policies:

```sql
create table if not exists public.automation_runs (
  id uuid primary key default uuid_generate_v4(),
  client_slug text,
  action text not null,
  status text not null default 'requested',
  payload jsonb,
  triggered_by text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table public.automation_runs enable row level security;

drop policy if exists "automation service" on public.automation_runs;
drop policy if exists "automation staff select" on public.automation_runs;
drop policy if exists "automation staff insert" on public.automation_runs;

create policy "automation service"
  on public.automation_runs
  for all
  to service_role
  using (true)
  with check (true);

create policy "automation staff select"
  on public.automation_runs
  for select
  to authenticated
  using (auth.email() = any (array['jack@teho.ai', 'jackwjtaylor@gmail.com']));

create policy "automation staff insert"
  on public.automation_runs
  for insert
  to authenticated
  with check (auth.email() = any (array['jack@teho.ai', 'jackwjtaylor@gmail.com']));
```

Automation requests created via `/admin` insert `{action: 'generate-summary', client_slug: 'gousto', payload: {...}}` with `status = requested`. The `teho automation-worker` command polls this table, processes each entry, updates `status` (`in_progress`, `succeeded`, `failed`), and uses the `payload` blob for extra context (report depth, manual overrides, etc.).

Once complete, the reports catalogue is locked down to the intended client, while automation retains full write access via the service key.

## 10. Briefing Notes (research/QA timeline)

Capture manual research notes or reminders per request so the entire team can see context without digging through chat logs.

```sql
create table if not exists public.briefing_notes (
  id uuid primary key default uuid_generate_v4(),
  request_id uuid references public.briefing_requests(id) on delete cascade,
  note text not null,
  created_by text,
  created_at timestamptz default now()
);

alter table public.briefing_notes enable row level security;

drop policy if exists "notes service" on public.briefing_notes;
drop policy if exists "notes staff insert" on public.briefing_notes;
drop policy if exists "notes staff select" on public.briefing_notes;

create policy "notes service"
  on public.briefing_notes
  for all
  to service_role
  using (true)
  with check (true);

create policy "notes staff select"
  on public.briefing_notes
  for select
  to authenticated
  using (auth.email() = any (array['jack@teho.ai', 'jackwjtaylor@gmail.com']));

create policy "notes staff insert"
  on public.briefing_notes
  for insert
  to authenticated
  with check (auth.email() = any (array['jack@teho.ai', 'jackwjtaylor@gmail.com']));
```

## 11. QA Reviews

Track checklist completion per `client_slug` so `/admin` can show “QA ready” badges and log reviewer details.

```sql
create table if not exists public.qa_reviews (
  id uuid primary key default uuid_generate_v4(),
  client_slug text not null,
  status text not null default 'in_progress',
  checklist jsonb not null default '{}'::jsonb,
  reviewer_email text,
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table public.qa_reviews enable row level security;

drop policy if exists "qa service" on public.qa_reviews;
drop policy if exists "qa staff select" on public.qa_reviews;
drop policy if exists "qa staff upsert" on public.qa_reviews;

create policy "qa service"
  on public.qa_reviews
  for all
  to service_role
  using (true)
  with check (true);

create policy "qa staff select"
  on public.qa_reviews
  for select
  to authenticated
  using (auth.email() = any (array['jack@teho.ai', 'jackwjtaylor@gmail.com']));

create policy "qa staff insert"
  on public.qa_reviews
  for insert
  to authenticated
  with check (auth.email() = any (array['jack@teho.ai', 'jackwjtaylor@gmail.com']));

create policy "qa staff update"
  on public.qa_reviews
  for update
  to authenticated
  using (auth.email() = any (array['jack@teho.ai', 'jackwjtaylor@gmail.com']))
  with check (auth.email() = any (array['jack@teho.ai', 'jackwjtaylor@gmail.com']));
```

The portal writes checklist data as JSON (`{ "context_ready": true, ... }`) and flips `status` to `approved` when all boxes are ticked.
