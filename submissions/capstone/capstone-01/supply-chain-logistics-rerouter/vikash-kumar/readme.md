# Project Overview

This project helps logistics team to handle different problems while doing the shipping due to bad weather, strikes, operational failures. It helps the stakeholders to take smart decision according to the situations.

# Solution Approach

We will first use the Extraction of the information, like shipment ID, cargo weights, etc. Then we will check it with the company policy and regulations. Then finally we will use Graph Evaluation which tests alternative routes one by one. If there is any issue then it alerts the supervisor about the issue. We have created AI-powered Logistics Incident Assistant that evaluates the disruption and recommends a suitable alternative route.

# Architecture

There will be the robust architecture for the project:

1. Raw Shipping Incident Text Input
2. AI Text Extraction for the clean data
3. RAG Poilcy Retrieval for company rules
4. Route and Warehouse Tools
5. Langgraph decision workflow
6. Report writer node for final report

# Project Structure

```bash
supply_chain_logistics_rerouter/
│├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│├── data/
│   ├── logistics_knowledge_base.txt
│   ├── inventory_status.json
│   ├── route_options.json
│   └── sample_incidents.json
│├── src/
│   ├── main.py
│   ├── state.py
│   ├── graph.py
│   ├── nodes.py
│   ├── tools.py
│   ├── rag.py
│   ├── schemas.py
│   └── report_writer.py
│├── tests/
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


# Setup Instructions

```python

uv venv

.venv\Scripts\activate

uv pip install -r requirements.txt
```

```bash
.env

GROQ_API_KEY=....

GROQ_MODEL=llama-3.3-70b-versatile
```

# Running the Application
```python

python -m src.main

uv run python src/main.py

python src/main.py
```
# Input
Example:

incident_id : "INC-001"

manifest_text: "CRITICAL DISRUPTION"

disrupted_port_id: "PORT-SEATTLE-02"

# Output
```bash
{"incident_id": "INC-001","original_incident_summary": "","parsed_metadata": {"shipment_id": "SH-4002","target_warehouse_id": "WH-WEST-202","cargo_weight_tons": 550,"cargo_type": "industrial electronics","has_perishables": true,"maximum_tolerable_delay_hours": 72},"rag_validation_rules_applied": [],"routes_evaluated": [],"final_selected_route": {},
"queried_warehouse_metrics": {},"graph_routing_metadata": {"loops_executed": 0,"final_decision_state": "","reroute_impact_score": 0},"final_operations_brief": ""}
```

# LangGraph Workflow

Nodes: We have used the following nodes in the workflow:
parse_incident,policy_rag_lookup,load_alternative_routes,select_route,check_warehouse,analyze_route,route_clarification,finalize_route,escalate_incident

Conditional routing: OPTIMAL_PATH_FOUND, ROUTE_CLARIFICATION, or CRITICAL_DELAY

Retry loop: If one exceeded target safety bound, it increases the retry-counter

Finalization: If the alternative route passes all safety validations, then the graph finalize the report

Escalation: If there is an issue with the workflow then it jumps to escalate_incident node

# RAG Implementation

Document: The main document is "logistics_knowledge_base.txt" which stores the company rules and regulations

Knowledge-base file: The location is at data/logistics_knowledge_base.txt

Document loading: The langchain TextLoader is used for this purpose

Chunking: The RecursiveCharacterTextSpiltter is being used in the chunking method.

Embeddings: for embedding "sentence-transformers/all-MiniLM-L6-v2" is used.

Chroma DB: We have used the chroma db as the vector Database

Retriever: The only top 2 chunks will be retrieved

# Tools Implemented

- query_warehouse_inventory_tool: checks for the warehouse_id

- get_alternative_routes_tool: deals with the disrupted port_id

# Testing

Different tools are used for the testing: 

test_warehouse_tool_valid_id, test_warehouse_tool_invalid_id,test_route_tool_valid_port,test_parse_incident_required_fields,test_routing_high_warehouse_utilization,test_routing_elevated_risk,test_routing_valid_route,test_graph_retry_selects_next_route,test_delay_constraint_triggers_clarificationtest_critical_delay_triggers_escalationtest_graph_escalates_when_routes_exhaustedtest_reroute_impact_scoretest_final_report_schema

```python

uv run pytest tests/ -v

uv run pytest tests/ -v > outputs/test_results.txt
```
# Test Results & Incident Execution Results

```bash
(Project Vik) PS C:\Users\Vikash Kumar\Desktop\Project Vik> uv run pytest tests/ -v
======================================================== test session starts ========================================================
platform win32 -- Python 3.11.15, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\Vikash Kumar\Desktop\Project Vik\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\Vikash Kumar\Desktop\Project Vik
configfile: pytest.ini (WARNING: ignoring pytest config in pyproject.toml!)
plugins: anyio-4.14.1, langsmith-0.9.7, env-1.6.0, mock-3.15.1
collected 12 items                                                                                                                   

tests/test_graph.py::test_graph_retry_selects_next_route PASSED                                                                [  8%]
tests/test_nodes.py::test_parse_incident_required_fields PASSED                                                                [ 16%]
tests/test_nodes.py::test_load_alternative_routes_initialization PASSED                                                        [ 25%]
tests/test_nodes.py::test_select_route_valid_index PASSED                                                                      [ 33%]
tests/test_routing.py::test_routing_high_warehouse_utilization PASSED                                                          [ 41%]
tests/test_routing.py::test_routing_elevated_risk PASSED                                                                       [ 50%]
tests/test_routing.py::test_routing_valid_route PASSED                                                                         [ 58%]
tests/test_routing.py::test_routing_critical_route_delay PASSED                                                                [ 66%]
tests/test_routing.py::test_routing_exceeds_shipment_delay_limit PASSED                                                        [ 75%]
tests/test_tools.py::test_warehouse_tool_valid_id PASSED                                                                       [ 83%]
tests/test_tools.py::test_warehouse_tool_invalid_id FAILED                                                                     [ 91%]
tests/test_tools.py::test_route_tool_valid_port PASSED                                                                         [100%]

============================================================= FAILURES ==============================================================
__________________________________________________ test_warehouse_tool_invalid_id ___________________________________________________

    def test_warehouse_tool_invalid_id():
        result = query_warehouse_inventory_tool("WH-UNKNOWN-999")
>       assert "error" in result
E       AssertionError: assert 'error' in {'Warehouse_id WH-UNKNOWN-999 is not found'}

tests\test_tools.py:13: AssertionError
========================================================= warnings summary ==========================================================
src\rag1.py:2
  C:\Users\Vikash Kumar\Desktop\Project Vik\src\rag1.py:2: DeprecationWarning: `langchain-community` is being sunset and is no longer actively maintained. See https://github.com/langchain-ai/langchain-community/issues/674 for details and migration guidance toward standalone integration packages.
    from langchain_community.document_loaders import TextLoader

tests\test_nodes.py:4
  C:\Users\Vikash Kumar\Desktop\Project Vik\tests\test_nodes.py:4: PytestUnknownMarkWarning: Unknown pytest.mark.integration - is this a typo?  You can register custom marks to avoid this warning - for details, see https://docs.pytest.org/en/stable/how-to/mark.html
    @pytest.mark.integration

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
====================================================== short test summary info ======================================================
FAILED tests/test_tools.py::test_warehouse_tool_invalid_id - AssertionError: assert 'error' in {'Warehouse_id WH-UNKNOWN-999 is not found'}
============================================= 1 failed, 11 passed, 2 warnings in 18.23s =============================================
(Project Vik) PS C:\Users\Vikash Kumar\Desktop\Project Vik> 

```

#  Known Limitations

We can make more tools specialized to handle more complex situatin, we can improve the workflow of the langgraph so that the system can be more robust.

# Author 

Vikash Kumar