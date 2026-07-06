# Supply Chain Crisis Management and Logistics Re-Router

1. ## Project Overview

```
This project is designed to solve a business problem. When there is a major shipping port suddenly becomes unavailable due to strike, weather disruption, oroperational failure.Since the shipment is already in transmit and must be re-routed accordingly.

The logistic team needs to quickly determine different parameters:
- which shipment is affected?
- what type of cargo is being transported?
-which alternative routes are available?
- can the warehouse assigned to the alternative route accept the shipment?
- Do any logistics rules prevent the route from being selected?
- Should another route be checked?
- Should the incident be escalated?

```

2. ## Solution Approach

```
We will approach with incident id and moving forward with langchain extraction.

In langchain extraction we will start with the given data groq llm setup, generate prompt templates, used to get structured output, extract shipment information from incident and to generate final operational breif.

RAG pipeline: loading->chunking->embedding->vectorstore->retriever  

We added two major python tools:
- query_warehouse_inventory_tool
- get_alternative_routes_tool

Langgraph is the crucial step in this project as will manage shared application state, handle execution of the workflow node, conditional routing, route retry logic, route finalization and incident escalation.
 ```


3. ## Architecture:

```
We will approach with incident id and moving forward with langchain extraction.

In langchain extraction we will start with the given data groq llm setup, generate prompt templates, used to get structured output, extract shipment information from incident and to generate final operational breif.

RAG pipeline: loading->chunking->embedding->vectorstore->retriever  

We added two major python tools:
- query_warehouse_inventory_tool
- get_alternative_routes_tool

Langgraph is the crucial step in this project as will manage shared application state, handle execution of the workflow node, conditional routing, route retry logic, route finalization and incident escalation.


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
-

```

4. ## Folder Structure:

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
├── run_incidents.py
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

```

5. ## Setup Instruction:

```

GROQ_API_KEY=your api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
HF_TOKEN=your hf_token_here

```

6. ## Commands for running:

- ### for running Test cases:

```bash
pytest tests/
```

- ### For running the application

```bash 
python -m src.main     (Runs main file directly from root.)

```

7. ## Input:


```
The application will take 3 major inputs:

- incident id - This is the unique indentifier for the incident used to fetch all the information about a particular incident.

- manifest_text - This text is basically containing the reason of the crisis and also the solution or step taken for particular crisis.

- disrupted_port_id -  This is the id of the dedicated port where crisis happened.

```

8. ## Output:


-  ### Running all test

```bash 
pytest tests/
```

```
(supply-chain-logistics-rerouter) C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter>pytest tests/
================================================== test session starts ==================================================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter
configfile: pyproject.toml
plugins: anyio-4.14.1, langsmith-0.9.7, mock-3.15.1
collected 13 items                                                                                                       

tests\test_graph.py ..                                                                                             [ 15%]
tests\test_nodes.py ...                                                                                            [ 38%]
tests\test_routing.py .....                                                                                        [ 76%]
tests\test_tools.py ...                                                                                            [100%]

=================================================== warnings summary ====================================================
src\rag.py:2
  C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter\src\rag.py:2: DeprecationWarning: `langchain-community` is being sunset and is no longer actively maintained. See https://github.com/langchain-ai/langchain-community/issues/674 for details and migration guidance toward standalone integration packages.
    from langchain_community.document_loaders import TextLoader

tests\test_nodes.py:4
  C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter\tests\test_nodes.py:4: PytestUnknownMarkWarning: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.integration

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================ 13 passed, 2 warnings in 18.79s ============================================

(supply-chain-logistics-rerouter) C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter>
```

- ### for running incident

```bash
python -m run_incidents
```

```
Output: 
(supply-chain-logistics-rerouter) C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter>python -m run_incidents
Running automated incident execution script...

Processing INC-001...

--- Node: parse_incident (INC-001) ---
Extracted Metadata: {"shipment_id": "SH-4002", "cargo_weight_tons": 550, "cargo_type": "industrial electronics", "target_warehouse_id": "WH-WEST-202", "has_perishables": true, "maximum_tolerable_delay_hours": 72}

--- Node: policy_rag_lookup ---
Loading weights: 100%|███████████████████████████████████████████████| 103/103 [00:00<00:00, 8091.05it/s]
Retrieved Logistics Rules:
RULE-02: Port South Fit Check
Cargo exceeding 500 tons and routed through Port-South requires a WAREHOUSE_FIT_CHECK to verify heavy machinery compatibility and structural floor load capacity.

RULE-03: Warehouse Utilization Limits
A warehouse operating above 85 percent utilization cannot accept a new automated cargo shipment. Any route assigned to a warehouse exceeding 85% utilization must be rejected, triggering a ROUTE_CLARIFICATION.

RULE-07: Perishable Cargo Processing
Perishable cooling components and general perishable cargo require immediate priority routing. If no acceptable alternative route under the delay limit is found, the incident must be escalated.

--- Node: load_alternative_routes ---
Available alternative routes for PORT-SEATTLE-02: [{'route_id': 'ROUTE-WEST-01', 'alternative_port': 'Port-West', 'warehouse_id': 'WH-WEST-202', 'added_delay_hours': 48}, {'route_id': 'ROUTE-SOUTH-02', 'alternative_port': 'Port-South', 'warehouse_id': 'WH-SOUTH-303', 'added_delay_hours': 72}, {'route_id': 'ROUTE-CENTRAL-03', 'alternative_port': 'Port-Central', 'warehouse_id': 'WH-CENTRAL-404', 'added_delay_hours': 96}]

--- Node: select_route ---
Selected route [0]: {'route_id': 'ROUTE-WEST-01', 'alternative_port': 'Port-West', 'warehouse_id': 'WH-WEST-202', 'added_delay_hours': 48}

--- Node: check_warehouse ---
Warehouse metrics for WH-WEST-202: {'warehouse_name': 'Pacific Gateway Storage', 'current_utilization_pct': 68, 'operational_status': 'ACTIVE', 'risk_tier': 'ELEVATED'}

--- Node: analyze_route ---
Reroute Impact Score: 25, Decision: ROUTE_CLARIFICATION, Reason: Warehouse risk tier is ELEVATED

--- Node: route_clarification ---
Checking next alternative route. Index: 1

--- Node: select_route ---
Selected route [1]: {'route_id': 'ROUTE-SOUTH-02', 'alternative_port': 'Port-South', 'warehouse_id': 'WH-SOUTH-303', 'added_delay_hours': 72}

--- Node: check_warehouse ---
Warehouse metrics for WH-SOUTH-303: {'warehouse_name': 'Southern Distribution Hub', 'current_utilization_pct': 72, 'operational_status': 'ACTIVE', 'risk_tier': 'NORMAL'}

--- Node: analyze_route ---
Reroute Impact Score: 0, Decision: OPTIMAL_PATH_FOUND, Reason: Warehouse and route conditions are acceptable

--- Node: finalize_route ---
Finalized Route: ROUTE-SOUTH-02

--- Node: generate_report ---
LLM Operations Brief:
Here is a concise final operations brief for the logistics team:

Incident INC-001 involved a critical disruption to cargo container SH-4002, which was stranded outside the Port of Seattle due to a worker strike. An alternative route, ROUTE-SOUTH-02, was selected to mitigate delays, as the original warehouse, WH-WEST-202, had an elevated risk tier. The decision was influenced by RULE-07: Perishable Cargo Processing, which prioritizes immediate routing for perishable components, and RULE-02: Port South Fit Check, ensuring compatibility with the new warehouse, WH-SOUTH-303, which has a normal risk tier and 72% utilization.
Incident INC-001 complete. Decision: OPTIMAL_PATH_FOUND

Processing INC-002...

--- Node: parse_incident (INC-002) ---
Extracted Metadata: {"shipment_id": "SH-4105", "cargo_weight_tons": 250, "cargo_type": "consumer electronics", "target_warehouse_id": "WH-SOUTH-303", "has_perishables": false, "maximum_tolerable_delay_hours": null}

--- Node: policy_rag_lookup ---
Retrieved Logistics Rules:
RULE-01: Delay Limits and Critical Delays
Any alternative route exceeding 120 hours of total added transit delay must be classified as CRITICAL_DELAY. Critical delays trigger immediate escalation to the port logistics director.

RULE-03: Warehouse Utilization Limits
A warehouse operating above 85 percent utilization cannot accept a new automated cargo shipment. Any route assigned to a warehouse exceeding 85% utilization must be rejected, triggering a ROUTE_CLARIFICATION.

RULE-02: Port South Fit Check
Cargo exceeding 500 tons and routed through Port-South requires a WAREHOUSE_FIT_CHECK to verify heavy machinery compatibility and structural floor load capacity.

--- Node: load_alternative_routes ---
Available alternative routes for PORT-SEATTLE-02: [{'route_id': 'ROUTE-WEST-01', 'alternative_port': 'Port-West', 'warehouse_id': 'WH-WEST-202', 'added_delay_hours': 48}, {'route_id': 'ROUTE-SOUTH-02', 'alternative_port': 'Port-South', 'warehouse_id': 'WH-SOUTH-303', 'added_delay_hours': 72}, {'route_id': 'ROUTE-CENTRAL-03', 'alternative_port': 'Port-Central', 'warehouse_id': 'WH-CENTRAL-404', 'added_delay_hours': 96}]

--- Node: select_route ---
Selected route [0]: {'route_id': 'ROUTE-WEST-01', 'alternative_port': 'Port-West', 'warehouse_id': 'WH-WEST-202', 'added_delay_hours': 48}

--- Node: check_warehouse ---
Warehouse metrics for WH-WEST-202: {'warehouse_name': 'Pacific Gateway Storage', 'current_utilization_pct': 68, 'operational_status': 'ACTIVE', 'risk_tier': 'ELEVATED'}

--- Node: analyze_route ---
Reroute Impact Score: 25, Decision: ROUTE_CLARIFICATION, Reason: Warehouse risk tier is ELEVATED

--- Node: route_clarification ---
Checking next alternative route. Index: 1

--- Node: select_route ---
Selected route [1]: {'route_id': 'ROUTE-SOUTH-02', 'alternative_port': 'Port-South', 'warehouse_id': 'WH-SOUTH-303', 'added_delay_hours': 72}

--- Node: check_warehouse ---
Warehouse metrics for WH-SOUTH-303: {'warehouse_name': 'Southern Distribution Hub', 'current_utilization_pct': 72, 'operational_status': 'ACTIVE', 'risk_tier': 'NORMAL'}

--- Node: analyze_route ---
Reroute Impact Score: 0, Decision: OPTIMAL_PATH_FOUND, Reason: Warehouse and route conditions are acceptable

--- Node: finalize_route ---
Finalized Route: ROUTE-SOUTH-02

--- Node: generate_report ---
LLM Operations Brief:
Here is a short, professional final operations brief for the logistics team:

The shipment SH-4105, containing 250 tons of consumer electronics, was delayed due to the temporary closure of the primary port. An alternative route, ROUTE-SOUTH-02, was selected, which adds 72 hours of transit delay, well below the 120-hour critical delay threshold outlined in RULE-01. The decision was influenced by RULE-03, which requires warehouses to be below 85% utilization to accept new shipments, and fortunately, WH-SOUTH-303 is currently operating at 72% utilization, making it an acceptable destination.
Incident INC-002 complete. Decision: OPTIMAL_PATH_FOUND

Processing INC-003...

--- Node: parse_incident (INC-003) ---
Extracted Metadata: {"shipment_id": "SH-4208", "cargo_weight_tons": 700, "cargo_type": "industrial machinery", "target_warehouse_id": "WH-EAST-101", "has_perishables": false, "maximum_tolerable_delay_hours": null}

--- Node: policy_rag_lookup ---
Retrieved Logistics Rules:
RULE-03: Warehouse Utilization Limits
A warehouse operating above 85 percent utilization cannot accept a new automated cargo shipment. Any route assigned to a warehouse exceeding 85% utilization must be rejected, triggering a ROUTE_CLARIFICATION.

RULE-02: Port South Fit Check
Cargo exceeding 500 tons and routed through Port-South requires a WAREHOUSE_FIT_CHECK to verify heavy machinery compatibility and structural floor load capacity.

RULE-05: Non-Active Operational Status
A warehouse with an operational_status that is not ACTIVE cannot receive any cargo shipments. The route assigned to it must be rejected under ROUTE_CLARIFICATION.

--- Node: load_alternative_routes ---
Available alternative routes for PORT-SEATTLE-02: [{'route_id': 'ROUTE-WEST-01', 'alternative_port': 'Port-West', 'warehouse_id': 'WH-WEST-202', 'added_delay_hours': 48}, {'route_id': 'ROUTE-SOUTH-02', 'alternative_port': 'Port-South', 'warehouse_id': 'WH-SOUTH-303', 'added_delay_hours': 72}, {'route_id': 'ROUTE-CENTRAL-03', 'alternative_port': 'Port-Central', 'warehouse_id': 'WH-CENTRAL-404', 'added_delay_hours': 96}]

--- Node: select_route ---
Selected route [0]: {'route_id': 'ROUTE-WEST-01', 'alternative_port': 'Port-West', 'warehouse_id': 'WH-WEST-202', 'added_delay_hours': 48}

--- Node: check_warehouse ---
Warehouse metrics for WH-WEST-202: {'warehouse_name': 'Pacific Gateway Storage', 'current_utilization_pct': 68, 'operational_status': 'ACTIVE', 'risk_tier': 'ELEVATED'}

--- Node: analyze_route ---
Reroute Impact Score: 25, Decision: ROUTE_CLARIFICATION, Reason: Warehouse risk tier is ELEVATED

--- Node: route_clarification ---
Checking next alternative route. Index: 1

--- Node: select_route ---
Selected route [1]: {'route_id': 'ROUTE-SOUTH-02', 'alternative_port': 'Port-South', 'warehouse_id': 'WH-SOUTH-303', 'added_delay_hours': 72}

--- Node: check_warehouse ---
Warehouse metrics for WH-SOUTH-303: {'warehouse_name': 'Southern Distribution Hub', 'current_utilization_pct': 72, 'operational_status': 'ACTIVE', 'risk_tier': 'NORMAL'}

--- Node: analyze_route ---
Reroute Impact Score: 0, Decision: OPTIMAL_PATH_FOUND, Reason: Warehouse and route conditions are acceptable

--- Node: finalize_route ---
Finalized Route: ROUTE-SOUTH-02

--- Node: generate_report ---
LLM Operations Brief:
Here is a short, professional final operations brief for the logistics team:

The primary maritime route for cargo SH-4208, containing 700 tons of industrial machinery, was unavailable, prompting an evaluation of alternative routes. The alternative route selected was ROUTE-SOUTH-02, with a destination of WH-SOUTH-303, due to its acceptable warehouse and route conditions. The decision was influenced by RULE-02: Port South Fit Check, which required verification of heavy machinery compatibility and structural floor load capacity for cargo exceeding 500 tons routed through Port-South. The chosen route met all necessary conditions, including a warehouse utilization of 72%, which is below the 85% limit outlined in RULE-03: Warehouse Utilization Limits.
Incident INC-003 complete. Decision: OPTIMAL_PATH_FOUND
```


- ### for running main file:

```bash
python -m src.main      
```

```
Output:

(supply-chain-logistics-rerouter) C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter>python -m src.main
==================================================
SUPPLY CHAIN CRISIS & LOGISTICS RE-ROUTER
==================================================
1. Process Sample Incident INC-001
2. Process Sample Incident INC-002
3. Process Sample Incident INC-003
4. Custom Incident Chatbot Mode
5. Exit
==================================================

Select Option > 

```


9. ## Langgraph Workflow:

```
shipping Incident Input
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
├── OPTIMAL_PATH_FOUND ──> Finalize Route ──> Generate Report
│          
│
├── ROUTE_CLARIFICATION
│                    ↓
│             Try Next Route
│                    ↓
│             Select Route
│                    ↓
│             Check Warehouse
│                    ↓
│             Analyze Route
│
└── CRITICAL_DELAY
        ↓
    Escalate Incident
        ↓
    Generate Report

```


10. ## RAG Implementation:

```
knowledge_Base_file(txt)
    ↓
Document Loading
    ↓
Chunking
    ↓
Embedding
    ↓
FAISS (in-memory)
    ↓
Retriever

```

11. ## Tools Implemented


```
We implemented two major python tools:

- query_warehouse_inventory_tool: Queries warehouse inventory database to retrieve utilization, status, and risk tier.

- get_alternative_routes_tool: Queries alternative routes database to retrieve available routes for a disrupted port.
```


12. ## Testing 

```bash 
pytest tests/
```
```
(supply-chain-logistics-rerouter) C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter>pytest tests/
================================================== test session starts ==================================================
platform win32 -- Python 3.13.13, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter
configfile: pyproject.toml
plugins: anyio-4.14.1, langsmith-0.9.7, mock-3.15.1
collected 13 items                                                                                                       

tests\test_graph.py ..                                                                                             [ 15%]
tests\test_nodes.py ...                                                                                            [ 38%]
tests\test_routing.py .....                                                                                        [ 76%]
tests\test_tools.py ...                                                                                            [100%]

=================================================== warnings summary ====================================================
src\rag.py:2
  C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter\src\rag.py:2: DeprecationWarning: `langchain-community` is being sunset and is no longer actively maintained. See https://github.com/langchain-ai/langchain-community/issues/674 for details and migration guidance toward standalone integration packages.
    from langchain_community.document_loaders import TextLoader

tests\test_nodes.py:4
  C:\Users\Poonam Bhatt\Desktop\supply-chain-logistics-rerouter\tests\test_nodes.py:4: PytestUnknownMarkWarning: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.integration

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================ 13 passed, 2 warnings in 18.79s ============================================
```


13. ## Test Results:


All the file under tests/ folder are runnable and the results are saved in outputs/ folder

test files: 

```bash
tests/
```
Output files:

```bash
outputs/
```

14. ## Incident Execution Results:

All the three given incidents were ran and output is saved in output folder.


```bash
python -m run_incidents
```

Outputs:

```
outputs/INC-001_reroute_advisory_report.json
outputs/INC-002_reroute_advisory_report.json
outputs/INC-003_reroute_advisory_report.json

```



15. ## Known Limitation:


```
This project may contain few limitation:

- Uses local operational data - Worked on the given local small data.
- Does not use live port data - No use of live port involved in this project for now.
- Uses a fixed route dataset  - Routing depends on fixed dataset not a real time data.
- LLM output may vary slightly - LLM output may vary after few number of runs.
- No web UI interaction - This project currently doesnot support Web interaction (streamlit, FastAPI etc).
```


16. ## Future Plan:

```
 - Add a web design or interaction of chatbot rather than the CLI dependency.
 - Use live port data rather than local static data.
 - Enable dynamic routing for datasets.
```



Note : Added __init__.py file in src and tests folder to make run command access sub-file and folders.

``` bash

Author - Poonam Bhatt
Capstone-01 - Supply chain logistics rerouter
Date - 06/07/2026

```




