import argparse
import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

from teho_automation.context import CompanyContext, save_context
from teho_automation.packaging import (
    create_report_assets,
    FULL_DEPTH_LABEL,
    FULL_DISPLAY_NAME,
    SUMMARY_DEPTH_LABEL,
    SUMMARY_DISPLAY_NAME,
)

try:  # Optional Google Drive deps
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
except Exception:  # pragma: no cover
    Credentials = None  # type: ignore
    InstalledAppFlow = None  # type: ignore
    build = None  # type: ignore
    MediaFileUpload = None  # type: ignore


SCOPES = ["https://www.googleapis.com/auth/drive.file"]
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORTS_ROOT = REPO_ROOT / "reports"
DEFAULT_CONTEXT_ROOT = REPO_ROOT / "data" / "raw"
DEFAULT_NODE = "node"
DEFAULT_PUPPETEER_SCRIPT = Path(__file__).parent / "html_to_pdf.mjs"


def slugify(text: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"-+", "-", value)
    return value or "company"


def strip_title(markdown: str) -> str:
    lines = markdown.splitlines()
    if lines and lines[0].lstrip().startswith("#"):
        return "\n".join(lines[1:]).lstrip()
    return markdown.strip()


def build_report_markdown(body: str, *, title: str, date_str: str, business: str, depth_label: str) -> str:
    meta_lines = [
        f"# {title}  ",
        f"**Date:** {date_str}  ",
        "**Analyst:** Teho Consulting AI Advisory Team  ",
        f"**Business:** {business}  ",
        f"**Report Depth:** {depth_label}  ",
        "",
        body.strip(),
    ]
    return "\n".join(meta_lines).strip() + "\n"


def ensure_context(path: Path, company_name: str, company_url: Optional[str]) -> CompanyContext:
    if not path.exists():
        context = CompanyContext(business_name=company_name, business_url=company_url)
        save_context(str(path), context)
        return context
    raw = json.loads(path.read_text(encoding="utf-8"))
    if "business_url" in raw:
        raw["business_url"] = normalize_url(raw.get("business_url"))
    return CompanyContext.model_validate(raw)


def apply_email_links(
    email_body: str,
    summary_link: Optional[str],
    full_link: Optional[str],
    calendly_link: Optional[str],
) -> str:
    body = email_body
    if summary_link:
        body = body.replace("[SNAPSHOT_LINK]", summary_link)
    if full_link:
        body = body.replace("[FULL_REPORT_PREVIEW_LINK]", full_link)
    if calendly_link:
        body = body.replace("[CALENDLY_LINK]", calendly_link)

    if summary_link and "Snapshot:" in body and summary_link not in body:
        body = re.sub(r"(Snapshot:\s*).*", r"\\1" + summary_link, body)
    if full_link and "Full report preview:" in body and full_link not in body:
        body = re.sub(r"(Full report preview:\s*).*", r"\\1" + full_link, body)
    if calendly_link and "calendar" in body.lower() and calendly_link not in body:
        body = body.replace("calendar:", f"calendar: {calendly_link}")

    if not summary_link:
        body = re.sub(r"^Snapshot:.*\n?", "", body, flags=re.MULTILINE)
    if not full_link:
        body = re.sub(r"^Full report preview:.*\n?", "", body, flags=re.MULTILINE)

    if summary_link and summary_link not in body:
        body = body.rstrip() + f"\n\nSnapshot: {summary_link}\n"
    if full_link and full_link not in body:
        body = body.rstrip() + f"\nFull report preview: {full_link}\n"

    return body.strip() + "\n"


def normalize_url(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    if not re.match(r"^https?://", trimmed, flags=re.IGNORECASE):
        return f"https://{trimmed}"
    return trimmed


def render_pdfs_with_puppeteer(pairs: list[tuple[Path, Path]], node: str = DEFAULT_NODE) -> None:
    args = [node, str(DEFAULT_PUPPETEER_SCRIPT)]
    for html_path, pdf_path in pairs:
        args += ["--pair", str(html_path), str(pdf_path)]
    subprocess.run(args, check=True)


def drive_service(client_secrets: Path, token_path: Path):
    if Credentials is None or build is None or MediaFileUpload is None:
        raise RuntimeError("Google Drive dependencies missing.")

    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # type: ignore[name-defined]
        else:
            if InstalledAppFlow is None:
                raise RuntimeError("Google OAuth library missing.")
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")
    return build("drive", "v3", credentials=creds)


def upload_to_drive(
    file_path: Path,
    client_secrets: Path,
    token_path: Path,
    folder_id: Optional[str] = None,
) -> str:
    service = drive_service(client_secrets, token_path)
    metadata = {"name": file_path.name}
    if folder_id:
        metadata["parents"] = [folder_id]

    media = MediaFileUpload(str(file_path), resumable=True)
    created = service.files().create(body=metadata, media_body=media, fields="id").execute()
    file_id = created["id"]

    service.permissions().create(
        fileId=file_id,
        body={"type": "anyone", "role": "reader"},
        fields="id",
    ).execute()

    return f"https://drive.google.com/file/d/{file_id}/view?usp=sharing"


def export_reports(
    output_path: Path,
    slug: str,
    company_name: str,
    company_url: Optional[str],
    reports_root: Path,
    model_label: str,
    include_full_link: bool,
    use_puppeteer: bool,
    drive_client_secrets: Optional[Path],
    drive_token_path: Optional[Path],
    drive_folder_id: Optional[str],
) -> dict:
    data = json.loads(output_path.read_text(encoding="utf-8"))
    report = data["report"]["content"]
    summary = data["summary_one_pager"]["summary_content"]
    email_body = data["email"]["body"]
    created_at = data["report"].get("created_at") or datetime.utcnow().strftime("%Y-%m-%d")

    reports_dir = reports_root / slug
    reports_dir.mkdir(parents=True, exist_ok=True)

    full_markdown = build_report_markdown(
        strip_title(report),
        title=FULL_DISPLAY_NAME,
        date_str=created_at,
        business=company_name,
        depth_label=FULL_DEPTH_LABEL,
    )
    summary_markdown = build_report_markdown(
        strip_title(summary),
        title=SUMMARY_DISPLAY_NAME,
        date_str=created_at,
        business=company_name,
        depth_label=SUMMARY_DEPTH_LABEL,
    )

    full_md_path = reports_dir / "full.md"
    summary_md_path = reports_dir / "summary.md"
    full_md_path.write_text(full_markdown, encoding="utf-8")
    summary_md_path.write_text(summary_markdown, encoding="utf-8")

    context_path = DEFAULT_CONTEXT_ROOT / slug / "context.json"
    normalized_url = normalize_url(company_url)
    context = ensure_context(context_path, company_name, normalized_url)

    full_assets = create_report_assets(
        full_markdown,
        title=FULL_DISPLAY_NAME,
        output_dir=reports_dir,
        basename="full",
        context=context,
        depth_label=FULL_DEPTH_LABEL,
        generate_pdf=False,
    )
    summary_assets = create_report_assets(
        summary_markdown,
        title=SUMMARY_DISPLAY_NAME,
        output_dir=reports_dir,
        basename="summary",
        context=context,
        depth_label=SUMMARY_DEPTH_LABEL,
        generate_pdf=False,
    )

    full_pdf_path = reports_dir / "full.pdf"
    summary_pdf_path = reports_dir / "summary.pdf"

    if use_puppeteer:
        render_pdfs_with_puppeteer(
            [(Path(full_assets["html"]), full_pdf_path), (Path(summary_assets["html"]), summary_pdf_path)]
        )

    summary_link = None
    full_link = None
    drive_error = None

    if drive_client_secrets and drive_token_path:
        try:
            summary_link = upload_to_drive(summary_pdf_path, drive_client_secrets, drive_token_path, drive_folder_id)
            if include_full_link:
                full_link = upload_to_drive(full_pdf_path, drive_client_secrets, drive_token_path, drive_folder_id)
        except Exception as exc:  # pragma: no cover
            drive_error = str(exc)

    calendly_link = f"https://calendly.com/teho-jack/{slug}"
    email_final = apply_email_links(email_body, summary_link, full_link, calendly_link)
    email_path = reports_dir / "email_draft.txt"
    email_path.write_text(email_final, encoding="utf-8")

    return {
        "slug": slug,
        "reports_dir": str(reports_dir),
        "full": {
            "md": str(full_md_path),
            "html": str(full_assets["html"]),
            "pdf": str(full_pdf_path),
            "drive_link": full_link,
        },
        "summary": {
            "md": str(summary_md_path),
            "html": str(summary_assets["html"]),
            "pdf": str(summary_pdf_path),
            "drive_link": summary_link,
        },
        "email_path": str(email_path),
        "email_text": email_final,
        "drive_error": drive_error,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export agent outputs to reports + PDFs.")
    parser.add_argument("--output", required=True, help="Path to agent output JSON")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--slug", help="Slug override (default slugified company name)")
    parser.add_argument("--company-url", default="", help="Company website URL")
    parser.add_argument("--reports-root", default=str(DEFAULT_REPORTS_ROOT), help="Reports root folder")
    parser.add_argument("--model-label", default="gpt-5.2", help="Model label for metadata")
    parser.add_argument("--include-full-link", action="store_true", help="Include full report link in email")
    parser.add_argument("--no-puppeteer", action="store_true", help="Skip Puppeteer PDF rendering")
    parser.add_argument("--drive-client-secrets", default=os.getenv("GOOGLE_OAUTH_CLIENT_SECRETS", ""))
    parser.add_argument("--drive-token", default=os.getenv("GOOGLE_DRIVE_TOKEN", ""))
    parser.add_argument("--drive-folder-id", default=os.getenv("GOOGLE_DRIVE_FOLDER_ID", ""))

    args = parser.parse_args()
    slug = args.slug or slugify(args.company)

    drive_client_secrets = Path(args.drive_client_secrets) if args.drive_client_secrets else None
    drive_token = Path(args.drive_token) if args.drive_token else None
    drive_folder_id = args.drive_folder_id or None

    result = export_reports(
        output_path=Path(args.output),
        slug=slug,
        company_name=args.company,
        company_url=args.company_url or None,
        reports_root=Path(args.reports_root),
        model_label=args.model_label,
        include_full_link=args.include_full_link,
        use_puppeteer=not args.no_puppeteer,
        drive_client_secrets=drive_client_secrets,
        drive_token_path=drive_token,
        drive_folder_id=drive_folder_id,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
