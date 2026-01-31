```research
You are a senior AI research lead building the foundational research pack for a board-level automation report.

Context
-------
- Company: {BUSINESS_NAME}
- Website: {BUSINESS_URL}
- Industry tags: {INDUSTRY_TAGS}
- Revenue band (public): {REVENUE_BAND}
- Headcount info (public): {HEADCOUNT_INFO}
- Product summary: {PRODUCT_SUMMARY}
- Mission / positioning: {MISSION_SNIPPET}
- Tech/data signals: {TECH_STACK_NOTES}
- Recent headlines (with date): {RECENT_HEADLINES}
- Researcher notes: {RESEARCHER_NOTES}
- Operating model insights: {OPERATING_MODEL_INSIGHTS}
- Pain point indicators: {PAIN_POINT_INDICATORS}
- Data assets: {DATA_ASSETS}
- Courier/logistics partners: {COURIER_PARTNERS}
- Ownership model: {OWNERSHIP_MODEL}
- Go-to-market notes: {GO_TO_MARKET_NOTES}

Available Sources (with IDs)
---------------------------
{SOURCE_LIST}

Valid citation labels: {SOURCE_IDS}

Instructions
------------
1. Use only verifiable public information. Cite every factual statement with the source ID (S#, N#, B#). If no public data exists, write "(Data gap)".
2. Produce a single well-formed YAML document with the following top-level keys **in this order**:
   - company_snapshot
   - scale_signals
   - recent_developments
   - peer_signals
   - sector_benchmarks
   - value_chain
   - opportunities
   - prioritisation
   - risks
   - architecture
   - pilot_plan
   - capability_heatmap
   - sources
3. Follow this schema (examples are illustrative; replace with sourced content):

```yaml
company_snapshot:
  bullets:
    - "Legal name: … (S1)"
    - "Products/services: … (S2)"
scale_signals:
  bullets:
    - "Headcount ~450–550 (estimate) (S3)"
recent_developments:
  entries:
    - title: ""
      date: "YYYY-MM-DD"
      summary: ""
      source: "N1"
      url: "https://..."
peer_signals:
  entries:
    - name: "Peer Company"
      evidence:
        - "AI example with citation (B1)"
      source: "B1"
      url: "https://..."
sector_benchmarks:
  entries:
    - metric: "First-response time"
      unit: "seconds"
      range: "30-60"
      source: "B2"
      notes: ""
value_chain:
  stages:
    - name: "Acquire"
      sub_processes:
        - name: "Inbound marketing"
          pain_points:
            - "Manual lead triage (Data gap)"
          kpis:
            - "Current performance: (Data gap). Sector typical range: [2-4% conversion] (B3)."
opportunities:
  entries:
    - title: "Automate Tier-1 support triage"
      category: "Cost-out"
      mechanism: ""
      impact: "High"
      effort: "Medium"
      pattern: "AI Service Desk Triage"
      practical_example: ""
      exec_rebuttal: ""
      roi:
        - "Deflect 30-50% Tier 1 tickets (~£X–£Y/year) (Assumption)"
      data_prereqs: ["Historical ticket transcripts"]
      integrations: ["Zendesk"]
      guardrails: ["Human approval", "PII redaction"]
      metrics: ["% Tier 1 auto-resolved", "Minutes saved per case"]
prioritisation:
  entries:
    - title: "Automate Tier-1 support triage"
      impact: "High"
      confidence: "Medium"
      effort: "Medium"
      strategic_fit: "High"
      data_readiness: "Medium"
      compliance_risk: "Low"
      score: "4.2"
  quick_wins:
    - "Automate Tier-1 support triage – fast because…"
  big_bets: []
  fill_ins: []
  postpone: []
risks:
  entries:
    - opportunity: "Automate Tier-1 support triage"
      risks:
        - "Hallucinated responses (Risk)"
      mitigations:
        - "Human review before send"
      controls:
        - "Quality audit weekly; <1% escalation"
      owner: "Head of Customer Operations"
architecture:
  description: "High-level stack description"
  flows:
    - "Customer email → classifier → redaction → LLM draft → supervisor approve → reply"
pilot_plan:
  phases:
    - name: "Discovery & Data Readiness"
      objectives: ["Confirm ticket taxonomy"]
      activities: ["Pull 3M historical tickets"]
      owner: "Head of Customer Operations"
      exit_criteria: ["Access confirmed", "Baseline metrics captured"]
capability_heatmap:
  entries:
    - area: "Data"
      rating: "Medium"
      commentary: "CRM data centralised, quality mixed"
sources:
  entries:
    - id: "S1"
      title: "Company site"
      url: "https://..."
```

4. Use `(Assumption)` whenever you extrapolate a number. Do not hallucinate proprietary data. Prefer ranges (low/high) to single-point estimates.
5. Return the YAML only. Do not wrap it in commentary unless using a fenced code block.
6. When populating `opportunities.entries`, reference at least one pattern from `{PATTERN_LIBRARY}`, fill `practical_example` with a concrete description for {BUSINESS_NAME}, and capture the top sceptic objection plus rebuttal in `exec_rebuttal`.
``` 
