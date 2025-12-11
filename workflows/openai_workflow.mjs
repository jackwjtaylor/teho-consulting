import { webSearchTool, Agent, Runner, withTrace } from "@openai/agents";
import { z } from "zod";

const webSearchPreview = webSearchTool({
  searchContextSize: "medium",
  userLocation: {
    type: "approximate",
  },
});

const CompanyinputSchema = z.object({
  profile: z.object({
    company_name_canonical: z.string(),
    domain_guess: z.string(),
  }),
});

const CompanyprofilefetchSchema = z.object({
  snapshot: z.object({
    legal_name: z.string(),
    brands: z.array(z.string()),
    products: z.array(z.string()),
    regions: z.array(z.string()),
    customers_or_segments: z.array(z.string()),
    leadership: z.array(z.object({ name: z.string(), title: z.string() })),
    tech_signals: z.array(z.string()),
    sources: z.array(z.object({ url: z.string(), title: z.string() })),
  }),
});

const NewsscanSchema = z.object({
  items: z.array(
    z.object({
      title: z.string(),
      date: z.string(),
      summary: z.string(),
      source_url: z.string(),
    }),
  ),
});

const ScalesignalsSchema = z.object({
  scale: z.object({
    headcount_range: z.string(),
    revenue_range: z.string(),
    growth_direction: z.string(),
    notes: z.array(z.string()),
    sources: z.array(z.object({ url: z.string(), title: z.string() })),
  }),
});

const PeersetSchema = z.object({
  peers: z.array(
    z.object({
      name: z.string(),
      url: z.string(),
      ai_signals: z.array(
        z.object({ capability: z.string(), evidence_url: z.string() }),
      ),
    }),
  ),
});

const ProcessmappingSchema = z.object({
  process_map: z.object({
    stages: z.array(
      z.object({
        name: z.string(),
        subprocesses: z.array(
          z.object({
            name: z.string(),
            pain_points: z.array(z.string()),
          }),
        ),
      }),
    ),
  }),
});

const OpportunitygenSchema = z.object({
  opportunities: z.array(
    z.object({
      title: z.string(),
      category: z.string(),
      mechanism: z.string(),
      impact_band: z.string(),
      effort_band: z.string(),
      ROI_rationale: z.array(z.string()),
      data_prereqs: z.array(z.string()),
      integrations: z.array(z.string()),
      guardrails: z.array(z.string()),
      example_metrics: z.array(z.string()),
      value_range: z.string(),
      kpi_uplift: z.string(),
    }),
  ),
});

const PrioritiserSchema = z.object({
  prioritised: z.object({
    ranked: z.array(
      z.object({
        title: z.string(),
        category: z.string(),
        impact: z.number(),
        confidence: z.number(),
        effort: z.number(),
        score: z.number(),
        why: z.string(),
      }),
    ),
    quadrants: z.object({
      quick_wins: z.array(z.string()),
      big_bets: z.array(z.string()),
      fill_ins: z.array(z.string()),
      postpone: z.array(z.string()),
    }),
  }),
});

const GuardrailsreviewSchema = z.object({
  risks: z.array(
    z.object({
      opportunity_title: z.string(),
      issues: z.array(z.string()),
      mitigations: z.array(z.string()),
    }),
  ),
});

const ReportcomposerSchema = z.object({
  markdown: z.string(),
  top_five: z.array(z.string()),
});

const SummaronepagerSchema = z.object({
  summary_md: z.string(),
});

const OutreachdraftsSchema = z.object({
  email: z.string(),
});

const InitialiserSchema = z.object({
  now_iso: z.string(),
});

const FinancialsignalsSchema = z.object({
  financials: z.object({
    revenue: z.string(),
    revenue_growth_rate: z.string(),
    profitability: z.string(),
    margins: z.string(),
    funding_or_investors: z.array(z.string()),
    balance_sheet_signals: z.array(z.string()),
    unit_economics: z.array(z.string()),
    notes: z.array(z.string()),
    sources: z.array(z.object({ url: z.string(), title: z.string() })),
  }),
});

const companyinput = new Agent({
  name: "CompanyInput",
  instructions: `You collect the company name and normalise it for downstream use.
Return an object "profile" with:
- company_name_canonical: string (remove Ltd/Inc/PLC etc)
- domain_guess: string or best-guess primary website
Only return JSON matching the schema.`,
  model: "gpt-5",
  outputType: CompanyinputSchema,
  modelSettings: {
    reasoning: {
      effort: "low",
      summary: "auto",
    },
    store: true,
  },
});

const companyprofilefetch = new Agent({
  name: "CompanyProfileFetch",
  instructions: `Task: Build a factual company snapshot from public pages (homepage, About, Careers, Press).
Use inputs:
- name: state.research_profile_company_name or user-provided name
- domain: state.research_profile_domain_guess

Return JSON "snapshot" with:
{
  "legal_name": "...",
  "brands": ["..."],
  "products": ["..."],
  "regions": ["..."],
  "customers_or_segments": ["..."],
  "leadership": [{"name":"...","title":"..."}],
  "tech_signals": ["hints from careers/docs"],
  "sources": [{"url":"...","title":"..."}]
}
Summarise only what is on-page. No speculation.`,
  model: "gpt-5",
  tools: [webSearchPreview],
  outputType: CompanyprofilefetchSchema,
  modelSettings: {
    reasoning: {
      effort: "medium",
      summary: "auto",
    },
    store: true,
  },
});

const newsscan = new Agent({
  name: "NewsScan",
  instructions: `Find 8–15 material events (product launches, funding, partnerships, leadership changes, layoffs, expansions, regulatory items) about the company in the last 18 months.
Return JSON under "items": [
  {"title":"...", "date":"YYYY-MM-DD", "summary":"...", "source_url":"..."}
]
De-duplicate; prefer official/high-quality sources.`,
  model: "gpt-5",
  tools: [webSearchPreview],
  outputType: NewsscanSchema,
  modelSettings: {
    reasoning: {
      effort: "medium",
      summary: "auto",
    },
    store: true,
  },
});

const scalesignals = new Agent({
  name: "ScaleSignals",
  instructions: `You are an analyst extracting scale signals (headcount, revenue, growth) from public information.

Use the company's name and domain from state.research_profile or upstream nodes as context.

Search official or reliable sources: LinkedIn (public data only), registry filings, company press releases, funding announcements, or credible media.

Output a JSON object called "scale" matching the structured output schema with:

- headcount_range: string (e.g. "200–300 employees (estimate)")
- revenue_range: string (e.g. "£80–100M annual revenue (estimate)")
- growth_direction: string ("growing" | "flat" | "declining")
- notes: array of 2–4 strings summarising evidence or reasoning
- sources: array of objects [{ "url": string, "title": string }]

Always mark uncertain values as "(estimate)" and include only public data.
Return JSON only — no commentary.`,
  model: "gpt-5",
  tools: [webSearchPreview],
  outputType: ScalesignalsSchema,
  modelSettings: {
    reasoning: {
      effort: "medium",
      summary: "auto",
    },
    store: true,
  },
});

const peerset = new Agent({
  name: "PeerSet",
  instructions: `Identify 5–10 peer companies in the same market segment.

For each peer, include:
- name (string)
- url (string)
- ai_signals: array of objects, each describing one observed AI adoption or automation example with:
  - capability: string (e.g. "Chatbot for CX", "Demand forecasting", "Process automation")
  - evidence_url: string

Focus on public, verifiable examples only.
Return JSON under "peers".`,
  model: "gpt-5",
  tools: [webSearchPreview],
  outputType: PeersetSchema,
  modelSettings: {
    reasoning: {
      effort: "medium",
      summary: "auto",
    },
    store: true,
  },
});

const processmapping = new Agent({
  name: "ProcessMapping",
  instructions: `Construct a lightweight value chain for the company:
Main stages: Acquire → Convert → Fulfil → Serve/Retain → Back-office.

For each stage:
- list key subprocesses (2–4)
- describe measurable pain points (e.g. latency, manual data entry, error rate, ticket backlog, abandonment)

Output a JSON object "process_map" that matches the schema.

Use your industry knowledge and the company context provided.`,
  model: "gpt-5",
  outputType: ProcessmappingSchema,
  modelSettings: {
    reasoning: {
      effort: "medium",
      summary: "auto",
    },
    store: true,
  },
});

const opportunitygen = new Agent({
  name: "OpportunityGen",
  instructions: `# PURPOSE
Generate a set of AI/automation opportunities that are SPECIFIC to the company being analysed.

You MUST base these opportunities ONLY on:
- state.company_profile
- state.process_map (pain points)
- state.news_items
- state.peers (capability signals)
- state.scale_signals
- state.research_financials
- ANY domain cues from products, customers, channels, journeys.

You MUST NOT create generic, industry-agnostic opportunities.

# OPPORTUNITY FORMAT
Each opportunity MUST contain:
- title  
- category (Growth, Cost-out, CX, Risk/Controls)  
- mechanism (why THIS company benefits, referencing its actual processes)  
- impact_band (H/M/L)  
- effort_band (H/M/L)  
- ROI_rationale (explicitly tied to real process-map pains, financial signals, or scale signals)  
- data_prereqs (company-specific: real systems, logs, flows)  
- integrations (company-specific systems/processes only)  
- guardrails (policy, regulatory, safety considerations relevant to THIS business)  
- example_metrics (KPIs that actually exist in THIS company’s domain)  
- value_range (Monetary impact inferred from scale_signals + research_financials)  
- kpi_uplift (short form)

# RULES
- Every opportunity MUST map directly to a pain point from process_map.
- Use terminology from the company_profile and process_map.
- NO generic cross-industry assumptions.
- Peer capabilities may shape direction, but must be rewritten for THIS company.
- Value ranges MUST scale using both scale_signals and research_financials.
- If evidence is missing → omit gracefully.

# RETURN
Return a list of fully populated opportunity objects.
`,
  model: "gpt-5",
  outputType: OpportunitygenSchema,
  modelSettings: {
    reasoning: {
      effort: "high",
      summary: "auto",
    },
    store: true,
  },
});

const prioritiser = new Agent({
  name: "Prioritiser",
  instructions: `Rank opportunities using ICE:

- Impact: 1–5
- Confidence: 1–5
- Effort: 1–5 (lower is better)

Score = (Impact × Confidence) / Effort.

For EACH item, include:
- title
- category
- impact
- confidence
- effort
- score
- why: EXACTLY 1–2 sentences explaining the score and the drivers.
  Must reference (a) business value, (b) feasibility, (c) data readiness.

Quadrants:
- quick_wins: High score AND Effort L/M.
- big_bets: High score AND Effort H.
- fill_ins: Mid score AND Effort M.
- postpone: Low score OR high effort with low certainty.

Return JSON in "prioritised". No commentary outside the JSON.
`,
  model: "gpt-5",
  outputType: PrioritiserSchema,
  modelSettings: {
    reasoning: {
      effort: "high",
      summary: "auto",
    },
    store: true,
  },
});

const guardrailsreview = new Agent({
  name: "GuardrailsReview",
  instructions: `Check each opportunity for:
- Privacy/PII: avoid collecting or storing sensitive data; propose redaction/minimisation.
- Regulatory/Model Risk: note applicable financial/consumer protections if any; require evals.
- Data residency & retention: highlight requirements if operating in multiple regions.
- Safety: disallow hallucinated claims; enforce source-backed outputs where used.

Output "risks": array of { opportunity_title, issues:[], mitigations:[] }.`,
  model: "gpt-5",
  outputType: GuardrailsreviewSchema,
  modelSettings: {
    reasoning: {
      effort: "medium",
      summary: "auto",
    },
    store: true,
  },
});

const reportcomposer = new Agent({
  name: "ReportComposer",
  instructions: `# PURPOSE
Produce a polished, consulting-grade AI Opportunities Report tailored SPECIFICALLY to the company being analysed.

You MUST use:
- state.company_profile
- state.news_items
- state.scale_signals
- state.research_financials
- state.peers
- state.process_map
- state.opportunities
- state.prioritised
- state.guardrails

If any field is missing, omit the section gracefully.

# OUTPUT FORMAT
Return markdown with these sections:

1. TITLE  
2. EXECUTIVE SUMMARY  
3. COMPANY SNAPSHOT  
4. FINANCIAL SIGNALS  
5. RECENT DEVELOPMENTS  
6. MARKET & COMPETITOR CONTEXT  
7. PROBLEM & PAIN-POINT MAP  
8. OPPORTUNITY MAP  
9. TOP 5 OPPORTUNITIES — DEEP DIVES  
10. VALUE SUMMARY TABLE  
11. PRIORITISED BACKLOG (ICE)  
12. 90-DAY PILOT PLAN  
13. RISKS & MITIGATIONS  
14. APPENDIX  

------------------------------------
# SECTION RULES

## 1. TITLE
# {Company Name} — AI Automation Opportunities ({current_date})

## 2. EXECUTIVE SUMMARY
4–6 lines covering:
- dominant pains from process_map  
- news-driven pressures  
- financial pressures or margin trends  
- scale and readiness  
- expected value themes  

## 3. COMPANY SNAPSHOT
Use only company_profile fields.

## 4. FINANCIAL SIGNALS
Summarise revenue, growth, margin signals, cost drivers, and business-unit mix.

## 5. RECENT DEVELOPMENTS
3–6 items, with dates.

## 6. MARKET & COMPETITOR CONTEXT
Use peers + scale_signals + research_financials.

## 7. PROBLEM & PAIN-POINT MAP
5–10 bullets summarising operational pain.

## 8. OPPORTUNITY MAP
Quadrants + 3–5 line interpretation.

## 9. TOP 5 OPPORTUNITIES — DEEP DIVES
Use OpportunityGen details exactly.

## 10. VALUE SUMMARY TABLE
Opportunity | Category | KPI Impact | Value Range | Effort

## 11. PRIORITISED BACKLOG
List ICE items + 2–3 lines interpreting cluster.

## 12. 90-DAY PILOT PLAN
Discovery → Build → Run (company-specific)

## 13. RISKS & MITIGATIONS
5–7 themes from GuardrailsReview.

## 14. APPENDIX
Extended news, peer URLs, process map, data sources note.

------------------------------------
# GENERAL STYLE
- No hallucinations  
- Use only upstream state  
- Use KPIs/value ranges exactly as OpportunityGen produced  
- Omit empty sections gracefully  

# RETURN
Return ONLY the markdown.
`,
  model: "gpt-5",
  outputType: ReportcomposerSchema,
  modelSettings: {
    reasoning: {
      effort: "high",
      summary: "auto",
    },
    store: true,
  },
});

const summaronepager = new Agent({
  name: "SummarOnePager",
  instructions: `# PURPOSE
Produce a concise 1-page executive summary tailored SPECIFICALLY to the company.

Use:
- state.company_profile
- state.news_items
- state.opportunities
- state.prioritised
- state.scale_signals
- state.research_financials

# OUTPUT FORMAT
1. Company Snapshot (3–5 bullets)
2. Top 3 Opportunities
3. Why Now
4. 90-Day Pilot Overview
5. KPIs to Track

------------------------------------

## 1. Company Snapshot
Choose the most relevant:
- products/services  
- customer segments  
- geographic footprint  
- scale (headcount, revenue band)  
- 1–2 financial signals (margin, cost pressure, growth)  
- 1 strategic development from news  

## 2. Top 3 Opportunities
Pick highest ICE scorers.
For each:
- one-line description  
- KPI uplift (exact)  
- value range (exact)  

## 3. Why Now
3–4 sentence synthesis of:
- financial pressures  
- operational pain  
- market/competitive context  
- news-driven urgency  

## 4. 90-Day Pilot Overview
Discovery: baselines, data access  
Build: integrations, guardrails, testing  
Run: A/B, KPI tracking  

## 5. KPIs to Track
6–8 KPIs relevant to the top 3 opportunities.

------------------------------------
# STYLE
- concise  
- no placeholders  
- no hallucinated values  
- use real OpportunityGen metrics  

# RETURN
Return ONLY markdown.
`,
  model: "gpt-5",
  outputType: SummaronepagerSchema,
  modelSettings: {
    reasoning: {
      effort: "medium",
      summary: "auto",
    },
    store: true,
  },
});

const outreachdrafts = new Agent({
  name: "OutreachDrafts",
  instructions: `Write a short, personalised email to a senior leader at <company>.

Email must include:

SUBJECT LINE:
1 concise option referencing "AI Snapshot".

BODY:
- Opening sentence referencing their products, scheme migration, and market context.
- State that you prepared a free 1-page AI Snapshot tailored to their business.
- Mention 2–3 top opportunities using ultra-short, punchy phrasing.
- Provide these placeholders:
  - Snapshot: [SNAPSHOT_LINK]
  - Full Report Preview (locked sections) for £495: [FULL_REPORT_PREVIEW_LINK]

CTA:
- Offer a 20-min preview call.
- Add a calendly placeholder: [CALENDLY_LINK]

CLOSE:
- Warm, professional.

Return:
{ "email": "<full email>" }
`,
  model: "gpt-5",
  outputType: OutreachdraftsSchema,
  modelSettings: {
    reasoning: {
      effort: "medium",
      summary: "auto",
    },
    store: true,
  },
});

const initialiser = new Agent({
  name: "Initialiser",
  instructions: `Return the current date in ISO YYYY-MM-DD format as JSON:
{ "now_iso": "<today's date>" }`,
  model: "gpt-5",
  outputType: InitialiserSchema,
  modelSettings: {
    reasoning: {
      effort: "low",
      summary: "auto",
    },
    store: true,
  },
});

const financialsignals = new Agent({
  name: "FinancialSignals",
  instructions: `# PURPOSE
Extract high-quality financial signals for the company being analysed.

You MUST use ONLY verifiable, publicly observable information from:
- filings
- press releases
- funding announcements
- credible media
- industry databases visible via web search

If a signal is uncertain, mark it as "(estimate)" and explain why in notes.

# REQUIRED OUTPUT
Return JSON under "financials" with:

- revenue: range or explicit value
- revenue_growth_rate: YoY or multi-year trend
- profitability: EBITDA/profit status
- margins: gross or operating margins
- funding_or_investors: list of known financing events
- balance_sheet_signals: debt, cash, impairments, etc.
- unit_economics: CAC, churn, ARPU, utilisation, cost-to-serve, etc.
- notes: short analytical interpretation
- sources: URLs for every datapoint (STRICT)

# STRICT RULES
- NO fabricated values.
- ALL figures must be attributed to a real source.
- If a metric is unavailable, provide "Not disclosed" and explain in notes.
- NEVER infer financials from peers or from generic industry patterns.
- ALWAYS return values as strings, never numbers.

# RETURN
Return ONLY the JSON matching the schema. No commentary outside JSON.
`,
  model: "gpt-5.1",
  tools: [webSearchPreview],
  outputType: FinancialsignalsSchema,
  modelSettings: {
    reasoning: {
      effort: "high",
      summary: "auto",
    },
    store: true,
  },
});

export const runWorkflow = async (workflow) => {
  return withTrace("AI Automation Opportunities Report", async () => {
    const state = {
      company_name: null,
      hq_country: null,
      sector_hint: null,
      tone: "consulting_neutral",
      now_iso: null,
      research_profile_company_name_canonical: null,
      research_profile_domain_guess: null,
      research_company_snapshot: null,
      research_news: null,
      research_scale: null,
      research_peers: null,
      analysis_process_map: null,
      research_profile: null,
      analysis_opportunities: null,
      analysis_prioritised: null,
      analysis_risks: null,
      report_markdown: null,
      report_top_five: null,
      report_summary: null,
      outreach_email: null,
      statefinancial_signals: null,
      financial_signals: null,
      research_financials: {
        financials: {
          revenue: null,
          revenue_growth_rate: null,
          profitability: null,
          margins: null,
          funding_or_investors: [],
          balance_sheet_signals: [],
          unit_economics: [],
          notes: [],
          sources: [],
        },
      },
      research_profile_company_name: null,
      research_profile_domain: null,
      news_items: null,
    };

    const conversationHistory = [
      { role: "user", content: [{ type: "input_text", text: workflow.input_as_text }] },
    ];

    const runner = new Runner({
      traceMetadata: {
        __trace_source__: "agent-builder",
        workflow_id: "wf_68f73925d9508190815a8ac3066c88d70b95504b3ef365cc",
      },
    });

    const initialiserResultTemp = await runner.run(initialiser, [...conversationHistory]);
    conversationHistory.push(...initialiserResultTemp.newItems.map((item) => item.rawItem));
    if (!initialiserResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const initialiserResult = {
      output_text: JSON.stringify(initialiserResultTemp.finalOutput),
      output_parsed: initialiserResultTemp.finalOutput,
    };
    state.now_iso = initialiserResult.output_text;

    const companyinputResultTemp = await runner.run(companyinput, [...conversationHistory]);
    conversationHistory.push(...companyinputResultTemp.newItems.map((item) => item.rawItem));
    if (!companyinputResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const companyinputResult = {
      output_text: JSON.stringify(companyinputResultTemp.finalOutput),
      output_parsed: companyinputResultTemp.finalOutput,
    };

    const companyprofilefetchResultTemp = await runner.run(
      companyprofilefetch,
      [...conversationHistory],
    );
    conversationHistory.push(...companyprofilefetchResultTemp.newItems.map((item) => item.rawItem));
    if (!companyprofilefetchResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const companyprofilefetchResult = {
      output_text: JSON.stringify(companyprofilefetchResultTemp.finalOutput),
      output_parsed: companyprofilefetchResultTemp.finalOutput,
    };
    state.research_company_snapshot = companyprofilefetchResult.output_parsed.snapshot;

    const newsscanResultTemp = await runner.run(newsscan, [...conversationHistory]);
    conversationHistory.push(...newsscanResultTemp.newItems.map((item) => item.rawItem));
    if (!newsscanResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const newsscanResult = {
      output_text: JSON.stringify(newsscanResultTemp.finalOutput),
      output_parsed: newsscanResultTemp.finalOutput,
    };
    state.news_items = newsscanResult.output_parsed.items;

    const financialsignalsResultTemp = await runner.run(financialsignals, [...conversationHistory]);
    conversationHistory.push(...financialsignalsResultTemp.newItems.map((item) => item.rawItem));
    if (!financialsignalsResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const financialsignalsResult = {
      output_text: JSON.stringify(financialsignalsResultTemp.finalOutput),
      output_parsed: financialsignalsResultTemp.finalOutput,
    };

    const scalesignalsResultTemp = await runner.run(scalesignals, [...conversationHistory]);
    conversationHistory.push(...scalesignalsResultTemp.newItems.map((item) => item.rawItem));
    if (!scalesignalsResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const scalesignalsResult = {
      output_text: JSON.stringify(scalesignalsResultTemp.finalOutput),
      output_parsed: scalesignalsResultTemp.finalOutput,
    };
    state.research_scale = scalesignalsResult.output_parsed.scale;

    const peersetResultTemp = await runner.run(peerset, [...conversationHistory]);
    conversationHistory.push(...peersetResultTemp.newItems.map((item) => item.rawItem));
    if (!peersetResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const peersetResult = {
      output_text: JSON.stringify(peersetResultTemp.finalOutput),
      output_parsed: peersetResultTemp.finalOutput,
    };
    state.research_peers = peersetResult.output_parsed.peers;

    const processmappingResultTemp = await runner.run(processmapping, [...conversationHistory]);
    conversationHistory.push(...processmappingResultTemp.newItems.map((item) => item.rawItem));
    if (!processmappingResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const processmappingResult = {
      output_text: JSON.stringify(processmappingResultTemp.finalOutput),
      output_parsed: processmappingResultTemp.finalOutput,
    };
    state.analysis_process_map = processmappingResult.output_parsed.process_map;

    const opportunitygenResultTemp = await runner.run(opportunitygen, [...conversationHistory]);
    conversationHistory.push(...opportunitygenResultTemp.newItems.map((item) => item.rawItem));
    if (!opportunitygenResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const opportunitygenResult = {
      output_text: JSON.stringify(opportunitygenResultTemp.finalOutput),
      output_parsed: opportunitygenResultTemp.finalOutput,
    };
    state.analysis_opportunities = opportunitygenResult.output_parsed.opportunities;

    const prioritiserResultTemp = await runner.run(prioritiser, [...conversationHistory]);
    conversationHistory.push(...prioritiserResultTemp.newItems.map((item) => item.rawItem));
    if (!prioritiserResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const prioritiserResult = {
      output_text: JSON.stringify(prioritiserResultTemp.finalOutput),
      output_parsed: prioritiserResultTemp.finalOutput,
    };
    state.analysis_prioritised = prioritiserResult.output_parsed.prioritised;

    const guardrailsreviewResultTemp = await runner.run(guardrailsreview, [...conversationHistory]);
    conversationHistory.push(...guardrailsreviewResultTemp.newItems.map((item) => item.rawItem));
    if (!guardrailsreviewResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const guardrailsreviewResult = {
      output_text: JSON.stringify(guardrailsreviewResultTemp.finalOutput),
      output_parsed: guardrailsreviewResultTemp.finalOutput,
    };
    state.analysis_risks = guardrailsreviewResult.output_parsed.risks;

    const reportcomposerResultTemp = await runner.run(reportcomposer, [...conversationHistory]);
    conversationHistory.push(...reportcomposerResultTemp.newItems.map((item) => item.rawItem));
    if (!reportcomposerResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const reportcomposerResult = {
      output_text: JSON.stringify(reportcomposerResultTemp.finalOutput),
      output_parsed: reportcomposerResultTemp.finalOutput,
    };
    state.report_markdown = reportcomposerResult.output_parsed.markdown;
    state.report_top_five = reportcomposerResult.output_parsed.top_five;

    const summaronepagerResultTemp = await runner.run(summaronepager, [...conversationHistory]);
    conversationHistory.push(...summaronepagerResultTemp.newItems.map((item) => item.rawItem));
    if (!summaronepagerResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const summaronepagerResult = {
      output_text: JSON.stringify(summaronepagerResultTemp.finalOutput),
      output_parsed: summaronepagerResultTemp.finalOutput,
    };
    state.report_summary = summaronepagerResult.output_parsed.summary_md;

    const outreachdraftsResultTemp = await runner.run(outreachdrafts, [...conversationHistory]);
    conversationHistory.push(...outreachdraftsResultTemp.newItems.map((item) => item.rawItem));
    if (!outreachdraftsResultTemp.finalOutput) {
      throw new Error("Agent result is undefined");
    }

    const outreachdraftsResult = {
      output_text: JSON.stringify(outreachdraftsResultTemp.finalOutput),
      output_parsed: outreachdraftsResultTemp.finalOutput,
    };
    state.outreach_email = outreachdraftsResult.output_parsed.email;

    const endResult = {
      report: {
        title: state.research_company_snapshot,
        content: state.report_markdown,
        created_at: state.now_iso,
      },
      summary_one_pager: {
        headline: state.report_top_five,
        summary_content: state.report_summary,
        created_at: state.now_iso,
      },
      email: {
        to: "",
        subject: "",
        body: state.outreach_email,
        sent_at: "",
      },
    };

    return endResult;
  });
};

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8").trim();
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const run = async () => {
    const argInput = process.argv.slice(2).join(" ").trim();
    const input_as_text = argInput || (await readStdin());
    if (!input_as_text) {
      throw new Error("No input provided to workflow");
    }
    const result = await runWorkflow({ input_as_text });
    console.log(JSON.stringify(result, null, 2));
  };

  run().catch((error) => {
    console.error(error?.message || error);
    process.exit(1);
  });
}
