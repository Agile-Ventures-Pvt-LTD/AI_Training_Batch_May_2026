# Project Overview

A major shipping port has suddenly become unavailable because of a strike, weather disruption, or
operational failure.
A shipment is already in transit and must be rerouted.
The logistics team needs to quickly determine:
- What shipment is affected?
- What type of cargo is being transported?
- How much delay can the shipment tolerate?
- Which alternative routes are available?
- Can the warehouse assigned to the alternative route accept the shipment?
- Do any logistics rules prevent the route from being selected?
- Should another route be checked?
- Should the incident be escalated?

# Solution Approach

Our solution is here that If any sudden incident occur on the port the transportation process does not stop and we get immediate escalation methods to overcome that challenges with the reasoning behind that incidents. Our solution is an orchestration framework which pass through every node that are responsible for giving good response for the incidents that occur.For this approach we used LangChain, RAG, LangGraph and Groq LLM.

# Architecture
- **RAG** here RAG is used to get the exact way of escalating the incident that has occur so to get proper response.
- **LangChain** here LangChain is used to structure the output and make tools from where we get the knowledge about our warehouse and ports
- **LangGraph** here is used for orchestration purpose where we orchestrate through many nodes to get the accurate result for the incidents that had occured using LLM.
- **Groq LLM** here it is used to provide LLM Model to LangGraph Agent to generate a summarize answer how to escalate the incidents.

# Project Folder

```text
supply_chain_logistics_rerouter/
│
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── data/
│   ├── logistics_knowledge_base.txt       #It contains the the process how to escalate incident used by RAG
│   ├── inventory_status.json              # It contatins data about how much capacity left in warehouse
│   ├── route_options.json
│   └── sample_incidents.json
│
├── src/
│   ├── main.py                            # File to run the framework
│   ├── state.py                           # Here we had define the State of the LangGraph used by the nodes
│   ├── graph.py                           # Here the workflow of nodes and tools are described
│   ├── nodes.py                           # In this we had described the work of different nodes.
│   ├── tools.py                           # Here two langchain tools are made to perform operations
│   ├── rag.py                             # It is used for the document loading and chunking
│   ├── schemas.py
│   └── report_writer.py
│
├── tests/
│   ├── test_tools.py                      # pytest of our tool is done for verification purpose.
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
# Setup Instrution
1. .env file setup
```bash
GROQ_API_KEY=
HF_TOKEN=
GROQ_MODEL=llama-3.3-70b-versatile
```
2. Project setup
```bash
uv venv
uv pip install requirements.txt
```
# Run The Aplication
1. Run the main.py file using
```bash
python -m src.main
```
2. Run the test_tool file for pytest
```bash
pytest -m tests/test_tool
```
# Output

```
"**Final Report: Incident Analysis and Routing Decision**\n\n**I. Introduction**\n\nThis report provides an analysis of the incident metadata, extracted metadata, retrieved context, and selected route for the stranded cargo container SH-4002 at the Port of Seattle. The report aims to summarize the key findings and provide a structured overview of the incident and routing decision.\n\n**II. Incident Summary**\n\n* **Incident Type:** CRITICAL DISRUPTION\n* **Cause:** Active worker strike at the Port of Seattle\n* **Affected Cargo:** 550 tons of industrial electronics (perishable cooling components)\n* **Original Destination:** WH-WEST-202\n* **Maximum Allowable Delay:** 72 hours\n\n**III. Extracted Metadata**\n\n* **Manifest Text:** CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle due to an active worker strike.\n* **Key Details:**\n\t+ Cargo type: Industrial electronics\n\t+ Cargo weight: 550 tons\n\t+ Perishable cooling components\n\t+ Original destination: WH-WEST-202\n\n**IV. Retrieved Context**\n\n* **Routing Rules:**\n\t+ Any alternative route exceeding 120 hours of total added transit delay must be classified as CRITICAL_DELAY.\n\t+ Cargo exceeding 500 tons and routed through Port-South requires a WAREHOUSE_FIT_CHECK.\n* **Warehouse Operating Rules:**\n\t+ A warehouse operating above 85 percent utilization cannot accept a new automated cargo shipment.\n\t+ If a warehouse has an ELEVATED risk tier, another route or alternative facility must be checked before finalizing the route.\n\n**V. Selected Route**\n\n* **Route ID:** ROUTE-WEST-01\n* **Alternative Port:** Port-West\n* **Warehouse ID:** WH-WEST-202\n* **Added Delay Hours:** 48\n\n**VI. Warehouse Context**\n\n* **Warehouse Utilization:** Not available\n* **Risk Tier:** Not available\n\n**VII. Reroute Impact Score**\n\n* **Score:** 48\n\n**VIII. Routing Decision**\n\n* **Decision:** OK\n* **Justification:** The selected route (ROUTE-WEST-01) with an added delay of 48 hours does not exceed the maximum allowable delay of 72 hours. The cargo weight (550 tons) exceeds the threshold for a WAREHOUSE_FIT_CHECK, but the warehouse context is not available to determine the feasibility of the selected route.\n\n**IX. Conclusion**\n\nThe incident analysis and routing decision have been completed, and the selected route (ROUTE-WEST-01) has been deemed acceptable with an added delay of 48 hours. However, it is essential to monitor the warehouse context and utilization to ensure that the selected route remains feasible and does not pose any additional risks to the cargo."
```

# LangGraph Flow
- **Nodes** these perform some action that needs to be done
- **Conditional Routing** it helps to route between the conditions.
- **Retry Loop** it loops to retry the certain condition for some retries
- **Finalization** it finalize if the loop is executed.
- **Escalation** if maximum retries reach it escalate from there
- **Graph** it is used to decide the flow of the nodes and tools.

# RAG Implementation

1. Load the database
2. create chunk of database
3. get the embedding model
4. create a persisted vector store
5. create a retriver to retrive relevant chunks

# Tools Implemented
- query_warehouse_inventory_tool: It provides the output of warehouse capacity using input as warehouse id
- get_alternative_routes_tool: It provides output of the port routes from given port is as input.

# Limitation

- More tools can be implemented 
- A good user interface can be created
- We can use Advance RAG for more better retrival.

# Author 

**Mohd Zaid Ansari**
