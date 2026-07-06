## 1. Project Overview
This is a supply chain crisis management logistics rerouter workflow.

---
## 2. Solution Approach

- Explain how the application processes a shipping incident.
- Accept a shipping incident as input.
- Extract important shipment information using LangChain structured output.
- Retrieve relevant logistics rules using RAG.
- Load available alternative routes.
- Check warehouse capacity and operational status.
- Evaluate the selected route.
- Try another route if the current route is unsuitable.
- Escalate the incident when no acceptable route is available.
- Generate a final logistics advisory report.


---

## 3. Architecture

Explain the responsibility of:
```
LangChain
RAG
LangGraph
Python tools
Groq LLM
```
A simple workflow diagram is recommended.

Example:
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
---

## 4. Project Structure

Explain the main folders and important files.

```
subhranshu-pattnayak
├── .env
├── .gitignore
├── .python-version
├── README.md
├── data
│   ├── inventory_status.json
│   ├── logistics_knowledge_base.txt
│   ├── route_options.json
│   └── sample_incidents.json
├── pyproject.toml
├── src
│   ├── graph.py
│   ├── main.py
│   ├── nodes.py
│   ├── rag.py
│   ├── schemas.py
│   ├── state.py
│   ├── tools.py
│   └── utils
│       ├── __init__.py
│       ├── chunker.py
│       ├── config.py
│       ├── embedding.py
│       ├── llm.py
│       └── loader.py
└── uv.lock
```

---

## 5. Setup Instructions

Document:
```
Environment setup:

uv venv

.env configuration:

GROQ_MODEL=openai/gpt-oss-120b
GROQ_API_KEY=...

OUTPUT_PATH=outputs
SRC_PATH=src
DATA_PATH=data
COLLECTION_NAME=logistics-rule-collection
DB_PATH=./logistics_rule_db

data_file_name=logistics_knowledge_base.txt
alternate_route_file_name=route_options.json
warehouse_file_name=inventory_status.json

Dependency installation
uv sync

```
---

## 6. Running the Application

Provide the exact run command.

```
uv run python src/main.py
```

## 7. Input

Explain:
```
incident_id
manifest_text
disrupted_port_id
```
Include one sample input.

---

## 8. Output

Explain the final JSON report.

Include the output file location.

---

## 9. LangGraph Workflow

Explain:

* Nodes
* Conditional routing
* Retry loop
* Finalization
* Escalation

---

## 10. RAG Implementation

Document:

* Knowledge-base file
* Document loading
* Chunking
* Embeddings
* Chromadb
* Retriever

## 11. Tools Implemented

Document:
```python
query_warehouse_inventory_tool
get_alternative_routes_tool
```
Explain the input and output of each tool.

---

## 12. Known Limitations

- No tests
- no outputs registered.