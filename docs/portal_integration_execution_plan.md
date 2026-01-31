# Portal Integration Execution Plan

Goal: unify the Teho Consulting automation (currently Streamlit + CLI) and the Activity Analysis product into a single portal UI (Next.js `teho-portal`) with shared auth, tenancy, and deployment management.

## Current state (Feb 2025)

- Consulting automation runs via CLI + Streamlit; portal already manages reports, QA, and queue.
- Activity Analysis runs as a FastAPI service with an admin-less dashboard.
- No unified UI for deployments, orgs, or device monitoring.

## Guiding decisions

- Single front-end: `../teho-portal` (Next.js + Supabase).
- Separate backends for each product (consulting agent + activity analysis).
- Supabase is the shared data plane for auth, orgs, deployments, and assets.
- Aggregated reporting only for Activity Analysis (no user-level UI).

## Phase 0: Alignment & contracts (Week 1)

Deliverables
- [ ] API contract doc for both services (endpoints + payloads)
- [ ] Shared data model in Supabase (orgs, deployments, run logs, assets)
- [ ] Auth decision: token vs. Supabase JWT for service calls

## Phase 1: Backend readiness (Weeks 1-3)

Activity Analysis service
- [x] Ingest tokens + org scoping
- [x] Aggregated-only mode
- [x] Deployment config endpoint (sampling rate, start/end date, allowlist)
- [x] Device enrollment endpoint + device status tracking
- [ ] Report export endpoint (PDF/CSV packaged for portal)

Consulting agent service
- [ ] FastAPI wrapper for the CLI actions (queue, generate, package)
- [ ] Job status endpoint (progress, errors)
- [ ] Upload outputs to Supabase storage

## Phase 2: Portal integration (Weeks 3-6)

Core UI
- [x] Deployment dashboard (Activity Analysis)
- [x] Device list + health status
- [ ] Report viewer unified across products
- [x] Admin controls for orgs, tokens, config

Auth & RLS
- [ ] Supabase RLS policies for org-scoped data
- [ ] Service role usage only where required

## Phase 3: Rollout readiness (Weeks 6-8)

- [ ] Pilot workflow: create org, enroll devices, start/stop deployment
- [ ] Executive pack export (PDF + summary)
- [ ] QA checklist integration for Activity Analysis
- [ ] Billing/entitlements model for deployments

## Phase 4: Streamlit deprecation (Weeks 8-10)

- [ ] Replicate Streamlit flows in portal
- [ ] Internal fallback for 1 release
- [ ] Remove Streamlit dependency

## Operational checklist (client deployment)

- [ ] Confirm data capture window + consent approach
- [ ] Approve taxonomy + value tiers
- [ ] Pilot 25-50 devices
- [ ] Quality review (confidence + low-value share)
- [ ] Full rollout
- [ ] Executive pack + automation backlog

## Notes

- Update weekly; add dates and owners when tasks move to in-progress.
- Track dependencies and client commitments here.

## Update log

- 2025-02-10: Plan created.
- 2025-02-11: Added Activity Analysis deployment dashboard, device health, and admin controls in the portal.
- 2025-02-11: Added Activity Analysis report preview (Mekko + L1 summary) inside the portal admin.
