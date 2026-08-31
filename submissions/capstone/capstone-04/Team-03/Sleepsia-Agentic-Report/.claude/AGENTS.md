# Sleepsia Agent Architecture — as built

> This file used to be the **pre-implementation design spec**. It's now rewritten to describe
> what's actually in the repository, verified against the real route files, service files, and
> `agents/`/`analytics/` packages. Endpoint paths, file names, and code snippets below are real,
> not illustrative. The durable *principles* from the original spec (no unrestricted SQL, no
> invented numbers, controlled tools) turned out to hold up and are kept — the parts that changed
> are the concrete shapes: actual endpoint paths, actual file names, and which components are
> genuinely wired to something live versus tested-but-dormant.
>
> The AI Assistant / RAG stack (`app/rag/*`, `ai_assistant_service.py`, `query_router.py`,
> `knowledge.py`) is under **active concurrent development by another party** as of this writing —
> more so than the rest of the app. Treat the specifics in that section as a snapshot, and re-read
> the real files before depending on exact function signatures.

## System overview — three separate tracks, not one pipeline

The original spec imagined one layered pipeline (Validation → Analytics → Alerts → Report →
AI, all as "agents"). What's actually built is three mostly-independent tracks that happen to
share a database:

```
Track 1 — Live dashboard (what every chart/KPI page actually calls)
  React pages → REST API (backend/app/api/routes/*.py)
              → backend/app/services/*.py (plain deterministic SQL services —
                kpi_service, platform_service, product_service, advertising_service,
                inventory_service, warehouse_service, alert_service)
              → MySQL views
  This is the path the dashboard actually exercises today, and it's deliberately not
  agentic. But `products.py` is an exception worth knowing about — see the callout
  right after this diagram before assuming "Track 1" means zero agent involvement.

Track 2 — PDF report generation ("Management Summary" report only)
  POST /api/reports → backend/app/services/report_service.py
    → its own SQL aggregation (channel/product/inventory/P&L sections)
    → agents/analysis_agent.py (DataAnalysisAgent) + agents/insight_recommendation_agent.py
      (InsightRecommendationAgent) for the "Audit Notes / Actions" section specifically
    → reportlab PDF / openpyxl Excel
  This is the only place the DASHBOARD's own request flow reaches agents/*.py.

Track 3 — AI Business Assistant (/assistant page)
  React page → POST /api/ai/ask → ai_assistant_service.py
    → query_router.py picks SQL vs RAG vs HYBRID vs CLARIFICATION
    → SQL route: sql_tools.py (controlled, parameterized query functions) + Groq LLM
      for tool selection / explanation
    → RAG route: app/rag/retriever.py + app/rag/answer_generator.py against a vector
      store populated via /api/knowledge/upload (new, evolving)
  This is real LLM usage (Groq), unlike Tracks 1 and 2 which are fully deterministic.
```

**The one place Track 1 isn't purely deterministic**: `backend/app/api/routes/products.py`
wraps `from backend.services.agent_service import AgentService` in a try/except (falls back to
`AGENT_SERVICE_AVAILABLE = False` on import error, so a missing dependency degrades silently
rather than crashing the route). `backend/services/agent_service.py` (a *third* services
directory, distinct from both `backend/app/services/` and top-level `analytics/`) instantiates
the full agent stack — `DataValidationAgent`, `DataAnalysisAgent`, `InsightRecommendationAgent`,
`LLMAnalysisAgent` — and:
- On `GET /api/product-performance`, `/top`, and `/bottom`: only runs if the caller passes
  `include_analysis=true` (default `False`). The dashboard's real calls to `/top` and `/bottom`
  (`dashboard/src/services/analyticsApi.js`) do **not** pass this flag, so in practice the
  frontend never triggers it today.
- On `GET /api/product-performance/{sku}`: runs **unconditionally** whenever
  `AGENT_SERVICE_AVAILABLE` is true, wrapped in a try/except that swallows failures. Nothing in
  the current frontend calls this endpoint, so it's live-and-reachable but not presently exercised.

So "Track 1 has no agent involvement" is true of what the UI exercises today, but false as a
statement about the code — a direct API call (Swagger `/docs`, curl, or a future frontend change)
can invoke the full agent stack, including a Groq-backed `LLMAnalysisAgent`, from what looks like
a plain analytics endpoint. Don't refactor `agents/*.py` assuming `report_service.py` is the only
caller, and don't assume enabling `include_analysis` is free — it constructs an LLM client.

`backend/app/services/comprehensive_report_service.py` and `analytics/orchestration/`
(`WorkflowOrchestrator`) exist, are tested, and are **not called by the dashboard frontend** —
but see §4 below: the comprehensive-report *endpoints* are real and callable directly, so "not
called by anything live" would overstate it. Don't assume either is dead code you can break freely.

---

## 1. Agent philosophy (unchanged from spec, still holds)

Use agents/LLM reasoning where natural-language interpretation genuinely adds value (tool
selection, explaining a number, summarizing). Use deterministic Python for anything that produces
a number a business decision depends on. Don't convert a plain SQL service into an "agent" just
for the label — Track 1 above is deliberately not agentic, and that's correct, not a shortcut.

---

## 2. Validation

`agents/validation_agent.py` (`DataValidationAgent`) exists, is unit-tested, and validates
datasets against a `DatasetSpec` (required columns, types, referential checks) — but despite what
you'd guess from the name, it does **not** run in the ETL/ingestion path. `backend/etl/loader.py`
has its own separate, hand-written `DataValidator` class and never imports anything from `agents/`.
The only place `DataValidationAgent` is even instantiated is `backend/services/agent_service.py`'s
`AgentService.__init__`, and nothing in that file appears to call methods on it — it's constructed
but effectively unused today. There's no `/api/validate` endpoint either way. If you're checking
why an ETL-loaded value looks wrong, check `backend/etl/loader.py`'s `DataValidator`, not this
agent; if you're checking why a dashboard value looks wrong, check the SQL view or the
`backend/app/services/*.py` file for that page.

---

## 3. Track 1: the live analytics services

Each is a plain static-method class in `backend/app/services/`, doing parameterized SQL against a
MySQL view and mapping rows to a Pydantic response model — deliberately not agentic, for the same
reason as everywhere else: these numbers back financial decisions and must be reproducible and
auditable by reading the SQL, not by trusting a model's arithmetic. The one exception is
`products.py`'s optional `include_analysis`/`{sku}` agent path, covered in the callout above —
know about it, but it doesn't change the "reproducible SQL" story for the numbers these endpoints
return by default.

Real endpoints (all under `/api` — see `backend/app/main.py` for the `include_router` calls):

| Path | Router file | Backing service |
|---|---|---|
| `GET /api/kpis`, `/api/kpis/by-date`, `/api/kpis/health` | `kpis.py` | `kpi_service.py`, `kpi_orchestrator.py` |
| `GET /api/platform-performance`, `/profitability`, `/advertising` | `platforms.py` | `platform_service.py` |
| `GET /api/product-performance`, `/top`, `/bottom`, `/{sku}` | `products.py` | `product_service.py` (+ optional `agent_service.py`, see above) |
| `GET /api/warehouses` | `warehouses.py` | `warehouse_service.py` |
| `GET /api/inventory`, `/low-stock`, `/stockouts` | `inventory.py` | `inventory_service.py` |
| `GET /api/alerts` | `alerts.py` | `alert_service.py` |
| `GET /api/advertising` | `advertising.py` | `advertising_service.py` (delegates, same pattern as the rest — no inline SQL in the route) |

All of these accept a `start_date`/`end_date` range (via the shared `get_date_range` dependency in
`app/api/dependencies.py`) except `warehouses`/`inventory`, which are point-in-time snapshots with
no date-range or platform dimension — see `sleepsia-dashboard` skill for why that matters when
wiring frontend filters.

---

## 4. Track 2: Report generation and the `agents/` package

`POST /api/reports` (`reports.py` → `report_service.py`) is what the Reports page actually calls.
`report_service.py` builds each report section (Channel Performance, Product-by-Platform,
Inventory & Warehouse, Consolidated SKU, P&L) from its own SQL, matching the "Sleepsia
Omni-Channel Audit Template" structure — columns with no real data source (e.g. OTIF%,
warehouse "Damaged/Hold") are omitted rather than faked.

The **Audit Notes / Actions** section of the `executive_summary` report type is the one place
`agents/*.py` runs for real:

```
report_service.py._get_audit_notes()
  → builds ProductMetrics / PlatformMetrics (analytics/models.py dataclasses) from real
    aggregated DB rows
  → agents/analysis_agent.py: DataAnalysisAgent.analyze_platform_performance() /
    .analyze_product_performance() / .detect_anomalies() → PerformanceFinding[]
  → agents/insight_recommendation_agent.py: InsightRecommendationAgent.analyze()
    → InsightRecommendationResult (insights, recommendations, management_summary)
  → rendered as Observation/Action/Due Date/Status rows in the PDF
```

Both agent classes are deterministic (threshold/rule-based against real numbers, not LLM calls)
despite the "agent" name — see `agents/analysis_agent.py`'s `THRESHOLDS` dict for the actual rules
(margin, return rate, cancellation rate, ROAS, ACOS, organic share). `agents/llm_analysis_agent.py`
(`LLMAnalysisAgent`) exists and is tested and is **not** called from `report_service.py` — but it
is instantiated (unconditionally, per-request) inside `backend/services/agent_service.py`, which
`products.py` uses for its `include_analysis`/`{sku}` path described in the system-overview
callout above. So "not called anywhere live" would be wrong; the more precise statement is: not
called from the report path, and not currently triggered by anything the dashboard frontend does.
If you need LLM-generated narrative in a *report*, it isn't wired into `report_service.py` yet.

Other report endpoints, all real: `GET /api/reports` (list), `GET /api/reports/{id}`,
`GET /api/reports/{id}/download?format=pdf|json|excel`, `POST /api/reports/{id}/email`,
`DELETE /api/reports/{id}`. `POST /api/reports/comprehensive/generate` and `/comprehensive/json`
are also real, registered, directly-callable endpoints that produce a differently-structured,
arguably nicer report — the dashboard frontend does not call them (so don't assume either is what
a user gets from clicking "Generate" on the Reports page), but they are live, not dead code: a
direct request (Swagger `/docs`, curl, a future integration) executes `ComprehensiveReportService`
end to end.

---

## 5. Track 3: AI Business Assistant

**Frontend**: `dashboard/src/pages/AIAssistant.jsx` at route `/assistant`, calling
`dashboard/src/services/aiAssistantApi.js` (not `aiApi.js` — that filename doesn't exist in this
repo). Real endpoints:

- `POST /api/ai/ask` — main Q&A entry point (`ai_assistant.py` → `ai_assistant_service.py`)
- `GET /api/ai/suggestions` — suggested-question chips shown on the page
- `POST /api/ai/explain-metric` — plain-language definition of a named metric

**Backend flow** (`ai_assistant_service.py`, actively evolving — verify against the live file):

1. `query_router.py`'s `QueryRouter` classifies the question into one of `ROUTE_SQL`,
   `ROUTE_RAG`, `ROUTE_HYBRID`, or `ROUTE_CLARIFICATION`.
2. **SQL route**: dispatches to a controlled function in `sql_tools.py`, registered in its
   `SQL_TOOLS` dict and exposed to Groq via `get_groq_tool_definitions()`. As of this writing that
   dict has six entries (`get_kpi_summary`, `get_platform_metrics`, `get_product_metrics`,
   `get_advertising_metrics`, `get_inventory_status`, `get_quality_metrics`) via
   `execute_tool(db, tool_name, tool_input)`, but treat that list as illustrative, not
   authoritative — `SQL_TOOLS` is the actual source of truth and this is exactly the kind of detail
   that drifts first in a subsystem under active concurrent development. This is a
   real controlled-tool pattern — the model picks a tool and parameters, the tool runs
   parameterized SQL, the model narrates the structured result. There is no path from a user
   question to arbitrary SQL execution; `sql_tools.py`'s own module docstring calls out avoiding
   "interpolation of LLM-controlled input" as a SQL-injection surface — keep it that way when
   touching this file.
3. **RAG route**: `app/rag/retriever.py` + `app/rag/answer_generator.py` (`generate_rag_answer`,
   `generate_hybrid_answer`) query a vector store (`app/rag/vector_store.py`) populated from
   documents uploaded through the new Knowledge Base admin API. Worth flagging explicitly:
   `.claude/CLAUDE.md`'s Development Philosophy section lists "Vector databases" under "Avoid
   unnecessary" infrastructure for the MVP — this vector store is a real, deliberate departure from
   that guidance (the same section does allow RAG for unstructured documents like SOPs/policies
   "introduced later," which is what this is), not an oversight. If you're deciding whether to
   extend this further, that's the tension to weigh, not something to treat as already-settled.
4. The LLM provider is **Groq** (`from groq import Groq`), not OpenAI/Anthropic — if you're
   adding a new capability here, match the existing provider rather than introducing a second one
   unless asked.

**Knowledge Base admin API** (`knowledge.py`, prefix `/api/knowledge`) — new since this doc was
last accurate:

- `POST /api/knowledge/upload`, `GET /api/knowledge/documents`,
  `DELETE /api/knowledge/documents/{source_file}` (keyed by the source filename, not a generic id),
  `POST /api/knowledge/reindex-corpus`
- Gated by a single shared-secret header (`X-Admin-Key` vs `settings.KNOWLEDGE_ADMIN_API_KEY`) —
  explicitly documented in the file's own docstring as a minimal, not-a-real-auth-system gate,
  fail-closed if the key is unset. This is the RAG ingestion path the original spec flagged as a
  post-MVP nice-to-have ("RAG may be introduced later for unstructured documents") — it's now in
  progress. `python-multipart` is a hard runtime dependency of this file (file upload parsing) —
  see the `sleepsia-dashboard` skill's note on the backend crashing without it.

---

## 6. Safety rules (unchanged, still enforced)

- Never execute arbitrary LLM-generated SQL; only named, parameterized functions in `sql_tools.py`.
- Never invent a metric value — every number in a report, alert, or AI answer must trace back to a
  real query result, not a plausible-looking constant (this bit the codebase before — see the
  `sleepsia-dashboard` skill's "real data only" note).
- If required data is unavailable, say so plainly rather than guessing — the AI assistant should
  return something equivalent to "I don't have sufficient data to answer that accurately," not a
  best-effort fabrication.
- Recommendations (wherever generated — `agents/insight_recommendation_agent.py` or the AI
  assistant) should carry Finding → Evidence → Business Impact → Recommended Action, and should
  not claim causality the data doesn't support.

---

## 7. If you're extending this system

- Adding a live dashboard capability → new query in the relevant `backend/app/services/*.py` +
  route in `backend/app/api/routes/*.py`, registered in `main.py`. Track 1. No agent needed.
- Adding report content → extend `report_service.py`'s section builders; only route through
  `agents/` if it's genuinely a rule-based finding/recommendation for Audit Notes, not raw data.
- Adding an AI Assistant capability → add a function to `sql_tools.py` + its tool definition, or
  extend the RAG retriever/prompts — check with whoever's currently working in `app/rag/*` first,
  given the concurrent-editing situation on this exact subsystem.
- Before believing any endpoint path or file name not listed above, grep for it — this file was
  wrong for a long time because nobody re-verified it against the actual code after the MVP got
  built out.
