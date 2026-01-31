# Opportunity Report – Executive Summary  
**Date:** 2025-12-31  
**Analyst:** Teho Consulting AI Advisory Team  
**Business:** Tomoro.ai  
**Report Depth:** Executive Summary  

## 1) Company Snapshot
- **Business:** Tomoro AI Ltd (brand: **Tomoro**) — enterprise AI strategy + build + infrastructure + rollout, with emphasis on **agentic / multi-agent systems**, **RAG/knowledge pipelines**, and governed delivery in **regulated industries**.
- **Footprint:** London, Edinburgh, Singapore (APAC HQ), Sydney, Melbourne.
- **Proof points / clients referenced:** Supercell (Brawl Stars RT-GP1 gameplay/support agent), Virgin Atlantic (Concierge rollout), Fidelity, DPD, OakNorth Bank.
- **Tech signals:** Founded 2023 (alliance with OpenAI). Works with OpenAI and open source models; references Nvidia/Microsoft ecosystem. Demonstrated **multi-modal** agent patterns (classifiers → retrieval → response generation → persona control) and released **open-weights multimodal embeddings** (Tomoro ColQwen3).
- **Scale signals:** ~**120–150** headcount estimate; company statements suggest ~**130** by end-2025/start-2026; rapid international expansion and stated multi-year Scotland talent investments (£4m in 2024; £10m over 3 years announced 2025). Revenue not disclosed; company-reported **10x+ monthly revenue growth** (directional).

## 2) Top 3 Opportunities
1) **Inbound qualification agent + fast-track NDA workflow (Acquire)**
   - **Goal:** Cut speed-to-lead and eliminate NDA delays for regulated prospects.
   - **Mechanism:** Brand-aligned intake agent captures structured qualification, auto-routes by region/team, and triggers **template-based NDA generation + e-sign**.
   - **Expected uplift:** Speed-to-lead **<1 hour**, **50–80%** reduction in time-to-NDA-sign; **15–30%** reduction in rep time spent on low-fit inbound.

2) **Agent observability + prompt/behaviour regression testing (Fulfil)**
   - **Goal:** Increase reliability of multi-agent systems and persona/brand control while reducing debugging and incidents.
   - **Mechanism:** End-to-end tracing of tool calls/retrieval/steps + automated regression suites and CI gating for safety/brand thresholds.
   - **Expected uplift:** **50–80%** fewer critical regressions; **20–40%** less debugging time; **30–60%** reduction in unsafe/brand-off outputs.

3) **PoC-to-production NFR gate + cost/latency estimator (Convert)**
   - **Goal:** Improve PoC→prod conversion and prevent cost/latency surprises for agentic/multi-modal workloads.
   - **Mechanism:** Standard NFR capture (SLA, privacy/safety, monitoring) + estimator built from real PoC traces and usage scenarios.
   - **Expected uplift:** **30–60%** reduction in PoC→prod failures; fewer late blockers; materially lower inference spend variance.

## 3) Why Now
- **Scaling pressure:** Fast headcount growth and multi-region delivery increases the cost of inconsistent intake, tooling, and release practices.
- **Market validation:** High-profile production launches (e.g., **Virgin Atlantic Concierge**) raise expectations for **SLA, safety, and brand alignment**—making observability/NFR gates urgent.
- **Operational leverage:** With a premium cost base (specialist hiring across regions), compressing **cycle time** (NDA → discovery → PoC → prod) and reducing **engineering rework** are direct margin levers.

## 4) 90-Day Pilot Overview
**Pilot objective:** Deliver measurable cycle-time and reliability improvements using “quick win” opportunities that reuse existing systems (forms/CRM/calendar/e-sign + observability stack/CI).

**Workstreams & timeline**
- **Days 0–15 (Design + data readiness):**
  - Map current inbound → CRM stages → NDA → first meeting; define required intake fields and routing rules.
  - Define regression test sets (representative conversations), safety/brand policies, and trace schema.
  - Agree NFR templates and estimator assumptions (latency, throughput, cost, privacy/safety).
- **Days 16–45 (Build MVPs):**
  - Deploy inbound agent on contact/referral paths; integrate CRM + calendar + e-sign; implement template-only NDA automation.
  - Implement tracing and initial regression suite; add release gate thresholds and rollback/runbook triggers.
  - Add NFR gate checklist + automated report; prototype cost/latency estimator from traces.
- **Days 46–75 (Run + iterate):**
  - A/B test inbound flow (agent-assisted vs baseline) for response time, qualification completeness, NDA turnaround.
  - Run regression suite on every prompt/tool update; tune policies, redaction, and dashboards.
  - Use NFR gate outputs in 1–2 live PoCs to validate go/no-go discipline.
- **Days 76–90 (Handover + scale plan):**
  - Finalize governance: logging/audit, consent, template controls, human-in-the-loop approvals.
  - Produce playbooks and rollout plan across regions (London/Edinburgh/Singapore/AU).

## 5) KPIs to Track
**Acquire (Inbound + NDA)**
- Median **speed-to-lead** (target: **<1 hour**)
- **% inbound leads auto-scored & routed** without manual intervention
- **Time from first contact → NDA signed** (target: **-50–80%** vs baseline)
- Rep hours/week spent on **unqualified inbound**

**Convert (PoC → Prod readiness)**
- **% PoCs progressing to production**
- # of **production blockers found post-PoC**
- **Variance** between estimated vs actual **inference spend**
- p95 **latency vs target** (PoC and first prod release)

**Fulfil (Reliability + governance)**
- **Critical regressions per sprint**
- **MTTR** and time-to-diagnose (supported by traces)
- Eval rates: **unsafe/brand-off** outputs (pre-release + production sampling)
- **Release approval cycle time** (as gates become standard)
