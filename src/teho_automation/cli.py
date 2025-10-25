"""Command-line interface for Teho automation."""

from __future__ import annotations

import csv
import json
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import typer
from rich import print as rprint
from rich.console import Console
from rich.table import Table

from dotenv import load_dotenv

from .collector_runner import collect_and_store
from .context import CompanyContext, load_context, load_sources
from .packaging import (
    FULL_DEPTH_LABEL,
    FULL_DISPLAY_NAME,
    REPORT_STORAGE_FOLDER,
    SUMMARY_DEPTH_LABEL,
    SUMMARY_DISPLAY_NAME,
    create_report_assets,
    package_snapshot,
    rewrite_markdown_intro,
)
from .paths import get_company_paths
from .prompt_runner import PromptRunner, validate_report_structure
from .prompt_templates import build_prompt, load_prompt_templates
from .supabase_client import (
    download_attachment_blob,
    ensure_reports_bucket,
    fetch_automation_runs,
    fetch_briefing_attachments,
    fetch_requests,
    insert_briefing_request,
    log_outreach_event,
    set_portal_user_access,
    update_automation_run,
    update_briefing_status,
    upload_report_asset,
    upsert_report_entry,
)

app = typer.Typer(help="Automation commands for Teho Consulting.")
console = Console()

# Ensure environment variables from .env are available (e.g. OPENAI_API_KEY)
load_dotenv()

REPORT_DEFINITIONS = {
    "executive": {
        "canonical": "summary",
        "report_key": "opportunity-report-summary",
        "display_name": SUMMARY_DISPLAY_NAME,
        "title_suffix": "Opportunity Report",
        "depth_label": SUMMARY_DEPTH_LABEL,
        "storage_folder": REPORT_STORAGE_FOLDER,
    },
    "comprehensive": {
        "canonical": "full",
        "report_key": "opportunity-report-full",
        "display_name": FULL_DISPLAY_NAME,
        "title_suffix": "Opportunity Report",
        "depth_label": FULL_DEPTH_LABEL,
        "storage_folder": REPORT_STORAGE_FOLDER,
    },
}

SUMMARY_DEFINITION = {
    "report_key": "opportunity-report-summary",
    "display_name": SUMMARY_DISPLAY_NAME,
    "depth_label": SUMMARY_DEPTH_LABEL,
    "storage_folder": REPORT_STORAGE_FOLDER,
}


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
    for directory in [paths.raw_dir, paths.attachments_dir, paths.reports_dir, paths.base_dir / "logs" / "qa"]:
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

    supabase_payload = {
        **record,
        "priority": int(record["priority"]),
        "payload": record,
    }
    result = insert_briefing_request(supabase_payload)
    if result.success:
        typer.secho("Supabase queue updated.", fg=typer.colors.GREEN)
    else:
        typer.secho(
            f"Skipping Supabase sync ({result.message or 'not configured'}).",
            fg=typer.colors.YELLOW,
        )


@app.command()
def list_requests(
    status: Optional[str] = typer.Option(None, help="Filter by status e.g. queued"),
    limit: int = typer.Option(20, help="Number of results to show"),
) -> None:
    """List recent briefing requests."""
    result = fetch_requests(status=status, limit=limit)
    if result.success and isinstance(result.data, list):
        table = Table(title="Supabase briefing requests")
        table.add_column("Company")
        table.add_column("Slug")
        table.add_column("Status")
        table.add_column("Priority")
        table.add_column("Requested at")
        for row in result.data:
            table.add_row(
                row.get("company_name", ""),
                row.get("slug", ""),
                row.get("status", ""),
                str(row.get("priority", "")),
                row.get("requested_at", ""),
            )
        console.print(table)
        return

    # Fallback to CSV if Supabase unavailable
    queue_path = Path("data/company_queue.csv")
    if not queue_path.exists():
        typer.secho("No queue entries found (Supabase unavailable and CSV missing).", fg=typer.colors.YELLOW)
        raise typer.Exit()

    table = Table(title="Local CSV queue (Supabase unavailable)")
    table.add_column("Company")
    table.add_column("Slug")
    table.add_column("Status")
    table.add_column("Priority")
    table.add_column("Requested at")
    with queue_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if status and row.get("status") != status:
                continue
            table.add_row(
                row.get("company_name", ""),
                row.get("slug", ""),
                row.get("status", ""),
                row.get("priority", ""),
                row.get("requested_at", ""),
            )
    console.print(table)


def _load_local_queue(status: Optional[str] = None, limit: Optional[int] = None) -> List[dict]:
    queue_path = Path("data/company_queue.csv")
    if not queue_path.exists():
        return []

    with queue_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            if status and row.get("status") != status:
                continue
            rows.append(row)
        rows.sort(key=lambda r: r.get("requested_at", ""))
        if limit:
            rows = rows[:limit]
        return rows


def _write_context_defaults(slug: str, company_name: str, contact: str, email: str) -> None:
    paths = get_company_paths(slug)
    if not paths.context_file.exists():
        return
    data = json.loads(paths.context_file.read_text(encoding="utf-8"))
    changed = False
    if not data.get("business_name") and company_name:
        data["business_name"] = company_name
        changed = True
    if not data.get("primary_contact") and contact:
        data["primary_contact"] = contact
        changed = True
    if not data.get("primary_email") and email:
        data["primary_email"] = email
        changed = True
    if changed:
        paths.context_file.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _sync_request_attachments(request: Dict[str, Any], paths: CompanyPaths) -> None:
    request_id = request.get("id")
    if not request_id:
        return

    result = fetch_briefing_attachments(str(request_id))
    if not result.success:
        typer.secho(
            f"Unable to fetch attachments for {paths.slug}: {result.message}",
            fg=typer.colors.YELLOW,
        )
        return

    attachments: List[Dict[str, Any]] = result.data or []  # type: ignore[assignment]
    if not attachments:
        return

    paths.attachments_dir.mkdir(parents=True, exist_ok=True)
    downloaded = 0
    for attachment in attachments:
        storage_path = attachment.get("storage_path")
        if not storage_path:
            continue
        file_name = attachment.get("file_name") or Path(storage_path).name
        safe_name = _sanitize_filename(file_name)
        destination = paths.attachments_dir / safe_name
        if destination.exists():
            continue
        blob = download_attachment_blob(storage_path)
        if not blob.success or blob.data is None:
            typer.secho(
                f"Unable to download attachment {file_name}: {blob.message}",
                fg=typer.colors.YELLOW,
            )
            continue
        destination.write_bytes(blob.data)
        downloaded += 1

    if downloaded:
        typer.secho(
            f"Downloaded {downloaded} attachment(s) for {paths.slug}",
            fg=typer.colors.GREEN,
        )


def _sanitize_filename(name: str) -> str:
    sanitized = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-._")
    return sanitized or "attachment"


@app.command()
def process_queue(
    limit: int = typer.Option(1, help="Number of queued requests to process"),
    status: str = typer.Option("queued", help="Queue status to consume"),
    generate: bool = typer.Option(False, help="Generate reports via OpenAI"),
    package: bool = typer.Option(False, help="Create snapshot HTML/PDF and email draft"),
    model: str = typer.Option("gpt-4.1-mini", help="OpenAI model to use when generating"),
    template: Path = typer.Option(Path("docs/prompt_v1.md"), help="Prompt template path"),
    dry_run: bool = typer.Option(False, help="Preview actions without making changes"),
) -> None:
    """Process queued requests from Supabase (or CSV fallback)."""

    # Fetch requests from Supabase
    requests_data: List[dict] = []
    supabase_result = fetch_requests(status=status, limit=limit)
    if supabase_result.success and isinstance(supabase_result.data, list):
        requests_data = list(reversed(supabase_result.data))  # oldest first
    else:
        requests_data = _load_local_queue(status=status, limit=limit)

    if not requests_data:
        typer.secho("No requests found for the given status.", fg=typer.colors.YELLOW)
        raise typer.Exit()

    template_map: Optional[dict[str, str]] = None
    runner: Optional[PromptRunner] = None

    for entry in requests_data[:limit]:
        slug = entry.get("slug") or "".join(
            ch.lower() if ch.isalnum() or ch == " " else " " for ch in entry.get("company_name", "")
        ).strip().replace(" ", "-")
        company_name = entry.get("company_name", "")
        domain = entry.get("domain", "") or entry.get("payload", {}).get("domain", "")
        primary_contact = entry.get("primary_contact", "")
        primary_email = entry.get("primary_email", "")
        paths = get_company_paths(slug)

        typer.secho(f"Processing {company_name} ({slug})", fg=typer.colors.CYAN)

        if dry_run:
            typer.secho(
                f"Dry run: would initialise folders, collect signals, generate={generate}, package={package}",
                fg=typer.colors.BLUE,
            )
            continue

        update_briefing_status(slug, "collecting")

        init_company(slug)
        _write_context_defaults(slug, company_name, primary_contact, primary_email)
        _sync_request_attachments(entry, paths)

        if domain:
            try:
                collect_and_store(slug, domain)
                typer.secho("Collected automation signals.", fg=typer.colors.GREEN)
            except Exception as exc:  # pragma: no cover - network failures
                typer.secho(f"Signal collection failed: {exc}", fg=typer.colors.RED)
        else:
            typer.secho("No domain provided; skipping automated collection.", fg=typer.colors.YELLOW)

        try:
            context = load_context(str(paths.context_file))
        except ValueError as exc:
            typer.secho(str(exc), fg=typer.colors.RED)
            update_briefing_status(slug, "needs_context")
            continue

        if generate:
            if template_map is None:
                template_map = load_prompt_templates(template)
            if runner is None:
                try:
                    runner = PromptRunner(model=model)
                except RuntimeError as exc:
                    typer.secho(str(exc), fg=typer.colors.RED)
                    update_briefing_status(slug, "needs_review")
                    break

            if template_map is None:
                typer.secho("No prompt templates available.", fg=typer.colors.RED)
                update_briefing_status(slug, "needs_review")
                break

            for report in ("executive", "comprehensive"):
                template_str = template_map.get(report) or template_map.get("default")
                if template_str is None:
                    typer.secho(f"No prompt template found for {report}", fg=typer.colors.RED)
                    continue
                prompt = build_prompt(template_str, context, report_depth=report)
                console.print(f"Generating {report} report for [bold]{company_name}[/bold]...")
                report_text = runner.run(prompt)
                if report != "executive":
                    missing = validate_report_structure(report_text)
                    if missing:
                        typer.secho(f"{report} report missing sections {missing}", fg=typer.colors.YELLOW)
                output_file = paths.reports_dir / f"{report}.md"
                output_file.write_text(report_text, encoding="utf-8")
                typer.secho(f"Wrote {output_file}", fg=typer.colors.GREEN)

            update_briefing_status(slug, "needs_qa")

            if package:
                snapshot_path = paths.reports_dir / "snapshot.md"
                if snapshot_path.exists():
                    result = package_snapshot(
                        slug=slug,
                        snapshot_markdown=snapshot_path,
                        output_dir=paths.reports_dir,
                        context=context,
                        generate_pdf=True,
                    )
                    typer.secho(f"Snapshot packaged: {result['html']}", fg=typer.colors.GREEN)
                    update_briefing_status(slug, "ready_to_send")
                else:
                    typer.secho("Snapshot markdown missing; run snapshot generator before packaging.", fg=typer.colors.YELLOW)
        else:
            update_briefing_status(slug, "needs_context")


@app.command()
def package(
    slug: str,
    snapshot: Path = typer.Option(Path("reports/{slug}/snapshot.md"), help="Snapshot markdown path"),
    output_dir: Optional[Path] = typer.Option(None, help="Output directory for packaged assets"),
    no_pdf: bool = typer.Option(False, help="Skip PDF generation even if WeasyPrint is installed."),
    upload: bool = typer.Option(True, help="Upload packaged snapshot assets to Supabase storage."),
) -> None:
    """Create snapshot HTML/PDF and email draft for outreach."""

    paths = get_company_paths(slug)
    context = load_context(str(paths.context_file))
    sources = load_sources(str(paths.sources_file))

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

    remote_paths: dict[str, Optional[str]] = {}
    if upload:
        bucket_result = ensure_reports_bucket()
        if not bucket_result.success:
            typer.secho(
                f"Supabase upload skipped: {bucket_result.message}", fg=typer.colors.YELLOW
            )
        else:
            for key, value in result.items():
                if not value:
                    continue
                upload_result = upload_report_asset(
                    slug, Path(value), folder=SUMMARY_DEFINITION["storage_folder"]
                )
                if upload_result.success:
                    typer.secho(f"Uploaded {upload_result.message}", fg=typer.colors.GREEN)
                    remote_paths[key] = upload_result.message
                else:
                    typer.secho(f"Upload failed: {upload_result.message}", fg=typer.colors.YELLOW)

    if upload:
        entry = {
            "client_slug": slug,
            "report_key": SUMMARY_DEFINITION["report_key"],
            "display_name": SUMMARY_DEFINITION["display_name"],
            "html_path": remote_paths.get("html"),
            "pdf_path": remote_paths.get("pdf"),
            "generated_at": datetime.utcnow().isoformat(),
            "model": None,
        }
        upsert_report_entry(entry)


@app.command()
def ensure_storage() -> None:
    """Ensure the Supabase reports storage bucket exists."""

    result = ensure_reports_bucket()
    if result.success:
        typer.secho("Supabase reports bucket is ready.", fg=typer.colors.GREEN)
    else:
        typer.secho(f"Unable to prepare storage: {result.message}", fg=typer.colors.RED)


@app.command()
def assign_portal_user(
    email: str = typer.Argument(..., help="Portal user's email address"),
    client_slug: str = typer.Argument(..., help="Company slug they should see"),
    client_id: Optional[str] = typer.Option(None, help="Optional Supabase auth user ID to store"),
) -> None:
    """Attach a client slug to a Supabase user for portal access control."""

    result = set_portal_user_access(email=email, client_slug=client_slug, client_id=client_id)
    if result.success:
        typer.secho("Portal user metadata updated ✅", fg=typer.colors.GREEN)
    else:
        typer.secho(f"Failed to update portal user: {result.message}", fg=typer.colors.RED)


@app.command()
def log_outreach(
    client_slug: str = typer.Option(..., help="Company slug"),
    contact_email: str = typer.Option(..., help="Primary contact email"),
    event_type: str = typer.Option(..., help="Event type: sent, opened, clicked, replied"),
    channel: str = typer.Option("email", help="Channel (email, call, linkedin, etc.)"),
    report_key: Optional[str] = typer.Option(None, help="Associated report key, if any"),
    notes: Optional[str] = typer.Option(None, help="Freeform notes"),
    metadata: Optional[str] = typer.Option(None, help="JSON string with extra metadata"),
) -> None:
    """Log an outreach event to Supabase for analytics."""

    allowed = {"sent", "opened", "clicked", "replied"}
    if event_type.lower() not in allowed:
        typer.secho(f"event_type must be one of: {', '.join(sorted(allowed))}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    extra_meta: Optional[Dict[str, Any]] = None
    if metadata:
        try:
            extra_meta = json.loads(metadata)
        except json.JSONDecodeError as exc:
            typer.secho(f"Invalid metadata JSON: {exc}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    payload: Dict[str, Any] = {
        "client_slug": client_slug,
        "contact_email": contact_email,
        "event_type": event_type.lower(),
        "channel": channel,
    }
    if report_key:
        payload["report_key"] = report_key
    if notes:
        payload["notes"] = notes
    if extra_meta is not None:
        payload["metadata"] = extra_meta

    result = log_outreach_event(payload)
    if result.success:
        typer.secho("Outreach event logged ✅", fg=typer.colors.GREEN)
    else:
        typer.secho(f"Unable to log outreach event: {result.message}", fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def automation_worker(
    poll: int = typer.Option(0, help="Seconds to wait between polls (0 = run once if no work)"),
    batch_size: int = typer.Option(3, help="Number of jobs to fetch per batch"),
    dry_run: bool = typer.Option(False, help="Preview actions without executing them"),
) -> None:
    """Process automation runs created from the admin portal."""

    typer.secho("Starting automation worker", fg=typer.colors.CYAN)
    while True:
        pending = fetch_automation_runs(["requested"], limit=batch_size)
        if not pending.success:
            typer.secho(f"Unable to fetch automation runs: {pending.message}", fg=typer.colors.RED)
            if poll <= 0:
                raise typer.Exit(code=1)
            time.sleep(max(poll, 5))
            continue

        runs: List[Dict[str, Any]] = pending.data or []  # type: ignore[assignment]
        if not runs:
            if poll > 0:
                time.sleep(poll)
                continue
            typer.secho("No pending automation runs.", fg=typer.colors.GREEN)
            break

        for run in runs:
            _process_automation_run(run, dry_run=dry_run)

        if poll <= 0:
            break


@app.command()
def generate(
    slug: str,
    reports: List[str] = typer.Option(
        ["executive"],
        "--report",
        "-r",
        help="Report depths to generate (executive, ...).",
    ),
    template: Path = typer.Option(Path("docs/prompt_v1.md"), help="Prompt template path."),
    output_dir: Optional[Path] = typer.Option(None, help="Directory for generated reports."),
    model: str = typer.Option("gpt-4.1-mini", help="OpenAI model to use."),
    dry_run: bool = typer.Option(False, help="Print prompts without calling the API."),
    upload: bool = typer.Option(True, help="Upload generated reports to Supabase storage."),
) -> None:
    """Generate reports for a company using the OpenAI API."""
    paths = get_company_paths(slug)
    context = load_context(str(paths.context_file))
    sources = load_sources(str(paths.sources_file))
    template_map = load_prompt_templates(template)

    target_dir = output_dir or paths.reports_dir
    target_dir.mkdir(parents=True, exist_ok=True)

    runner: Optional[PromptRunner] = None
    bucket_ready = True
    if upload and not dry_run:
        bucket_result = ensure_reports_bucket()
        if not bucket_result.success:
            bucket_ready = False
            typer.secho(
                f"Supabase upload disabled: {bucket_result.message}", fg=typer.colors.YELLOW
            )
        else:
            typer.secho("Supabase storage ready.", fg=typer.colors.GREEN)
    for report in reports:
        template_text = template_map.get(report) or template_map.get("default")
        if template_text is None:
            typer.secho(f"No prompt template available for {report}", fg=typer.colors.RED)
            continue
        prompt = build_prompt(
            template_text,
            context,
            report_depth=report,
            sources=sources,
        )
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
        if report != "executive":
            missing = validate_report_structure(report_text)
            if missing:
                typer.secho(
                    f"Warning: report missing sections {missing}", fg=typer.colors.YELLOW
                )

        definition = REPORT_DEFINITIONS.get(report, REPORT_DEFINITIONS["executive"])
        canonical = definition["canonical"]
        report_text = rewrite_markdown_intro(
            report_text,
            title=definition["display_name"],
            depth_label=definition["depth_label"],
        )

        markdown_path = target_dir / f"{canonical}.md"
        markdown_path.write_text(report_text, encoding="utf-8")
        typer.secho(f"Saved {markdown_path}", fg=typer.colors.GREEN)

        assets = create_report_assets(
            report_text,
            title=definition["display_name"],
            output_dir=target_dir,
            basename=canonical,
            context=context,
            depth_label=definition["depth_label"],
            generate_pdf=True,
        )
        typer.secho(f"HTML created at {assets['html']}", fg=typer.colors.GREEN)
        if assets["pdf"]:
            typer.secho(f"PDF created at {assets['pdf']}", fg=typer.colors.GREEN)

        remote_html: Optional[str] = None
        remote_pdf: Optional[str] = None
        if upload and bucket_ready:
            if assets["html"]:
                html_upload = upload_report_asset(
                    slug, Path(assets["html"]), folder=definition["storage_folder"]
                )
                if html_upload.success:
                    remote_html = html_upload.message
                    typer.secho(f"Uploaded {remote_html}", fg=typer.colors.GREEN)
                else:
                    typer.secho(
                        f"Upload failed: {html_upload.message}", fg=typer.colors.YELLOW
                    )
            if assets["pdf"]:
                pdf_upload = upload_report_asset(
                    slug, Path(assets["pdf"]), folder=definition["storage_folder"]
                )
                if pdf_upload.success:
                    remote_pdf = pdf_upload.message
                    typer.secho(f"Uploaded {remote_pdf}", fg=typer.colors.GREEN)
                else:
                    typer.secho(
                        f"Upload failed: {pdf_upload.message}", fg=typer.colors.YELLOW
                    )

        if upload:
            record = {
                "client_slug": slug,
                "report_key": definition["report_key"],
                "display_name": definition["display_name"],
                "html_path": remote_html,
                "pdf_path": remote_pdf,
                "generated_at": datetime.utcnow().isoformat(),
                "model": model,
            }
            upsert_report_entry(record)


if __name__ == "__main__":
    app()


def _process_automation_run(run: Dict[str, Any], *, dry_run: bool = False) -> None:
    run_id = run.get("id")
    action = run.get("action") or ""
    payload = run.get("payload") if isinstance(run.get("payload"), dict) else {}
    client_slug = run.get("client_slug")

    if not run_id:
        typer.secho("Automation run missing ID; skipping", fg=typer.colors.RED)
        return

    merged_payload = dict(payload)
    merged_payload["last_attempt"] = datetime.utcnow().isoformat()
    update_automation_run(run_id, status="in_progress", payload=merged_payload)

    try:
        if dry_run:
            message = "Dry run requested"
        else:
            message = _execute_automation_action(action, client_slug, payload)
        merged_payload["last_result"] = message
        update_automation_run(run_id, status="succeeded", payload=merged_payload)
        typer.secho(f"Automation run {run_id} completed: {message}", fg=typer.colors.GREEN)
    except Exception as exc:
        merged_payload["last_error"] = str(exc)
        update_automation_run(run_id, status="failed", payload=merged_payload)
        typer.secho(f"Automation run {run_id} failed: {exc}", fg=typer.colors.RED)


def _execute_automation_action(action: str, slug: Optional[str], payload: Dict[str, Any]) -> str:
    template_path = Path(payload.get("template") or "docs/prompt_v1.md")
    model_name = payload.get("model") or "gpt-4.1-mini"

    if action == "generate-summary":
        if not slug:
            raise ValueError("client_slug required for generate-summary")
        generate(
            slug=slug,
            reports=["executive"],
            template=template_path,
            output_dir=None,
            model=model_name,
            dry_run=False,
            upload=True,
        )
        return "Generated executive summary"

    if action == "generate-full":
        if not slug:
            raise ValueError("client_slug required for generate-full")
        generate(
            slug=slug,
            reports=["comprehensive"],
            template=template_path,
            output_dir=None,
            model=model_name,
            dry_run=False,
            upload=True,
        )
        return "Generated full report"

    if action == "package-snapshot":
        if not slug:
            raise ValueError("client_slug required for package-snapshot")
        snapshot_template = payload.get("snapshot") or "reports/{slug}/snapshot.md"
        package(
            slug=slug,
            snapshot=Path(str(snapshot_template).format(slug=slug)),
            output_dir=None,
            no_pdf=False,
            upload=True,
        )
        return "Packaged snapshot"

    if action == "process-queue":
        limit = int(payload.get("limit") or 1)
        status = payload.get("status") or "queued"
        generate_flag = bool(payload.get("generate", True))
        package_flag = bool(payload.get("package", True))
        try:
            process_queue(
                limit=limit,
                status=status,
                generate=generate_flag,
                package=package_flag,
                model=model_name,
                template=template_path,
                dry_run=False,
            )
        except typer.Exit:
            pass  # process_queue uses typer.Exit when no work remains
        return "Processed queue"

    raise ValueError(f"Unsupported automation action: {action}")
