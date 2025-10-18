"""Command-line interface for Teho automation."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from .collector_runner import collect_and_store
from .context import CompanyContext, load_context
from .packaging import package_snapshot
from .paths import get_company_paths
from .prompt_runner import PromptRunner, validate_report_structure
from .prompt_templates import build_prompt, load_prompt_template

app = typer.Typer(help="Automation commands for Teho Consulting.")
console = Console()


@app.command()
def validate_context(path: Path) -> None:
    """Validate a context JSON file and report missing values."""
    try:
        context = load_context(str(path))
    except ValueError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc

    missing = context.missing_fields()
    if missing:
        table = Table(title="Fields needing attention")
        table.add_column("Field")
        for field in missing:
            table.add_row(field)
        console.print(table)
        typer.secho("Context is valid but has gaps. Fill before prompting.", fg=typer.colors.YELLOW)
    else:
        typer.secho("Context looks good 👍", fg=typer.colors.GREEN)

    stale = context.stale_headlines()
    if stale:
        table = Table(title="Headline dates older than 24 months")
        table.add_column("Headline")
        for item in stale:
            table.add_row(item)
        console.print(table)
        typer.secho("Refresh headlines with more recent coverage where possible.", fg=typer.colors.YELLOW)


@app.command()
def init_company(slug: str, base_dir: Optional[Path] = None) -> None:
    """Create folder skeleton for a company."""
    paths = get_company_paths(slug, base_dir)
    for directory in [paths.raw_dir, paths.reports_dir, paths.base_dir / "logs" / "qa"]:
        directory.mkdir(parents=True, exist_ok=True)

    context_template = CompanyContext(
        business_name="",
        industry_tags=[],
        product_summary=[],
    )
    if not paths.context_file.exists():
        paths.context_file.write_text(
            json.dumps(json.loads(context_template.model_dump_json(indent=2)), indent=2),
            encoding="utf-8",
        )
    if not paths.sources_file.exists():
        paths.sources_file.write_text("id,title,url,retrieved,summary,confidence\n", encoding="utf-8")

    typer.secho(f"Initialised folders for {slug}", fg=typer.colors.GREEN)


@app.command()
def show_paths(slug: str) -> None:
    """Display key paths for a company."""
    paths = get_company_paths(slug)
    table = Table(title=f"Paths for {slug}")
    table.add_column("Key")
    table.add_column("Path")
    table.add_row("Raw data", str(paths.raw_dir))
    table.add_row("Reports", str(paths.reports_dir))
    table.add_row("Context file", str(paths.context_file))
    table.add_row("Sources file", str(paths.sources_file))
    table.add_row("QA log", str(paths.qa_log))
    rprint(table)


@app.command()
def collect_signals(slug: str, domain: str = typer.Option(..., help="Company domain e.g. gousto.co.uk")) -> None:
    """Run automated collectors and store results for review."""
    try:
        output = collect_and_store(slug, domain)
    except FileNotFoundError:
        typer.secho("Context file missing. Run init-company first.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    typer.secho(f"Stored automation signals at {output}", fg=typer.colors.GREEN)


@app.command()
def queue_request(
    company_name: str = typer.Argument(..., help="Company name, e.g. 'Bloom & Wild'"),
    domain: str = typer.Option(..., help="Primary domain, e.g. bloomandwild.com"),
    slug: Optional[str] = typer.Option(None, help="Slug to use; defaults to kebab-case company name"),
    persona: Optional[str] = typer.Option(None, help="Target persona e.g. Founder/CEO"),
    contact: Optional[str] = typer.Option(None, help="Primary contact name"),
    email: Optional[str] = typer.Option(None, help="Primary contact email"),
    priority: int = typer.Option(5, help="Priority (1 = highest)"),
    source: str = typer.Option("manual", help="Source for tracking e.g. manual, website"),
) -> None:
    """Add a company request to the queue for snapshot/briefing generation."""

    queue_path = Path("data/company_queue.csv")
    queue_path.parent.mkdir(parents=True, exist_ok=True)

    slug_value = slug or "".join(ch.lower() if ch.isalnum() or ch == " " else " " for ch in company_name).strip().replace(" ", "-")
    if not slug_value:
        typer.secho("Unable to derive slug from company name.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    record = {
        "company_name": company_name,
        "slug": slug_value,
        "domain": domain,
        "status": "queued",
        "priority": str(priority),
        "persona": persona or "",
        "primary_contact": contact or "",
        "primary_email": email or "",
        "requested_at": datetime.utcnow().isoformat(timespec="seconds"),
        "source": source,
    }

    headers = [
        "company_name",
        "slug",
        "domain",
        "status",
        "priority",
        "persona",
        "primary_contact",
        "primary_email",
        "requested_at",
        "source",
    ]

    file_exists = queue_path.exists() and queue_path.stat().st_size > 0
    with queue_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(record)

    typer.secho(f"Queued {company_name} ({slug_value}) for briefing", fg=typer.colors.GREEN)


@app.command()
def package(
    slug: str,
    snapshot: Path = typer.Option(Path("reports/{slug}/snapshot.md"), help="Snapshot markdown path"),
    output_dir: Optional[Path] = typer.Option(None, help="Output directory for packaged assets"),
    no_pdf: bool = typer.Option(False, help="Skip PDF generation even if WeasyPrint is installed."),
) -> None:
    """Create snapshot HTML/PDF and email draft for outreach."""

    paths = get_company_paths(slug)
    context = load_context(str(paths.context_file))

    snapshot_path = Path(str(snapshot).format(slug=slug))
    if not snapshot_path.exists():
        typer.secho(f"Snapshot not found at {snapshot_path}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    target_dir = output_dir or paths.reports_dir
    result = package_snapshot(
        slug=slug,
        snapshot_markdown=snapshot_path,
        output_dir=target_dir,
        context=context,
        generate_pdf=not no_pdf,
    )

    typer.secho(f"Snapshot HTML saved to {result['html']}", fg=typer.colors.GREEN)
    if result["pdf"]:
        typer.secho(f"Snapshot PDF saved to {result['pdf']}", fg=typer.colors.GREEN)
    else:
        typer.secho("PDF not generated (WeasyPrint not installed).", fg=typer.colors.YELLOW)
    typer.secho(f"Email draft saved to {result['email']}", fg=typer.colors.GREEN)


@app.command()
def generate(
    slug: str,
    reports: List[str] = typer.Option(
        ["executive", "comprehensive"],
        "--report",
        "-r",
        help="Report depths to generate (executive, comprehensive).",
    ),
    template: Path = typer.Option(Path("docs/prompt_v1.md"), help="Prompt template path."),
    output_dir: Optional[Path] = typer.Option(None, help="Directory for generated reports."),
    model: str = typer.Option("gpt-4.1-mini", help="OpenAI model to use."),
    dry_run: bool = typer.Option(False, help="Print prompts without calling the API."),
) -> None:
    """Generate reports for a company using the OpenAI API."""
    paths = get_company_paths(slug)
    context = load_context(str(paths.context_file))
    template_text = load_prompt_template(template)

    target_dir = output_dir or paths.reports_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    runner: Optional[PromptRunner] = None
    for report in reports:
        prompt = build_prompt(template_text, context, report_depth=report)
        if dry_run:
            console.rule(f"Prompt preview for {report}")
            console.print(prompt)
            continue

        if runner is None:
            try:
                runner = PromptRunner(model=model)
            except RuntimeError as exc:
                typer.secho(str(exc), fg=typer.colors.RED)
                raise typer.Exit(code=1) from exc

        console.print(f"Generating {report} report for [bold]{context.business_name}[/bold]...")
        report_text = runner.run(prompt)
        missing = validate_report_structure(report_text)
        if missing:
            typer.secho(
                f"Warning: report missing sections {missing}", fg=typer.colors.YELLOW
            )

        output_file = target_dir / f"{report}.md"
        output_file.write_text(report_text, encoding="utf-8")
        typer.secho(f"Saved {output_file}", fg=typer.colors.GREEN)


if __name__ == "__main__":
    app()
