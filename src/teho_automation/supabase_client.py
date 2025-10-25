"""Utilities for interacting with Supabase."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import mimetypes
import requests

from dotenv import load_dotenv

try:  # pragma: no cover - import guarded for environments without dependency
    from supabase import Client, create_client
except Exception:  # pragma: no cover - handled gracefully
    Client = None  # type: ignore
    create_client = None  # type: ignore

TABLE_NAME = "briefing_requests"
REPORTS_BUCKET = "reports"
ATTACHMENTS_BUCKET = os.getenv("ATTACHMENTS_BUCKET", "briefing-uploads")


@dataclass
class SupabaseResult:
    success: bool
    message: str = ""
    data: Optional[Any] = None


def _load_env_credentials() -> Optional[Tuple[str, str]]:
    """Return Supabase URL and service key if available."""
    env_path = Path(os.getenv("DOTENV_PATH", Path.cwd() / ".env"))
    if env_path.exists():
        load_dotenv(dotenv_path=env_path, override=False)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        return None
    return url, key


def _build_client() -> Optional["Client"]:
    """Return a Supabase client if credentials are available."""
    credentials = _load_env_credentials()
    if credentials is None or create_client is None:
        return None
    try:
        url, key = credentials
        return create_client(url, key)
    except Exception:  # pragma: no cover - network failure handled by caller
        return None


def insert_briefing_request(record: Dict[str, Any]) -> SupabaseResult:
    """Insert or upsert a briefing request into Supabase."""
    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    try:
        response = (
            client.table(TABLE_NAME)
            .upsert(record, on_conflict="slug", ignore_duplicates=False)
            .execute()
        )
        return SupabaseResult(success=True, data=response.data or {}, message="Upserted")
    except Exception as exc:  # pragma: no cover - network error not deterministic in tests
        return SupabaseResult(success=False, message=str(exc))


def update_briefing_status(slug: str, status: str) -> SupabaseResult:
    """Update status for a given slug."""
    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    try:
        response = (
            client.table(TABLE_NAME)
            .update({"status": status})
            .eq("slug", slug)
            .execute()
        )
        return SupabaseResult(success=True, data=response.data or {}, message="Updated")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))


def fetch_requests(status: Optional[str] = None, limit: int = 50) -> SupabaseResult:
    """Fetch briefing requests, optionally filtered by status."""
    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    try:
        query = client.table(TABLE_NAME).select("*").order("requested_at", desc=True)
        if status:
            query = query.eq("status", status)
        if limit:
            query = query.limit(limit)
        response = query.execute()
        return SupabaseResult(success=True, data=response.data or [], message="Fetched")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))


def ensure_reports_bucket() -> SupabaseResult:
    """Ensure the reports storage bucket exists."""
    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    try:
        storage = client.storage
        buckets = storage.list_buckets()
        names = [getattr(bucket, "name", None) for bucket in buckets]
        if REPORTS_BUCKET not in names:
            storage.create_bucket(REPORTS_BUCKET, public=False)
        return SupabaseResult(success=True, message="Bucket ready")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))


def upload_report_asset(slug: str, file_path: Path, folder: Optional[str] = None) -> SupabaseResult:
    """Upload a report asset to Supabase storage under reports/<slug>/..."""

    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    storage = client.storage
    destination = f"{slug}/{file_path.name}" if not folder else f"{slug}/{folder}/{file_path.name}"
    mime_type, _ = mimetypes.guess_type(str(file_path))
    file_options = {"content-type": mime_type or "application/octet-stream"}

    resource = storage.from_(REPORTS_BUCKET)
    data = file_path.read_bytes()

    try:
        resource.upload(destination, data, file_options=file_options)
    except Exception:
        try:
            resource.update(destination, data, file_options=file_options)
        except Exception as exc:  # pragma: no cover
            return SupabaseResult(success=False, message=str(exc))

    return SupabaseResult(success=True, message=destination)


def fetch_briefing_attachments(request_id: str) -> SupabaseResult:
    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    try:
        response = (
            client.table("briefing_attachments")
            .select("id, file_name, storage_path, mime_type, size_bytes, uploaded_by, created_at")
            .eq("request_id", request_id)
            .order("created_at", desc=True)
            .execute()
        )
        return SupabaseResult(success=True, data=response.data or [], message="Fetched")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))


def download_attachment_blob(storage_path: str, bucket: Optional[str] = None) -> SupabaseResult:
    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    bucket_name = bucket or ATTACHMENTS_BUCKET
    storage = client.storage
    resource = storage.from_(bucket_name)
    try:
        data = resource.download(storage_path)
        return SupabaseResult(success=True, data=data, message="Downloaded")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))


def upsert_report_entry(record: Dict[str, Any]) -> SupabaseResult:
    """Upsert a report entry into the public.reports table."""

    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    try:
        response = (
            client.table("reports")
            .upsert(record, on_conflict="client_slug,report_key")
            .execute()
        )
        return SupabaseResult(success=True, data=response.data or {}, message="Report stored")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))


def set_portal_user_access(
    email: str,
    client_slug: str,
    *,
    client_id: Optional[str] = None,
) -> SupabaseResult:
    """Attach client metadata to a Supabase auth user so portal RLS can restrict access."""

    credentials = _load_env_credentials()
    if credentials is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    if not email or not client_slug:
        return SupabaseResult(success=False, message="Email and client_slug are required")

    base_url = credentials[0].rstrip("/")
    service_key = credentials[1]
    admin_base = f"{base_url}/auth/v1/admin"
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }

    try:
        lookup = requests.get(
            f"{admin_base}/users",
            params={"email": email},
            headers=headers,
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover - network failure
        return SupabaseResult(success=False, message=f"User lookup failed: {exc}")

    if lookup.status_code != 200:
        return SupabaseResult(success=False, message=f"User lookup failed: {lookup.text}")

    payload = lookup.json() if lookup.content else {}
    users = payload.get("users") if isinstance(payload, dict) else None
    if not users:
        return SupabaseResult(success=False, message=f"No user found for {email}")

    user = users[0]
    user_id = user.get("id")
    if not user_id:
        return SupabaseResult(success=False, message="Supabase user record missing id")

    metadata = (user.get("user_metadata") or {}).copy()
    metadata.update({"client_slug": client_slug})
    if client_id:
        metadata.setdefault("client_id", client_id)

    app_metadata = (user.get("app_metadata") or {}).copy()
    app_metadata.update({"client_slug": client_slug})
    if client_id:
        app_metadata.setdefault("client_id", client_id)

    update_body: Dict[str, Any] = {
        "user_metadata": metadata,
        "app_metadata": app_metadata,
    }

    try:
        update_resp = requests.patch(
            f"{admin_base}/users/{user_id}",
            headers=headers,
            json=update_body,
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover - network failure
        return SupabaseResult(success=False, message=f"User update failed: {exc}")

    if update_resp.status_code >= 400:
        return SupabaseResult(success=False, message=f"User update failed: {update_resp.text}")

    return SupabaseResult(success=True, message="Portal access updated", data=update_resp.json())


def log_outreach_event(payload: Dict[str, Any]) -> SupabaseResult:
    """Record an outreach event (send, open, click, reply) for analytics."""

    required = {"client_slug", "contact_email", "event_type", "channel"}
    if not required.issubset(payload.keys()):
        return SupabaseResult(success=False, message="Missing required outreach fields")

    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    data = {
        "client_slug": payload["client_slug"],
        "contact_email": payload["contact_email"],
        "event_type": payload["event_type"],
        "channel": payload.get("channel", "email"),
        "report_key": payload.get("report_key"),
        "notes": payload.get("notes"),
        "metadata": payload.get("metadata"),
    }

    try:
        response = client.table("outreach_events").insert(data).execute()
        return SupabaseResult(success=True, data=response.data or {}, message="Outreach logged")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))


def fetch_automation_runs(statuses: List[str], limit: int = 10) -> SupabaseResult:
    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    try:
        query = (
            client.table("automation_runs")
            .select("id, client_slug, action, status, payload, triggered_by, created_at")
            .order("created_at", desc=False)
        )
        if statuses:
            query = query.in_("status", statuses)
        if limit:
            query = query.limit(limit)
        response = query.execute()
        return SupabaseResult(success=True, data=response.data or [], message="Fetched")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))


def update_automation_run(
    run_id: str,
    *,
    status: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> SupabaseResult:
    client = _build_client()
    if client is None:
        return SupabaseResult(success=False, message="Supabase not configured")

    patch: Dict[str, Any] = {"updated_at": datetime.utcnow().isoformat()}
    if status:
        patch["status"] = status
    if payload is not None:
        patch["payload"] = payload

    try:
        response = client.table("automation_runs").update(patch).eq("id", run_id).execute()
        return SupabaseResult(success=True, data=response.data or {}, message="Updated")
    except Exception as exc:  # pragma: no cover
        return SupabaseResult(success=False, message=str(exc))
