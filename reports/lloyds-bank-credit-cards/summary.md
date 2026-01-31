# Opportunity Report – Executive Summary  
**Date:** 2026-01-12  
**Analyst:** Teho Consulting AI Advisory Team  
**Business:** Lloyds Bank - Credit Cards  
**Report Depth:** Executive Summary  

## 1) Company Snapshot
- **Entity/brands:** Lloyds Bank plc across **Lloyds, Halifax, Bank of Scotland, MBNA**.
- **Core products in scope:** Credit cards (prime + credit-builder + business), current accounts, mortgages, savings/investments; strong **mobile/online banking** with in‑app servicing (activation, PIN, card controls) and secure messaging.
- **Footprint:** UK plus **Jersey/Guernsey/Isle of Man**.
- **Scale & financial context (Group-level):** ~**61k FTE**; FY2024 statutory total income **~£34.3bn (–3% YoY)**; **PBT ~£6.0bn (–20% YoY)**; **cost:income 60.4%** (management targeting sub‑50% by 2026); NIM **2.95%** (down from 3.11%). Efficiency and customer experience improvements are immediate levers.
- **Strategic signals from news:** accelerating **AI platform build (Vertex AI)**; planned **AI financial assistant (early 2026)**; continued **branch closures** (digital shift); heightened emphasis on **fraud prevention**; and strong innovation posture (tokenised deposits/collateral; Curve acquisition).

## 2) Top 3 Opportunities
1) **Secure messaging triage + GenAI response drafting (Serve/Retain)**
   - **What:** Intent classification, vulnerability/complaint cueing, brand/product-grounded retrieval, and agent-approved drafting with auto-resolve for low-risk intents.
   - **Why it matters:** Directly cuts backlog and repeat contacts; improves **FCR** and consistency across Lloyds/Halifax/BoS/MBNA.
   - **Indicative value:** **£10m–£50m/yr**; **20–50%** backlog reduction; **+5–10pt FCR**.

2) **GenAI “copy-to-compliance” accelerator (Acquire)**
   - **What:** Controlled drafting/redlining for product pages, offers, and in‑app prompts using a **versioned clause bank**, mandatory disclosures, structured reviewer diffs and audit trail.
   - **Why it matters:** Compresses financial promotion cycles; improves clarity/CTR while lowering pre‑apply questions.
   - **Indicative value:** **£5m–£25m/yr**; **30–60%** cycle-time reduction; **2–5%** CTR uplift.

3) **Eligibility-to-underwriting consistency monitor (Acquire/Convert)**
   - **What:** “Shadow underwriting” at eligibility + monitoring deltas between eligibility estimates and final outcomes by brand/segment/channel; governed recalibration proposals.
   - **Why it matters:** Reduces **eligibility vs approval** expectation gaps that drive complaints and wasted applications; improves estimated limit accuracy.
   - **Indicative value:** **£5m–£30m/yr**; **10–25%** reduction in eligibility/approval gap.

## 3) Why Now
- **Cost pressure + efficiency targets:** Rising cost:income and lower profitability make **contact deflection, faster handling, and fewer reopens** high-ROI, low-regret moves.
- **Digital migration at scale:** Branch closures increase reliance on **secure messaging and self-serve**; service quality becomes a primary brand differentiator.
- **Platform readiness:** Expanded investment in **Google Cloud/Vertex AI** lowers delivery risk for retrieval-grounded GenAI and monitoring/MLOps patterns.
- **Regulatory scrutiny / Consumer Duty:** Needs **clear, auditable, consistent** customer communications and controlled AI—these opportunities are compatible with strong governance (human approval, disclosure libraries, audit trails).

## 4) 90-Day Pilot Overview
**Pilot goal:** Prove measurable improvements in customer servicing throughput and quality while maintaining strict compliance controls.

**Scope (single product + 1–2 brands first):** Credit cards servicing via **secure messaging** (e.g., Lloyds + Halifax), then expand to BoS/MBNA.

**Workplan:**
- **Weeks 1–2 (Design & controls):** Define intent taxonomy; agree “auto-resolve allowed” list; implement PII redaction rules; configure retrieval over approved knowledge articles by brand; complaint/vulnerability escalation logic.
- **Weeks 3–6 (Build):** Classifier + routing; GenAI drafting with citations; agent UI with suggested response + reason/KB links; full audit logging.
- **Weeks 7–10 (Run A/B pilot):** 10–20% traffic to assisted-draft flow; limited auto-resolve for low-risk intents (status/how-to) with monitoring.
- **Weeks 11–13 (Hardening & scale decision):** Evaluate outcomes; expand intent coverage; finalize operating model and rollout plan.

**Non-negotiable guardrails:** retrieval-only content; **human approval** for regulated/high-risk intents (fees/APR changes, disputes, fraud, hardship); immutable audit trail; Consumer Duty review; access controls by brand/role.

## 5) KPIs to Track
**Servicing performance (primary):**
- **Time-to-first-response** (p50/p95) and **backlog volume**
- **First-contact resolution (FCR)** and **reopen/repeat-contact rate**
- **Handle time / agent productivity** (draft acceptance rate; edits per message)

**Customer & risk outcomes:**
- Complaint rate and vulnerability-case SLA adherence
- QA/compliance defect rate (incorrect disclosure, misrouting, unsupported claims)

**Business outcomes (secondary):**
- Contact cost per resolved case
- CSAT/NPS for messaging journeys

**Pilot success bar (typical):** ≥**25%** reduction in backlog *or* ≥**5pt** FCR uplift with no increase in compliance defects.
