# CAPSTONE PROJECT BUILD – 1

## Supply Chain Crisis Management and Logistics Re-Router
---
## Working 

- Accepts a shipping incident as input.
- Extracts important shipment information using LangChain structured output.
- Retrieve relevant logistics rules using RAG.
- Loads available alternative routes.
- Check warehouse capacity and operational status.
- Evaluates the selected route.
- Try another route if the current route is unsuitable.
- Escalate the incident when no acceptable route is available.
- Generate a final logistics advisory report.
---
## Framework Responsibilities: 
The responsibilities of each framework:
### LangChain
Used LangChain for:

1. Groq LLM integration
2. Prompt templates
3. Structured output
4. Extracting shipment information from the incident
5. Generating the final operations brief

---
### RAG
-  Used RAG to retrieve relevant logistics rules from the provided knowledge-base document.
#### The RAG pipeline:

1. Loads the logistics knowledge-base file.
2. Splits the document into chunks.
3. Creates embeddings.
4. Stores the chunks in a local vector store.
5. Retrieves rules relevant to the current shipping incident.

---
## LangGraph
Used LangGraph to manage:

1. Shared application state
2. Execution of workflow nodes
3. Conditional routing
4. Route retry logic
5. Route finalization
6. Incident escalation
---

## Requirement:
- create a requirements.txt file ith the above libraries
```text
langchain
langchain-core
langchain-community
langchain-groq
langchain-huggingface
langgraph
chromadb
sentence-transformers
pydantic
python-dotenv
pytest
pytest-mock
```
## How to run the Project:
- initialize venv
```bash
uv init
```
- create venv
```bash
uv venv
```
- activate venv
```bash
.venv/Scripts/Activate
```
## Install Dependencies

```bash
uv add requirements.txt
```

## Run Project
Run the Project
```bash
uv run python src/main.py
```

## Run All Tests

```bash
uv run pytest tests/ -v
```

## Run Integration Tests

```bash
uv run pytest -m integration -v
```

## Save Test Results

```bash
uv run pytest tests/ -v > outputs/test_results.txt
```
---
## Execution Flow 

```bash
Shipping Incident Input
↓
Parse Incident
↓
Retrieve Logistics Rules using RAG
↓
Load Alternative Routes
↓
Select Route
↓
Check Assigned Warehouse
↓
Analyze Route
↓
Make Routing Decision
            │
            ├── OPTIMAL_PATH_FOUND
            │         ↓ 
            |    Finalize Route
            |          ↓
            |    Generate Report
            │     
            │          
            │     
            │
            ├── ROUTE_CLARIFICATION
            │          ↓
            │     Try Next Route
            │          ↓
            │     Select Route
            │          ↓
            │     Check Warehouse
            │          ↓
            │     Analyze Route
            │
            └── CRITICAL_DELAY
                     ↓
              Escalate Incident
                     ↓
              Generate Report
```
## LangGraph Nodes:
```bash
parse_incident
policy_rag_lookup 
load_alternative_routes
select_route
check_warehouse
analyze_route
route_clarification
finalize_route
escalate_incident
generate_report
```
## USES:
- parse_incident
Purpose:
Uses LangChain structured output to extract shipment information from manifest_text

- policy_rag_lookup
Purpose:
Retrieve logistics rules relevant to the current incident.

-  
load_alternative_routes
Purpose:
Use:
get_alternative_routes_tool
Load routes for the disrupted port.
Store the result in:
available_routes

- select_route
Purpose:
Select a route from available_routes .
The selected route is in: current_route_index
Stores the selected route in:
selected_rout

- check_warehouse
Purpose:

Reads the warehouse_id from the selected route.

query_warehouse_inventory_tool
Stores the result in:
warehouse_db_context

-  
analyze_route
Purpose:

Evaluates the selected route using:

Extracted shipment metadata
Retrieved logistics rules
Selected route details
Added route delay
Warehouse utilization
Warehouse operational status
Warehouse risk tier

- route_clarification
Purpose:
Reject the current route and check the next available route.
The node:
Increases
clarification_attempts .
Increases
current_route_index . & 
Check whether another route exists.

- finalize_route
Purpose:
Finalize the accepted route.
The final selected route must be retained in the graph state.

- 
escalate_incident
Purpose:
Mark the incident for escalation.

-  generate_report
Purpose:
Generate the final result.
Use LangChain and the Groq LLM to create a short 
final_operations_brief 
 
### Scores logic:
+30 if warehouse utilization is above 85 percent
+25 if warehouse risk tier is ELEVATED
+30 if warehouse status is not ACTIVE
+25 if added route delay exceeds the shipment delay limit
+50 if added route delay exceeds 120 hours
MAX = 100

## Test Output:
```bash
outputs/
├── INC-001_reroute_advisory_report.json
├── INC-002_reroute_advisory_report.json
├── INC-003_reroute_advisory_report.json
└── test_results.txt
```
## Folder Structure:
```bash
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
│
└── outputs/
├── INC-001_reroute_advisory_report.json
├── INC-002_reroute_advisory_report.json
├── INC-003_reroute_advisory_report.json
└── test_results.txt
```
---
