# Project - Supply Chain Crisis Management and Logistics Rerouter

## Business Scenario (Need of the project in real World)

A major shipping port has suddenly become unavailable because of a strike, weather disruption, or
operational failure.

A shipment is already in transit and must be rerouted.

The logistics team needs to quickly determine:
1. What shipment is affected?
2. What type of cargo is being transported?
3. How much delay can the shipment tolerate?
4. Which alternative routes are available?
5. Can the warehouse assigned to the alternative route accept the shipment?
6. Do any logistics rules prevent the route from being selected?
7. Should another route be checked?
8. Should the incident be escalated?

This AI-powered Logistics Incident Assistant will evaluate the disruption and will recommend a suitable alternative route.

## Solution approach

The solution is designed using this system which makes the efficient use of RAG, Langchain, LangGraph.

- RAG -> This technology is used to load documents efficiently
         Perform chunking and convert them into embeddings
         Technically making our system more specific towards the posed problem or situation.

- LangChain -> Groq LLM integration, 
               Prompt templates
               Structured output
               Extracting shipment information from the incident
               Generating the final operations brief

- LangGraph -> Use LangGraph to manage:
               Shared application state
               Execution of workflow nodes
               Conditional routing
               Route retry logic
               Route finalization
               Incident escalation


## Main technologies used in the project

LangChain
RAG
LangGraph
Groq LLM
Local JSON and text data
pytest

## Working Expectations from this project

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

The main objective of this capstone is to demonstrate how LangChain, RAG, and LangGraph can work
together in one application.

## Framework responsibilties

### LangChain
Use of LangChain for:
- Groq LLM integration
- Prompt templates
- Structured output
- Extracting shipment information from the incident
- Generating the final operations brief

### RAG
Use of RAG to retrieve relevant logistics rules from the provided knowledge-base document.
The RAG pipeline must:
- Load the logistics knowledge-base file.
- Split the document into chunks.
- Create embeddings.
- Store the chunks in a local vector store.
- Retrieve rules relevant to the current shipping incident.
- Participants must not pass the complete logistics rulebook to the LLM for every incident.

### LangGraph
Use of LangGraph to manage:
- Shared application state
- Execution of workflow nodes
- Conditional routing
- Route retry logic
- Route finalization
- Incident escalation

## Virtual environment

- All the execution of the project, dependencies installation, environment variable configuration is being done in the virtual environemnt only.
- The virtual environment is created using uv command.
- Run this command to create a virtual environment:
cmd command:
"uv .venv"
- Virtual environment is made by the name .venv and can be made by any name as per user's choice.


## Technical Dependencies

Use Python and the following packages:
- langchain
- langchain-core
- langchain-community
- langchain-groq
- langchain-huggingface
- langgraph
- chromadb
- sentence-transformers
- pydantic
- python-dotenv
- pytest
- pytest-mock
- Compatible versions of all these packages are being installed in the virtual environment.


## Folder structure

supply-chain-logistics-rerouter/
 └── vaishnavi-gupta/
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
 └── outputs/
 ├── INC-001_reroute_advisory_report.json
 ├── INC-002_reroute_advisory_report.json
 ├── INC-003_reroute_advisory_report.json
 └── test_results.txt

## Input

3 variables are taken as input.
- incident_id
- manifest_text
- disrupted_port_id
For example:
{
    "incident_id": "INC-001",

    "manifest_text": "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle due to an active worker strike. The vessel is carrying 550 tons of industrial electronics originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling components and cannot sustain delays exceeding 72 hours.",

    "disrupted_port_id": "PORT-SEATTLE-02"
},

## data folder

This folder contains multiple files which consists of data which is fed to the RAG.

### logistics_knowledge_base.txt

This file contains the logistics rules used by the RAG pipeline.
The document contains rules related to:
- Maximum route delay
- Alternative ports
- Cargo weight
- Warehouse capacity
- Warehouse operational status
- Warehouse risk levels
- Route clarification
- Incident escalation

### inventory_status.json

This file contains the current operational information for warehouses.
Example structure:

"WH-EAST-101": {
"warehouse_name": "East Coast Logistics Hub",
"current_utilization_pct": 92,
"operational_status": "ACTIVE",
"risk_tier": "NORMAL"
}

### route_options.json

- This file contains the routes available when a port is disrupted.
Example structure:

"PORT-SEATTLE-02": [
{
"route_id": "ROUTE-WEST-01",
"alternative_port": "Port-West",
"warehouse_id": "WH-WEST-202",
"added_delay_hours": 48
},
{
"route_id": "ROUTE-SOUTH-02",
"alternative_port": "Port-South",
"warehouse_id": "WH-SOUTH-303",
"added_delay_hours": 72
}
]

### sample_incidents.json

- This file contains the incidents used to test the application.

Example structure:
[
{
"incident_id": "INC-001",
"manifest_text": "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded 
outside the Port of Seattle due to an active worker strike. The vessel is 
carrying 550 tons of industrial electronics originally scheduled for delivery to 
WH-WEST-202. The shipment contains perishable cooling components and cannot 
sustain delays exceeding 72 hours.",
"disrupted_port_id": "PORT-SEATTLE-02"
}
]

## src folder

This is the main working folder of the project.It consists of the files that together make RAG and LangGraph working.

### graph.py

- This file combines nodes and edges to make a complete graph structure of LangGraph.

### main.py

- This is the main file which connects all the files. This file is also responsible to run the project.

### nodes.py

- This file contains all the working nodes of the graph. 
1. parse_incident_node
2. policy_rag_lookup_node
3. load_alternative_routes_node
4. select_route_node
5. check_warehouse_node
6. analyze_route_node
7. route_clarification_node
8. finalize_route_node
9. escalate_incident_node
10. generate_output_node

### rag.py

- This file contains the code for performing RAG processes, like loading, chunking, embeddings, creating vector DB, retriever etc.

### report_writer.py

- This file is for writing the output in the required format.

### schemas.py

- This file defines the schema or design of the required output.  

### state.py

- This file contains multiple states of the graph.

### tools.py

- This file contains all the tools made for different functions.

## tests folder

- This folder consists of file that perform testing on the working of the project:

### test_graph.py

- This file tests whether the graph is created correctly and the edges, nodes, loops are working properly or no, using pytest module.

### test_nodes.py

- This file tests whether the nodes are made properly or not, whether they are functioing properly or not, using pytest module.

### test_tools.py

- This file tests the working of tools that are made in the project, using the pytest module.

### test_routing.py

- This tool checks whether the router is working or not and the loop is correctly created or not, using pytest module.

### pyproject.toml

- This file gets created as soon as the command "uv init" runs in the VSCode(cmd) terminal.
- This file contains summarization infomation about the project i.e,

[project]
name = "supply-chain-logistics-rerouter"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.14"
dependencies = []

## .env.example

- This file contains the secret keys that must not be revealed.
- Keys from this file are loaded using python-dotenv.
In this project:
.env.example file contains - "GROQ_API_KEY"
                             "MODEL_NAME"

## README.md

- This is a markdown file that consists of the whole information of the project
i.e, business scenario, real life use cases, technical as well as non-technical requirements of the 
project, from where the data is extracted, the outputs, file structure, the workflow and many more.

## requirements.txt

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

- These are the packages that need to be installed before running the project.

## outputs folder

- This folder consists of thev files that contains the output geneated by running the project.

### INC-001_reroute_advisory_report.json

- This file contains all the information about the supply chain incident 1.
- The output gets stored in the .json format.

### INC-002_reroute_advisory_report.json

- This file contains all the information about the incident 2.
- The output gets stored in the .json format.

### INC-003_reroute_advisory_report.json

- This file contains all the information about the incident 3.
- The output gets stored in the .json format.

### test_results.txt

- This is a text file that conatins all the outputs of pytest commands.
- It contains the output of the all the testing files i.e, 
1. test_graph.py
2. test_nodes.py
3. test_routing.py
4. test_tools.py
- for testing tools, there are multiple test cases i.e,
-> test_warehouse_tool_valid_id
-> test_warehouse_tool_invalid_id
-> test_route_tool_valid_port
-> test_parse_incident_required_fields
-> test_routing_high_warehouse_utilization
-> test_routing_elevated_risk
-> test_routing_valid_route
-> test_graph_retry_selects_next_route

## RAG workflow

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

## Working flow of the project

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

- The ROUTE_CLARIFICATION path creates an actual LangGraph loop.
- The graph does not immediately ends after a route is rejected.

## How to run the project

Run the command in the VSCode terminal :
cmd command:
"uv run main.py"
OR
"uv python run main.py"

## How to run the tests

Run the command in the VSCode terminal :
cmd command:
"uv run pytest tests/ -v"

## Author
Vaishnavi Gupta