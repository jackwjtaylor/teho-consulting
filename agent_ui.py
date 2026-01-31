import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import importlib.util
import streamlit as st

ROOT = Path(__file__).resolve().parent
SRC_PATH = ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))
AGENT_RUNNER_DIR = ROOT / "agent-runner"
RUNNER_SCRIPT = AGENT_RUNNER_DIR / "run.mjs"
EXPORT_SCRIPT = AGENT_RUNNER_DIR / "export_reports.py"

spec = importlib.util.spec_from_file_location("export_reports", EXPORT_SCRIPT)
export_module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(export_module)
export_reports = export_module.export_reports
slugify = export_module.slugify

st.set_page_config(page_title="Teho Agent Runner", layout="wide")

st.title("Teho Agent Runner")
st.caption("Run AI opportunity reports without the terminal.")

col_left, col_right = st.columns([2, 1])

with col_left:
    company_name = st.text_input("Company name", placeholder="Tomoro.ai")
    domain = st.text_input("Company domain (optional)", placeholder="tomoro.ai")
    additional_context = st.text_area(
        "Additional context (optional)",
        placeholder="Notes, product focus, leadership priorities, anything you want the agent to factor in...",
        height=160,
    )

    model = st.selectbox(
        "Agent model", ["gpt-5.2", "gpt-5.1", "gpt-5-mini", "gpt-4.1-mini"], index=0
    )
    financial_model = st.selectbox(
        "Financials model", ["gpt-5.1", "gpt-5.2", "gpt-5-mini", "gpt-4.1-mini"], index=0
    )

    include_full_link = st.checkbox(
        "Include full report link in email", value=False, help="Leave off if you want to paywall the full report."
    )

with col_right:
    st.subheader("Google Drive")
    client_secrets = st.text_input(
        "OAuth client secrets JSON path",
        value=os.getenv("GOOGLE_OAUTH_CLIENT_SECRETS", str(AGENT_RUNNER_DIR / "client_secrets.json")),
    )
    drive_token = st.text_input(
        "OAuth token path",
        value=os.getenv("GOOGLE_DRIVE_TOKEN", str(AGENT_RUNNER_DIR / "drive_token.json")),
    )
    drive_folder = st.text_input(
        "Drive folder ID (optional)",
        value=os.getenv("GOOGLE_DRIVE_FOLDER_ID", ""),
        placeholder="Paste the folder ID if you want uploads organized",
    )
    st.caption(
        "First run will open a Google login flow in your browser. Use hello@teho.ai to grant Drive access."
    )

slug_preview = slugify(company_name) if company_name else "company"
slug = st.text_input("Slug (report folder name)", value=slug_preview)

run_button = st.button("Run report", type="primary", disabled=not company_name)

if run_button:
    status = st.status("Running agent...", expanded=True)
    log_placeholder = st.empty()
    output_path = AGENT_RUNNER_DIR / f"{slug}-agent-output.json"

    context_file = None
    try:
        env = os.environ.copy()
        env["TEHO_AGENT_MODEL"] = model
        env["TEHO_AGENT_FINANCIAL_MODEL"] = financial_model

        cmd = ["node", str(RUNNER_SCRIPT), "--company", company_name, "--out", str(output_path)]
        if domain:
            cmd += ["--domain", domain]
        if additional_context:
            context_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
            context_file.write(additional_context.encode("utf-8"))
            context_file.close()
            cmd += ["--context-file", context_file.name]

        log_lines = []
        status.update(label="Running agent...", state="running")
        process = subprocess.Popen(
            cmd,
            cwd=str(AGENT_RUNNER_DIR),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        assert process.stdout is not None
        for raw_line in process.stdout:
            line = raw_line.rstrip()
            if not line:
                continue
            log_lines.append(line)
            if len(log_lines) > 200:
                log_lines = log_lines[-200:]
            log_placeholder.code("\n".join(log_lines))

            match = re.search(r"\[agent-runner\]\s+(.*)", line)
            if match:
                step_text = match.group(1).strip()
                if step_text.endswith("..."):
                    status.update(label=f"Running agent • {step_text[:-3]}", state="running")
                elif step_text.endswith("done"):
                    status.update(
                        label=f"Completed • {step_text.replace(' done', '')}", state="running"
                    )

        exit_code = process.wait()
        if exit_code != 0:
            raise subprocess.CalledProcessError(exit_code, cmd, "\n".join(log_lines))

        status.update(label="Generating report assets...", state="running")

        export_result = export_reports(
            output_path=output_path,
            slug=slug,
            company_name=company_name,
            company_url=domain or None,
            reports_root=ROOT / "reports",
            model_label=model,
            include_full_link=include_full_link,
            use_puppeteer=True,
            drive_client_secrets=Path(client_secrets) if client_secrets else None,
            drive_token_path=Path(drive_token) if drive_token else None,
            drive_folder_id=drive_folder or None,
        )

        status.update(label="Done", state="complete")

        st.success("Reports generated")
        st.subheader("Report links")

        summary_link = export_result["summary"]["drive_link"]
        full_link = export_result["full"]["drive_link"]

        if summary_link:
            st.link_button("Open summary PDF (Drive)", summary_link)
        if full_link:
            st.link_button("Open full PDF (Drive)", full_link)

        st.caption("Local files")
        st.write(export_result["summary"]["pdf"])
        st.write(export_result["full"]["pdf"])

        st.subheader("Outreach email")
        st.text_area("Copy into Gmail", export_result["email_text"], height=260)

        if export_result.get("drive_error"):
            st.warning(f"Drive upload issue: {export_result['drive_error']}")
            st.info("You can still attach the PDFs manually or fix the Drive credentials and re-run.")

    except subprocess.CalledProcessError as exc:
        status.update(label="Agent run failed", state="error")
        st.error("Agent run failed")
        st.text(exc.stderr or exc.stdout or str(exc))
    except Exception as exc:  # pragma: no cover
        status.update(label="Unexpected error", state="error")
        st.error(str(exc))
    finally:
        if context_file and os.path.exists(context_file.name):
            os.unlink(context_file.name)
