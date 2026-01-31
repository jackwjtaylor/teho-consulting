# Opportunity Report – Full  
**Date:** 2026-01-01  
**Analyst:** Teho Consulting AI Advisory Team  
**Business:** P H Media Group  
**Report Depth:** Full  

## 1. EXECUTIVE SUMMARY

- Context: PHMG is a profitable, growing audio‑branding and caller‑experience business (FY2023 revenue £85.5m; >36,000 clients; transitioned to an Employee Ownership Trust in Apr 2025). Retention and expansion of the large recurring base are the highest‑leverage levers for near‑term margin and cash‑flow improvement.

- Recommendation (short list for the Chief Client Officer):
  1. Predictive churn scoring and early‑intervention playbooks — priority pilot (quick win, medium effort). Directly addresses churn; leverages PHMG Portal and Complete Caller Experience telemetry. Illustrative retained revenue: £0.8M–£2.5M/yr; churn −1 to −3 p.p.
  2. Renewal & upsell orchestration with tailored offer generation — quick win to shorten renewal cycles and raise ARPU. Illustrative uplift: £0.9M–£4.0M/yr.
  3. Automated 'Action Pack' insights from caller analytics — automated, prioritized recommendations to drive adoption of analytics‑led changes. Illustrative uplift: £0.4M–£2.0M/yr.

- Strategic / Big bet: Automated A/B experimentation platform for caller experiences — high impact on reported ROI and stickiness but high implementation complexity and safety/regulatory controls required. Illustrative uplift: £0.5M–£4.0M/yr.

- Near term actions (30–90 days): approve a 90‑day pilot for predictive churn scoring; run a DPIA & data map; allocate a small cross‑functional team (Data/ML, Product, CSM, Legal, Engineering); implement human‑in‑the‑loop playbooks surfaced in the PHMG Portal.

- Caution: All automation affecting customers, pricing or contract terms must maintain human approval gates; cross‑border data flows, profiling rules under GDPR and electronic‑marketing rules must be addressed upfront (see Risks & Mitigations and Guardrails).

## 2. COMPANY SNAPSHOT

- Legal & ownership: PHMG operating across multiple legal entities (PH Media (USA) Inc.; Please Hold (UK) Ltd.; PHMG (Australia) PTY LTD; PHMG (Canada) Inc.; PHMG (New Zealand) Ltd.). Transitioned to Employee Ownership Trust (Apr 2025).

- Core offers: exclusive music, on‑hold marketing, copywriting & voice artistry, post‑production, sonic identity, Complete Caller Experience (named cloud telephony product), PHMG Portal (client portal), analytics & caller consultancy.

- Customers & footprint: enterprise global brands (Samsung, Adidas, Coca‑Cola, Audi, Rawlings), plus a large SME base across primary English‑speaking markets (UK, US, Australia, Canada, NZ) and 50+ countries.

- Tech signals: cloud telephony platforms, caller behaviour analytics (Complete Caller Experience), PHMG Portal, some AI‑enabled capabilities and patented processes noted on site.

- Leadership: experienced commercial and product leadership (CEO, CRO, CCO, CSO, CTO, Product Director (Cloud), Director of Client Technical Services, VP Creative) — favourable governance for cross‑functional pilots.

## 3. FINANCIAL SIGNALS (RELEVANT TO RETENTION)

- Revenue & growth: Group revenue £85.5m in FY2023 (up from £75.0m in 2022). Double‑digit growth over 2021–2023.

- Profitability & margins: consistently profitable (FY2023 operating profit £16.5m; PBT £12.3m; net profit ~£9.4m). Gross/operating margins have compressed modestly as growth investment increased.

- Unit economics: management reports c.90–91% of client subscription revenue retained each year (2021–2023). Implied revenue per client (2023) ~£2.3k/year (illustrative). With ~36k clients, small percentage improvements in churn or ARPU scale materially.

- Balance sheet / funding posture: trading subsidiaries show strong net assets and working capital; holding companies carry structural leverage. Financing is bank/institutional debt rather than external equity.

Implication: retention investments that reduce churn even modestly and increase adoption/upsell should deliver disproportionately high ROI versus headcount increases.

## 4. RECENT DEVELOPMENTS (INPUT DATA NOTES)

- Inputs used: PHMG corporate site, FY2023 disclosures and corporate blogs (including EOT announcement Apr 2025). No additional live web search has been run for events since 2024‑07‑01; I can run a targeted news search if you want a compiled timeline of product launches, leadership movement or partnerships (please confirm language and event‑type preferences).

## 5. MARKET & COMPETITOR CONTEXT

- Direct/adjacent competitors include Mood Media, PlayNetwork, Soundtrack (Soundtrack Your Brand), Rockbot, TouchTunes, SiriusXM Music for Business and analytics specialists like Veritonic.

- Observed peer capabilities: multi‑location music streaming, curated playlists, audio messaging, multi‑zone scheduling, some analytics/testing capabilities and (in parts of the market) AI playlist/curation tools.

- PHMG differentiators: exclusive music catalogue, voice/artistry and creative capability, patented processes, cloud telephony product (Complete Caller Experience), and a client portal with analytics — putting PHMG in a strong position to monetize analytics and caller experience optimisation at scale.

## 6. PROBLEM & PAIN‑POINT MAP (RETENTION‑FOCUSED)

- Primary retention friction points (from the provided process map):
  - Low frequency of actionable insights delivered to clients -> low adoption of analytics‑driven changes.
  - Incomplete onboarding / low PHMG Portal activation -> clients don’t see the value that drives renewals/upsell.
  - Slow pilot → commercial conversion; long proposal turnaround -> revenue leakage and delayed expansion.
  - Contract/renewal friction & discounting -> lost renewal margin and slower closes.
  - Support/incident MTTR and billing disputes -> customer dissatisfaction and potential churn.

- These issues map directly to CCO account objectives: reduce churn, raise net retention and increase upsell conversion while containing operating cost in CSM function.

## 7. OPPORTUNITY MAP (GROUPED BY RETENTION IMPACT)

- Retention & Upsell (high direct impact):
  - Predictive churn scoring + early‑intervention playbooks (H impact / M effort)
  - Renewal & upsell orchestration with tailored offer generation (H impact / M effort)
  - Account health scoring + templated strategic growth plans (M impact / M effort)

- Activation & analytics adoption (scales consultancy):
  - Automated 'Action Pack' insights from caller analytics (H impact / M effort)
  - Automated A/B experimentation platform for caller experiences (H impact / H effort; big bet)
  - PHMG Portal intelligent onboarding assistant (M impact / M effort)

- Risk reduction & efficiency (operational leverage):
  - AI‑driven pre‑deployment QA & licensing clearance accelerator (M impact / M effort)
  - AI‑augmented support triage and knowledge‑assist (M impact / M effort)
  - Automated billing anomaly detection & DSO forecasting (M impact / M effort)
  - Pilot‑to‑commercial acceleration workflow (M impact / M effort)

Each opportunity includes defined data prerequisites, integrations and guardrails in the appended inventory. Quick wins are those that reuse Portal + Complete Caller Experience telemetry and require moderate engineering to surface outputs to CSMs and clients.

## 8. TOP 5 OPPORTUNITIES — DEEP DIVES (PRIORITISED FOR THE CHIEF CLIENT OFFICER)

Note: each deep dive pulls directly from the opportunity inventory. Values are illustrative ranges provided in the input and should be treated as delta estimates dependent on adoption.

1) Predictive churn scoring and early‑intervention playbooks

- What it does: train a churn‑risk model using PHMG Portal engagement, Complete Caller Experience analytics, CRM metadata, billing and support history; surface scored accounts in the Portal; auto‑generate ranked playbooks (proactive analytics review, tailored audio refresh offers, timed renewal touches) with templated client communications. Low‑effort actions auto‑trigger; higher‑impact offers require CSM approval.

- Why it matters to retention: small reductions in churn scale across ~36k clients (illustrative retained revenue £0.8M–£2.5M/yr). KPI uplift: churn −1 to −3 p.p.; net retention +1 to +4 p.p.; renewals within 90 days +10–25%.

- Data prerequisites: Portal activity logs, caller analytics (call volumes/IVR metrics), CRM/account metadata, billing/subscription status, support ticket history, creative delivery/revision history.

- Integrations: PHMG Portal (CSM UI & notification surface), Complete Caller Experience, CRM, billing ledger, email/marketing automation and calendar.

- Guardrails/compliance highlights: human‑in‑the‑loop for pricing/contract changes; DPIA and lawful basis for profiling; GDPR/marketing consent management; model explainability for CSMs; secure RBAC and encryption for billing/contract data.

- MVP / pilot scope (90 days):
  - Cohort: a representative pilot cohort (e.g., 500–2,000 SME accounts or a set of top enterprise accounts depending on data availability).
  - Deliverables: offline model + risk scores; Portal dashboard surfacing top 50–200 at‑risk accounts; 3 templated early‑intervention playbooks; a reporting pack comparing pilot cohort churn vs control.
  - Success criteria: achieve ≥1 p.p. reduction in churn for pilot cohort vs control; ≥10% adoption of recommended playbooks; CSM qualitative buy‑in.

- Estimated resources: Product owner (CSM sponsor), 1 Data Engineer, 1 ML Engineer/Data Scientist, 1 Integration Engineer, 1 Portal/Frontend dev, part‑time Legal/Compliance.

2) Automated 'Action Pack' insights from caller analytics to increase frequency and adoption

- What it does: deterministic rules + LLM summarisation on Complete Caller Experience data produce prioritized recommendations (Action Packs) with estimated impact and effort; delivered in‑portal and to CSM dashboards with one‑click options to request creative refresh or run experiments.

- Why it matters: increases the cadence of value delivered to clients, drives adoption of analytics‑led actions, and creates more upsell and renewal evidence. Illustrative value £0.4M–£2.0M/yr. KPI uplift: +2–6 insights/client/month; recommendation adoption +10–35%.

- Data prerequisites & integrations: Complete Caller Experience exports, Portal engagement logs, creative asset performance history, client segmentation; integration points: Portal, caller analytics engine, creative production workflow, CSM dashboard/CRM.

- Guardrails: redact/pseudonymise caller‑level PII; require client approval for production changes; LLM outputs constrained to templates with confidence labels; check recommendations against client brand rules.

- MVP / pilot scope: generate Action Packs for a subset of clients (e.g., 500), surface to CSMs and a sample of clients, enable one‑click request workflow for creative refresh (not auto‑deploy), measure adoption and lift.

3) Renewal and upsell orchestration with tailored offer generation

- What it does: combine churn risk, Portal engagement, usage of services and contract data to auto‑generate personalised renewal and upsell packages, populate proposal templates, recommend pricing bands and trigger timed outreach; exceptions escalate to sales/legal.

- Why it matters: shortens renewal time, reduces discounting, increases ARPU and protects margin. Illustrative uplift £0.9M–£4.0M/yr. KPI uplift: time to close renewal −20–60%; upsell conversion +5–20%.

- Data prerequisites & integrations: contract terms & renewal dates, historical discounting/win‑loss data, Portal usage, creative/licensing status, CRM, billing, legal workflow.

- Guardrails: manager/legal approval for discounts above thresholds; auto‑validate licensing before including assets; audit trail for proposals.

- MVP / pilot scope: target renewals in the next 90 days (e.g., 100–300 accounts), auto‑generate proposals for those accounts, measure time‑to‑close and discount incidence vs baseline.

4) Account health scoring and templated strategic growth‑plan generation

- What it does: compute an account health score from usage, revenue, support activity and churn risk; auto‑produce templated QBR/growth plans (QBR agenda, recommended investments, pilot proposals) for CSM customisation and prioritised outreach.

- Why it matters: ensures high‑value accounts receive consistent, timely coverage and growth plans — directly improving expansion probability. Illustrative uplift £0.6M–£3.0M/yr. KPI uplift: strategic account coverage +30–80%; upsell +5–15%.

- Data prerequisites & integrations: CRM segmentation, Portal & caller analytics, support history, pilot outcomes, Calendar/proposal tools.

- Guardrails: CSM final approval required; auditability and bias audits of scoring; sanitise cross‑account comparisons.

- MVP / pilot scope: compute health scores for the top 200 strategic accounts, generate templated growth plans for each, measure CSM time saved and conversion of plans to proposals.

5) Automated A/B experimentation platform for caller experiences (big bet)

- What it does: deploy alternate on‑hold scripts, music tracks, IVR timings or messages via cloud telephony integrations; collect caller analytics; compute statistically valid lift on KPIs and recommend winners with auto‑rollout gated by human approval.

- Why it matters: provides proof of incremental value from creative changes and analytics, increasing client confidence, adoption and upsell; differentiates PHMG consultancy. Illustrative uplift £0.5M–£4.0M/yr.

- Data prerequisites & integrations: permissioned access to telephony flows, Complete Caller Experience call‑level metrics, creative asset IDs, client KPI definitions.

- Guardrails (critical): explicit client consent, prohibit experiments on emergency/regulatory IVR paths, statistical power checks, human sign‑off before rollout, localised data handling.

- MVP / pilot scope: run 3 experiments with 1–2 enterprise clients that consent and have sufficient call volumes; validate randomisation, measure conversion lift and test rollout process. Success is statistically valid lift and a safe, documented roll‑out path.

## 9. VALUE SUMMARY (ILLUSTRATIVE RANGES & KPIS)

- Predictive churn scoring and early‑intervention playbooks: £0.8M–£2.5M/yr; churn −1 to −3 p.p.; Net retention +1 to +4 p.p.
- Renewal & upsell orchestration: £0.9M–£4.0M/yr; time to close renewal −20–60%; upsell +5–20%.
- Automated 'Action Pack' insights: £0.4M–£2.0M/yr; +2–6 insights/client/month; recommendation adoption +10–35%.
- Account health scoring & growth plans: £0.6M–£3.0M/yr; strategic account coverage +30–80%; upsell +5–15%.
- Automated A/B experimentation platform: £0.5M–£4.0M/yr; conversion lift/Campaign ROI +2–12%; insight adoption +20–50%.

Note: ranges are illustrative and partially overlapping (same clients may benefit from multiple initiatives). Use the pilot results to calibrate realistic attributable lift and avoid double‑counting when modelling full roll‑out.

## 10. PRIORITISED BACKLOG (ICE-style summary — from supplied prioritisation)

Top ranked (score = (impact * confidence) / effort):

1. Predictive churn scoring and early‑intervention playbooks — Impact 9 / Confidence 8 / Effort 6 — Score 12.0 — Why: high impact on retention; required telemetry exists; moderate integration.

2. Renewal and upsell orchestration with tailored offer generation — Impact 9 / Confidence 7 / Effort 6 — Score 10.5 — Why: high revenue upside; requires CRM/billing/legal alignment.

3. Automated 'Action Pack' insights from caller analytics — Impact 9 / Confidence 7 / Effort 6 — Score 10.5 — Why: scales consultancy; leverages existing analytics.

4. Account health scoring & templated growth plans — Impact 6 / Confidence 7 / Effort 6 — Score 7.0 — Why: standardises strategic coverage, medium effort.

5. Automated billing anomaly detection & DSO forecasting — Impact 6 / Confidence 7 / Effort 6 — Score 7.0 — Why: improves cash flow and reduces dispute‑driven churn risk.

6. AI‑augmented support triage & knowledge‑assist — Impact 6 / Confidence 7 / Effort 6 — Score 7.0 — Why: operational ROI; improves CSAT.

7. AI‑driven pre‑deployment QA & licensing clearance accelerator — Impact 6 / Confidence 7 / Effort 6 — Score 7.0 — Why: reduces rework/delays in go‑live.

8. Automated A/B experimentation platform for caller experiences — Impact 9 / Confidence 6 / Effort 9 — Score 6.0 — Why: strategic, but complex and higher risk; treat as a major program.

9. PHMG Portal intelligent onboarding assistant — Impact 6 / Confidence 6 / Effort 6 — Score 6.0 — Why: improves activation but requires secure connector work.

10. Pilot‑to‑commercial acceleration workflow — Impact 6 / Confidence 6 / Effort 6 — Score 6.0 — Why: standardises pilot success → contract conversion.

(Quadrant mapping: first three are Quick Wins; A/B experimentation is a Big Bet; others are Fill‑Ins.)

## 11. 90‑DAY PILOT PLAN (FOCUS: Predictive Churn Scoring & Playbooks)

Objective: validate that risk scoring + automated playbooks reduce churn in a measurable cohort and are operationally safe and compliant.

Core success metrics (pilot):
- Churn reduction in pilot cohort ≥1 percentage point vs control (60–90 day measurement window + 6 months post‑pilot monitoring recommended).
- Playbook adoption rate ≥10% of high‑risk cases within pilot cohort.
- No material privacy/compliance incidents; DPIA completed prior to pilot launch.

Team (recommended minimal):
- CCO (sponsor / decision owner)
- CSM lead (product owner for playbooks)
- Product Manager (Portal integrations)
- 1 Data Engineer (ETL & feature pipeline)
- 1 Data Scientist / ML Engineer
- 1 Integration/Backend Engineer (Portal APIs)
- 1 Frontend dev (Portal UI for CSMs) — small scope
- Legal/Compliance (part‑time) and Security (part‑time)

High‑level timeline (90 days)

- Week 0 (approval & kickoff): scope, governance, pilot cohort selection, DPIA initiation, data access approvals.

- Weeks 1–2 (data discovery & mapping): extract/validate Portal logs, caller analytics exports, CRM, billing, support tickets; pseudonymise as required; agree success/control cohorts.

- Weeks 3–5 (model & playbook design): feature engineering; build baseline churn model; design 2–3 templated playbooks (low effort, medium effort, high effort); include human‑in‑the‑loop escalation rules and manager approval gating.

- Weeks 6–8 (integration & UI): surface risk scores in Portal CSM dashboard; implement notification and playbook action workflow (no auto‑pricing changes); logging + explainability tooltips for CSMs.

- Weeks 9–12 (pilot execution & evaluation): run pilot for selected cohort; collect outcomes vs control; gather CSM/client feedback; legal/compliance review; prepare go/no‑go and scale recommendations.

Deliverables at 90 days:
- Operational risk scores surfaced in Portal with explainability and confidence.
- 3 playbook templates and workflows (with audit trails).
- Pilot evaluation report: churn delta, playbook adoption, CSM time/effort impact, compliance sign‑offs, recommended roadmap to scale.

Go/no‑go criteria (example): net pilot churn improvement ≥1 p.p. or strong qualitative evidence to iterate; legal/compliance sign‑offs in place; acceptable false‑positive rate and CSM confidence.

## 12. RISKS & MITIGATIONS (PRIORITISED FOR CCO)

1. Data protection & profiling risk (GDPR, PECR, CAN‑SPAM, CASL): run DPIA; document lawful basis; integrate suppression/consent lists; provide opt‑out and transparency in privacy notices.

2. Cross‑border data transfers: map flows; adopt SCCs or localise processing where required; pseudonymise data sent across jurisdictions.

3. Model error / false positives leading to inappropriate outreach: require human review for customer‑impacting actions; show confidence and reason (feature explainability) to CSMs.

4. Pricing / contracting exposure: never allow automated price/contract changes without manager/legal sign‑off; set discount thresholds and approval workflows.

5. Telephony safety/regulatory risk (experiments/configs): prohibit experiments/automations on emergency/compliance flows; require explicit client consent and technical safety checks.

6. IP & licensing risk for creative assets: auto‑validate license metadata before recommending or bundling assets; human legal sign‑off for exceptions.

7. Security of credentials & payment data: use vaults for credentials, tokenisation for payment details, PCI compliance where required; strict RBAC and audit logging.

Governance recommendations:
- Establish a cross‑functional AI governance working group (Product/CSM/Data/Legal/Security) chaired by CCO/CTO for retention projects.
- Require DPIA and legal sign‑off before any pilot that profiles or triggers customer contact.
- Maintain model performance dashboards and retrain cadence plus a human escalation path for disputed scores.

## 13. APPENDIX

A. Primary inputs for this report (provided): PHMG corporate site and leadership pages; provided process map of Acquire→Convert→Fulfil→Serve/Retain→Back Office; detailed opportunity inventory and prioritisation; financial signals & scale signals (FY2023 revenue, client counts, EOT transition). Specific source list in the supplied dataset includes corporate.phmg.com pages and statutory filings.

B. Next immediate steps (recommended):
  1. Approve the 90‑day pilot (budget & core team). 
  2. Initiate DPIA and data‑flow mapping; confirm legal/marketing engagement to manage outreach rules.
  3. Identify pilot cohort and CSM sponsor(s); schedule a kickoff within 2 weeks.
  4. Decide whether to run a targeted live web search to gather 8–15 recent material events about PHMG (product launches, partnerships, leadership moves) to enrich competitive and go‑to‑market context — if yes, specify language preference (English) and event types to prioritise.

C. Contact point for follow up: prepare a one‑page executive brief for the CEO/CFO and a technical annex for CTO/Head of Data if you want the 90‑day pilot resourcing estimate converted to an internal budget request.

-- End of report --
