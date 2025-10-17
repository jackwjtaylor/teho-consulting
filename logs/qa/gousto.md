# Gousto Report QA Notes
**Date:** 7 Oct 2025  
**Reviewer:** Jack Taylor  

## Checks completed
- [x] Tone matches plain British English style.  
- [x] Figures labelled with assumptions where internal data is missing.  
- [x] Sources cited correctly (S1–S5).  
- [x] Executive and comprehensive reports align on key messages.  
- [x] Board snapshot numbers match comprehensive report.

## Findings
- Refund amount (£5–6m) and active customer estimate (250k) rely on assumptions; need confirmation once finance data is available.  
- Waste reduction estimate (1% → 0.7%) pulled from public claim; requires validation from latest internal reporting.  
- Courier partner list limited to Evri/Yodel; confirm other partners before outreach.  
- Extensive automation detail sourced from Medium post; consider backing up with additional source when available.

## Prompt tweak ideas
- Add optional field for “Known courier partners” in context schema to improve accuracy.  
- Encourage model to state when operational data is assumed (template now doing so but worth testing).  
- Add reminder in prompt to suggest data required for follow-up workshop (e.g., refund totals, waste data).

## Actions
- [ ] Update `context.json` schema to include `courier_partners`.  
- [ ] Once internal numbers arrive, refresh ROI figures and mark QA checklist complete.  
- [ ] Log these prompt tweaks in backlog for next prompt revision.

## Changes
- 7 Oct 2025 – JT: Logged assumption gaps (refunds, waste) and added courier partner note; prompt schema updated accordingly.

## 17 Oct 2025 – QA Sign-off
- Ran full checklist: tone, sources, section order, ROI assumptions all reviewed.  
- Confirmed board snapshot and comprehensive report aligned; packaging assets generated via CLI.  
- Outstanding data gaps: actual refund totals and courier SLA metrics (called out in reports). Await finance update before refreshing figures.  
- Task: move refund/SLA data collection to backlog (no blocker for outreach).  
- Status: Approved for outreach.
