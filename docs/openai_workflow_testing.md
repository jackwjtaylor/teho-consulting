# OpenAI Agent Builder workflow – usage and testing

The reporting pipeline now delegates generation to the OpenAI Agent Builder workflow defined in `workflows/openai_workflow.mjs`.
Follow the steps below to run it end-to-end in this repository.

## Setup
1. Ensure Node.js 18+ is available: `node -v`.
2. Install workflow dependencies (runs once): `npm install`.
3. Export your API key: `export OPENAI_API_KEY=sk-...`.
4. (Optional) Activate the Python environment used by the CLI: `source .venv/bin/activate`.

## Generate a report via the CLI (uses the Agent Builder workflow)
1. Prepare context files as before: `teho init-company <slug>` then populate `data/raw/<slug>/context.json` and `sources.csv`.
2. Run collectors if needed: `teho collect-signals <slug> --domain example.com`.
3. Run generation (now powered by the Agent Builder workflow):
   ```bash
   teho generate <slug> --report executive --report comprehensive
   ```
   The command feeds the company context into the JS workflow, saves markdown/HTML/PDF under `reports/<slug>/`, and uploads to Supabase when enabled.

## Run the workflow directly (for debugging)
1. Provide seed text on stdin or as an argument. Example with stdin:
   ```bash
   echo "Company: ExampleCo\nWebsite: example.com" | node workflows/openai_workflow.mjs
   ```
2. The script returns JSON containing the report markdown, one-pager summary, and outreach email.

## What changed
- The CLI no longer calls the legacy prompt runner; it now shells out to the Agent Builder workflow for every generated report.
- Queue processing and automation actions reuse the same workflow-backed `generate` command for consistency.
