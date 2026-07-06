# Supply‑Chain Logistics Rerouter  
**Capstone Project – Build 1**  

---  

## 1. Project Overview  
A major shipping port can become suddenly unavailable (strike, weather, equipment failure). A shipment already in transit must be rerouted quickly. The logistics team needs to know:

* Which shipment is affected?  
* What cargo is on board?  
* How much delay can be tolerated?  
* Which alternative routes exist?  
* Can the destination warehouse accept the cargo?  
* Do any logistics rules forbid the route?  
* Should another route be tried?  
* When must the incident be escalated?    
--- 

## 2. Solution Approach  

1. **Input** – an incident (`incident_id`, `manifest_text`, `disrupted_port_id`).  
2. **LangChain extraction** – parses `manifest_text` with a structured‑output prompt and returns shipment metadata (cargo weight, type, target warehouse, perishability, max tolerable delay, …).  
3. **RAG** – retrieves only the logistics rules that are relevant to the current incident from `logistics_knowledge_base.txt`.  
4. **Tools** –  
   * `get_alternative_routes_tool` returns every alternative route for the disrupted port.  
   * `query_warehouse_inventory_tool` returns the current utilization, status and risk tier of the warehouse assigned to a candidate route.  
5. **LangGraph workflow** – evaluates each route deterministically (warehouse utilization, operational status, risk tier, added delay, shipment‑delay limit).  
   * If a rule is violated the node **route_clarification** increments the route index and retries (up‑to 2 retries).  
   * If a route exceeds 120 h added delay → **CRITICAL_DELAY** → escalation.  
   * When a route passes all checks → **OPTIMAL_PATH_FOUND** → finalize.  
6. **Report generation** – a Groq LLM builds a short “final operations brief”. All state information is saved as JSON to `outputs/reroute_advisory_report.json`.  

---  

## 3. Architecture  

| Component | Responsibility |
|-----------|-----------------|
| **LangChain** | • Groq LLM integration  <br>• Prompt templates  <br>• Structured‑output extraction of shipment metadata  <br>• Generation of the final brief |
| **RAG** | • Load `logistics_knowledge_base.txt`  <br>• Chunk the document  <br>• Create embeddings with a local HuggingFace model  <br>• Store chunks in a FAISS vector store  <br>• Retrieve only rules relevant to the incident |
| **LangGraph** | • Holds the shared `LogisticsIncidentState`  <br>• Executes workflow nodes (parse, rag lookup, load routes, select, check, analyze, retry, finalize, escalation, report)  <br>• Conditional routing based on deterministic rule checks  <br>• Retry loop for alternative routes  <br>• Escalation handling |
| **Python tools** | • `query_warehouse_inventory_tool` – fetches warehouse utilization, status & risk tier from `inventory_status.json`  <br>• `get_alternative_routes_tool` – returns all routes for a given disrupted port from `route_options.json` |
| **Groq LLM** | • Provides the language model (`llama‑3.3‑70b‑versatile`) for extraction and brief generation. |

### Simple workflow diagram  

```
Incident
   ↓
LangChain Extraction (metadata)
   ↓
RAG Rule Retrieval (relevant logistics rules)
   ↓
Route & Warehouse Tools
   ↓
LangGraph Decision & Retry Loop
   ├─ Route Clarification (retry) ──► next route
   ├─ Critical Delay ──► Escalate
   └─ Optimal Path Found ──► Finalize
   ↓
Final Report (JSON + LLM brief)
```  

---  

## 4. Project Structure  

```
supply_chain_logistics_rerouter/
│
├── README.md
├── pyproject.toml
├── .env.example          # template for API key & model
├── .gitignore
│
├── data/
│   ├── logistics_knowledge_base.txt
│   ├── inventory_status.json
│   ├── route_options.json
│   └── sample_incidents.json
│
├── src/
│   ├── main.py               # CLI entry point
│   ├── state.py              # TypedDict for graph state
│   ├── graph.py              # LangGraph definition
│   ├── nodes.py              # All workflow nodes
│   ├── tools.py              # warehouse & route tools
│   ├── rag.py                # RAG pipeline (FAISS)
│   ├── schemas.py            # Pydantic models / prompts
│   └── report_writer.py      # JSON report helper
│
├── tests/
│   ├── test_tools.py
│   ├── test_routing.py
│   ├── test_nodes.py
│   └── test_graph.py
│
└── outputs/
    ├── INC-001_reroute_advisory_report.json
    ├── INC-002_reroute_advisory_report.json
    ├── INC-003_reroute_advisory_report.json
    └── test_results.txt
```  

---  

## 5. Setup Instructions  

1. **Clone the repository**  

   ```bash
   git clone <repo_url>
   cd supply_chain_logistics_rerouter
   ```

2. **Create a virtual environment with UV (recommended)**  

   ```bash
   uv venv               # creates .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**  

   ```bash
   uv pip install -r requirements.txt   # or:
   uv add langchain langchain-core langchain-community \
          langchain-groq langchain-huggingface \
          langgraph chromadb sentence-transformers \
          pydantic python-dotenv
   uv add --dev pytest pytest-mock
   ```

4. **Configure environment variables**  

   ```bash
   cp .env.example .env
   # edit .env and add your Groq API key
   ```

   The file must **not** be committed.  

---  

## 6. Running the Application  

```bash
uv run python src/main.py
```

The CLI lists the incident IDs from `data/sample_incidents.json` and prompts for a selection, e.g.:

```
Available Incidents:
1. INC-001
2. INC-002
3. INC-003
Select incident: 1
```

The full LangGraph workflow executes and a JSON report is written to `outputs/<INC‑XXX>_reroute_advisory_report.json`.  

---  

## 7. Input  

The application expects a dictionary with three keys:

| Field | Description |
|-------|-------------|
| `incident_id` | Unique identifier, e.g. `"INC-001"` |
| `manifest_text` | Free‑form incident description (the LLM extracts all required metadata) |
| `disrupted_port_id` | Port that is unavailable, e.g. `"PORT‑SEATTLE‑02"` |

### Sample input (used by the CLI)

```python
initial_input = {
    "incident_id": "INC-001",
    "manifest_text": (
        "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded "
        "outside the Port of Seattle due to an active worker strike. "
        "The vessel is carrying 550 tons of industrial electronics "
        "originally scheduled for delivery to WH-WEST-202. "
        "The shipment contains perishable cooling components and "
        "cannot sustain delays exceeding 72 hours."
    ),
    "disrupted_port_id": "PORT-SEATTLE-02",
}
```

---  

## 8. Output  

A **JSON** file is written to `outputs/<incident_id>_reroute_advisory_report.json`.  

Key sections:

| Field | Description |
|-------|-------------|
| `incident_id` | Echo of the input ID |
| `original_incident_summary` | Short human readable summary of the disruption |
| `parsed_metadata` | Shipment data extracted by LangChain |
| `rag_validation_rules_applied` | List of logistics rules retrieved by RAG |
| `routes_evaluated` | Array of every route checked with decision & reason |
| `final_selected_route` | The route that was finally accepted (empty if escalated) |
| `queried_warehouse_metrics` | Warehouse info for the final route (or last checked) |
| `graph_routing_metadata` | `loops_executed`, `final_decision_state`, `reroute_impact_score` |
| `final_operations_brief` | LLM‑generated concise brief for the logistics team |

**Example (truncated)**  

```json
{
  "incident_id": "INC-001",
  "original_incident_summary": "Port of Seattle strike blocks cargo SH-4002.",
  "parsed_metadata": {
    "shipment_id": "SH-4002",
    "target_warehouse_id": "WH-WEST-202",
    "cargo_weight_tons": 550,
    "cargo_type": "industrial electronics",
    "has_perishables": true,
    "maximum_tolerable_delay_hours": 72
  },
  "rag_validation_rules_applied": [
    "Any alternative route exceeding 120 hours ...",
    "Cargo exceeding 500 tons ... WAREHOUSE_FIT_CHECK"
  ],
  "routes_evaluated": [
    {
      "route_id": "ROUTE-WEST-01",
      "decision": "ROUTE_CLARIFICATION",
      "reason": "Warehouse risk tier is ELEVATED"
    },
    {
      "route_id": "ROUTE-SOUTH-02",
      "decision": "OPTIMAL_PATH_FOUND",
      "reason": "All conditions acceptable"
    }
  ],
  "final_selected_route": {
    "route_id": "ROUTE-SOUTH-02",
    "alternative_port": "Port-South",
    "warehouse_id": "WH-SOUTH-303",
    "added_delay_hours": 72
  },
  "queried_warehouse_metrics": {
    "warehouse_name": "Southern Distribution Hub",
    "current_utilization_pct": 72,
    "operational_status": "ACTIVE",
    "risk_tier": "NORMAL"
  },
  "graph_routing_metadata": {
    "loops_executed": 1,
    "final_decision_state": "OPTIMAL_PATH_FOUND",
    "reroute_impact_score": 25
  },
  "final_operations_brief": "Route ROUTE‑SOUTH‑02 via Port‑South can deliver the cargo within the 72‑hour tolerance. Warehouse capacity and status are normal."
}
```

---  

## 9. LangGraph Workflow  

### Nodes  

| Node | Purpose |
|------|---------|
| `parse_incident` | LangChain structured extraction → `extracted_metadata` |
| `policy_rag_lookup` | Retrieve logistics rules → `routing_rag_context` |
| `load_alternative_routes` | Call `get_alternative_routes_tool` → `available_routes`; initialise indices |
| `select_route` | Pick route at `current_route_index` → `selected_route` |
| `check_warehouse` | Call `query_warehouse_inventory_tool` using the route’s `warehouse_id` → `warehouse_db_context` |
| `analyze_route` | Deterministic rule evaluation (utilization, status, risk, added delay, shipment‑delay limit). Sets `reroute_impact_score` and `routing_decision`. |
| `route_clarification` | If decision = `ROUTE_CLARIFICATION` → increment `clarification_attempts` & `current_route_index`. If another route exists, loop back to `select_route`; else set `routing_decision = CRITICAL_DELAY`. |
| `finalize_route` | Accepts the route, stores it permanently, ends the retry loop. |
| `escalate_incident` | Marks the incident as escalated (no acceptable route or critical delay). |
| `generate_report` | Uses Groq LLM to craft `final_operations_brief`; assembles the full JSON and writes it to `outputs/`. |

### Conditional Routing  

* **Decision = OPTIMAL_PATH_FOUND** → `finalize_route` → `generate_report`.  
* **Decision = ROUTE_CLARIFICATION** → `route_clarification` (retry).  
* **Decision = CRITICAL_DELAY** → `escalate_incident` → `generate_report`.  

### Retry Loop  

* Maximum clarification attempts = **2** (`max_clarification_attempts`).  
* Each retry increments `current_route_index`.  
* Loop stops when a route is accepted, when attempts exceed the limit, or when no more routes exist.  

### Finalization & Escalation  

* `finalize_route` records the selected route and associated warehouse metrics.  
* `escalate_incident` records an empty `final_selected_route` and the reason for escalation.  

---  

## 10. RAG Implementation  

1. **Load knowledge base** – `data/logistics_knowledge_base.txt`.  
2. **Chunking** – split into ~500‑word chunks using LangChain’s `RecursiveCharacterTextSplitter`.  
3. **Embeddings** – use a local HuggingFace sentence‑transformer model (e.g., `all-MiniLM-L6-v2`).  
4. **FAISS vector store** – `faiss-cpu` stores the embeddings locally.  
5. **RETRIRVER** - Uses local FIASS persistent DB for loading the chunks and do seantic search
---
## 14. Incident Execution Results  

The application was run against **all three** trainer‑provided incidents (INC‑001, INC‑002, INC‑003).  
Each run creates a JSON advisory report under `outputs/` and the following summary table records the final routing decision, the number of routes that were evaluated, and how many loop iterations (clarification retries) were performed.

| Incident | Final Decision | Routes Checked | Loops Executed |
|----------|----------------|----------------|----------------|
| **INC‑001** | `OPTIMAL_PATH_FOUND` | 2 | 1 |
| **INC‑002** | `OPTIMAL_PATH_FOUND` | 1 | 0 |
| **INC‑003** | `CRITICAL_DELAY` (escalated) | 3 | 2 |

*Explanation of the numbers*  

* **Routes Checked** – total distinct routes that the graph evaluated (including the one that finally succeeded or the last rejected one).  
* **Loops Executed** – how many times the **`route_clarification`** node was entered (i.e., number of retry attempts).  

All three reports are stored as:

```
outputs/INC-001_reroute_advisory_report.json
outputs/INC-002_reroute_advisory_report.json
outputs/INC-003_reroute_advisory_report.json
```

Each JSON follows the schema defined in the PRD (incident metadata, parsed shipment data, retrieved rules, route evaluations, final decision, impact score, and a short Groq‑LLM generated operations brief).

---  

## 15. Known Limitations  

| Limitation | Impact |
|------------|--------|
| **Local operational data only** – All warehouse utilisation, status, and route information come from static JSON files shipped with the repo. | The system cannot reflect real‑time changes (e.g., a warehouse suddenly becomes unavailable). |
| **No live port data** – Disruption detection and alternative‑port information are pre‑populated; there is no integration with external maritime APIs. | The assistant cannot react to new or unexpected port closures that are not already described in `route_options.json`. |
| **Fixed route dataset** – `data/route_options.json` is the single source of truth for alternative routes. | If a new route is added in production, the code mustbe redeployed with an updated file. |
| **Deterministic routing logic + LLM variability** – The routing decision (OPTIMAL_PATH_FOUND, ROUTE_CLARIFICATION, CRITICAL_DELAY) is performed by pure Python rules, but the **final operations brief** is generated by the Groq LLM. Because LLM output can vary slightly on each call, the human‑readable summary may differ between runs even when the underlying decision is identical. | Minor differences in phrasing do not affect downstream automation but should be considered when comparing reports verbatim. |
| **Embedding model is static** – The RAG pipeline uses a locally‑cached HuggingFace sentence‑transformer model. | Changing the model would require re‑building the FAISS index; the current index is tied to the specific embedding model version. |
| **No external persistence** – All state lives in‑memory during a single graph execution; there is no database or cache to store historic incidents. | Re‑runningthe same incident will re‑process everything from scratch. |

These limitations are intentional for the scope of the capstone project and keep the solution lightweight, reproducible, and fully runnable in a local developmentenvironment. Future extensions could plug in live data sources, a persistent vector store, or a micro‑service layer for real‑time updates.