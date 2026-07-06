import pytest
from src.graph import supply_app

def test_graph_retry_selects_next_route():
    # INC-001: Stranded outside Port of Seattle. Carrier WH-WEST-202 (risk elevated, delay 48).
    # Expected: Route 1 (ROUTE-WEST-01) rejected due to ELEVATED risk.
    # Route 2 (ROUTE-SOUTH-02) accepted (delay 72 <= limit 72, risk normal, utilization 72% <= 85%).
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
        "disrupted_port_id": "PORT-SEATTLE-02",
        "extracted_metadata": {},
        "routing_rag_context": "",
        "available_routes": [],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": [],
        "final_report": {}
    }
    
    res = supply_app.invoke(initial_input)
    
    assert res["routing_decision"] == "OPTIMAL_PATH_FOUND"
    assert res["current_route_index"] == 1 # First route was index 0 (rejected), second is index 1 (accepted)
    assert res["clarification_attempts"] == 1 # Loop executed once
    assert res["selected_route"]["route_id"] == "ROUTE-SOUTH-02"
    
    # Check that route evaluations are logged
    logs = res["logs"]
    assert any("Route Checked: ROUTE-WEST-01. Decision: ROUTE_CLARIFICATION" in log for log in logs)
    assert any("Route Checked: ROUTE-SOUTH-02. Decision: OPTIMAL_PATH_FOUND" in log for log in logs)

def test_graph_escalates_when_routes_exhausted():
    # Test case where no routes are acceptable or all are clarified/exhausted
    initial_input = {
        "incident_id": "INC-EXHAUST",
        "manifest_text": "Disruption with extremely low delay tolerance of 10 hours.",
        "disrupted_port_id": "PORT-SEATTLE-02",
        "extracted_metadata": {},
        "routing_rag_context": "",
        "available_routes": [],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": [],
        "final_report": {}
    }
    
    res = supply_app.invoke(initial_input)
    assert res["routing_decision"] == "CRITICAL_DELAY"
    assert res["selected_route"] == {}




### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026