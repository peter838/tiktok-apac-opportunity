# js/

## Responsibility

The `js/` directory contains the complete client-side application logic for the DHL Opportunity Intelligence multi-country task management platform. It orchestrates task tracking, user management, and live data visualization across 9 APAC markets (AU, CN, HK, ID, IN, JP, MY, SG, TH).

**Core responsibilities:**
- **Task state management**: CRUD operations on country-scoped tasks with undo/redo history, cross-session persistence via Convex backend
- **Data aggregation & visualization**: Real-time fetching of SA API data with 24h localStorage caching, entity margin tracking, order analysis, and cost-savings metrics
- **User access control**: Dashboard user CRUD with role-based permissions (admin/editor/viewer) and country-specific market access
- **Shared UI primitives**: Reveal animations, navigation scroll effects, category bar charts, heatmaps, and Q1 chart tooltips

**Key architectural constraint:** Zero framework dependency – vanilla JS only. Shared logic is imported by country-specific HTML pages (e.g., `sg/index.html`, `cn/index.html`). Each page instantiates its own isolated state partition keyed by country code.

## Design

### Module Architecture

**1. `shared.js` – Foundation Layer (1057 lines)**
The monolithic shared runtime containing all cross-cutting concerns. Three major domains:

- **Task Tracker (lines 518–1037)**: State machine pattern with deep cloning for immutability. `cloneTaskState()` / `cloneTaskSnapshot()` produce isolated copies. Normalization via `normalizeTask()` and `normalizeTaskState()` ensures schema consistency across Convex ↔ local divergences.
  - **Undo/Redo**: Snapshot stack (`past[]`) limited to 20 entries. `pushUndoSnapshot()` captures pre-edit state; `restoreUndoSnapshot()` rehydrates.
  - **Dual persistence**: Convex mutations (when available) + optimistic local updates. Periodic polling (4s interval) reconciles remote changes unless local edits are recent (<5s).
  - **History log**: Append-only event stream with GMT+8 timestamps. Records field-level deltas (date, description, owner, deadline, status).
  - **Inline editing**: Event delegation on table cells with auto-grow textareas and native date pickers.

- **UI Primitives (lines 280–405)**: Reusable visual behaviors.
  - `initReveal()`: IntersectionObserver for scroll-triggered fade-ins; special handling for category bars (animates `bar-fill` width on intersect).
  - `initBars()`: Legacy load-triggered bar animations.
  - `initQ1Tooltips()`: Keyboard-accessible SVG circle tooltips with month formatting (`formatQ1Month`).
  - **Formatters**: `fmtK()` (thousands→millions), `fmtSGD()`, `fmtCostSaving()`, `fmtExact()` for currency display.

- **Data Layer (lines 408–421)**: `loadSiteData()` fetches `../site-data.json` with singleton caching (`SITE_DATA_CACHE`). Returns `{}` on failure.

- **Cross-Page Utilities (lines 511–559)**: `getCountryCodeFromPath()` extracts country from URL path; `getCountryCostSaving()` computes savings from site data.

**2. `main-page-data.js` – Analytics Pipeline (623 lines)**
Enterprise data aggregation for the root landing page. Three-layer architecture:

- **`MainPageAPIClient`**: Proxy-based SA API gateway (`/api/sa-proxy`). Resilient error handling – 502 upstream errors return empty structures instead of throwing, preventing UI deadlocks. Handles three endpoints:
  - `/v1.0/agent/analytics/tracking/entity-margin` (paginated)
  - `/v1.0/agent/analytics/entity/order-analysis`
  - Order values (transformed into spend/margin calculations)

- **`DataCache`**: 24h `localStorage` cache with timestamp validation. Singleton read/write/clear API.

- **`MainPageDataFetcher`**: Orchestrates parallel data collection across all 9 regions. For each region, fires `entity-margin` and `order-analysis` concurrently. Processes results:
  - Filters deduplicated DHL entities (`entity_name` contains "DHL")
  - Aggregates orders, margins, spend (prefers real order spend over margin fallback)
  - Computes modeled potential (7.5× multiplier) and gap percentage
  - Regional rollups into `aggregated` summary (marketsAnalyzed, activeRegions, totalSpend, totalMargin, totalOrders, totalEntities, modeledPotential, modeledGap, costSavingsAchieved)

- **`MainPageUIUpdater`**: Declarative DOM reconciliation. Updates:
  - Hero stats (5 agg-stat cards)
  - Country cards (observed/potential/saved with progress bars)
  - Trend sections (region rows with spend amounts)
  - CTA section (gap + savings text)
  - Loading/error state teardown

**3. `user-management.js` – Access Control System (541 lines)**
Full CRUD dashboard user administration with dual persistence strategy.

- **`UserManagement` class**: Lifecycle-managed component. Auto-initializes on DOMContentLoaded. Detects country pages via path matching; injects into `.tasks-section` → `.story` → `.cta` anchor hierarchy.

- **Dual Storage**: Convex backend (`users:*` mutations/queries) ↔ `localStorage` fallback (`dhl_dashboard_users`). Default seed user provided for cold starts.

- **Role system**: `admin` (red), `editor` (amber), `viewer` (green). Statuses: `active`, `inactive`, `pending`. Market access: per-country checkboxes or "all markets" when empty.

- **UI Components**:
  - Stats summary cards (total, active, pending, admins, editors, viewers)
  - Sortable table with inline badges (role/status) and country tags
  - Modal form with validation and country grid picker
  - Action buttons (edit/delete) with confirmation dialogs

### Key Patterns & Principles

1. **Event Delegation**: All dynamic table interactions use bubbling (`tbody.addEventListener('change')`, `onclick` on parent). Eliminates per-row listener overhead.

2. **Snapshot Immutability**: Task state mutations always `pushUndoSnapshot()` before mutation. Deep clone prevents reference aliasing.

3. **Graceful Degradation**: Convex unavailability → localStorage. API 502 → empty data. No fatal errors; UI remains functional.

4. **Country Partitioning**: State is scoped by `countryCode`. `TASK_TRACKER_SEEDS` provides initial data per market. `injectTaskTrackerSection()` creates isolated table instances.

5. **GMT+8 Temporal Consistency**: All timestamps use Asia/Singapore timezone via `formatGMT8()`.

6. **Reveal.js Scroll System**: `.reveal` + `.reveal-delay-{1,2,...}` classes driven by `initReveal()` IntersectionObserver with negative bottom margin for early trigger.

7. **Reactive Polling**: 4-second remote sync when Convex configured. Suppressed during active editing (`hasLocalChanges` guard with 5s cooldown).

### Data Flow

1. **Page Load** (e.g., `sg/index.html`):
   - Loads `shared.js`
   - `initAll()` → `initTasks()` → `getCountryCodeFromPath()` = "sg"
   - `injectTaskTrackerSection("sg")`: Creates table, fetches remote state via `loadSharedTaskState("sg")`
   - Renders initial rows, starts 4s poll loop

2. **Main Page Data** (`index.html`):
   - Loads `main-page-data.js`
   - `initMainPageData()` → `showLoadingState()`
   - `MainPageDataFetcher.fetchAllRegions()`: Parallel API calls × 9 regions
   - Cache write → `MainPageUIUpdater.updateAll()`
   - Hero stats, country cards, trends, CTA update

3. **User Management** (any country page):
   - `UserManagement.init()` on DOM ready
   - Loads users (Convex or localStorage)
   - Injects `.users-section` after tasks/story/cta
   - Modal form → `createUser()` / `updateUser()` / `deleteUser()`
   - Optimistic local update → Convex mutation (if available)

4. **Cross-Module Communication**:
   - No direct imports. All coordination via global namespace (`window.DHLConvexClient`, `window.DHL_TASK_TRACKER_DATA`, `window.dhlApacData`)
   - Task edits trigger `syncSharedTaskState()` Convex mutations with conflict detection (local vs remote diff)

## Flow

### Task Edit Sequence
1. User changes table cell → `tbodyEl` change listener captures event
2. `recordAndRender()` called: previous vs next comparison
3. `pushUndoSnapshot(state)` – snapshot saved to `state.past`
4. `appendHistory()` – delta logged with GMT+8 timestamp
5. `renderRows()` – immediate UI refresh
6. Async `DHLConvexClient.mutation('tasks:updateTask')` (best-effort)
7. On error: local state preserved; background sync continues

### Remote Sync Sequence (poll)
1. `loadSharedTaskState(countryCode)` triggers Convex query
2. Remote task list fetched; local `hasLocalChanges` checked
3. If no recent edits (<5s): overwrite `state.tasks` + `state.nextId`
4. `renderRows()` – full table re-render
5. Cycle repeats every 4000ms while Convex configured

### Add Task Sequence
1. "Add task" button → `addButton` click handler
2. `pushUndoSnapshot(state)`
3. Generate `newTask` with `state.nextId++`
4. `state.tasks.push(newTask)`
5. `renderRows()` – scroll to new row, focus description textarea
6. Async `tasks:createTask` mutation (best-effort)
7. History entry: "Added Task {N} as a new editable row."

### Undo Sequence
1. Undo button enabled when `state.past.length > 0`
2. Click → pop last snapshot from `state.past`
3. `restoreUndoSnapshot(state, previousState)` – full state rehydration
4. `appendHistory()` – "Undid the last change and restored the previous saved state."
5. `renderRows()` – UI reflects rolled-back state
6. `syncSharedTaskState()` – push entire current state to Convex (reconciles all rows)

### Main Page Data Fetch
1. Check `DataCache.get()` – return if <24h old
2. For each region in `REGIONS`:
   - Parallel: `getEntityMarginTracking()` + `getOrderAnalysisByCategory()`
   - `processRegionData()`: filter DHL entities, dedupe by `entity_id`, sum orders/margins
   - `processOrderAnalysisSpend()`: sum DHL entity `order_value`
3. `aggregateAllRegions()`: rollup totals, compute 7.5× modeled potential, gap %
4. `DataCache.set()` – persist with timestamp
5. `MainPageUIUpdater` updates DOM

### User Management Lifecycle
1. `UserManagement.init()` → `loadUsers()`
2. Convex query `users:listUsers` or localStorage read
3. `render()` – inject table into page
4. Add/Edit/Delete → modal form with validation
5. `createUser()` / `updateUser()` / `deleteUser()`
6. Optimistic local array mutation → `saveLocalUsers()` (if no Convex)
7. Re-render stats table

## Integration

### Convex Backend Hooks
All mutations/queries assume these Convex functions exist:
- **Tasks**: `tasks:getTasksByCountry`, `tasks:createTask`, `tasks:updateTask`, `tasks:deleteTask`
- **Users**: `users:listUsers`, `users:createUser`, `users:updateUser`, `users:deleteUser`, `users:getUserStats`

**Convex Client Detection**: `window.DHLConvexClient` must expose `{ isConfigured: boolean, query(), mutation() }`. If falsy, system falls back to localStorage seeds.

### HTML Integration Points
- **Task Table**: `injectTaskTrackerSection()` anchors after `section.annual-section` or `section.story`. Requires DOM element with `data-tasks-body`, `data-summary`, `data-history-panel`, `data-history-list`, `data-convex-status`.
- **Country Cards**: `main-page-data.js` expects `a[href="{code}/index.html"]` cards with `.country-card-stat-value` and `.country-card-bar-fill` children.
- **Singapore Special Case**: IDs `sg-observed`, `sg-potential`, `sg-saved`, `sg-bar`, `sg-trend-amount` hard-coded for home-market card.
- **Trend Sections**: `a[href$="/index.html"]` with flag emoji selector (`style*="font-size:28px"`) and amount span (`style*="margin-left:auto"`).
- **Aggregate Stats**: `.agg-stats` container with 5 `.agg-stat` > `.agg-stat-value` elements.

### Global Namespace
Shared state exposed for debugging:
- `window.DHL_TASK_TRACKER_DATA` – seed data (countries, tasks per country)
- `window.DHLConvexClient` – backend client
- `window.dhlApacData` – latest fetched analytics data
- `window.MainPageDataFetcher`, `window.initMainPageData`, `window.formatSGD`
- `window.UserManagement`, `window.initUserManagement`
- `window.initAll` – bootstraps all modules

### Asset Dependencies
- **Reveal animations**: CSS classes `.reveal`, `.visible`, `.reveal-delay-*` (expected from stylesheet)
- **Chart.js**: Referenced in comments (bar charts, heatmaps) – actual rendering via inline SVG/CSS in this codebase
- **No bundler**: Direct `<script src="shared.js">` in HTML; globals expected

### Country Coverage
All modules support 9 markets: `cn` (China), `jp` (Japan), `au` (Australia), `my` (Malaysia), `id` (Indonesia), `in` (India), `sg` (Singapore), `hk` (Hong Kong), `th` (Thailand). Each has seed tasks and localized names in `TASK_TRACKER_COUNTRIES` / `COUNTRY_NAMES`.

### Error Boundaries
- **API failures**: Return empty data structures; UI shows zeros/placeholders
- **Convex unconfigured**: localStorage persistence with warnings
- **Cache corruption**: JSON parse errors caught; cache cleared
- **DOM missing**: Functions early-return if selectors empty (no thrown errors)

### Build-Time Notes
- No compilation step – ES5-compatible syntax
- Modules are concatenated in HTML `<script>` tags (order: shared.js, then page-specific)
- `js/codemap.md` documents architecture for developer onboarding