## Gousto AI Opportunity Report (Comprehensive Edition)
**Date:** 7 Oct 2025  
**Analyst:** Teho Consulting – Jack Taylor  
**Business:** Gousto (SCA Investments Limited)  
**Report depth:** Comprehensive (about 2,000 words)

---

### Executive Summary _(Confidence: Medium)_
- Gousto has grown strongly since 2012, now running two modern factories in Warrington and Clay Lake, serving the UK and Ireland with more than 100 weekly meal-kit choices and around 900 staff (Source 1, Source 3).  
- Reviews show consistent praise for recipe choice but regular frustration with late deliveries, missing items, or ingredients that fail to stay fresh—these issues drive refunds and risk repeat orders (Source 2).  
- Eight AI opportunities were identified. Three near-term actions—smarter demand planning, a live courier view, and a support assistant—could together protect or add roughly £13m a year. Additional ideas include vision-based quality checks, personal menu tips, and clearer sustainability reporting.  
- We advise kicking off with a short readiness session to agree shared metrics, cleaning the necessary data, piloting the support assistant, and building the courier dashboard with one delivery partner before scaling. Teho can support each step via teho.ai.

---

### Company & Process Overview _(Confidence: Medium)_
- **Business snapshot:** Gousto supplies meal kits on subscription and as one-off orders, sending pre-portioned ingredients and recipe cards to households nationwide. It remains privately owned with backing from investors such as BGF and Unilever Ventures (Source 1, Source 4).  
- **Operations today:**  
  - _Menu development:_ Food and nutrition teams create more than 100 rotating recipes weekly. Success depends on reading customer taste trends, spotting health focuses (for example the “Health Hub”), and understanding the cost impact of new dishes (Source 4).  
  - _Demand planning & buying:_ Procurement teams work with a network of suppliers. Forecast mistakes lead to waste or shortages, undermining Gousto’s <1% waste boast (Source 4).  
  - _Factory execution:_ Two main sites—Warrington (opened 2022) and Clay Lake—use a bespoke Factory API to link warehouse systems, lifts, and conveyors. In-house algorithms such as Auto Replenish, Auto Routing, and Pick Face Optimisation deliver 140% faster packing and 99.97% pick accuracy compared with earlier sites (Source 3, Source 5).  
  - _Delivery:_ Third-party couriers (Evri, Yodel and others) run the last mile. Public comments highlight inconsistent delivery windows, damaged packaging, and missing ingredients (Source 2).  
  - _Customer experience:_ A web and app platform manages menus, delivery slots, and support. Gousto has also launched new product lines (for example Health Hub recipes, premium add-ons) to defend loyalty (Source 4).  
- **Financial position:** Public sources state FY2024 revenue at about £312m (up 1% year-on-year) with record adjusted EBITDA of £42m, 55% gross margin, and positive free cash flow of £3m. For 2025, management is targeting 5–10% revenue growth and more profit gains (Source 4).  
- **Data posture:** Gousto controls rich order data, supplier feeds, and support transcripts. Courier data sits with partners and must be ingested. Waste and refund detail is not publicly shared.  
- **Strategic direction:** Expand Health Hub recipes by 150%, test next-day delivery, enter Ireland, and keep waste low while proving sustainability credentials (Source 4).

---

### Pain-Point Scan _(Confidence: Low)_
- **Deliveries:** Trustpilot reviews regularly mention late or missing boxes and food arriving warm. Customers often contact support for refunds, implying courier visibility is weak once orders leave the factory (Source 2).  
- **Freshness & waste:** Some customers receive ingredients close to expiry, hinting at forecasting slips, cold-chain breaks, or both (Source 2).  
- **Support load:** The default fix is to issue credits, which soothes the customer but fails to prevent repeat problems and keeps costs high (Source 2).  
- **Margin pressure:** Rising ingredient costs and energy prices make it vital to keep waste low and avoid ad-hoc refunds (Source 4).  
- **Data & tooling gaps:** Public information does not show live delivery dashboards, detailed waste reporting by ingredient, or automated root-cause analysis. These gaps need checking with internal teams.

---

### Opportunity Table _(Confidence: Medium)_

| Rank | Opportunity | Area helped | Plain-English approach | Impact (1–5) | Effort (1–5) | One-line reason |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Smarter demand planning | Forecasting & buying | Use richer forecasting and human review to order the right stock | 5 | 3 | Protects low waste targets and keeps recipes in stock. |
| 2 | Courier live view | Delivery | Combine courier feeds, predict delays, and trigger fixes | 5 | 4 | Tackles the biggest source of refunds and bad reviews (Source 2). |
| 3 | Support assistant | Customer care | AI tool drafts replies and suggests actions from order data | 4 | 2 | Speeds ticket handling and keeps tone consistent. |
| 4 | Ingredient quality cameras | Factory quality | Cameras spot bruised or missing ingredients before boxing | 4 | 3 | Reduces refunds linked to damaged goods. |
| 5 | Personal menu tips | Retention & growth | Recommend recipes based on taste, health signals, and history | 4 | 2 | Supports Health Hub push and drives repeat orders (Source 4). |
| 6 | Sustainability tracker | ESG & comms | Simple data model to report waste, packaging, and emissions | 3 | 2 | Provides proof for marketing and investors. |
| 7 | Supplier risk radar | Procurement | Monitor supplier data and news for early warning signs | 3 | 3 | Helps avoid last-minute shortages. |
| 8 | Offer testing engine | Commercial | Structured testing of pricing and bundles | 3 | 4 | Protects margin but needs careful change management.

Impact scores reflect the size of the prize; effort scores blend technical work, data access, and change effort. Lower scores mean easier wins.

---

### Top Five Opportunity Deep Dives _(Confidence: Low)_

#### 1. Smarter demand planning
- **Problem today:** Forecast slips cause waste or shortages, which then show up as freshness complaints, late substitutions, or lost sales (Source 2).  
- **Suggested approach:**  
  - Build improved forecasting models (for example gradient boosted trees or Prophet-style models) using order history, planned marketing, weather, holidays, and supplier lead times.  
  - Layer in reinforcement-style logic or simple decision rules to fine-tune top SKUs, while leaving room for human override.  
  - Present forecasts in an S&OP (sales and operations planning) view with confidence bands and clear exceptions.  
- **What is needed:** Clean order and cancellation data, waste logs by ingredient, supplier lead times, marketing calendar, weather feeds, AWS infrastructure already in place.  
- **Risks & controls:**  
  - New recipes lack history → use category-level priors and manual guardrails.  
  - Sudden demand spikes → run “what-if” scenarios before big campaigns.  
  - Data quality issues → establish weekly data hygiene checks.  
- **Money story:** If waste drops from 1% to 0.7% and stock-outs fall by 20%, Gousto could protect roughly £7–9m per year (assumes £312m revenue and 55% gross margin).  
- **Next research step:** Confirm actual waste percentage by ingredient family and understand current forecast accuracy.

#### 2. Courier live view
- **Problem today:** Customers only learn about delays after the slot has passed; support teams react rather than prevent issues, leading to refunds and poor reviews (Source 2).  
- **Suggested approach:**  
  - Ingest courier data (status scans, GPS pings) into a single stream.  
  - Predict arrival times using simple machine-learning models trained on route history, weather, day of week, and factory dispatch times.  
  - Surface a live dashboard for operations and send proactive SMS or in-app updates when risk is high.  
  - Build playbooks for reroutes, quick replacement boxes, or automatic credits where justified.  
- **What is needed:** Courier API access, production timestamps, customer comms platform integration, a small “control room” team to monitor alerts.  
- **Risks & controls:**  
  - Courier cooperation → negotiate data clauses in SLAs.  
  - Privacy concerns → minimise personal data, use order IDs.  
  - False alarms → tune thresholds with operations feedback.  
- **Money story:** Cutting goodwill credits by 30% could save about £5–6m a year (assumes credits currently equal 2% of revenue).  
- **Next research step:** Gather refund totals, current SLA terms, and existing delivery KPIs.

#### 3. Support assistant
- **Problem today:** Agents spend time pulling order details, writing responses, and issuing refunds. Knowledge is inconsistent across shifts.  
- **Suggested approach:**  
  - Build a retrieval-augmented large language model (LLM) assistant that reads knowledge base articles, policy documents, and anonymised transcripts.  
  - Present suggested replies and actions (replacement, credit, apology script) that the agent can approve or edit.  
  - Log responses to spot recurring issues and feed back into operations.  
- **What is needed:** Structured knowledge base, order management link (with redaction where needed), transcript samples for fine-tuning, secure environment (Azure OpenAI or similar).  
- **Risks & controls:**  
  - Incorrect advice → keep humans in the loop until accuracy is proven.  
  - Tone mismatches → craft a style guide and run spot checks.  
  - Data security → strip personal data before feeding the model.  
- **Money story:** 30% quicker handling and 10% more self-service could save roughly £1.8m each year (assumes support cost at 3% of revenue).  
- **Next research step:** Confirm ticket volumes, handle times, existing tools, and top contact reasons.

#### 4. Ingredient quality cameras
- **Problem today:** Manual checks miss damaged produce or incomplete boxes, leading to refunds and unhappy customers (Source 2).  
- **Suggested approach:**  
  - Install affordable cameras on critical packing points.  
  - Train vision models (e.g. YOLOv8) to spot bruises, leaks, or missing components.  
  - Trigger re-check or removal via the Factory API when a fault is spotted.  
- **What is needed:** Sample footage with labelled good vs bad items, edge hardware (NVIDIA Jetson or similar), maintenance plan, integration with existing PLC controls.  
- **Risks & controls:**  
  - False positives slowing throughput → run pilots on specific lines, adjust thresholds.  
  - Lighting and camera placement challenges → work with site engineers on set-up.  
  - Staff adoption → involve quality teams early, provide simple dashboards.  
- **Money story:** Reducing quality-related refunds by 25% could protect £3–4m annually and improve customer retention.  
- **Next research step:** Gather current defect rates, refund categories, and maintenance budgets.

#### 5. Personal menu tips
- **Problem today:** Customers may struggle to find the best recipes for their tastes or health needs, reducing repeat orders and the value of the expanded menu (Source 4).  
- **Suggested approach:**  
  - Build customer taste profiles using past choices, ratings, dietary filters, and responses to Health Hub content.  
  - Recommend weekly picks and bundles and support them with simple LLM-generated messages that highlight why they suit the customer.  
  - Test variations via the existing experimentation platform before broad roll-out.  
- **What is needed:** Consent for personalised marketing, feature store to combine signals, collaboration with nutritionists to ensure compliant claims.  
- **Risks & controls:**  
  - Overfitting to past choices → enforce diversity rules, surface “try something new” options.  
  - Compliance with health claims → involve nutrition team and legal sign-off.  
  - Customer fatigue → offer opt-out and control frequency.  
- **Money story:** Adding 0.3 orders per customer per quarter at £30 per order could add around £9m (assumes 250k active customers).  
- **Next research step:** Confirm active subscriber count, AOV, and current personalisation tools.

---

### Competitor & Industry View _(Confidence: Low)_
- **HelloFresh UK:** Open press around personalisation, automation, and sustainability. Likely investing in similar forecasting and vision systems, so Gousto must match or surpass reliability claims (Source 4).  
- **Mindful Chef:** Smaller scale but strong on health messaging. Focus appears to be on curated menus and customer storytelling; limited evidence of heavy automation investment.  
- **Oddbox and Allplants:** Compete on sustainability and plant-based credentials. Both talk about using data to cut waste but less about live operations.  
- **Marley Spoon:** International rival offering premium and diet-specific boxes. Financial filings mention automation, yet UK-specific details are scarce.  
- **Gap for Gousto:** None of the above loudly offers live courier tracking or AI-backed support. Owning the “reliable delivery” story with proof could set Gousto apart.

---

### Recommendations & Timeline _(Confidence: Low)_
- **0–3 months:**  
  - Hold an AI readiness workshop with Teho (or internal equivalent) to agree success metrics, data owners, and governance.  
  - Audit data quality for orders, waste, courier feeds, and support transcripts.  
  - Pilot the support assistant with a small group of agents; capture handle time, satisfaction, and error metrics.  
  - Begin negotiating courier data access and align on privacy standards.
- **3–9 months:**  
  - Roll out the demand planning pilot on the top 50 high-cost ingredients with manual oversight.  
  - Stand up the courier live view with one courier partner, issuing proactive alerts and measuring refund trends.  
  - Launch personal menu experiments focused on Health Hub recipes to support the 150% growth target.  
  - Collect footage and start a limited ingredient vision pilot on the highest-risk lines.
- **9–18 months:**  
  - Scale forecasting and courier dashboards across all categories and partners, backed by an MLOps process (model monitoring, retraining, rollback plans).  
  - Extend the support assistant to procurement (supplier briefings) and operations (shift handovers).  
  - Deploy vision checks across both factories, building a maintenance schedule and ROI tracker.  
  - Publish a quarterly reliability and sustainability update (delivery success, waste, carbon) to strengthen brand trust.  
  - Formalise AI governance: data privacy review boards, change management plans, and regular training for staff using AI tools.

Teho Consulting can guide each stage—book a session through `teho.ai` or use the above roadmap to move ahead internally.

---

### Appendix _(Confidence: Medium)_
- **Source list:**  
  - Source 1 – [Gousto - Wikipedia](https://en.wikipedia.org/wiki/Gousto) (retrieved 7 Oct 2025)  
  - Source 2 – [Gousto Reviews | Trustpilot](https://uk.trustpilot.com/review/gousto.co.uk) (retrieved 7 Oct 2025)  
  - Source 3 – [Inside Gousto’s Factory API: Simplifying Complexity in a Data-Driven Kitchen](https://medium.com/gousto-engineering-techbrunch/inside-goustos-factory-api-simplifying-complexity-in-a-data-driven-kitchen-ad34901086de) (retrieved 7 Oct 2025)  
  - Source 4 – [How Does Gousto Company Work?](https://canvasbusinessmodel.com/blogs/how-it-works/gousto-how-it-works) (retrieved 7 Oct 2025)  
  - Source 5 – [Tech and AI Help Gousto Return to Profitability](https://www.hulkapps.com/blogs/ecommerce-hub/tech-and-ai-help-gousto-return-to-profitability) (retrieved 7 Oct 2025)
- **Data notes:** Revenue, margin, refund totals, waste by ingredient, and active customer counts come from public estimates and need confirmation. Courier SLAs and ticket metrics are not public.  
- **Glossary:**  
  - _Factory API:_ Gousto’s internal software layer that coordinates warehouse systems (Source 3).  
  - _LLM:_ Large language model, the type of AI used in the support assistant idea.  
  - _S&OP:_ Sales and operations planning meeting to balance demand and supply.  
- **Assumptions:** Revenue £312m, gross margin 55%, support cost 3% of revenue, active customers 250k, credits equal 2% of revenue.  
- **Next research steps:** Confirm refund and waste figures, gather courier SLA performance, validate competitor AI claims, and review health claim compliance process.
