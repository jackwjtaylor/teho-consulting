# Lead-Gen Workflow & RACI

## Overview

The process must run with minimal manual input so a single operator can handle volume. Automation covers data gathering, prompting, packaging, and outreach; human review happens only at defined gates. The flow works for any company provided the checklist data is available.

1. **Intake & Prioritisation (automated trigger + light review)**
   - Trigger: company name received via form/API. Automation checks country, size, and duplicate status.
   - Queue entry stored in `data/company_queue.csv` (or chosen CRM table) with status and priority.
   - Human confirms the priority list for the week.

2. **Research & Data Capture (automation first, human tidy-up)**
   - Scripts gather site metadata, filings, recent news, customer reviews, contact hints, and enrich with industry tags.
   - Human pass only to fill true gaps or add nuance (e.g., mission quote, confirm contact email).
   - Output: validated `context.json`, `sources.csv`, auto-generated research log.

3. **Report Generation (fully automated)**
   - Prompt runner ingests context, calls OpenAI, and saves executive, comprehensive, and snapshot drafts.
   - Automatic diff check ensures structure compliance; deviations flagged for review.
   - Output: Markdown files in `/reports/{company}/`.

4. **Quality Review (human gate)**
   - Operator reviews flagged sections only (facts, tone, assumptions) using QA checklist.
   - Any edits written back to reports; schema/prompt tweaks logged for automation update.
   - Output: QA-approved reports + change notes.

5. **Packaging (automated)**
   - Script converts snapshot to PDF, applies branding, and merges personalised email copy.
   - Links to landing page and Calendly checked automatically.
   - Output: ready-to-send email bundle (PDF + HTML + tracking IDs).

6. **Outreach & Follow-Up (automated send, human escalation)**
   - Email automation sends teaser and schedules follow-ups.
  - CRM/log updates auto-capture opens, clicks, replies; only high-priority replies escalate to human for personalised follow-up.
   - Output: outreach log, tasks for calls/meetings.

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
