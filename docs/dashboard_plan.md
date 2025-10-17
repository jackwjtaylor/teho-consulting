# Outreach Metrics Dashboard Plan

## Purpose

Monitor lead-gen performance from first email send through follow-up so we can prioritise companies, test messaging, and forecast revenue.

## Core Metrics

| Stage | Metric | Description | Data Source |
| --- | --- | --- | --- |
| Email delivery | Emails sent | Count of initial and follow-up sends | ESP (Postmark/Sendgrid) webhooks |
| Engagement | Opens | Unique opens per email | ESP webhook events |
| Engagement | Link clicks | Unique clicks on briefing link and Calendly link | ESP webhook events + UTM parameters |
| Conversion | Calendar bookings | Calls booked via Calendly | Calendly API export |
| Conversion | Briefing unlocks | Form submissions/downloads on teho.ai | Landing page backend (Supabase/Notion form) |
| Pipeline | Status updates | Manual tag: replied, booked, not interested, follow-up | CRM/Notion table |
| Revenue | Deals won | Value of signed projects | Invoicing tool / manual entry |

## Data Flow

1. **ESP Webhooks** → collect `delivered`, `open`, `click` events into a webhook handler (FastAPI/Cloud Function) writing to a Postgres table (`email_events`).
2. **Calendly Webhook** → capture `invitee.created` events with meeting type and slug, store in `calendar_events` table.
3. **Landing Page Form** → gate full report; capture submissions with company slug and contact email (`briefing_unlocks`).
4. **CRM Table** → single source (e.g. Notion or Airtable) with company status, manual notes, revenue values.

## Visualisation

- Use Looker Studio or Retool connected to Postgres/Sheets. Provide filters by company slug, week, and cohort.
- Key widgets: funnel (sent → opens → clicks → unlocks → calls → deals), conversion rates, time-to-first-response, revenue pacing.
- Table view showing latest status per company with last engagement timestamp.

## Alerts & Reporting

- Daily digest (Slack/email) summarising new replies, bookings, and stalled leads (>7 days since last activity).
- Monthly summary deck auto-generated from dashboard snapshots.

## Implementation Steps

1. Stand up Postgres (Supabase) with tables: `email_events`, `calendar_events`, `briefing_unlocks`, `companies`.
2. Build webhook endpoints (Python FastAPI deployed on Fly.io/Render) to receive ESP + Calendly events.
3. Add tracking parameters to teho CLI-generated emails (UTM + unique slugs).
4. Configure teho.ai landing page form to write to `briefing_unlocks`.
5. Connect dashboard tool and create initial charts.
6. Automate daily summary (cron job querying Postgres, posting to Slack).
