# Capstone project 01 - Supply chain logistics rerouter

## Project overview

This project demonstrates a logistics rerouting application using:
-LangChain
-RAG
-LangGraph
-Groq LLM
-Local JSON and text data
-pytest

The application:
-Accepts a shipping incident as input.
-Extract important shipment information using LangChain structured output.
-Retrieve relevant logistics rules using RAG.
-Load available alternative routes.
-Check warehouse capacity and operational status.
-Evaluate the selected route.
-Try another route if the current route is unsuitable.
-Escalate the incident when no acceptable route is available.
-Generate a final logistics advisory report.

**The main objective of this capstone is to demonstrate how LangChain, RAG, and LangGraph can work together in one application.**

## Solution approach

The implementation showcases the use of RAG, Langchain and Langgraph. To process the shipping incident, the knowledge base is firstly processed and stored as embeddings, while inventory status, route options and sample incidents are stored as json for reference. For the processing we have used langchain, while langgraph managing the heavy burden for the project is used to manage Shared application state, Execution of workflow nodes, Conditional routing, Route retry logic, Route finalization, Incident escalation.

## Architecture

**Langchain:** 
-Groq LLM integration
-Prompt templates
-Structured output
-Extracting shipment information from the incident
-Generating the final operations brief

**Langgraph:**
-Shared application state
-Execution of workflow nodes
-Conditional routing
-Route retry logic
-Route finalization
-Incident escalation

**RAG**
-Load the logistics knowledge-base file.
-Split the document into chunks.
-Create embeddings.
-Store the chunks in a local vector store.
-Retrieve rules relevant to the current shipping incident.

```mermaid

    Incident-->LangChain Extraction;
    LangChain Extraction-->RAG Rule Retrieval;
    RAG Rule Retrieval-->Route and Warehouse Tools;
    Route and Warehouse Tools-->LangGraph Decision and Retry Loop;
    LangGraph Decision and Retry Loop-->Final report
```

## Project structure

```bash
supply_chain_logistics_rerouter/
│
├── README.md 
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── data/  #this is the dataset directory
│ ├── logistics_knowledge_base.txt
│ ├── inventory_status.json
│ ├── route_options.json
│ └── sample_incidents.json
│
├── src/ # the main directory 
│ ├── main.py  # like app.py
│ ├── state.py  #creates state 
│ ├── graph.py  # has graph compilation
│ ├── nodes.py  # has graph nodes
│ ├── tools.py  # has tools for langgraph
│ ├── rag.py   # chunking, embeddings of txt file
│ ├── schemas.py  #schema for metadata
│ └── report_writer.py
│
├── tests/ # test directory
│ ├── test_tools.py
│ ├── test_routing.py
│ ├── test_nodes.py
│ └── test_graph.py
└── outputs/  #outputs of run
 ├── INC-001_reroute_advisory_report.json
 ├── INC-002_reroute_advisory_report.json
 ├── INC-003_reroute_advisory_report.json
 └── test_results.txt

```

##  Setup Instructions

Do 'uv init' to initialize uv, then create a venv and activate it

### 1. Installation
install the dependencies from requirements.txt:
```bash
uv pip install -r requirements.txt
```

### 2. Configuration
Copy the `.env.example` file to `.env` and add your Groq API Key and model

### 3. Run the app
```bash
python src/main.py
```

## Input

```bash
{
"incident_id": "INC-001",
"manifest_text": "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle due to an active worker strike. The vessel is carrying 550 tons of industrial electronics originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling components and cannot sustain delays exceeding 72 hours.",
"disrupted_port_id": "PORT-SEATTLE-02"
}
```

## Output

```bash
{
    "incident_id": "INC-001",
    "original_incident_summary": "A cargo container carrying 550 tons of industrial electronics, including perishable components, is stranded outside the Port of Seattle due to a worker strike, with delivery delays exceeding 72 hours potentially causing significant damage.",
    "parsed_metadata": {
        "shipment_id": "SH-4002",
        "cargo_weight_tons": 550,
        "cargo_type": "industrial electronics",
        "target_warehouse_id": "WH-WEST-202",
        "has_perishables": true,
        "maximum_tolerable_delay_hours": 72
    },
    "rag_validation_rules_applied": [
        "Any alternative route exceeding 120 hours of total added transit delay must be",
        "classified as CRITICAL_DELAY.",
        "Cargo exceeding 500 tons and routed through Port-South requires a",
        "WAREHOUSE_FIT_CHECK.",
        "A warehouse operating above 85 percent utilization cannot accept a new automated",
        "cargo shipment.",
        "If a warehouse has an ELEVATED risk tier, another route or alternative facility",
        "must be checked before finalizing the route."
    ],
    "routes_evaluated": [
        {
            "route_id": "ROUTE-WEST-01",
            "decision": "ROUTE_CLARIFICATION",
            "reason": "Warehouse risk tier is elevated"
        },
        {
            "route_id": "ROUTE-SOUTH-02",
            "decision": "OPTIMAL_PATH_FOUND",
            "reason": "All conditions are successful"
        }
    ],
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
    "final_operations_brief": "**Incident Summary:**\nA critical disruption occurred due to a worker strike at the Port of Seattle, stranding a cargo container (SH-4002) carrying 550 tons of industrial electronics. The shipment, originally bound for WH-WEST-202, contains perishable components that cannot sustain delays over 72 hours.\n\n**Selected Route:**\nThe final selected route was \"ROUTE-SOUTH-02\", which involves diverting the cargo to the \"Port-South\" and storing it at warehouse \"WH-SOUTH-303\". This route adds a delay of 72 hours.\n\n**Key Rule or Warehouse Condition:**\nThe key rule driving this decision is related to the evaluation of alternative routes and warehouse conditions. Specifically:\n- The original route (ROUTE-WEST-01) was rejected due to the warehouse having an elevated risk tier, which requires checking another route or facility according to the logistics rules.\n- The selected warehouse (WH-SOUTH-303) at \"Port-South\" has a current utilization of 72%, which is below the 85% threshold, allowing it to accept the new automated cargo shipment.\n- The added delay of 72 hours is within the acceptable limit, as any route exceeding 120 hours of added transit delay would be classified as a CRITICAL_DELAY.\n\nOverall, the decision to select \"ROUTE-SOUTH-02\" was made because it meets all the necessary conditions, including not exceeding the critical delay threshold and utilizing a warehouse that is operational and not over capacity."
}
```

## Langgraph workflow

This mermaid workflow showcases the langgraph workflow
```mermaid

LogisticsIncidentState-->parse_incident,
parse_incident-->policy_rag_lookup,
policy_rag_lookup-->policy_rag_lookup,
load_alternative_routes-->select_route,
select_route-->check_warehouse,
check_warehouse-->analyze_route,
analyze_route-->finalize_route,
analyze_route-->route_clarification,
analyze_route-->escalate_incident,
route_clarification-->select_route,
route_clarification-->escalate_incident,
finalize_route-->generate_report,
escalate_incident-->generate_report,
generate_report-->END
```

## Tool implementation
Two tools are implemented:
-query_warehouse_inventory_tool
-get_alternative_routes_tool


## Testing

I have implemented 12 testcases and they have been passed by the project.
I had also added checks to validate the
to run the pytest,
```bash
pytest
```

## Known Limitations
-Uses local operational data
-Does not use live port data
-Uses a fixed route dataset
-LLM output may vary slightly
-No UI integration


## Challenges

The major challenge that i faced was while Tool calling in langgraph due to 'Structured tool' error, 
which was solved using Toolwrapper, another was building nodes and maintaining the specified logic.

## Author
Taniya Gupta