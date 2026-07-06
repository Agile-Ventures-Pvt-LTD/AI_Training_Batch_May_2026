# Project Overview

A major shipping port has suddenly become available because of a strike, weather disruption, oroperational failure.A shipment is already in transit and must be rerouted.The logistics team needs to quickly determine:
What shipment is affected?
What type of cargo is being transported?
How much delay can the shipment tolerate?
Which alternative routes are available?
Can the warehouse assigned to the alternative route accept the shipment?
Do any logistics rules prevent the route from being selected?Should another route be checked?
Should the incident be escalated?


# Solution Approach

This problem can be solved by developing a AI-powered Logistics Incident Assistant that evaluates the disruption and recommends a suitable alternative route. The project is implemented using Langchain, RAG and Langgraph.

# Architecture
The application must:
-Accept a shipping incident as input.
-Extract important shipment information using LangChain structured output.
-Retrieve relevant logistics rules using RAG.Load available alternative routes.
-Check warehouse capacity and operational status.
-Evaluate the selected route.Try another route if the current route is unsuitable.
-Escalate the incident when no acceptable route is available.
-Generate a final logistics advisory report.
-The main objective of this capstone is to demonstrate how LangChain, RAG, and LangGraph can worktogether in one application

```text
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

# Project Structure
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
          │          ├── OPTIMAL_PATH_FOUND
          │          ↓          │     Finalize Route
          │          ↓          │     Generate Report
12
          │          ├── ROUTE_CLARIFICATION
          │          ↓          │     Try Next Route
          │          ↓          │     Select Route
          │          ↓          │     Check Warehouse
          │          ↓          │     Analyze Route
          │          └── CRITICAL_DELAY
                     ↓
              Escalate Incident
                     ↓
              Generate Report

# Setup Instructions
.env file includes
```text
GROQ_API_KEY=
HF_TOKEN=
```

requirements.txt
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
langchain_chroma
faiss-cpu
langchain-openai
```

# Running the Application

```bash
python -m main.py
```

# Input

User will provide 3 variables as input
1. incident_id: it contain the incident id of the shipment
2. manifest_text: it contains the additional details which will be stored in extract_metadata
3. disrupted_port_id: it is the disrupted port id
Include one sample input.

# Output

{"incident_id": "INC-001","original_incident_summary": "","parsed_metadata": {"shipment_id": "SH-4002","target_warehouse_id": "WH-WEST-202","cargo_weight_tons": 550,"cargo_type": "industrial electronics","has_perishables": true,"maximum_tolerable_delay_hours": 72},"rag_validation_rules_applied": [],"routes_evaluated": [],"final_selected_route": {},
"queried_warehouse_metrics": {},"graph_routing_metadata": {"loops_executed": 0,"final_decision_state": "","reroute_impact_score": 0},"final_operations_brief": ""}

# LangGraph Workflow

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
          │          ├── OPTIMAL_PATH_FOUND
          │          ↓          │     Finalize Route
          │          ↓          │     Generate Report

          │          ├── ROUTE_CLARIFICATION
          │          ↓          │     Try Next Route
          │          ↓          │     Select Route
          │          ↓          │     Check Warehouse
          │          ↓          │     Analyze Route
          │          └── CRITICAL_DELAY
                     ↓
              Escalate Incident
                     ↓
              Generate Report

# RAG Implementation

# Tools Implemented
Document:
-query_warehouse_inventory_tool: it takes warehouse_id as input and return details of the warehouse.
-get_alternative_routes_tool: it provide a list of all the alternative routes present

Explain the input and output of each tool.
# Testing
Tools testing is performed in test_tools.py
```bash
python -m pytest
```

# Known Limitations
Document genuine limitations of the implementation.
-Uses local operational data
-Does not use live port data
-Uses a fixed route dataset
-LLM output may vary slight