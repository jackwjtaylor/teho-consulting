# Portal Integration API Contract (Draft)

This document defines the initial API contracts for the portal integration. Update as endpoints evolve.

## 1) Activity Analysis service

Base URL: `ACTIVITY_ANALYSIS_API_URL`

Auth:
- `X-Ingest-Token` header for org-scoped access (recommended).
- Optional `X-Org-Id` for report scoping when tokens are not used.

### Ingestion
- `POST /events/upload` (CSV)
- `POST /events/upload-with-images` (CSV + zip)
- `POST /events/bulk` (JSON)

### Reporting
- `GET /reports/mekko`
- `GET /reports/taxonomy-summary?level=1|2|3`
- `GET /reports/activity-summary`
- `GET /reports/confidence-alerts`
- `GET /reports/mekko.csv`

### Admin (available)
- `POST /admin/orgs` (create org + token)
- `GET /admin/orgs`
- `POST /admin/orgs/{id}/rotate-token`
- `GET /admin/deployments`
- `POST /admin/deployments`
- `POST /admin/deployments/{id}`
- `POST /admin/deployments/{id}/status`
- `GET /admin/devices` (enrolled devices + status)

### Device management
- `POST /devices/heartbeat` (device status + deployment config)

## 2) Consulting agent service

Base URL: `CONSULTING_API_URL`

### Queue + report generation
- `POST /requests` (enqueue)
- `GET /requests?status=queued`
- `POST /requests/{id}/run` (execute pipeline)
- `GET /requests/{id}/status`

### Assets
- `GET /reports/{slug}` (metadata)
- `GET /reports/{slug}/assets` (HTML/PDF/email paths)

### Admin (planned)
- `POST /clients` (create client, metadata)
- `POST /clients/{id}/assign-user`
- `POST /outreach/events`

## 3) Shared data (Supabase)

Tables (proposed):
- `orgs` (id, name, settings)
- `deployments` (org_id, start/end, sampling config)
- `devices` (deployment_id, device_id, status, last_seen)
- `reports` (client_slug, report_key, storage paths)

## 4) Notes

- This contract is a draft; update as endpoints are implemented.
- Portal should never request user-level activity from Activity Analysis.
