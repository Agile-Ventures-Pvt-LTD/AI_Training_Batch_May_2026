# Supply Chain Logistics Rerouter

## 1. Project Overview

It is an AI-powered Supply Chain Logistics Rerouter system built using LangGraph, LangChain, Groq LLM, and RAG and pytest.

The agent can answer customer service queries by retrieving information from ccms.db database through a set of specializes tools as we used in this project.

The project demonstrates two implementations:
1. Custom LangGraph Agent 
---

## 2. Solution Approach

Go through PRD in detailed, after that i build rag, then i build schemas and architecture of the project,then in next phase i build tools, in next phase build langgraph nodes and graphs using langchain and langgraph, then do the relavant test by using pytest.

---
## Architecture.

```
Incident
↓
LangChain Extraction
↓
RAG Rule Retrieval
↓
Route and Warehouse Tools
↓
LangGraph Decision and Retry Loop
↓
Final Report

```

## Tech Stack

* Python 3.12+
* LangChain
* LangGraph
* Groq API
* RAG
* python-dotenv
* Pytest
* JSON

---

## 4. Project Structure

```text
supply_chain_logistics_rerouter/
│
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── data/
│   ├── logistics_knowledge_base.txt
│   ├── inventory_status.json
│   ├── route_options.json
│   └── sample_incidents.json
│
├── src/
│   ├── main.py
│   ├── state.py
│   ├── graph.py
│   ├── nodes.py
│   ├── tools.py
│   ├── rag.py
│   ├── schemas.py
│   └── report_writer.py
│
├── tests/
│   ├── test_tools.py
│   ├── test_routing.py
│   ├── test_nodes.py
│   └── test_graph.py
└── outputs/
├── INC-001_reroute_advisory_report.json
├── INC-002_reroute_advisory_report.json
├── INC-003_reroute_advisory_report.json
└── test_results.txt
```

---

## 5. Setup Instructions

### 1. Clone Repository

```bash
git clone <repository-url>
cd supply_chain_logistics_rerouter
```

### 2. Create Virtual Environment

```bash
uv venv
.venv\Scripts\activate
```

### 3. Install Dependencies

```bash
uv pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
KB_PATH = data
EMBEDDING_MODEL = 'sentence-transformers/all-mpnet-base-v2'
VECTOR_STORE_PATH = chroma_db
```

---

## 6.Running the Application

# For running RAG:
```bash
python src\rag.py
```

# For Running the mainapplication:
```bash
python src\main.py
```

---

## 7. Input
Explain:
incident_id
manifest_text
disrupted_port_id
Include one sample input.

Available Incidents:
  1. INC-001
  2. INC-002
  3. INC-003
  4. Run all incidents

Select incident: 4
---

## Output
```
{
  "incident_id": "INC-001",
  "original_incident_summary": "Cargo container SH-4002 is stranded outside the Port of Seattle due to a worker strike, carrying 550 tons of industrial electronics with perishable cooling components that cannot sustain delays over 72 hours.",
  "parsed_metadata": {
    "shipment_id": "SH-4002",
    "target_warehouse_id": "WH-WEST-202",
    "cargo_weight_tons": 550,
    "cargo_type": "industrial electronics",
    "has_perishables": true,
    "maximum_tolerable_delay_hours": 72
  },
  "rag_validation_rules_applied": [],
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
    "loops_executed": 1,
    "final_decision_state": "OPTIMAL_PATH_FOUND",
    "reroute_impact_score": 0
  },
  "final_operations_brief": "Optimal path found: ROUTE-SOUTH-02, diverting to Port-South and warehouse WH-SOUTH-303 with an added delay of 72 hours, utilizing the Southern Distribution Hub which is currently 72% utilized and operational."
}
```
## 9. LangGraph Workflow
Nodes
Conditional routing
Retry loop
Finalization
Escalation

---
## 10. ## RAG Implementation
```
Load logistics_knowledge_base.txt
↓
Split the document into chunks
↓
Create embeddings
↓
Store chunks in FAISS
↓
Create a retriever
↓
Retrieve relevant rules
```

## 11. Tools Implemented

1. query_warehouse_inventory_tool
2. get_alternative_routes_tool

---

## 12. Testing

Run tool tests:

```bash
pytest tests/ -v
```

---

## Future Enhancements

* Streamlit UI
* FastAPI deployment
* Authentication and authorization
* Add Persistent memory


---

## Author
Ashish Sinha
