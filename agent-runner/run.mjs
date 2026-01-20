import { webSearchTool, Agent, Runner, withTrace } from "@openai/agents";
import { z } from "zod";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function loadEnvFile(filePath) {
  if (process.env.OPENAI_API_KEY) return;
  if (!fs.existsSync(filePath)) return;
  const content = fs.readFileSync(filePath, "utf-8");
  for (const rawLine of content.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#")) continue;
    const eqIndex = line.indexOf("=");
    if (eqIndex === -1) continue;
    const key = line.slice(0, eqIndex).trim();
    let value = line.slice(eqIndex + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    if (!(key in process.env)) {
      process.env[key] = value;
    }
  }
}

loadEnvFile(path.resolve(__dirname, "..", ".env"));

function parseArgs(argv) {
  const parsed = {
    company: "",
    domain: "",
    context: "",
    contextFile: "",
    outFile: "",
    activityBundle: "",
  };

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--company" || arg === "-c") {
      parsed.company = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--domain" || arg === "-d") {
      parsed.domain = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--context" || arg === "-x") {
      parsed.context = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--context-file") {
      parsed.contextFile = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--out" || arg === "-o") {
      parsed.outFile = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (arg === "--activity-bundle") {
      parsed.activityBundle = argv[i + 1] || "";
      i += 1;
      continue;
    }
    if (!arg.startsWith("-") && !parsed.company) {
      parsed.company = arg;
    }
  }

  return parsed;
}

function loadContextText(context, contextFile) {
  if (contextFile) {
    return fs.readFileSync(contextFile, "utf-8");
  }
  return context || "";
}

async function loadActivityBundle(bundlePath) {
  if (!bundlePath) return null;
  if (bundlePath.startsWith("http://") || bundlePath.startsWith("https://")) {
    const response = await fetch(bundlePath);
    if (!response.ok) {
      throw new Error(`Failed to fetch activity bundle (${response.status})`);
    }
    return response.json();
  }
  if (!fs.existsSync(bundlePath)) {
    throw new Error(`Activity bundle not found: ${bundlePath}`);
  }
  const raw = fs.readFileSync(bundlePath, "utf-8");
  return JSON.parse(raw);
}

function buildInputText(data) {
  return `Input JSON:\n${JSON.stringify(data, null, 2)}`;
}

async function runAgentJson(runner, agent, input) {
  const result = await runner.run(agent, [
    {
      role: "user",
      content: [{ type: "input_text", text: buildInputText(input) }],
    },
  ]);
  if (!result.finalOutput) {
    throw new Error(`Agent ${agent.name} returned no output`);
  }
  return result.finalOutput;
}

async function runStep(label, fn) {
  console.error(`[agent-runner] ${label}...`);
  const result = await fn();
  console.error(`[agent-runner] ${label} done`);
  return result;
}

const DEFAULT_MODEL = process.env.TEHO_AGENT_MODEL || "gpt-5";
const FINANCIAL_MODEL = process.env.TEHO_AGENT_FINANCIAL_MODEL || "gpt-5.1";

function buildModelSettings(model, effort) {
  const settings = { store: true };
  if (model.startsWith("gpt-5")) {
    settings.reasoning = { effort, summary: "auto" };
  }
  return settings;
}

const webSearchPreview = webSearchTool({
  searchContextSize: "medium",
  userLocation: { type: "approximate" },
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
    })
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
        z.object({
          capability: z.string(),
          evidence_url: z.string(),
        })
      ),
    })
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
          })
        ),
      })
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
    })
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
      })
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
    })
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
  instructions: `You receive JSON input with:\n{ "company_name": "...", "domain": "..." }\n\nNormalize the company name for downstream use and guess the primary website if missing.\nReturn JSON only in this shape:\n{ "profile": { "company_name_canonical": "...", "domain_guess": "..." } }`,
  model: DEFAULT_MODEL,
  outputType: CompanyinputSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "low"),
});

const companyprofilefetch = new Agent({
  name: "CompanyProfileFetch",
  instructions: `You receive JSON input with:\n{ "company_name_canonical": "...", "domain_guess": "...", "additional_context": "..." }\n\nTask: Build a factual company snapshot from public pages (homepage, About, Careers, Press).\nSummarise only what is on-page. No speculation.\nReturn JSON only in this shape:\n{\n  "snapshot": {\n    "legal_name": "...",\n    "brands": ["..."],\n    "products": ["..."],\n    "regions": ["..."],\n    "customers_or_segments": ["..."],\n    "leadership": [{"name":"...","title":"..."}],\n    "tech_signals": ["..."],\n    "sources": [{"url":"...","title":"..."}]\n  }\n}`,
  model: DEFAULT_MODEL,
  tools: [webSearchPreview],
  outputType: CompanyprofilefetchSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "medium"),
});

const newsscan = new Agent({
  name: "NewsScan",
  instructions: `You receive JSON input with:\n{ "company_name_canonical": "...", "domain_guess": "..." }\n\nFind 8-15 material events (product launches, funding, partnerships, leadership changes, layoffs, expansions, regulatory items) about the company in the last 18 months.\nReturn JSON only under "items":\n{ "items": [{"title":"...", "date":"YYYY-MM-DD", "summary":"...", "source_url":"..."}] }`,
  model: DEFAULT_MODEL,
  tools: [webSearchPreview],
  outputType: NewsscanSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "medium"),
});

const scalesignals = new Agent({
  name: "ScaleSignals",
  instructions: `You receive JSON input with:\n{ "company_name_canonical": "...", "domain_guess": "..." }\n\nExtract scale signals (headcount, revenue, growth) from public information.\nAlways mark uncertain values as "(estimate)" and include only public data.\nReturn JSON only in this shape:\n{\n  "scale": {\n    "headcount_range": "...",\n    "revenue_range": "...",\n    "growth_direction": "growing|flat|declining",\n    "notes": ["..."],\n    "sources": [{"url":"...","title":"..."}]\n  }\n}`,
  model: DEFAULT_MODEL,
  tools: [webSearchPreview],
  outputType: ScalesignalsSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "medium"),
});

const peerset = new Agent({
  name: "PeerSet",
  instructions: `You receive JSON input with:\n{ "company_name_canonical": "...", "domain_guess": "..." }\n\nIdentify 5-10 peer companies in the same market segment.\nReturn JSON only under "peers" with public, verifiable examples:\n{ "peers": [{"name":"...","url":"...","ai_signals":[{"capability":"...","evidence_url":"..."}]}] }`,
  model: DEFAULT_MODEL,
  tools: [webSearchPreview],
  outputType: PeersetSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "medium"),
});

const processmapping = new Agent({
  name: "ProcessMapping",
  instructions: `You receive JSON input with:\n{ "company_profile": {...}, "additional_context": "...", "internal_activity_evidence": {...} }\n\nConstruct a lightweight value chain:\nAcquire -> Convert -> Fulfil -> Serve/Retain -> Back-office.\nFor each stage, list 2-4 subprocesses and measurable pain points.\nIf internal_activity_evidence is provided, anchor subprocesses and pain points to observed work patterns.\nReturn JSON only in this shape:\n{ "process_map": { "stages": [{"name":"...","subprocesses":[{"name":"...","pain_points":["..."]}]}] } }`,
  model: DEFAULT_MODEL,
  outputType: ProcessmappingSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "medium"),
});

const opportunitygen = new Agent({
  name: "OpportunityGen",
  instructions: `You receive JSON input with:\n{\n  "company_profile": {...},\n  "process_map": {...},\n  "news_items": [...],\n  "peers": [...],\n  "scale_signals": {...},\n  "financial_signals": {...},\n  "additional_context": "...",\n  "internal_activity_evidence": {...}\n}\n\nGenerate AI/automation opportunities specific to this company.\nRules:\n- Every opportunity must map directly to a pain point from process_map.\n- Use terminology from company_profile and process_map.\n- If internal_activity_evidence is provided, prioritise opportunities that address observed time drains or low-value work.\n- No generic cross-industry assumptions.\nReturn JSON only in this shape:\n{ "opportunities": [{\n  "title":"...", "category":"...", "mechanism":"...", "impact_band":"H|M|L", "effort_band":"H|M|L",\n  "ROI_rationale":["..."], "data_prereqs":["..."], "integrations":["..."], "guardrails":["..."],\n  "example_metrics":["..."], "value_range":"...", "kpi_uplift":"..."\n}] }`,
  model: DEFAULT_MODEL,
  outputType: OpportunitygenSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "high"),
});

const prioritiser = new Agent({
  name: "Prioritiser",
  instructions: `You receive JSON input with:\n{ "opportunities": [...] }\n\nRank opportunities using ICE and return JSON only in this shape:\n{ "prioritised": {\n  "ranked": [{"title":"...","category":"...","impact":1,"confidence":1,"effort":1,"score":1,"why":"..."}],\n  "quadrants": { "quick_wins":[], "big_bets":[], "fill_ins":[], "postpone":[] }\n} }`,
  model: DEFAULT_MODEL,
  outputType: PrioritiserSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "high"),
});

const guardrailsreview = new Agent({
  name: "GuardrailsReview",
  instructions: `You receive JSON input with:\n{ "opportunities": [...] }\n\nCheck each opportunity for privacy, regulatory, residency, and safety risks.\nReturn JSON only in this shape:\n{ "risks": [{"opportunity_title":"...","issues":["..."],"mitigations":["..."]}] }`,
  model: DEFAULT_MODEL,
  outputType: GuardrailsreviewSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "medium"),
});

const reportcomposer = new Agent({
  name: "ReportComposer",
  instructions: `You receive JSON input with:\n{\n  "company_name": "...",\n  "now_iso": "YYYY-MM-DD",\n  "company_profile": {...},\n  "news_items": [...],\n  "scale_signals": {...},\n  "financial_signals": {...},\n  "peers": [...],\n  "process_map": {...},\n  "opportunities": [...],\n  "prioritised": {...},\n  "guardrails": [...],\n  "additional_context": "...",\n  "internal_activity_evidence": {...}\n}\n\nProduce a consulting-grade AI Opportunities Report tailored to the company.\nIf internal_activity_evidence is provided, integrate observed work patterns and quantify where possible.\nReturn JSON only in this shape:\n{ "markdown": "<full report markdown>", "top_five": ["...", "...", "...", "...", "..."] }\n\nIn the markdown, use these sections in order:\n1. TITLE\n2. EXECUTIVE SUMMARY\n3. COMPANY SNAPSHOT\n4. FINANCIAL SIGNALS\n5. RECENT DEVELOPMENTS\n6. MARKET & COMPETITOR CONTEXT\n7. PROBLEM & PAIN-POINT MAP\n8. OPPORTUNITY MAP\n9. TOP 5 OPPORTUNITIES - DEEP DIVES\n10. VALUE SUMMARY TABLE\n11. PRIORITISED BACKLOG (ICE)\n12. 90-DAY PILOT PLAN\n13. RISKS & MITIGATIONS\n14. APPENDIX\n\nTitle format: # {Company Name} - AI Automation Opportunities ({now_iso})\nAvoid hallucinations. Omit empty sections gracefully.`,
  model: DEFAULT_MODEL,
  outputType: ReportcomposerSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "high"),
});

const summaronepager = new Agent({
  name: "SummarOnePager",
  instructions: `You receive JSON input with:\n{\n  "company_profile": {...},\n  "news_items": [...],\n  "opportunities": [...],\n  "prioritised": {...},\n  "scale_signals": {...},\n  "financial_signals": {...},\n  "internal_activity_evidence": {...}\n}\n\nProduce a concise 1-page executive summary.\nIf internal_activity_evidence is provided, highlight observed time allocation and friction signals.\nReturn JSON only in this shape:\n{ "summary_md": "<markdown>" }\n\nSections:\n1. Company Snapshot\n2. Top 3 Opportunities\n3. Why Now\n4. 90-Day Pilot Overview\n5. KPIs to Track`,
  model: DEFAULT_MODEL,
  outputType: SummaronepagerSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "medium"),
});

const outreachdrafts = new Agent({
  name: "OutreachDrafts",
  instructions: `You receive JSON input with:\n{ "company_name": "...", "top_five": ["..."] }\n\nWrite a short, personalised email to a senior leader.\nInclude placeholders:\n- [SNAPSHOT_LINK]\n- [FULL_REPORT_PREVIEW_LINK]\n- [CALENDLY_LINK]\n\nReturn JSON only in this shape:\n{ "email": "<full email>" }`,
  model: DEFAULT_MODEL,
  outputType: OutreachdraftsSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "medium"),
});

const initialiser = new Agent({
  name: "Initialiser",
  instructions: `Return JSON with the current date in ISO format:\n{ "now_iso": "YYYY-MM-DD" }`,
  model: DEFAULT_MODEL,
  outputType: InitialiserSchema,
  modelSettings: buildModelSettings(DEFAULT_MODEL, "low"),
});

const financialsignals = new Agent({
  name: "FinancialSignals",
  instructions: `You receive JSON input with:\n{ "company_name_canonical": "...", "domain_guess": "..." }\n\nExtract high-quality financial signals from public sources only.\nIf unavailable, use "Not disclosed" and explain in notes.\nReturn JSON only in this shape:\n{\n  "financials": {\n    "revenue": "...",\n    "revenue_growth_rate": "...",\n    "profitability": "...",\n    "margins": "...",\n    "funding_or_investors": ["..."],\n    "balance_sheet_signals": ["..."],\n    "unit_economics": ["..."],\n    "notes": ["..."],\n    "sources": [{"url":"...","title":"..."}]\n  }\n}`,
  model: FINANCIAL_MODEL,
  tools: [webSearchPreview],
  outputType: FinancialsignalsSchema,
  modelSettings: buildModelSettings(FINANCIAL_MODEL, "high"),
});

async function runWorkflow(workflow) {
  return await withTrace("AI Automation Opportunities Report", async () => {
    const runner = new Runner({
      traceMetadata: {
        __trace_source__: "agent-sdk",
      },
    });
    const activityEvidence = workflow.activity_bundle || null;

    const now = await runStep("Initialiser", () =>
      runAgentJson(runner, initialiser, {})
    );

    const companyProfile = await runStep("CompanyInput", () =>
      runAgentJson(runner, companyinput, {
        company_name: workflow.company_name,
        domain: workflow.domain || "",
      })
    );

    const canonicalName = companyProfile.profile.company_name_canonical;
    const domainGuess = companyProfile.profile.domain_guess;

    const profileSnapshot = await runStep("CompanyProfileFetch", () =>
      runAgentJson(runner, companyprofilefetch, {
        company_name_canonical: canonicalName,
        domain_guess: domainGuess,
        additional_context: workflow.additional_context || "",
      })
    );

    const news = await runStep("NewsScan", () =>
      runAgentJson(runner, newsscan, {
        company_name_canonical: canonicalName,
        domain_guess: domainGuess,
      })
    );

    const financials = await runStep("FinancialSignals", () =>
      runAgentJson(runner, financialsignals, {
        company_name_canonical: canonicalName,
        domain_guess: domainGuess,
      })
    );

    const scale = await runStep("ScaleSignals", () =>
      runAgentJson(runner, scalesignals, {
        company_name_canonical: canonicalName,
        domain_guess: domainGuess,
      })
    );

    const peers = await runStep("PeerSet", () =>
      runAgentJson(runner, peerset, {
        company_name_canonical: canonicalName,
        domain_guess: domainGuess,
      })
    );

    const processMap = await runStep("ProcessMapping", () =>
      runAgentJson(runner, processmapping, {
        company_profile: profileSnapshot.snapshot,
        additional_context: workflow.additional_context || "",
        internal_activity_evidence: activityEvidence,
      })
    );

    const opportunities = await runStep("OpportunityGen", () =>
      runAgentJson(runner, opportunitygen, {
        company_profile: profileSnapshot.snapshot,
        process_map: processMap.process_map,
        news_items: news.items,
        peers: peers.peers,
        scale_signals: scale.scale,
        financial_signals: financials.financials,
        additional_context: workflow.additional_context || "",
        internal_activity_evidence: activityEvidence,
      })
    );

    const prioritised = await runStep("Prioritiser", () =>
      runAgentJson(runner, prioritiser, {
        opportunities: opportunities.opportunities,
      })
    );

    const guardrails = await runStep("GuardrailsReview", () =>
      runAgentJson(runner, guardrailsreview, {
        opportunities: opportunities.opportunities,
      })
    );

    const report = await runStep("ReportComposer", () =>
      runAgentJson(runner, reportcomposer, {
        company_name: canonicalName,
        now_iso: now.now_iso,
        company_profile: profileSnapshot.snapshot,
        news_items: news.items,
        scale_signals: scale.scale,
        financial_signals: financials.financials,
        peers: peers.peers,
        process_map: processMap.process_map,
        opportunities: opportunities.opportunities,
        prioritised: prioritised.prioritised,
        guardrails: guardrails.risks,
        additional_context: workflow.additional_context || "",
        internal_activity_evidence: activityEvidence,
      })
    );

    const summary = await runStep("SummarOnePager", () =>
      runAgentJson(runner, summaronepager, {
        company_profile: profileSnapshot.snapshot,
        news_items: news.items,
        opportunities: opportunities.opportunities,
        prioritised: prioritised.prioritised,
        scale_signals: scale.scale,
        financial_signals: financials.financials,
        internal_activity_evidence: activityEvidence,
      })
    );

    const outreach = await runStep("OutreachDrafts", () =>
      runAgentJson(runner, outreachdrafts, {
        company_name: canonicalName,
        top_five: report.top_five,
      })
    );

    return {
      report: {
        title: `${canonicalName} - AI Automation Opportunities (${now.now_iso})`,
        content: report.markdown,
        created_at: now.now_iso,
      },
      summary_one_pager: {
        headline: report.top_five,
        summary_content: summary.summary_md,
        created_at: now.now_iso,
      },
      email: {
        to: "",
        subject: "",
        body: outreach.email,
        sent_at: "",
      },
    };
  });
}

async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error("OPENAI_API_KEY is not set. Add it to .env or export it.");
    process.exit(1);
  }

  const args = parseArgs(process.argv.slice(2));
  if (!args.company) {
    console.error("Usage: node run.mjs --company \"Company Name\" [--domain example.com] [--context \"...\"] [--context-file path] [--activity-bundle path_or_url] [--out output.json]");
    process.exit(1);
  }

  const contextText = loadContextText(args.context, args.contextFile);
  const activityBundle = await loadActivityBundle(args.activityBundle);

  const result = await runWorkflow({
    company_name: args.company,
    domain: args.domain,
    additional_context: contextText,
    activity_bundle: activityBundle,
  });

  const outputText = JSON.stringify(result, null, 2);
  if (args.outFile) {
    fs.writeFileSync(args.outFile, outputText, "utf-8");
  } else {
    console.log(outputText);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
