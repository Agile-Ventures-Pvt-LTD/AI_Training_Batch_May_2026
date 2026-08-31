# Project Build - 1  Supply Chain Crisis Management and Logistics Re-Router

A major shipping port has suddenly become unavailable because of a strike, weather disruption, oroperational failure.

A shipment is already in transit and must be rerouted.

The logistics team needs to quickly determine:
* What shipment is affected?What type of cargo is being transported?
* How much delay can the shipment tolerate?
* Which alternative routes are available?
* Can the warehouse assigned to the alternative route accept the shipment?
* Do any logistics rules prevent the route from being selected?
* Should another route be checked?
* Should the incident be escalated?
So, I build an AI-powered Logistics Incident Assistant that evaluates the disruption and recommends a suitable alternative route.
---
## Project Overview

Build a logistics rerouting application using:
LangChain
RAG
LangGraph
Groq LLM
Local JSON and text data
pytest

The application must:
1. Accept a shipping incident as input.
2. Extract important shipment information using LangChain structured output.
3. Retrieve relevant logistics rules using RAG.
4. Load available alternative routes.
5. Check warehouse capacity and operational status.
6. Evaluate the selected route.
7. Try another route if the current route is unsuitable.
8. Escalate the incident when no acceptable route is available.
9. Generate a final logistics advisory report.

---
## Tech Stack
- Python
- LangChain
- LangGraph
- Groq LLM
- FAISS / Vector Store
- Pytest
- pydantic

---
## Project Structure

```text
supply_chain_logistics_rerouter/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── data/
│   ├── logistics_knowledge_base.txt
│   ├── inventory_status.json
│   ├── route_options.json
│   └── sample_incidents.json
├── src/
│   ├── main.py
│   ├── state.py
│   ├── graph.py
│   ├── nodes.py
│   ├── tools.py
│   ├── rag.py
│   ├── schemas.py
│   └── report_writer.py
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
## Prerequisites

Before running the project, make sure you have:

- Python 3.11 or 3.11+
- A Groq API Key

---

## Setup Instructions

Clone the repository.

```bash
git clone <repository-url>
```

Move into the project directory.

```bash
cd supply_chain_logistics_rerouter
```

Create a virtual environment.

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies.

```bash
pip install -r requirements.txt
```
---

## Environment Configuration

Create a `.env` file using the provided `.env.example`.

```env
GROQ_API_KEY=<Your Api Key>
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```
---
## Running the Application

```bash
python src/main.py
```

Give Some input according to **incident_id**:
 ```
 INC-001
 ```

## Output Structure

Final Json Output:
```json
{
  "incident_id": "INC-001",
  "original_incident_summary": "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle due to an active worker strike. The vessel is carrying 550 tons of industrial electronics originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling components and cannot sustain delays exceeding 72 hours.",
  "parsed_metadata": {
    "shipment_id": "SH-4002",
    "target_warehouse_id": "WH-WEST-202",
    "cargo_weight_tons": 550,
    "cargo_type": "industrial electronics",
    "has_perishables": true,
    "maximum_tolerable_delay_hours": 72
  },
  "rag_validation_rules_applied": [
    "Any alternative route exceeding 120 hours of total added transit delay must be classified as CRITICAL_DELAY.\nCargo exceeding 500 tons and routed through Port-South requires a WAREHOUSE_FIT_CHECK.\nA warehouse operating above 85 percent utilization cannot accept a new automated cargo shipment.\nIf a warehouse has an ELEVATED risk tier, another route or alternative facility must be checked before finalizing the route."
  ],
  "routes_evaluated": [],
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
    "loops_executed": 0,
    "final_decision_state": "OPTIMAL_PATH_FOUND",
    "reroute_impact_score": 0
  },
  "final_operations_brief": "Incident ID: INC-001 reports a critical disruption at the Port of Seattle due to a worker strike, stranding cargo container SH-4002 carrying 550 tons of industrial electronics. The selected route, ROUTE-SOUTH-02, diverts the shipment to Port-South and warehouse WH-SOUTH-303, incurring a 72-hour delay, which is within the maximum allowable delay of 72 hours for the perishable cargo. The decision was influenced by the warehouse condition that WH-SOUTH-303 is operating at 72% utilization, below the 85% threshold, allowing it to accept the new cargo shipment. The route was chosen as it did not exceed the 120-hour critical delay threshold, and a WAREHOUSE_FIT_CHECK was presumably required due to the cargo weight exceeding 500 tons routed through Port-South."
}
```

## LangGraph Workflow

```
   START
     │
     ▼
parse_incident
     │
     ▼
policy_rag_lookup
     │
     ▼
load_alternative_routes
     │
     ▼
select_route
     │
     ▼
select_route_router ──( escalate )──► escalate_incident
     │                                        │
( check_warehouse )                           │
     │                                        │
     ▼                                        │
check_warehouse                               │
     │                                        │
     ▼                                        │
analyze_route                                 │
     │                                        │
     ▼                                        │
route_decision_router                         │
     │   │   │                                │
     │   │   └────( CRITICAL_DELAY )──────────┤
     │   │                                    │
     │   └────────( ROUTE_CLARIFICATION )──► route_clarification
     │                                                │
( OPTIMAL_PATH_FOUND )                                ▼
     │                                      clarification_router
     ▼                                           │        │
finalize_route                                   │        │
     │                                   ( retry )   ( escalate )
     │                                       │            │
     │                                       ▼            │
     │                                 [select_route]     │
     │                                                    │
     └───────────────────────┬────────────────────────────┘
                             │
                             ▼
                      generate_report
                             │
                             ▼
                            END

```
---
## Rag Implementation

Document:
* Knowledge-base file
* Document loading
* Chunking
* Embeddings
* FAISS
* Retriever
---

## Tools Implemented

Tools:
```
query_warehouse_inventory_tool
get_alternative_routes_tool
```
---
## Testing

Execute all test cases using:

```bash
python test_rag_metrics.py
```
---
## Incident Execution Results

| Incident ID | Final Decision | Routes Checked | Loops Executed |
| :--- | :--- | :---: | :---: |
| **INC-001** | `OPTIMAL_PATH_FOUND` | 2 | 1 |
| **INC-002** | `OPTIMAL_PATH_FOUND` | 1 | 0 |
| **INC-003** | `CRITICAL_DELAY` | 3 | 2 |
---
## Limitations
Genuine limitations of the implementation.
- Uses local operational data
- Does not use live port data
- Uses a fixed route dataset
- LLM output may vary slightly
---
### Author
**Pranay Gupta**


