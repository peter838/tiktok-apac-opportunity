# api/

## Responsibility

Proxy layer for external API routing, providing CORS bypass and fallback handling between Convex (primary) and Supabase/SourceSage API (legacy). Enables browser clients to access cross-origin backends through same-origin endpoints.

## Design

### Architecture Pattern
**Fallback/Proxy Pattern** — Environment-based routing determines backend target:
- `CONVEX_URL` configured → Routes to Convex (primary backend)
- `SUPABASE_URL` configured → Routes to Supabase (legacy fallback)
- Default → Local Convex development server (`http://127.0.0.1:3210`)

### Key Abstractions

| File | Purpose | Timeout | Status |
|------|---------|---------|--------|
| `sa-proxy.js` | SourceSage API proxy | 25s upstream | Active |
| `convex-proxy.js` | Convex API proxy | No timeout | Active |
| `tasks.js` | Task API route | N/A | **DEPRECATED** (returns 410) |

### Error Handling Strategy
- **Timeout handling**: Race condition with Promise.race (25s for SA API)
- **Empty data responses**: No demo data — returns `_apiUnavailable: true` flags
- **Special endpoint handling**: `orders/values` returns explicit errors (504/502) rather than masked zero values
- **Retry logic**: Client-side retry via `SAAPIClient` (max 2 retries, exponential backoff)

### CORS Handling
All proxies set identical CORS headers:
```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: POST, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
```

## Flow

```
Browser Client
      │
      ├── GET/POST /api/sa-proxy ──→ sa-proxy.js ──→ SA API (sourcesage.co)
      │                                   │
      │                                   └─ Validates endpoint prefix (/v1.0/agent/analytics/ OR /v1.0/agent/orders/)
      │                                   └─ Timeouts after 25s → Empty data response
      │                                   └─ Errors → Empty data with _apiUnavailable flag
      │
      ├── GET/POST /api/convex-proxy ──→ convex-proxy.js ──→ Convex
      │                                    │
      │                                    └─ Forwards to CONVEX_URL from env
      │
      └── GET/POST /api/tasks ──→ tasks.js ──→ 410 DEPRECATED
                                        │
                                        └─ "Task Tracker now reads/writes through Convex client functions"
```

### Request/Response Shapes

**SA Proxy (`POST /api/sa-proxy`)**:
```json
{
  "endpoint": "/v1.0/agent/analytics/tracking/entity-margin",
  "payload": { "from_date": "2025-01-01", "to_date": "2025-12-31", "region": "SG" }
}
```

**Convex Proxy (`POST /api/convex-proxy`)**:
```json
{
  "path": "tasks:getTasksByCountry",
  "body": { "args": { "country": "sg" } }
}
```

## Integration

### Upstream Dependencies
- **SourceSage API** (`https://api-dhl-dev.sourcesage.co/api`) — Primary data source for analytics
  - Requires `X-SA-AGENT-KEY` header for authentication
  - Endpoints: `/v1.0/agent/analytics/*` and `/v1.0/agent/orders/*`
- **Convex** — Task tracking backend (configured via `CONVEX_URL` env var)

### Downstream Consumers

| Consumer | File | Integration Method |
|----------|------|-------------------|
| Dashboard | `js/main-page-data.js` | `MainPageAPIClient` → `/api/sa-proxy` |
| Subpage | `sa-api-client.js` | `SAAPIClient` → `/api/sa-proxy` |
| Task Tracker | `shared.js` + `convex-client.js` | Direct Convex client (bypasses api/tasks) |

### Configuration
```bash
# Convex URL (optional, defaults to localhost for dev)
CONVEX_URL="https://your-deployment.convex.cloud"

# SA API key (hardcoded in sa-proxy.js - should migrate to env)
# Currently: 3f03537cfb4c4ac089e50b08e4e0471f
```

### Migration Status
- **Task API**: Fully migrated to Convex client functions — `api/tasks.js` deprecated
- **Analytics API**: Currently using SA proxy — planned migration to Convex pending
- **Fallback behavior**: Client-side retry in `SAAPIClient`, empty data responses prevent UI failures