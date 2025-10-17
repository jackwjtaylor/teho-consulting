from pathlib import Path

import pytest

from teho_automation.context import CompanyContext
from teho_automation.prompt_runner import validate_report_structure
from teho_automation.prompt_templates import build_prompt, load_prompt_template


def test_load_prompt_template_extracts_code_block(tmp_path: Path) -> None:
    content = """# Title

````markdown
Hello {BUSINESS_NAME}
````
"""
    template_path = tmp_path / "template.md"
    template_path.write_text(content, encoding="utf-8")
    template = load_prompt_template(template_path)
    assert template.strip() == "Hello {BUSINESS_NAME}"


def test_build_prompt_inserts_context_fields() -> None:
    template = "Report for {BUSINESS_NAME} in {HEADQUARTERS} contact {PRIMARY_CONTACT}"
    context = CompanyContext(
        business_name="Acme Widgets",
        headquarters="London",
        industry_tags=[],
        product_summary=[],
        primary_contact="Alex Smith — CEO",
    )
    prompt = build_prompt(template, context, report_depth="executive")
    assert "Acme Widgets" in prompt
    assert "London" in prompt
    assert "Alex Smith" in prompt


def test_validate_report_structure_flags_missing_sections() -> None:
    text = """
    ## Company & Process Overview
    ## Pain-Point Scan
    """
    missing = validate_report_structure(text)
    assert "## Opportunity Table" in missing
    assert "## Appendix" in missing
