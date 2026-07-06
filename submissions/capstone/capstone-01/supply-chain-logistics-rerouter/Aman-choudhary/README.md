## Supply Chain Crisis Management and Logistics ReRouter
A major shipping port has suddenly become unavailable because of a strike, weather disruption, or
operational failure.
A shipment is already in transit and must be rerouted.
The logistics team needs to quickly determine
##  Project Objective
LangChain
RAG
LangGraph
Groq LLM
Local JSON and text data
pytest
##  Framework Responsibilities
LangChain
RAG
LangGraph
## 4. Technical Dependencies
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
## Environment Configuration 
.env
GROQ_API_KEY=<your_groq_api_key>
GROQ_MODEL=llama-3.3-70b-versatile
## Files Provided 
```
data/
├── logistics_knowledge_base.txt
├── inventory_status.json
├── route_options.json
└── sample_incidents.json
```
##  Project Execution Flow
```
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
 │ ↓
 │ Finalize Route
 │ ↓
 │ Generate Report
 │
 ├── ROUTE_CLARIFICATION
 │ ↓
 │ Try Next Route
 │ ↓
 │ Select Route
 │ ↓
 │ Check Warehouse
 │ ↓
 │ Analyze Route
 │
 └── CRITICAL_DELAY
 ↓
 Escalate Incident
 ↓
 Generate Report
```
## RAG Implementation Requirements
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

## 
## Project Structure
```

supply_chain_logistics_rerouter/
│
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── data/
│ ├── logistics_knowledge_base.txt
│ ├── inventory_status.json
│ ├── route_options.json
│ └── sample_incidents.json
│
├── src/
│ ├── main.py
│ ├── state.py
│ ├── graph.py
│ ├── nodes.py
│ ├── tools.py
│ ├── rag.py
│ ├── schemas.py
│ └── report_writer.py
│
├── tests/
│ ├── test_tools.py
│ ├── test_routing.py
│ ├── test_nodes.py
│ └── test_graph.py
│
34
└── outputs/
 ├── INC-001_reroute_advisory_report.json
 ├── INC-002_reroute_advisory_report.json
 ├── INC-003_reroute_advisory_report.json
 └── test_results.txt
```
## Setup Instructions

1.Clone
git clone url 
cd Aman-choudhary
## Create Virtual Environment
python -m venv .venv
## Activate Virtual Environment
venv\Scripts\activate
source .venv/bin/activate
## Install Dependencies
pip install -r requirements.txt
## Configure Environment Variables
create .env
.env---> GROQ_API_KEY=your_groq_api_key GROQ_MODEL=llama-3.3-70b-versatile DB_PATH=data/ccms.db