"""Bridge to run the OpenAI Agent Builder workflow from Python."""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional


DEFAULT_WORKFLOW_PATH = Path(__file__).resolve().parent.parent / "workflows" / "openai_workflow.mjs"


class WorkflowError(RuntimeError):
    """Raised when the workflow runner fails."""


def run_agent_workflow(
    input_text: str, workflow_path: Optional[Path] = None, *, env: Optional[dict[str, str]] = None
) -> Dict[str, Any]:
    """Execute the JS workflow and return parsed JSON.

    Args:
        input_text: Free-text company description or request that seeds the workflow.
        workflow_path: Override the workflow file path.
        env: Optional environment variables to pass through.

    Raises:
        FileNotFoundError: If the workflow file cannot be located.
        WorkflowError: When execution fails or JSON cannot be parsed.
    """

    script_path = workflow_path or DEFAULT_WORKFLOW_PATH
    if not script_path.exists():
        raise FileNotFoundError(f"Workflow script not found at {script_path}")

    command = ["node", str(script_path)]
    environment = os.environ.copy()
    if env:
        environment.update(env)

    process = subprocess.run(
        command,
        input=input_text.encode("utf-8"),
        capture_output=True,
        check=False,
        env=environment,
    )

    if process.returncode != 0:
        stderr = process.stderr.decode("utf-8", errors="ignore").strip()
        raise WorkflowError(f"Workflow execution failed ({process.returncode}): {stderr}")

    stdout_text = process.stdout.decode("utf-8", errors="ignore").strip()
    if not stdout_text:
        raise WorkflowError("Workflow returned no output")

    try:
        return json.loads(stdout_text)
    except json.JSONDecodeError as exc:
        raise WorkflowError("Unable to parse workflow output as JSON") from exc
