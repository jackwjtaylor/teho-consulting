## Gousto AI Opportunity Report (Executive Edition)
**Date:** 7 Oct 2025  
**Analyst:** Teho Consulting – Jack Taylor  
**Business:** Gousto (SCA Investments Limited)  
**Report depth:** Executive (about 1,000 words)

---

### Executive Summary _(Confidence: Medium)_
- Gousto now serves the UK and Ireland with more than 100 weekly menus and around 900 staff, backed by two highly automated factories (Source 1, Source 3).  
- Customers praise the recipes but often complain about late deliveries, missing ingredients, or food that does not stay fresh—issues that lead to refunds and churn (Source 2).  
- We found eight AI ideas; the top three could protect or add roughly £13m a year by tightening deliveries, sharpening ingredient planning, and speeding customer care.  
- Suggested next steps: tidy the data needed for demand forecasting and courier tracking, trial the support assistant with a small team, and agree a working group to steer the roll-out. Teho can help through a short “readiness” session booked via teho.ai.

---

### Company & Process Overview _(Confidence: Medium)_
- **What Gousto sells:** Subscription and one-off meal kits with pre-portioned ingredients delivered nationwide (Source 1).  
- **How work flows today:**  
  - _Menu design:_ Food teams build 100+ rotating recipes and need quick insight into trends, costs, and stock levels.  
  - _Buying & planning:_ Ingredients are sourced from trusted suppliers; wrong forecasts create waste or shortages (Source 4).  
  - _Factory operations:_ Sites in Warrington and Clay Lake pick, pack, and route boxes; in-house Factory API tools keep conveyors and lifts in sync (Source 3).  
  - _Delivery:_ Couriers such as Evri and Yodel handle the last mile; current tracking is patchy.  
  - _Digital touchpoints:_ Customers order via app or web, choose recipes, manage deliveries, and contact support.  
- **Constraints to note:** Perishable produce, cold-chain needs, and food safety rules mean mistakes are costly. Data on courier performance sits outside Gousto and must be pulled in.

---

### Pain-Point Scan _(Confidence: Low)_
- **Deliveries:** Reviews show frequent late or missing boxes, pointing to weak visibility once orders leave the factory (Source 2).  
- **Freshness:** Some customers receive meat or veg close to expiry, suggesting gaps in forecasting or temperature control (Source 2).  
- **Customer effort:** Support teams mainly issue credits after the fact rather than prevent issues, increasing cost and frustration (Source 2).  
- **Data gaps:** Public info does not show live dashboards for delivery performance or waste by ingredient—worth confirming with leadership.

---

### Opportunity Table _(Confidence: Medium)_

| Rank | Opportunity | Area helped | Approach | Impact (1–5) | Effort (1–5) | One-line reason |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Smarter demand planning | Buying & forecasting | Advanced forecasting models with simple tuning | 5 | 3 | Cuts waste and stock-outs across 200+ recipes. |
| 2 | Courier live view | Delivery | Merge courier feeds, predict delays early | 5 | 4 | Tackles main source of refunds and poor reviews (Source 2). |
| 3 | Support assistant | Customer care | AI helper pulls order data and drafts replies | 4 | 2 | Speeds responses on missing items and keeps tone consistent. |
| 4 | Ingredient quality cameras | Factory QA | Edge cameras flag damaged produce | 4 | 3 | Stops poor ingredients leaving the line. |
| 5 | Personal menu tips | Growth & loyalty | Recommend recipes with taste and health signals | 4 | 2 | Encourages extra orders and supports the “Health Hub” plan (Source 4). |
| 6 | Sustainability scorecard | ESG reporting | Simple data model for waste and packaging | 3 | 2 | Gives proof for eco claims and investor updates. |
| 7 | Supplier early-warning | Procurement | Track supplier data for risk signals | 3 | 3 | Helps keep factories stocked during shocks. |
| 8 | Offer testing engine | Commercial | Pricing and promo tests driven by data | 3 | 4 | Protects margin but needs careful set-up to avoid churn.

---

### Top Five Opportunity Deep Dives _(Confidence: Low)_

1. **Smarter demand planning**  
   - _Problem:_ Forecast slips drive waste and shortages, feeding freshness complaints (Source 2).  
   - _Fix:_ Use richer forecasting (for example gradient boosted models) combining orders, weather, promotions, and events. Add human review for new recipes.  
   - _Needs:_ Clean order history, supplier lead times, waste logs, weather feeds; hosted on existing AWS stack.  
   - _Risks:_ New recipes lack history; extreme events break models. Mitigate with guardrails and manual overrides.  
   - _Value:_ Dropping waste from 1% to 0.7% and cutting stock-outs by 20% could save about £7–9m a year (assumes £312m revenue, 55% gross margin).  
   - _Next research step:_ Confirm current waste by ingredient.

2. **Courier live view**  
   - _Problem:_ Customers do not know where their box is, and refunds stack up when couriers miss windows (Source 2).  
   - _Fix:_ Pull courier feeds into one dashboard, predict delays with simple machine-learning models, trigger texts or reroutes.  
   - _Needs:_ Courier APIs, production timestamps, customer contact preferences, small control room team.  
   - _Risks:_ Data access from partners, privacy concerns. Mitigate with new SLAs and data minimisation.  
   - _Value:_ Cutting goodwill credits by 30% could protect roughly £5–6m per year (assumes current credits equal 2% of revenue).  
   - _Next research step:_ Gather actual refund totals and courier SLA terms.

3. **Support assistant**  
   - _Problem:_ Agents spend time piecing together orders and writing replies; issues repeat.  
   - _Fix:_ Retrieval-augmented large language model (LLM) that reads knowledge base articles and order history, drafts replies, and suggests actions.  
   - _Needs:_ Clean knowledge base, transcript samples, secure link to order data, pilot group in support.  
   - _Risks:_ Wrong advice, tone missteps, data privacy. Use human approval during pilot and clear guardrails.  
   - _Value:_ 30% faster handling and 10% self-serve deflection could save around £1.8m a year (assumes support cost of 3% revenue).  
   - _Next research step:_ Confirm handle times and ticket volumes.

4. **Ingredient quality cameras**  
   - _Problem:_ Damaged or short-dated items slip through manual checks (Source 2).  
   - _Fix:_ Install lightweight cameras and vision models on key lines to flag bruising, tears, or missing items.  
   - _Needs:_ Sample images, edge devices (e.g. NVIDIA Jetson), integration with Factory API for rejection logic.  
   - _Risks:_ False positives slowing the line, hardware upkeep. Start small, monitor performance, schedule maintenance.  
   - _Value:_ 25% fewer quality-related refunds could save about £3–4m and lift Net Promoter Score.  
   - _Next research step:_ Gather current refund causes by category.

5. **Personal menu tips**  
   - _Problem:_ Customers may not see recipes that match their tastes or health goals, limiting repeat orders (Source 4).  
   - _Fix:_ Blend purchase history, health preferences, and upcoming menu data to suggest weekly picks, supported by a gentle LLM copy layer.  
   - _Needs:_ Consent for personalisation, feature store, experimentation rig for A/B tests.  
   - _Risks:_ Repeating the same meals, breaching dietary promises. Use diversity rules and nutritionist review.  
   - _Value:_ Adding 0.3 orders per customer each quarter at £30 per order could add roughly £9m (assumes 250k active customers).  
   - _Next research step:_ Confirm active customer count and average order value.

---

### Competitor & Industry View _(Confidence: Low)_
- **HelloFresh UK:** Talks openly about personalisation and fulfilment automation; likely investing in similar forecasting tools (Source 4).  
- **Mindful Chef:** Smaller scale but leans into health promises—little proof of live delivery tracking yet.  
- **Oddbox / Allplants:** Focus on sustainability stories; data use centred on waste reduction and messaging.  
- **Gap for Gousto:** No rival is bragging about full courier transparency or AI-backed support, giving Gousto space to lead on reliability.

---

### Recommendations & Timeline _(Confidence: Low)_
- **0–3 months:**  
  - Run an AI readiness workshop with Teho to agree targets and data owners.  
  - Audit data quality for orders, waste, and courier feeds.  
  - Pilot the support assistant with a small team and gather feedback.
- **3–9 months:**  
  - Launch the demand planning pilot on top ingredients with human oversight.  
  - Build the courier live view with one partner, expanding once stable.  
  - Start menu personalisation experiments for Health Hub recipes.
- **9–18 months:**  
  - Scale the forecasting and courier tools across all products and partners.  
  - Roll out vision checks to more lines.  
  - Publish a simple reliability and sustainability report for customers and investors.

Book a short session at `teho.ai` to shape the plan, or use the insights above to kick off internally.

---

### Appendix _(Confidence: Medium)_
- **Source list:**  
  - Source 1 – [Gousto - Wikipedia](https://en.wikipedia.org/wiki/Gousto) (retrieved 7 Oct 2025)  
  - Source 2 – [Gousto Reviews | Trustpilot](https://uk.trustpilot.com/review/gousto.co.uk) (retrieved 7 Oct 2025)  
  - Source 3 – [Inside Gousto’s Factory API: Simplifying Complexity in a Data-Driven Kitchen](https://medium.com/gousto-engineering-techbrunch/inside-goustos-factory-api-simplifying-complexity-in-a-data-driven-kitchen-ad34901086de) (retrieved 7 Oct 2025)  
  - Source 4 – [How Does Gousto Company Work?](https://canvasbusinessmodel.com/blogs/how-it-works/gousto-how-it-works) (retrieved 7 Oct 2025)
- **Data notes:** Revenue, margin, refund cost, and customer count figures need confirmation from internal finance. Courier SLA data is not public.  
- **Glossary:**  
  - _Factory API:_ Gousto’s internal software layer that links warehouse systems (Source 3).  
  - _LLM:_ Large language model, the type of AI used in the support assistant idea.  
- **Assumptions:** Revenue assumed at £312m, gross margin 55%, support cost 3% of revenue, active customers 250k.  
- **Next research steps:** Collect up-to-date refund totals, courier SLA metrics, waste by ingredient, and proven competitor AI moves.
