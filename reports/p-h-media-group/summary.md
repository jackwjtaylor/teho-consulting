# Opportunity Report – Executive Summary  
**Date:** 2026-01-01  
**Analyst:** Teho Consulting AI Advisory Team  
**Business:** P H Media Group  
**Report Depth:** Executive Summary  

1) Company Snapshot

- Legal name: PHMG (group entities: PH Media (USA) Inc.; Please Hold (UK) Ltd.; PHMG (AUSTRALIA) PTY LTD; PHMG (CANADA) Inc.; PHMG (NEW ZEALAND) Ltd.). Employee‑owned since Apr 2025.
- Scale & finance: ~36k clients; FY2023 revenue £85.5m (double‑digit growth 2021–23); profitable with healthy working capital at trading subsidiary level.
- Footprint: Manchester HQ + offices in Chicago, Phoenix, Brisbane; clients in 50+ countries.
- Core products: Exclusive music, audio branding, on‑hold marketing, Complete Caller Experience (cloud telephony), PHMG Portal, caller analytics, creative & production services.
- Tech signals: cloud telephony/analytics platform, PHMG Portal, AI‑referenced capabilities, patented processes.
- Customers: global enterprise brands and high‑volume SME base (implied ARPU ~£2.3k/year).

2) Top 3 Opportunities (condensed)

- Predictive churn scoring + early‑intervention playbooks (Priority #1)
  - What: model risk using Portal engagement, caller analytics, billing & support; surface scored accounts and auto‑generate ranked playbooks for CSMs.
  - Impact: High; estimated retained revenue £0.8M–£2.5M/yr for 1–3pp churn reduction. Effort: Medium.

- Renewal & upsell orchestration with tailored offer generation (Priority #2)
  - What: auto‑generate personalised renewal/upsell packages using churn score, usage and contract data; auto‑populate proposals and timed outreach.
  - Impact: High; estimated incremental revenue £0.9M–£4.0M/yr. Effort: Medium (CRM/billing/legal integrations required).

- Automated "Action Pack" insights from caller analytics (Priority #3)
  - What: deterministic rules + LLM summarisation to deliver prioritized, one‑click recommendations in‑portal (audio refresh, IVR tweaks, A/B tests).
  - Impact: High; estimated uplift £0.4M–£2.0M/yr through greater adoption and retention. Effort: Medium.

3) Why Now

- Large, recurring base (36k clients) means small % improvements scale to material revenue; implied ARPU ~£2.3k amplifies impact.
- PHMG already owns key telemetry (PHMG Portal + Complete Caller Experience) — data prerequisites are largely available.
- Company is growing, profitable and employee‑owned (EOT) — strategic orientation to invest in customer lifetime value and margin preservation.
- AI is already referenced on site and can accelerate automation (scoring, LLM summarisation, guided workflows) with moderate engineering lift.
- Quick wins protect ARR and free CSM capacity for higher‑value selling while larger bets (A/B experimentation) remain follow‑ons.

4) 90‑Day Pilot Overview (Predictive churn scoring + playbooks)

- Objective: demonstrate that a telemetry‑driven churn score + templated intervention increases early renewals and reduces near‑term churn among a test cohort.
- Scope: 2 segmented cohorts (1) 500 SME recurring clients with mid ARPU; (2) 100 enterprise/high‑ARR accounts. Use 6–12 weeks historical data + live 30‑day window.
- Key activities by week:
  - Week 0–2: Project kick‑off, data mapping (Portal logs, caller analytics, CRM, billing, support), privacy & legal checklist (GDPR). Identify success metrics and baseline.
  - Week 3–5: Build and validate churn risk model (explainability layer), design ranked playbooks and templated communications; instrumentation for logging and A/B assignment.
  - Week 6–8: Integrate prototype into PHMG Portal / CSM dashboard; run controlled rollout (auto emails + CSM escalations) to test cohort.
  - Week 9–12: Measure outcomes, collect qualitative CSM feedback, iterate playbook content; prepare scale recommendation.
- Team & resources: Data engineer, ML engineer / data scientist, Product owner, 2 CSMs, Legal/Privacy, 1 Portal engineer, Analytics PM. Minimal infra: existing Portal + analytics exports.
- Guardrails: human‑in‑the‑loop for pricing/contract changes, explicit client consent for outreach, GDPR compliance, no auto‑deploy of creative without client sign‑off.
- Success criteria (90 days): model precision/recall acceptable (e.g., lift in observed churn risk > baseline); increase in early renewals in test vs control by ≥10%; CSM time saved per at‑risk account measurable; playbook adoption ≥20%.

5) KPIs to Track

- Commercial / retention: annual client churn rate (%), net retention rate (%), retained revenue (£), number of early renewals within 90 days, upsell conversion rate (%).
- Adoption & engagement: PHMG Portal activation % (30 days), Action Packs delivered per client/month, recommendation adoption rate (%).
- Operational: CSM time spent per at‑risk account (hrs), time to close renewal (days), MTTR for support tickets (hours), ticket re‑open rate (%).
- Financial / cash: incremental ARR from pilots/upsells (£), DSO (days) and invoice dispute rate (%).

Next steps (recommended): greenlight 90‑day predictive churn pilot with data access approvals, nominate CSM & technical leads, and confirm legal/privacy guardrails to begin Week 0 data mapping.
