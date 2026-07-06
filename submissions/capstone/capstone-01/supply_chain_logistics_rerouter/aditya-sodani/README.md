# Supply Chain Crisis Management and Logistics ReRouter

# 1. Project Overview

A major shipping port has suddenly become unavailable because of a strike, weather disruption, or
operational failure.
A shipment is already in transit and must be rerouted.
The logistics team needs to quickly determine:
-What shipment is affected?
-What type of cargo is being transported?
-How much delay can the shipment tolerate?
-Which alternative routes are available?
-Can the warehouse assigned to the alternative route accept the shipment?
-Do any logistics rules prevent the route from being selected?
-Should another route be checked?
-Should the incident be escalated?

# 2. Solution Approach

1. we have our sample incident containing Incident id , manifest_text , etc.
2. Langgraph parsed_incident node retrieve the structure output from it.
3. using the manifest_text as a query, RAG artitecture invokes as in knowledge base there are some rules present which retrieve by the retriever and we get the rag_context
4. loading the alternative routes 
5. selecting the one route from available routes
6. checking the warehouses
7. then analysing routes , its a conditional edge where we move to others nodes on the basis of routing_decisions specified in the node and impact_scores
8. if it finds the optimal path it directed to the finalyze node and then generate report node
9. elif checks the critical_delay and max_clarification_attempts , if conditions met then it move to escalate_incident node , from there the incident is escalated and moved to finalize node 
10. else if it met some other conditions then it will move again to selct_route node , and begin analyze routes using different available rote
11. At the end we get the structured output 

# 3. Setup instruction

## step-1(to initializa the uv package)

run --> uv init 

## step-2(make virtual environment)

run --> uv venv --python 3.11

## step-3(install the requirements)

run --> uv pip install requirements.txt

## step-4(.env configuration)

add groq_api_key in it along with model name

# 4. Requirements:-

langchain 
langchain-core 
langchain-community 
langchain-groq 
langchain-huggingface 
langgraph 
faiss-cpu 
sentence-transformers 
pydantic 
python-dotenv
pytest
pytest-mock


# 5. Running the application

run --> python src/main.py

# 6. Sample Input :-

{
"incident_id": "INC-001",
"manifest_text": "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded outside the Port of Seattle due to an active worker strike. The vessel is carrying 550 tons of industrial electronics originally scheduled for delivery to WH-WEST-202. The shipment contains perishable cooling components and cannot sustain delays exceeding 72 hours.",
"disrupted_port_id": "PORT-SEATTLE-02"
}

# 7. Sample Output :-

{
    "incident_id": "INC-001",
    "parsed_metadata": {
        "shipment_id": "SH-4002",
        "cargo_weight_tons": 550,
        "cargo_type": "industrial electronics",
        "target_warehouse_id": "WH-WEST-202",
        "has_perishables": true,
        "maximum_tolerable_delay_hours": 72
    },
    "rag_validation_rules_applied": "Any alternative route exceeding 120 hours of total added transit delay must be \nclassified as CRITICAL_DELAY.\nCargo exceeding 500 tons and routed through Port-South requires a \nWAREHOUSE_FIT_CHECK.\nA warehouse operating above 85 percent utilization cannot accept a new automated \ncargo shipment.\nIf a warehouse has an ELEVATED risk tier, another route or alternative facility \nmust be checked before finalizing the route.",
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
    "final_operations_brief": "**Logistics Operation Brief**\n\n**Decision:** OPTIMAL_PATH_FOUND\n\n**Route Details:**\n\n* **Route ID:** ROUTE-SOUTH-02\n* **Alternative Port:** Port-South\n* **Warehouse ID:** WH-SOUTH-303\n* **Added Delay:** 72 hours\n\n**Summary:**\nThe optimal logistics route has been determined as ROUTE-SOUTH-02, utilizing Port-South as the alternative port and WH-SOUTH-303 as the designated warehouse. Please note that this route will incur an additional delay of 72 hours. All relevant teams and stakeholders should be informed of this decision to ensure a smooth execution of the logistics operation."
}

# 8. saved output path:
after executing the main file , the outputs are saved under outputs folder fro different incidented

