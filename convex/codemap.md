# Convex Backend — `convex/` Directory Codemap

**Scope:** Convex backend for multi-country task management system serving 9 Asia-Pacific markets.

---

## 1. Responsibility

### Core Purpose
Provides realtime backend as a service (BaaS) for task management with strict per-country data isolation and multi-role user access. All data operations are serverless queries/mutations with automatic type safety via Convex's codegen.

### Data Ownership
- **`tasks`** — Country-specific task tracks with per-country sequential IDs, owned by users, tracked by deadline and status
- **`users`** — Authentication-adjacent user records with role-based access control (RBAC) and country assignment
- **`countries`** — Static reference table of 9 supported country codes and display names

### Access Pattern
Queries are read-only, realtime-subscribable; mutations are transactional, optimistic-update safe. All operations run within Convex's ACID transaction model with OCC (optimistic concurrency control).

---

## 2. Data Model (schema.ts)

### Tables

#### `tasks`
```typescript
id: number                  // per-country sequential, starts at 1 per country
countryCode: "cn" | "jp" | "au" | "my" | "id" | "in" | "sg" | "hk" | "th"
date: string                // task creation date (YYYY-MM-DD)
description: string         // free-text task description
owner: string               // accountable person or team name
deadline: string            // due date (YYYY-MM-DD)
status: "not started" | "in progress" | "completed"
createdAt: number           // epoch ms
updatedAt: number           // epoch ms
```

**Indexes:**
- `by_country` → `[countryCode]`
- `by_country_and_id` → `[countryCode, id]` (composite, sortable by id desc)

**Query access:** `by_country_and_id` used for all per-country lookups and sorting; `by_country` available for existence/count scans.

#### `users`
```typescript
email: string               // unique identifier (indexed)
name: string
role: "admin" | "viewer" | "editor"
status: "active" | "inactive" | "pending"
countries: string[]         // array of authorized countryCodes, empty = no access
createdAt: number
updatedAt: number
createdBy: string | null    // audit trail: who created this user
lastLoginAt: number | null  // audit trail: last successful login timestamp
```

**Indexes:**
- `by_email` → `[email]` (unique constraint emulation)
- `by_status` → `[status]` (filter by account state)
- `by_role` → `[role]` (filter by privilege level)

**Purpose:** Supports login tracking, audit, and per-user country scoping for data access control.

#### `countries`
```typescript
code: countryCode           // matches tasks.countryCode exactly
name: string                // display name (e.g., "Singapore")
```

**Indexes:**
- `by_code` → `[code]` (unique lookup)

**Purpose:** Static reference data for country display; seeded but not modified at runtime.

### Validation Constraints

All enforced via `convex/values`:
- **countryCode:** 9 literal union values (`cn`, `jp`, `au`, `my`, `id`, `in`, `sg`, `hk`, `th`)
- **taskStatus:** 3-state finite machine
- **userRole:** RBAC triad
- **userStatus:** lifecycle triad

---

## 3. Operations

### tasks.ts — Task Management Module

#### Queries (read-only)

| Function | Purpose | Args | Returns |
|----------|---------|------|---------|
| `getTasksByCountry` | Fetch all tasks for one country, sorted by id asc | `{ countryCode }` | `{ countryCode, nextId, tasks[] }` |
| `getAllTasks` | Fetch all tasks across all countries, sorted country→id | `{}` | `Task[]` |

**Details:**
- `getTasksByCountry` calculates `nextId` by finding max id in country + 1. Used by UI to suggest next sequential task number.
- `getAllTasks` sort order: lex by `countryCode` then `id`. Used for admin/global views only.

#### Mutations (writes)

| Function | Purpose | Args | Side-effects |
|----------|---------|------|--------------|
| `createTask` | Insert new task with sequential id per country | `{ countryCode, date, description, owner, deadline, status, id? }` | Inserts with `createdAt=now`, `updatedAt=now`. If `id` omitted, auto-increment from latest in country via `by_country_and_id` desc query. |
| `updateTask` | Partial update of mutable fields | `{ id, countryCode, date?, description?, owner?, deadline?, status? }` | Patches `updatedAt=now`. Validates task exists via `by_country_and_id` composite lookup. Fails if `(countryCode, id)` not found. |
| `deleteTask` | Hard delete task record | `{ id, countryCode }` | Physical delete via `db.delete()`. Returns `{ok, deleted}` boolean flag. |
| `seedTasks` | Bootstrap initial data for all countries | `{}` | Idempotent: checks existing countries/tasks before insert. Populates `countries` table from `COUNTRY_NAMES` and `tasks` from `TASK_SEEDS`. Normalizes legacy status values (`"done"`→`"completed"`, `"delayed"`→`"not started"`). |

**Design notes:**
- All mutations explicitly index via `by_country_and_id` to avoid cross-country ID collision.
- `createTask` uses `order("desc").first()` to compute next sequential ID; works because tasks never deleted (holes acceptable if intermediate deletes occur).
- `seedTasks` is intended for dev/initial setup only; no production re-seeding safeguards.

### users.ts — User Management Module

#### Queries (read-only)

| Function | Purpose | Args | Returns |
|----------|---------|------|---------|
| `listUsers` | All users, newest first | `{}` | `User[]` sorted desc by `createdAt` |
| `listUsersByStatus` | Filter users by account status | `{ status }` | `User[]` sorted desc by `createdAt` |
| `getUserByEmail` | Lookup by unique email | `{ email }` | `User | null` |
| `getUserById` | Lookup by Convex document ID | `{ id }` | `User | null` |
| `getUserStats` | Aggregated user counts by role/status | `{}` | `{ total, active, inactive, pending, admins, editors, viewers }` |

**Details:**
- `getUserStats` runs full table scan (`collect()`) then filters in-memory. Acceptable for small user base (< 1000). Not indexed for count aggregation — intentional simplicity.

#### Mutations (writes)

| Function | Purpose | Args | Validation |
|----------|---------|------|------------|
| `createUser` | Register new user | `{ email, name, role, status?, countries?, createdBy? }` | Email uniqueness enforced via `by_email` index lookup; throws if duplicate. Defaults: `status="active"`, `countries=[]`. |
| `updateUser` | Patch mutable user fields | `{ id, email?, name?, role?, status?, countries? }` | Fetches by `_id`. If `email` changed, re-checks uniqueness. Returns `{ok, id}`. |
| `deleteUser` | Remove user account | `{ id }` | Returns `{ok, deleted, error?}`. Safe no-op if not found. |
| `recordLogin` | Update last login timestamp | `{ email }` | Lookup by email via `by_email`; patch `lastLoginAt=now`, `updatedAt=now`. Returns `{ok}` or `{ok:false, error}`. |
| `seedInitialAdmin` | Create initial admin user for deployment | `{ email, name }` | Creates user with `role="admin"`, `status="active"`, `countries=[all 9]`. Idempotent — returns `{ok:false}` if admin already exists. |

**Design notes:**
- `countries` field controls per-country data access; empty array means no country-specific task visibility.
- `createdBy` audit field tracks who provisioned the account (usually "system" or another user email).
- All mutations update `updatedAt` on every write.

### seedData.ts — Seed Constants Module

**Exports:**
- `COUNTRY_NAMES` — `Record<countryCode, string>` map of all 9 country display names
- `TASK_SEEDS` — Nested object keyed by `countryCode`, each with `nextId: number` and `tasks[]` matching task schema

**Structure:**
```typescript
TASK_SEEDS = {
  hk: { nextId: 12, tasks: [ {id, date, description, owner, deadline, status}, ... ] },
  sg: { nextId: 11, tasks: [...] },
  my: { nextId: 8,  tasks: [...] },
  th: { nextId: 10, tasks: [...] }
  // cn, jp, au, id, in entries not yet seeded (empty/unused as of this snapshot)
}
```

**Purpose:**
- Drives `seedTasks` mutation to populate initial demo/production data.
- `nextId` values used to set initial sequential counter per country; `seedTasks` does not reset `nextId` counter table — relies on runtime `createTask` auto-increment for new inserts post-seed.

---

## 4. Code Architecture

### File Organization
```
convex/
├─ schema.ts           # Table definitions + indexes + value constraints
├─ tasks.ts            # Task CRUD + country queries + seed mutation
├─ users.ts            # User CRUD + stats + login tracking + admin seed
├─ seedData.ts         # Static data constants (countries, initial tasks)
├─ tsconfig.json       # TypeScript configuration for Convex server
├─ codemap.md          # This file
└─ _generated/         # Auto-generated Convex client/server types (do not edit)
   ├─ api.d.ts         # Public/internal API typings
   ├─ api.js           # Runtime API bindings
   ├─ server.d.ts      # Server module typings
   ├─ server.js        # Runtime server bindings
   ├─ dataModel.d.ts   # Full data model types
   └─ ...
```

### Type Safety Strategy
- **Convex codegen** (`npx convex dev`) regenerates `_generated/` on schema changes
- All files import `v` from `convex/values` for runtime schema validation
- Local type aliases (`CountryCode`, `TaskStatus`) duplicated per-file for IDE support; no shared type module to avoid circular deps

### Index-First Query Design
Every read operation uses an explicit index chain (`.withIndex(...)`) — never relies on primary key scan. This guarantees O(log n) performance even as per-country task sets grow.

### Mutability Pattern
- **Tasks:** `createdAt`/`updatedAt` set on insert; `updatedAt` patched on every mutation
- **Users:** Same timestamp pattern plus optional `lastLoginAt` updated by `recordLogin`
- **Countries:** Immutable after seed — no update/delete paths exist

---

## 5. Integration Points

### Frontend (outside this directory)
Frontend code imports generated API via:
```typescript
import { api, internal } from "../convex/_generated/api";
```
- `api.*` → public functions (callable by client)
- `internal.*` → server-only (not exposed to client)
- All functions in `tasks.ts` and `users.ts` are `export const fnName = query/mutation(...)` and therefore public by default (Convex treats all exports as public unless marked internal via separate `_generated/internal` module).

### Authentication (not implemented here)
No auth checks in current mutations/queries. Production hardening requires:
- `ctx.auth.getUserIdentity()` guard in each mutation
- Row-level security: filter `tasks` by user's `countries` array
- Admin-only guards for `seed*` mutations

### Deployment / CI
- `convex dev` — watches `schema.ts`, regenerates `_generated/` on change
- `npx convex deploy` — uploads schema + code to Convex cloud
- `seedTasks` mutation must be called manually post-deploy to populate reference data

---

## 6. Data Flow Patterns

### Task Read (per-country)
```
Client calls api.tasks.getTasksByCountry({ countryCode: "sg" })
  → Convex routes to tasks.getTasksByCountry query
  → Query: db.query("tasks").withIndex("by_country_and_id", q.eq("countryCode", "sg"))
  → Results sorted by id asc, nextId computed from max id
  → Returned to client via realtime subscription or single fetch
```

### Task Create
```
Client calls api.tasks.createTask({ countryCode: "sg", ... })
  → Convex routes to tasks.createTask mutation (transactional)
  → Mutation: db.query("tasks").withIndex("by_country_and_id", q.eq("countryCode", "sg")).order("desc").first()
  → Computes nextId = (latest?.id ?? 0) + 1
  → Inserts: db.insert("tasks", { id: nextId, countryCode, ..., createdAt: now, updatedAt: now })
  → Convex ACID commit; subscribers notified
```

### User Login Tracking
```
Client calls api.users.recordLogin({ email: "user@example.com" })
  → Query by email via by_email index
  → Patch: { lastLoginAt: now, updatedAt: now }
  → Returns { ok: true } or error
```

### Seeding All Data
```
Admin triggers api.tasks.seedTasks()
  → Inserts all 9 countries if missing (idempotent)
  → For each country in TASK_SEEDS, inserts tasks if not already present
  → Returns summary { ok, countriesInserted, tasksInserted, totalCountries }
```

---

## 7. Design Rationale

### Country-First Partitioning
Every task operation requires a `countryCode` argument; no "global" task operations exist except `getAllTasks` (admin-only use). This enforces geographic data isolation at the API layer — a country's tasks cannot be queried without explicitly specifying the country code.

### Per-Country Sequential IDs
Tasks use `id: number` that restarts at 1 per country (not globally unique). Design choice: human-readable identifiers for local teams ("Task SG-7"). Composite uniqueness enforced implicitly by `(countryCode, id)` pair combined with `by_country_and_id` index.

### Index-Only Access
No table scans. Every query specifies `.withIndex(...)` ensuring predictable performance. `tasks` has 2 indexes; `users` has 3; `countries` has 1.

### Seed Data as Source of Truth
`seedData.ts` holds the authoritative initial dataset for each country. `seedTasks` is the only path to insert initial demo data — no separate SQL/CSV import path. This keeps data versioned in code.

### No Soft-Delete
`deleteTask` performs hard delete. Tasks are small; retention not a concern. If audit trail needed, move to `tasks_archived` table instead.

### Minimal RBAC
`users.role` field exists but unused in queries/mutations. Frontend must enforce UI restrictions; backend trusts client. Enhancement: add role-based guards to mutations (e.g., only `admin` can `createUser`).

---

## 8. Open Questions / Tech Debt

| Item | Status | Notes |
|------|--------|-------|
| Auth integration | Missing | No `ctx.auth` checks. All operations are effectively anonymous. |
| User→task ownership validation | Missing | `updateTask`/`deleteTask` do not verify requesting user owns the task or has admin rights. |
| Cross-country task linking | Not supported | Task dependencies across countries would require schema extension. |
| Task filtering by status/owner | Not indexed | Filtering requires full scan; consider adding compound indexes if needed. |
| Countries table maintenance | Manual | No mutation to update `countries.name`; schema change required for new country. |
| Task history/audit trail | Absent | No history table — updates are in-place only. |
| Pagination | Not implemented | `getTasksByCountry` returns all tasks per country; pagination not yet needed. |

---

**Last updated:** 2026-05-04
**Convex schema version:** 1 (inferred from `schema.ts`)
**Countries supported:** cn, jp, au, my, id, in, sg, hk, th (9 total)