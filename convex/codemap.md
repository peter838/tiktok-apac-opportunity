# Convex Backend — `convex/` Directory Codemap

**Scope:** Convex backend for a multi-country, multi-entity task management system serving 9 Asia-Pacific markets across 8 client entities (DHL, JLL, TikTok, Cushman & Wakefield, SMRT, Certis, Toll Group, Prudential).

---

## 1. Responsibility

### Core Purpose
Provides realtime backend as a service (BaaS) for task management with strict per-country and per-entity data isolation, multi-role user access, and shared/separate dashboards per client entity. All data operations are serverless queries/mutations with automatic type safety via Convex's codegen.

### Data Ownership
- **`tasks`** — Per-entity, per-country task tracks with sequential IDs per `(countryCode, entity)` pair, owned by users, tracked by deadline and status
- **`users`** — Authentication-adjacent user records with role-based access control (RBAC), entity assignment, and country scope
- **`countries`** — Static reference table of 10 supported country codes and display names (includes `vn` even though the country folders are not yet fully seeded)

### Access Pattern
Queries are read-only and realtime-subscribable; mutations are transactional and optimistic-update safe. All operations run within Convex's ACID transaction model with OCC (optimistic concurrency control).

### Entity Isolation Model
Every read/write that touches `tasks` or `users` takes an optional `entity` argument. Records are filtered through a `matchesEntity()` helper that treats missing `entity` as `"dhl"` for backward compatibility with pre-entity-scoping rows. This gives every client dashboard a clean view of its own data without needing separate Convex deployments.

---

## 2. Data Model (schema.ts)

### Tables

#### `tasks`
```typescript
id: number                  // per-(countryCode, entity) sequential, starts at 1
countryCode: "cn" | "jp" | "au" | "my" | "id" | "in" | "sg" | "hk" | "th" | "vn"
entity: "dhl" | "jll" | "tiktok" | "cushman-wakefield" | "smrt" | "certis" | "toll-group" | "prudential"  // optional; legacy rows without it resolve to "dhl"
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
- `by_country_and_id` → `[countryCode, `id`] (composite, sortable by `id` asc/desc)

**Notes:**
- `entity` is `v.optional(entity)` in the schema. All new writes should include it; reads filter by it. The pre-`entity` rows are still queryable because `matchesEntity` defaults to `"dhl"`.
- ID uniqueness is enforced by the `(countryCode, id)` composite — adding `entity` as a third dimension means the same numeric `id` can exist for two different entities within the same country (e.g. `sg:1/dhl` and `sg:1/tiktok` are distinct rows). Mutations always require `entity` in args to disambiguate.

#### `users`
```typescript
email: string               // unique identifier (indexed)
name: string
entity: "dhl" | "jll" | "tiktok" | "cushman-wakefield" | "smrt" | "certis" | "toll-group" | "prudential"  // optional; defaults to "dhl"
role: "admin" | "viewer" | "editor" | "staff"
status: "active" | "inactive" | "pending"
countries: ("cn" | "jp" | "au" | "my" | "id" | "in" | "sg" | "hk" | "th" | "vn")[]   // empty = no access
createdAt: number
updatedAt: number
createdBy: string | null    // audit trail: who created this user
lastLoginAt: number | null  // audit trail: last successful login timestamp
isActive: boolean | null    // optional flag (current code uses `status` for active/inactive)
passwordHash: string | null // optional, set by the auth layer
username: string | null     // optional alternate login handle
```

**Indexes:**
- `by_email` → `[email]` (unique constraint emulation, scoped to entity)
- `by_status` → `[status]` (filter by account state)
- `by_role` → `[role]` (filter by privilege level)

**Notes:**
- Email uniqueness is **per-entity**, not global. The same email can register as a user in two different entities (e.g. a person who wears two hats across `dhl` and `tiktok`). `createUser` enforces this via the `matchesEntity` check after the email index lookup.
- `isActive` and `passwordHash` exist in the schema for forward compatibility (auth migration) but are not yet read or written by any function in `users.ts`. All access control currently routes through `status` and the in-`role` checks.

#### `countries`
```typescript
code: "cn" | "jp" | "au" | "my" | "id" | "in" | "sg" | "hk" | "th" | "vn"   // 10 values
name: string                // display name (e.g., "Singapore")
```

**Indexes:**
- `by_code` → `[code]` (unique lookup)

**Notes:**
- The `v.union` for `countryCode` includes 10 values. `COUNTRY_NAMES` in `seedData.ts` matches all 10. However, `TASK_SEEDS` only populates `hk`, `sg`, `my`, `th` — the other 6 countries (`cn`, `jp`, `au`, `id`, `in`, `vn`) are valid for writes but have no seed data. New entities can still create tasks in any of the 10 countries; they'll just start at `id: 1`.
- `countries` is treated as immutable after seeding — no update or delete functions exist for this table.

### Validation Constraints

All enforced via `convex/values`:
- **countryCode:** 10 literal union values
- **entity:** 8 literal union values (dhl, jll, tiktok, cushman-wakefield, smrt, certis, toll-group, prudential)
- **taskStatus:** 3-state finite machine
- **userRole:** 4-state RBAC (admin, viewer, editor, staff)
- **userStatus:** 3-state lifecycle

---

## 3. Operations

### tasks.ts — Task Management Module

#### Queries (read-only)

| Function | Purpose | Args | Returns |
|----------|---------|------|---------|
| `getTasksByCountry` | Fetch all tasks for one country, filtered by entity, sorted by id asc | `{ countryCode, entity? }` | `{ countryCode, nextId, tasks[] }` |
| `getAllTasks` | Fetch all tasks across all countries for one entity, sorted country→id | `{ entity? }` | `Task[]` |

**Details:**
- `getTasksByCountry` calculates `nextId` from the filtered set's max `id` + 1. Used by UI to suggest the next sequential task number for the active dashboard.
- `getAllTasks` sort order: lex by `countryCode` then numeric `id`. Used for admin/global views per entity.
- Both queries use the `by_country_and_id` index then filter in-memory by entity. For very large datasets, consider adding `by_entity` or `by_entity_and_country` indexes.

#### Mutations (writes)

| Function | Purpose | Args | Side-effects |
|----------|---------|------|--------------|
| `createTask` | Insert new task with sequential id per (country, entity) | `{ countryCode, date, description, owner, deadline, status, id?, entity? }` | Inserts with `createdAt=now`, `updatedAt=now`. If `id` omitted, auto-increment from latest in `(country, entity)` via `by_country_and_id` desc query. Defaults `entity` to `"dhl"` if omitted. |
| `updateTask` | Partial update of mutable fields | `{ id, countryCode, entity?, date?, description?, owner?, deadline?, status? }` | Patches `updatedAt=now`. Finds the task by `(countryCode, id)` then matches entity via `matchesEntity`. Throws if not found. |
| `deleteTask` | Hard delete task record | `{ id, countryCode, entity? }` | Physical delete via `db.delete()`. Returns `{ok, deleted}` boolean flag. |
| `seedTasks` | Bootstrap initial data for all countries into a specific entity | `{ entity? }` | Idempotent: checks existing countries/tasks before insert. Populates `countries` from `COUNTRY_NAMES` and `tasks` from `TASK_SEEDS`, tagging every inserted task with the resolved `entity`. Normalizes legacy status values (`"done"`→`"completed"`, `"delayed"`→`"not started"`). |
| `migrateEntityField` | Backfill `entity` on legacy rows that pre-date entity-scoping | `{ entity, table: "tasks" \| "users" }` | Scans all docs in the target table; patches `entity` on any doc where it is missing. Idempotent (skips docs that already have an `entity`). |

**Design notes:**
- All task mutations require `countryCode` in args. Every find/update/delete is entity-scoped via the `matchesEntity` helper after the index lookup — no global task operations exist.
- `createTask` uses `order("desc").first()` against `by_country_and_id` to compute next sequential ID. This works per-(country, entity) because `by_country_and_id` is indexed on `[countryCode, id]` and the in-memory entity filter happens after the index fetch.
- `seedTasks` is intended for dev/initial setup only; it can be re-run safely (it skips rows that already exist for the target entity). No production re-seeding safeguards.
- `migrateEntityField` is the migration path for taking an older deployment that has rows with no `entity` and tagging them as belonging to `"dhl"` (or whichever entity is passed in). Typically run once after upgrading a deployment.

### users.ts — User Management Module

#### Queries (read-only)

| Function | Purpose | Args | Returns |
|----------|---------|------|---------|
| `listUsers` | All users for an entity, newest first | `{ entity? }` | `User[]` sorted desc by `createdAt` |
| `listUsersByStatus` | Filter users by account status, scoped to entity | `{ status, entity? }` | `User[]` sorted desc by `createdAt` |
| `getUserByEmail` | Lookup by unique email (per entity) | `{ email, entity? }` | `User \| null` |
| `getUserById` | Lookup by Convex document ID, verify entity | `{ id, entity? }` | `User \| null` |
| `getUserStats` | Aggregated user counts by role/status, scoped to entity | `{ entity? }` | `{ total, active, inactive, pending, admins, editors, viewers }` |

**Details:**
- `getUserStats` runs full table scan (`collect()`) then filters by entity and counts in-memory. Acceptable for a small user base (< 1000 per entity). Not indexed for count aggregation — intentional simplicity. Note: the returned object does not currently include a `staff` count, even though `staff` is a valid role in the union.
- All user queries are entity-scoped. Omitting `entity` returns only the `"dhl"` partition (backward compat).

#### Mutations (writes)

| Function | Purpose | Args | Validation |
|----------|---------|------|------------|
| `createUser` | Register new user into an entity | `{ email, name, role, status?, countries?, createdBy?, entity? }` | Email uniqueness enforced per-entity via `by_email` index + `matchesEntity` check; throws if duplicate. Defaults: `status="active"`, `countries=[]`, `entity="dhl"`. |
| `updateUser` | Patch mutable user fields | `{ id, entity?, email?, name?, role?, status?, countries? }` | Fetches by `_id`, verifies entity via `matchesEntity`. If `email` changed, re-checks uniqueness within the target entity. Returns `{ok, id}`. |
| `deleteUser` | Remove user account from an entity | `{ id, entity? }` | Verifies entity first; safe no-op (returns `{ok: false, deleted: false, error}`) if not found or wrong entity. |
| `recordLogin` | Update last login timestamp for a user in an entity | `{ email, entity? }` | Lookup by email via `by_email`; verify entity; patch `lastLoginAt=now`, `updatedAt=now`. Returns `{ok}` or `{ok:false, error}`. |
| `seedInitialAdmin` | Create initial admin user for a deployment | `{ email, name, entity? }` | Creates user with `role="admin"`, `status="active"`, `countries` set to all 10 country codes. Idempotent — returns `{ok:false}` if an admin with that email already exists in the target entity. |

**Design notes:**
- `countries` field controls per-country data access; empty array means no country-specific task visibility.
- `createdBy` audit field tracks who provisioned the account (usually `"system"` or another user's email).
- All mutations update `updatedAt` on every write.
- Email uniqueness is **per-entity** — the same email can register as a separate user in two entities (handled by the entity check in `createUser` and `updateUser`).
- The `role` field is **not enforced** by any mutation. RBAC is informational; UI/frontend must enforce it. This is documented as tech debt in section 8.

### seedData.ts — Seed Constants Module

**Exports:**
- `COUNTRY_NAMES` — `Record<countryCode, string>` map of all **10** country display names
- `TASK_SEEDS` — Nested object keyed by `countryCode`, each with `nextId: number` and `tasks[]` matching task schema

**Structure:**
```typescript
COUNTRY_NAMES = {
  cn: "China", jp: "Japan", au: "Australia", my: "Malaysia",
  id: "Indonesia", in: "India", sg: "Singapore", hk: "Hong Kong",
  th: "Thailand", vn: "Vietnam"
}

TASK_SEEDS = {
  hk: { nextId: 12, tasks: [ {id, date, description, owner, deadline, status}, ... ] },
  sg: { nextId: 11, tasks: [...] },
  my: { nextId: 8,  tasks: [...] },
  th: { nextId: 10, tasks: [...] }
  // cn, jp, au, id, in, vn: not seeded (empty / not yet defined)
}
```

**Purpose:**
- Drives `seedTasks` mutation to populate initial demo data per entity.
- `nextId` values are used as a starting sequential counter per country. `seedTasks` does not reset the per-(country, entity) `nextId` — runtime `createTask` auto-increment takes over for new inserts post-seed.
- The `history: []` field on each country is unused by current code (placeholder for future audit-trail feature).

---

## 4. Code Architecture

### File Organization
```
convex/
├─ schema.ts           # Table definitions + indexes + value constraints
├─ tasks.ts            # Task CRUD + country queries + seed + migrate (7 exports)
├─ users.ts            # User CRUD + stats + login tracking + admin seed (10 exports)
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
- The `entity` union literal list is duplicated across `schema.ts`, `tasks.ts`, and `users.ts`. When adding a new entity, all three files must be updated and redeployed.

### Index-First Query Design
Every read operation uses an explicit index chain (`.withIndex(...)`) for the country lookup, then filters by entity in-memory. This guarantees O(log n) performance on the indexed dimension even as per-country task sets grow. Entity filtering post-index is acceptable because per-country task sets are expected to stay small (< 1000 rows per country per entity).

### Mutability Pattern
- **Tasks:** `createdAt`/`updatedAt` set on insert; `updatedAt` patched on every mutation. `entity` set on insert, immutable after.
- **Users:** Same timestamp pattern plus optional `lastLoginAt` updated by `recordLogin`. `entity` is set on insert but is technically mutable via `updateUser` (though no UI flow currently changes it).
- **Countries:** Immutable after seed — no update/delete paths exist.

### Backward Compatibility
- `resolveEntity(undefined) → "dhl"` — every function treats a missing `entity` arg or missing `entity` field as `"dhl"`. This lets a pre-entity-scoping deployment upgrade without breaking existing reads.
- `migrateEntityField` is the one-shot tool to backfill `entity` on legacy rows.

---

## 5. Integration Points

### Frontend (outside this directory)
Frontend code imports generated API via:
```typescript
import { api, internal } from "../convex/_generated/api";
```
- `api.*` → public functions (callable by client)
- `internal.*` → server-only (not exposed to client)
- All functions in `tasks.ts` and `users.ts` are `export const fnName = query/mutation(...)` and therefore public by default. Convex treats all exports as public unless marked internal via a separate internal module.

### Per-Entity Dashboard Pattern
Each client entity (dhl, jll, tiktok, cushman-wakefield, smrt, certis, toll-group, prudential) gets its own dashboard that calls these public functions with `entity: "<their entity>"` on every request. The deployment is shared; the data is partitioned by the `entity` field. This is cheaper than running 8 separate Convex deployments and keeps a single source of truth for the schema.

### Authentication (not implemented here)
No `ctx.auth.getUserIdentity()` checks in current mutations/queries. All operations are effectively anonymous. Production hardening requires:
- `ctx.auth.getUserIdentity()` guard in each mutation
- Row-level security: filter `tasks` by user's `entity` AND `countries` array
- Admin-only guards for `seed*` and `migrate*` mutations

### Deployment / CI
- `npx convex dev` (default) — watches `schema.ts`, regenerates `_generated/` on change
- `npx convex dev --once --url https://moonlit-chickadee-458.convex.cloud` — push schema + code to the named cloud deployment (used for ad-hoc deploys to the dev backend)
- `npx convex deploy` — production deploy (requires prod deploy key, not used in the dev project)
- `seedTasks` mutation must be called manually post-deploy to populate reference data; `migrateEntityField` only needs to be run when upgrading an older deployment

---

## 6. Data Flow Patterns

### Task Read (per-country, per-entity)
```
Client calls api.tasks.getTasksByCountry({ countryCode: "sg", entity: "dhl" })
  → Convex routes to tasks.getTasksByCountry query
  → Query: db.query("tasks").withIndex("by_country_and_id", q.eq("countryCode", "sg"))
  → Results filtered in-memory by matchesEntity(task.entity, "dhl")
  → Sorted by id asc, nextId computed from filtered max id + 1
  → Returned to client via realtime subscription or single fetch
```

### Task Create
```
Client calls api.tasks.createTask({ countryCode: "sg", entity: "dhl", ... })
  → Convex routes to tasks.createTask mutation (transactional)
  → Mutation: db.query("tasks").withIndex("by_country_and_id", q.eq("countryCode", "sg")).order("desc").first()
  → Computes nextId = (latest?.id ?? 0) + 1
  → Inserts: db.insert("tasks", { id: nextId, countryCode, entity, ..., createdAt: now, updatedAt: now })
  → Convex ACID commit; subscribers notified
```

### Entity Migration (one-time)
```
Admin calls api.tasks.migrateEntityField({ entity: "dhl", table: "tasks" })
  → Collects all tasks (or users)
  → For each doc where doc.entity is missing, patch { entity: "dhl" }
  → Returns { ok: true, updated, total }
```

### User Login Tracking
```
Client calls api.users.recordLogin({ email: "user@example.com", entity: "dhl" })
  → Query by email via by_email index
  → Verify entity via matchesEntity
  → Patch: { lastLoginAt: now, updatedAt: now }
  → Returns { ok: true } or error
```

### Seeding All Data
```
Admin triggers api.tasks.seedTasks({ entity: "dhl" })
  → Inserts all 10 countries if missing (idempotent)
  → For each country in TASK_SEEDS, inserts tasks if not already present for the target entity
  → Returns summary { ok, countriesInserted, tasksInserted, totalCountries }
```

---

## 7. Design Rationale

### Per-Entity Partitioning
The same `tasks` and `users` tables serve all 8 client entities. Entity is a column, not a database. Rationale:
- Single schema, single deploy, single source of truth
- Easy to add a 9th entity (one literal added to the union in 3 files)
- The shared index `by_country_and_id` works for all entities
- Trade-off: every read does an in-memory filter after the index lookup. Acceptable while per-entity task sets are small.

### Per-(Country, Entity) Sequential IDs
Tasks use `id: number` that restarts at 1 per `(countryCode, entity)` pair (not globally unique). Design choice: human-readable identifiers for local teams ("Task SG-7 / dhl"). Composite uniqueness is enforced by the index + the entity filter at every read/write.

### Index-Only Access
No table scans on the country dimension. Every query specifies `.withIndex(...)` for the country lookup, ensuring predictable performance on that dimension. `tasks` has 2 indexes; `users` has 3; `countries` has 1. No composite index spans `entity` yet — see tech debt below.

### Seed Data as Source of Truth
`seedData.ts` holds the authoritative initial dataset for each country. `seedTasks` is the only path to insert initial demo data — no separate SQL/CSV import path. This keeps data versioned in code.

### No Soft-Delete
`deleteTask` performs hard delete. Tasks are small; retention not a concern. If audit trail needed, move to a `tasks_archived` table instead.

### Minimal RBAC
`users.role` field exists but is **not enforced** by any mutation. Frontend must enforce UI restrictions; backend trusts client. Enhancement: add role-based guards to mutations (e.g., only `admin` can `createUser`, only `editor` or above can `updateTask`).

### Shared Deployment vs Per-Entity Deployments
Choosing one shared Convex deployment for all 8 entities (instead of 8 deployments) keeps schema sync trivial and lets a developer add an entity in one PR. The cost is the in-memory entity filter on every read. If any entity grows past ~10k tasks in a single country, add a `by_entity_and_country` index and refactor the queries to use it.

---

## 8. Open Questions / Tech Debt

| Item | Status | Notes |
|------|--------|-------|
| Auth integration | Missing | No `ctx.auth.getUserIdentity()` checks. All operations are effectively anonymous. |
| User→task ownership validation | Missing | `updateTask`/`deleteTask` do not verify the requesting user owns the task or has admin rights in the entity. |
| Cross-country task linking | Not supported | Task dependencies across countries would require schema extension. |
| Task filtering by status/owner | Not indexed | Filtering requires full scan; consider adding compound indexes if needed. |
| Task filter by entity | In-memory only | The country index does not include entity. For entities with >10k tasks in one country, add a `by_entity_and_country` index. |
| `countries` table maintenance | Manual | No mutation to update `countries.name`; schema change required for new country. |
| Task history/audit trail | Absent | No history table — updates are in-place only. `seedData.ts` has unused `history: []` placeholder. |
| Pagination | Not implemented | `getTasksByCountry` returns all tasks per country; pagination not yet needed. |
| `getUserStats` does not count `staff` | Drift | The role is valid in the union but the returned stats object only includes `admins/editors/viewers`. Add a `staff` count or drop `staff` from the union. |
| `isActive` and `passwordHash` on users | Unused in code | Schema fields are present but no function reads or writes them. Either wire them up or remove until needed. |
| `seedTasks` has no production re-seed guard | Dev only | Calling `seedTasks` on a populated entity is idempotent at the row level, but it does not re-sync if a seed definition changes. Plan accordingly. |
| Entity union duplication | Maintenance hazard | Same 8-value list lives in `schema.ts`, `tasks.ts`, `users.ts`. A new entity requires editing all three files. Consider extracting to a shared `convex/entities.ts` constant if it grows. |

---

**Last updated:** 2026-06-10
**Convex schema version:** 2 (8-value entity union, with `entity` field on both `tasks` and `users`)
**Countries supported:** cn, jp, au, my, id, in, sg, hk, th, vn (10 total)
**Entities supported:** dhl, jll, tiktok, cushman-wakefield, smrt, certis, toll-group, prudential (8 total)
