## Supply Chain Crisis Management and Logistics Re-Router

 AI-powered Logistics Incident Assistant that evaluates the
 disruption and recommends a suitable alternative route using Langchain,Rag, Langraph, Grog LLM

 ## Project Overview 
 ``` A major shipping port has suddenly become unavailable because of a strike, weather disruption, or operational failure.
  A shipment is already in transit and must be rerouted.
  The logistics team needs to quickly determine:

What shipment is affected?
What type of cargo is being transported?
How much delay can the shipment tolerate?
Which alternative routes are available?
Can the warehouse assigned to the alternative route accept the shipment?
Do any logistics rules prevent the route from being selected?
Should another route be checked?
Should the incident be escalated
 Goal : AI-powered Logistics Incident Assistant that evaluates the disruption and recommends a suitable alternative route.
```
 ## Solution Approach
 By ussing
``` 
LangChain
RAG
LangGraph
Groq LLM
Local JSON and text data
pytest
```
 This application works as below : 
1. Accept a shipping incident as input.
2. Extract important shipment information using LangChain
3. structured output.
4. Retrieve relevant logistics rules using RAG.
5. Load available alternative routes.
6. Check warehouse capacity and operational status.
7. Evaluate the selected route.
8. Try another route if the current route is unsuitable.
9. Escalate the incident when no acceptable route is available.
10. Generate a final logistics advisory report.

## architecture 

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
## Project structure 
```
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
|
└── outputs/
├── INC-001_reroute_advisory_report.json
├── INC-002_reroute_advisory_report.json
├── INC-003_reroute_advisory_report.json
└── test_results.tx
```
## Setup Instructions

1. Create a virtual environment:
activate 
```
.venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Set up environment variables:
```
 .env.example  or .env
```

5.  `.env` with your API keys:
```
GROQ_API_KEY= your_groq_API_key
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB=chroma
CHUNK_SIZE=100
CHUNK_OVERLAP=50
TOP_K=3
```
6. requirements:
```
langchain-huggingface
pytest
pytest-mock
langgraph
langchain
langchain-core
langchain-community
langchain-groq
langchain-chroma
chromadb
sentence-transformers
python-dotenv
pydantic
numpy
```
6. dataset folder 
mentioned in above folder structure

## Running 
## How to run 

Run the agent
```bash
 uv run -m src.app
```
Run the tests
```bash
uv run -m tests/
```
## Input
 sample input 
 ```
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
"disrupted_port_id": "PORT-SEATTLE-02"
}

 ```
 ## Ouput
 output  will be given in below structure:

 ```
 {
}
"incident_id": "INC-001",
"original_incident_summary": "",
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
"final_selected_route": {},
"queried_warehouse_metrics": {},
"graph_routing_metadata": {
"loops_executed": 0,
"final_decision_state": "",
"reroute_impact_score": 0
},
"final_operations_brief": "
 ```
 Output is saved the report to outputs/reroute_advisory_report.json

## Rag Implementation
pipeline:
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
Retrieve relevant rule
```
## tools implemented
 1. query_warehouse_inventory_tool: to extract warehouse  curent operational information
 2. get_alternative_routes_tool : to get all available route for the requested disrupted port 

## testing
test command:
```bash
uv run pytest tests/-v
```
components tested:
```
 - Warehouse lookup tool
 - Alternative route lookup tool
 - Metadata extraction- Route decision logic
 - Reroute impact score
 - LangGraph retry loop
 - Incident escalation
 - Final report structure

```


## Known limitations
1. Uses local operational data
2. Does not use live port data
3. Uses a fixed route dataset
4. LLM output may vary slightly
