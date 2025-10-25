# Intake Pipeline Overview

The intake flow captures briefing requests from two entry points:

1. **Public form** on teho.ai (`landing/teho/get-started.html`).  
2. **Internal trigger** (CLI/CRM) when we want to add a company manually.

All submissions land in a Supabase table so the automation jobs can pick them up, update status, and keep a single source of truth.

## Supabase Setup

Create a new Supabase project and add environment variables to `.env` (see `env.example`):

```
SUPABASE_URL="https://YOUR-PROJECT.supabase.co"
SUPABASE_SERVICE_KEY="service_role_key"      # used by CLI/automation
SUPABASE_ANON_KEY="public_anon_key"          # used by web form (RLS protected)
```

> Never expose the service key in client-side code. It is only for trusted automation.

### Table: `briefing_requests`

| Column            | Type         | Notes                                                                 |
|-------------------|--------------|-----------------------------------------------------------------------|
| id                | uuid         | Default `uuid_generate_v4()`                                         |
| company_name      | text         | Company as entered                                                   |
| slug              | text         | Lowercase slug (unique). Use as id when generating folders.          |
| domain            | text         | Primary company domain                                               |
| persona           | text         | Target persona (Founder/CEO, COO, etc.)                              |
| primary_contact   | text         | Contact name if known                                                |
| primary_email     | text         | Contact email (nullable)                                             |
| status            | text         | `queued`, `collecting`, `needs_qa`, `ready_to_send`, `sent`, `closed`|
| priority          | integer      | 1 = highest                                                          |
| source            | text         | `website`, `manual`, `referral`, etc.                                |
| requested_at      | timestamptz  | Defaults to `now()`                                                  |
| payload           | jsonb        | Raw form submission or metadata                                      |
| notes             | text         | Internal comments                                                    |
| last_updated      | timestamptz  | Trigger to update on modification                                    |

Indexes: unique index on `slug`, index on `status`, optional on `priority`.

### Row Level Security (RLS)

Enable RLS and create policies:

- **Insert (anon key)**: allow `INSERT` when `auth.role() = 'anon'` and `status = 'queued'`. Populate the rest via the default values; limit to expected columns.  
- **Authenticated staff**: allow trusted emails to `SELECT`, `INSERT`, and `UPDATE` rows. Example SQL via the SQL Editor:

```sql
alter table public.briefing_requests enable row level security;

drop policy if exists "Website intake" on public.briefing_requests;
drop policy if exists "Service access" on public.briefing_requests;
drop policy if exists "Staff manage" on public.briefing_requests;

create policy "Website intake"
  on public.briefing_requests
  for insert
  to anon
  with check (auth.role() = 'anon');

create policy "Service access"
  on public.briefing_requests
  for all
  to service_role
  using (true)
  with check (true);

create policy "Staff manage"
  on public.briefing_requests
  for all
  to authenticated
  using (auth.email() = any (array['jack@teho.ai']))
  with check (auth.email() = any (array['jack@teho.ai']));
```

Adjust the email list to match whoever needs access to the internal CRM.

### Functions / Edge Workflows

- Create HTTPS function `/submit-briefing` that:
  1. Validates payload (name, email, company, size/objective, consent).  
  2. Derives slug + default priority.  
  3. Inserts into `briefing_requests`.  
  4. Returns success JSON for the form.
- Optional: create `/update-status` function if you want to hide service key from automation servers.

## Automation Flow

1. Web form POSTs to `/submit-briefing` using the anon key.  
2. CLI command `teho queue-request` can either call the same function or use service key to upsert.  
3. Scheduled job fetches rows with `status = 'queued'` (via service key), initialises folders, and moves them to `collecting`.  
4. Subsequent steps update status as the workflow runs (collecting → needs_qa → ready_to_send → sent).  
5. Analytics/dashboard read from the same table.

## Local Development

- Keep `.env` out of version control.  
- `python-dotenv` is loaded automatically by the Supabase helper, so CLI commands get keys when `.env` or environment variables are set.  
- For offline development, the CLI falls back to `data/company_queue.csv`. Once Supabase env vars exist, new entries will upsert into the remote table.

## Next Steps

- Create the Supabase project and table.  
- Configure Edge Function/endpoints for the public form.  
- Wire the website form (`assets/form.js`) to call the function.  
- Update automation to pull from Supabase rather than CSV when available.  
- Add dashboard queries against `briefing_requests`.

## Website Configuration

1. Copy `landing/config.example.js` to `landing/config.js` (ignored by git).  
2. Fill in:
   ```js
   window.TEHO_SUPABASE_URL = "https://your-project.supabase.co";
   window.TEHO_SUPABASE_KEY = "public-anon-key";
   // Optional: window.TEHO_FORM_ENDPOINT = "https://your-edge-function";
   ```
3. `landing/teho/get-started.html` automatically loads `../config.js`; no further edits to the HTML are needed. The internal queue is now managed at `/admin` inside the portal (see `docs/internal_crm.md`).  
4. If you deploy an Edge Function instead of direct REST, set `window.TEHO_FORM_ENDPOINT` and the website will POST there (the script uses that before trying Supabase REST).  
5. Remember: never expose the service role key in `config.js`.
