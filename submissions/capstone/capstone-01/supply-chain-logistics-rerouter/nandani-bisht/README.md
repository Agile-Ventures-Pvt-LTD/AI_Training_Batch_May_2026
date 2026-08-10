## Capstone Project Build - 01
Supply Chain Crisis Managment and Logistics Re-Router

## Participant Name:
Nandani Bisht

## Business use case:

A major shipping port has suddenly become unavailable beacause of the strike, weather disruption, or operational failure.so the logistics team needs to quickly determine:

.what shipment is afected?
.what type of cargo is being transported?
.how much delay can the shipment tolerate?
.which altenative routes are available?
.should another route be checked?
.should the incident be escalated?

## Project Objective:

we are building this project with the help of Langchain, Rag , LangGraph , Groq LLM , lOCAL JSON and text data and pytest.

## TechStack used:
```
Rag
LangChain
LangGraph
Groq LLM
Local JSON and text data
pytest
```

## Project Structure:
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
│
└── outputs/
├── INC-001_reroute_advisory_report.json
├── INC-002_reroute_advisory_report.json
├── INC-003_reroute_advisory_report.json
└── test_results.txt

```

## Setup Instructions:
```
uv init
uv venv
.venv/Scripts/activate
uv add -r requirements.txt
```


## input:
The application receive the following inputs:

**incident_id**:  The available incidents id's are INC-001 , INC-002 , INC-003

**manifest_text**: manifest_text tell about the **CRITICAL DISRUPTION** : Carge container SH-4002 is stranded outside the port of seattle due to an active worker strike.(Basically we use LangChain output to extract shipment information from manifest_text)

**disrupted_port_id**: Its the "PORT-SEATTLE-02" AND IT CONTAINS "route_id", "alternative_port", "warehouse_id", "added_delay_hours"

## Output:

The final json output looks like that:
```{
  "incident_id": "INC-001",
  "original_incident_summary": "A critical disruption has occurred due to a worker strike at the Port of Seattle, stranding cargo container SH-4002.",
  "parsed_metadata": {
    "shipment_id": "SH-4002",
    "cargo_weight_tons": 550,
    "cargo_type": "industrial electronics",
    "target_warehouse_id": "WH-WEST-202",
    "has_perishables": true,
    "maximum_tolerable_delay_hours": 72
  },
  "rag_validation_rules_applied": [
    "Cargo exceeding 500 tons and routed through Port-South requires a \nWAREHOUSE_FIT_CHECK.",
    "A warehouse operating above 85 percent utilization cannot accept a new automated \ncargo shipment."
  ],
  "routes_evaluated": [
    {
      "route_id": "ROUTE-WEST-01",
      "decision": "ROUTE_CLARIFICATION",
      "reason": "Warehouse risk tier is ELEVATED"
    },
    {
      "route_id": "ROUTE-SOUTH-02",
      "decision": "OPTIMAL_PATH_FOUND",
      "reason": "Warehouse and route conditions are acceptable"
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
  "final_operations_brief": "Incident ID: INC-001 - A worker strike at the Port of Seattle has disrupted cargo container SH-4002, prompting a rerouting decision. The alternative route selected is ROUTE-SOUTH-02, utilizing Port-South and warehouse WH-SOUTH-303, driven by the need to avoid elevated risk tiers and stay within the 72-hour maximum tolerable delay limit. This decision was guided by the acceptable warehouse and route conditions, including a normal risk tier and active operational status at the Southern Distribution Hub."
}
```

## LangGraph Workflow:
**Nodes**: Receives the current graph state as input , Perform some processing and returns updates to the state.
**Conditional routing**: At runtime , a routing function inspects the current state and decides which node(s) to execute next
**Retry loop**: this lets you automatically retry failed nodes with configurable limits, delays and backoff strategies.
**Finalization**: final step in a workflow /agent execution.
**Escalation**:escalation refers to the process of handing over a conversation or task from the automated agent to a human when certain conditions are met.


## RAG Implementation:
**Knowledge-base file**
**Document loading**
**Chunking**
**Enmbedding**
**Faiss**
**Retriever**


## Tools Implemented:

1 **query_warehouse_inventory_tool** : It receive current information from the warehouse inventory.

**Tool Input**
{
"warehouse_id": "WH-WEST-202
}

**Expected Tool Output**
{
"warehouse_name": "Pacific Gateway Storage",
"current_utilization_pct": 68,
"operational_status": "ACTIVE",
"risk_tier": "ELEVATED
}


2 **get_alternative_routes_tool**: Reterive alternate routes when the routes are disrupted.

**Tool input**
{
    "disrupted_port_id": "PORT-SEATTLE-02"
}

**Excepted Tool Output**
{
    "route_id": "ROUTE-WEST-01",
    "alternative_port": "Port-West",
    "warehouse_id": "WH-WEST-202",
    "added_delay_hours": 48
}
    
## Run Command:
``` uv run pytest tests/ -v ```
and the test output is saved in the `test_results.txt` file.











