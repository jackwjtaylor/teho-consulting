# Report QA Checklist

Use this checklist before any report leaves draft. Mark each item and capture notes in the QA log (`logs/qa/{company}.md`).

## 1. Facts & Sources

- [ ] Executive summary facts match the body of the report.  
- [ ] Revenue, headcount, and other figures include source IDs or clear assumption labels.  
- [ ] No unsupported claims (every factual sentence has `(Source #)` or “Data gap” note).  
- [ ] Competitor descriptions align with cited sources.

## 2. Tone & Structure

- [ ] Plain British English, no jargon or consultant-speak.  
- [ ] Section order matches prompt specification.  
- [ ] Each section carries a confidence label (High/Medium/Low).  
- [ ] Opportunities table sorted by impact/effort logic.

## 3. ROI & Assumptions

- [ ] Monetary ranges state basis (e.g. revenue band, customer count).  
- [ ] “Next research step” included wherever data is missing.  
- [ ] No hard numbers without context on source/assumption.

## 4. Outreach Readiness

- [ ] Primary contact and email present (or flagged for follow-up).  
- [ ] Board snapshot metrics match the comprehensive report.  
- [ ] CTA references teho.ai and Calendly (where applicable).

## 5. Packaging Prep

- [ ] Snapshot ready for PDF export (headings, bullets, ~1 page).  
- [ ] Sources list links resolve (spot check).  
- [ ] Research gaps noted in QA log for future data pulls.

## Change Log Template

Record adjustments after each QA pass:

```
## {Date} – {Reviewer}
- Summary of change
- Prompt tweaks needed?
- Data gaps to fill next run
```

Add entries to `logs/qa/{company}.md` under a “Changes” heading so we can track improvements over time.
