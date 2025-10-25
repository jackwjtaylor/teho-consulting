# Lead-Gen Workflow & RACI

## Overview

The process must run with minimal manual input so a single operator can handle volume. Automation covers data gathering, prompting, packaging, and outreach; human review happens only at defined gates. The flow works for any company provided the checklist data is available.

1. **Intake & Prioritisation (automated trigger + light review)**
   - Trigger: company name received via form/API. Automation checks country, size, and duplicate status.
   - Queue entry written to Supabase `briefing_requests` (CLI falls back to `data/company_queue.csv` if env keys missing) with status + priority.
   - Human confirms the weekly priority list from the queue dashboard.

2. **Research & Data Capture (automation first, human tidy-up)**
   - Scripts gather site metadata, filings, recent news, customer reviews, contact hints, and enrich with industry tags.
   - Human pass only to fill true gaps or add nuance (e.g., mission quote, confirm contact email).
   - Output: validated `context.json`, `sources.csv`, auto-generated research log.

3. **Report Generation (fully automated)**
   - Prompt runner ingests context, calls OpenAI, and saves `summary.md` (executive teaser) and `full.md` (comprehensive blueprint) plus the snapshot markdown.
   - Automatic diff check ensures section compliance for the full report; deviations flagged for review.
   - Output: Markdown files stored in `/reports/{company}/` and Supabase metadata stub prepared.

4. **Quality Review (human gate)**
   - Operator reviews flagged sections only (facts, tone, assumptions) using QA checklist.
   - Any edits written back to reports; schema/prompt tweaks logged for automation update.
   - Output: QA-approved reports + change notes.

5. **Packaging & Publishing (automated)**
   - Script converts snapshot to PDF, applies brand stylesheet, and merges quantified teaser bullets into the email draft.
   - HTML/PDF assets for `summary` and `full` reports are rendered and uploaded to the Supabase `reports` storage bucket; `teho upsert_report_entry` updates the `public.reports` table with signed paths and metadata.
   - Links to landing page and Calendly checked automatically.
   - Output: Supabase-hosted assets + ready-to-send email bundle (PDF + HTML + tracking IDs).

6. **Outreach & Follow-Up (automated send, human escalation)**
   - Email automation sends teaser and schedules follow-ups (includes Supabase report links for portal access).
   - Portal access assigned via `teho assign-portal-user <email> <client-slug>` so each client only sees their reports.
   - CRM/log updates auto-capture opens, clicks, replies; only high-priority replies escalate to human for personalised follow-up.
   - Output: outreach log, portal unlock audit, tasks for calls/meetings.

7. **Feedback & Continuous Improvement (hybrid)**
   - Automation aggregates metrics (conversion, response themes).
   - Human reviews weekly to adjust prompts, outreach hooks, and product ladder content.
   - Output: backlog updates, prompt/version notes.

## RACI Table

| Stage | Responsible | Accountable | Consulted | Informed | Artefacts |
| --- | --- | --- | --- | --- | --- |
| Intake & prioritisation | Automation + Founder (spot check) | Founder | Future sales advisor | Wider team | Queue entry, intake log |
| Research & data capture | Automation | Founder | Contractor (for deep dives) | Outreach lead | `/data/raw/{company}`, source log |
| Report generation | Automation | Founder | Prompt specialist (when needed) | Researcher | `/reports/{company}/...` |
| Quality review | Founder (or delegated editor) | Founder | Subject matter expert (if niche) | Outreach lead | QA checklist, change log |
| Packaging | Automation | Founder | Designer (future) | Researcher | Snapshot PDF, email draft |
| Outreach & follow-up | Automation (send) / Founder (calls) | Founder | Sales advisor | Team | CRM/activity log |
| Feedback loop | Founder | Founder | Whole team | Stakeholders | Prompt change log, backlog tickets |

## Handover Checklist (draft)

- Intake: company approved, researcher assigned, due date set.  
- Research: context JSON complete, sources labelled, gaps flagged.  
- Reports: files generated, automation verifies format, stored in folder, version noted.  
- QA: checklist signed, updates applied, change log updated.  
- Packaging: snapshot PDF confirmed, email personalised, links tested.  
- Outreach: activity logged, follow-up reminders set.  
- Feedback: insights added to backlog, prompt tweaks prioritised.
