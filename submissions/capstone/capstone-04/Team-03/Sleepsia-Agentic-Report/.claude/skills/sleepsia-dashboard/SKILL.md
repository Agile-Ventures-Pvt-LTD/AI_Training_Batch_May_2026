---
name: sleepsia-dashboard
description: Operational guide for working in the Sleepsia Agentic Reporting codebase (FastAPI backend, React/Vite dashboard, MySQL, agents/ package, reportlab PDF reports). Use this whenever starting, debugging, or changing anything in this repo — running the servers, fixing a backend crash, editing a chart/color, touching the PDF report generator, or working on alerts/inventory — so you don't re-discover gotchas that already cost real debugging time this session. Complements .claude/CLAUDE.md and .claude/architecture.md, which describe the original spec; this file describes how the built system actually behaves today.
---

# Sleepsia Dashboard — working guide

This is the **as-built** operational guide. `.claude/CLAUDE.md`, `architecture.md`, `database.md`,
`business-rules.md`, and `ui-requirements.md` describe the original spec and design intent — read
those for *why* something is shaped a certain way. `.claude/agents.md` is a second as-built
document, not spec — it's the detailed reference for the agent/report/AI-assistant subsystem
specifically; this file is the shorter operational guide for *how to actually work in the repo
without re-hitting bugs that already got debugged*, and points at `agents.md` for that one
subsystem's specifics rather than duplicating them.

## Starting the project

Two separate processes, both required:

- **Backend** (FastAPI on `:8000`): must run with `cwd = backend/` AND `PYTHONPATH` including the
  **project root** (not just `backend/`). `backend/app/main.py` uses absolute imports assuming
  `backend/` is on the path (`from app.config import ...`), but `backend/app/services/kpi_orchestrator.py`
  also imports the top-level `analytics` package from the project root. Miss either half and it
  won't start.
  ```powershell
  cd backend
  $env:PYTHONPATH = "<project root>"
  python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
  ```
  `start.ps1` at the project root does this for you (backend + dashboard + report scheduler).
- **Frontend** (Vite/React on `:3000`): `cd dashboard && npm run dev`.
- Verify both: `GET http://localhost:8000/api/kpis` and load `http://localhost:3000`.

**If the backend won't start / keeps dying on `--reload`:** almost always an import-time failure,
not a runtime one — a new route module got added somewhere under `backend/app/api/routes/` that
imports a package not yet in the venv (e.g. a file-upload endpoint needing `python-multipart`).
Diagnose fast instead of guessing:
```powershell
cd backend
python -c "import app.main"   # PYTHONPATH must still include the project root
```
The traceback names the missing import directly. Install it into `backend/venv` (or the active
`.venv`), and consider adding it to `backend/requirements.txt` if it's now a real dependency.

## This codebase is under active concurrent editing

Another party edits this repo directly (not through this assistant) — files can change between
when you last read them and now. Before a non-trivial change: `git status` / `git diff` on the
files you're about to touch, and re-`Read` a file if it's been more than a few turns since you
last looked at it. If something looks visually different from what you remember writing (a new
gradient/animation style, an extra route file, a changed component), that's most likely the other
party's work, not a bug in yours — don't silently overwrite it. This is also why the browser tool
sometimes shows stale console errors or an unstyled sidebar mid-session: reload before trusting
what you see.

## Architecture map (what's real vs stale)

- **Backend entrypoint**: `backend/app/main.py` + `backend/app/api/routes/*.py` — this is what
  `start.ps1` runs and what the dashboard actually calls. `backend/app.py` (root-level) is a stale
  duplicate against a different `backend/routes/*` module set — don't extend it, it isn't wired to
  anything live.
- **Frontend**: `dashboard/` is the real Vite app. A top-level `frontend/` folder is dead (no
  `package.json`) — ignore it.
- **Data flow**: MySQL → SQLAlchemy views (`vw_product_platform_daily`, `vw_warehouse_summary`,
  `vw_inventory_health`, ...) → `backend/app/services/*.py` → `backend/app/api/routes/*.py` →
  `dashboard/src/services/analyticsApi.js` (the one translation layer between backend snake_case
  and frontend camelCase — check this file first when a value looks wrong on screen) → pages.
- **Reports**: `backend/app/services/report_service.py` is what `POST /api/reports` actually
  calls (the PDF/Excel/JSON generator wired to the UI). `comprehensive_report_service.py` is a
  separate, nicer-looking generator the dashboard frontend doesn't call — but its endpoints
  (`/api/reports/comprehensive/generate`, `/comprehensive/json`) are real and directly callable, so
  it's not dead code, just not what a user gets from the Reports page.
- **Agents**: don't guess at how `agents/*.py`, `report_service.py`'s Audit Notes, or the AI
  Assistant/RAG stack fit together — it's three tracks with one real exception (`products.py` can
  invoke the full agent stack too, opt-in via `include_analysis`) that's easy to get wrong by
  intuition. Read `.claude/agents.md` before touching any of report generation, the agent
  pipeline, or the AI assistant/RAG stack — it's the maintained, as-built reference for that
  subsystem specifically, verified against the real route/service files as of its last edit.
- **Inventory/warehouse data has no date-range or platform dimension** — it's a point-in-time
  snapshot (`inventory_daily`, `replenishment_alerts`), unlike everything else in the app which is
  date-range aggregated. Don't wire the global date-range filter into inventory/warehouse calls;
  it either does nothing or picks a mismatched single day.

## Recurring bug patterns (all real, already hit this session)

- **Case-sensitive status strings.** Status values from the DB are natural-case with spaces —
  `'Healthy'`, `'At Risk'`, `'Critical'`, `'Low Stock'`, `'Stockout'` — never `'HEALTHY'`. A
  comparison like `status === 'HEALTHY'` silently never matches and everything falls through to
  one default color/branch. Always normalize (`.toLowerCase()`) before comparing, and look at
  `dashboard/src/pages/Inventory.jsx`'s `STATUS_META` map for the canonical mapping to reuse.
- **Reportlab table cells must go through `esc()`/`wrap()`.** In `report_service.py`'s
  `_render_pdf`, every dynamic string in a table must be wrapped as a `Paragraph` via the local
  `wrap()` helper (uses the correct small cell font and lets reportlab wrap it) — a raw Python
  string in a cell renders at the *default* larger font and, if it has no space to break on (a
  SKU like `SLP-1001`), overflows straight into the next column. `esc()` (XML-escapes `&`, `<`,
  `>`) is required on any text that isn't already going through `wrap()`/`P()` — otherwise `P&L`
  etc. renders mangled.
- **A filter can silently be a no-op.** Several backend query params exist in a route signature
  but the underlying table has no matching column (e.g. `platform_id` on inventory, which has no
  platform dimension). Check the actual SQL/table before assuming a filter does anything — verify
  by changing the filter and diffing the response, not by reading the route signature alone.
- **Don't fabricate variety that isn't in the data.** If every alert row shows the same threshold
  or recommendation, check whether that's genuinely because the seed data only has one SKU with
  alert history (`SELECT DISTINCT sku FROM replenishment_alerts`) before assuming it's a bug. Where
  real per-row fields exist but aren't surfaced (e.g. `gap`, `days_of_cover`,
  `recommended_reorder_qty` on `replenishment_alerts`), prefer wiring those through end-to-end over
  inventing text — see `alert_service.py` + `Alerts.jsx`'s `buildRecommendation()` for the pattern.
- **Frontend chart "0.0% vs previous" style indicators**: the backend does not compute
  period-over-period comparisons anywhere. Don't build UI that implies it does (a `previousValue`
  prop set to the same value as `value` will always render a fake 0.0%) — either wire a real
  comparison or leave it out.

## Conventions worth following

- **Platform identity color**: one fixed color per platform, defined once in
  `dashboard/src/utils/platformColors.js` (`getPlatformColor(nameOrId)`), reused in every chart via
  `BarChart`'s `colorFor` prop so "Amazon" is the same color on every page. Don't hand-pick a flat
  color per chart for anything with cross-page identity (platforms, warehouses) — do fold in a new
  entity type if one shows up (e.g. regions) rather than inventing a parallel scheme.
- **Status color**: green = Healthy, yellow = At Risk/Low Stock, red = Critical/Stockout,
  everywhere — reuse `STATUS_META`-style local maps rather than re-deriving thresholds per page.
- **Real data only.** Several fields in this codebase used to be hardcoded stubs presented as real
  (`capacity: 5000`, `daysOfCover: 30` in `analyticsApi.js`'s old warehouse transform; a
  hand-written free-text recommendation echoed for every alert). When adding a field, prefer
  showing nothing (or omitting the column, per the report-generation "drop columns with no data
  source" rule already established) over a plausible-looking constant.
- **Verify in the browser after any frontend change**, not just by reading the diff — this app has
  hit real runtime-only bugs (Recharts margin math producing zero-width bars, a raw string in a
  table cell overflowing) that were invisible from the source alone. Use `get_page_text` /
  `javascript_tool` DOM queries over screenshots — this environment's browser pane doesn't
  composite frames when not the foreground tab, so screenshots/transform-based rect measurements
  are unreliable; text/DOM/class assertions are not.
- **A fresh tab or client-side route change can render a chart with zero bars** (ResponsiveContainer
  measures a 0×0 container once, before layout settles). If a chart looks empty right after
  navigating, reload before concluding it's broken.
