import pytest
from src.graph import app
from src.state import get_initial_state

@pytest.mark.integration
def test_graph_retry_selects_next_route():
    """
    Test 8: Verify that the graph loops correctly when the first route is rejected.
    Uses INC-001 where the first route is ROUTE-WEST-01 (rejected due to ELEVATED risk)
    and the second route is ROUTE-SOUTH-02 (accepted).
    """
    manifest_text = (
        "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded "
        "outside the Port of Seattle due to an active worker strike. "
        "The vessel is carrying 550 tons of industrial electronics "
        "originally scheduled for delivery to WH-WEST-202. "
        "The shipment contains perishable cooling components and "
        "cannot sustain delays exceeding 72 hours."
        
    )
    initial_state = get_initial_state("INC-001", manifest_text, "PORT-SEATTLE-02")
    final_state = app.invoke(initial_state)
    
    report = final_state.get("final_report", {})
    routes_eval = report.get("routes_evaluated", [])
    
    
    assert len(routes_eval) >= 2
    assert routes_eval[0]["route_id"] == "ROUTE-WEST-01"
    assert routes_eval[0]["decision"] == "ROUTE_CLARIFICATION"
    assert "elevated" in routes_eval[0]["reason"].lower()
    
    
    assert routes_eval[1]["route_id"] == "ROUTE-SOUTH-02"
    assert routes_eval[1]["decision"] == "OPTIMAL_PATH_FOUND"
    
    assert final_state["current_route_index"] == 1
    assert final_state["clarification_attempts"] == 1
    assert report["graph_routing_metadata"]["loops_executed"] == 1
    assert report["graph_routing_metadata"]["final_decision_state"] == "OPTIMAL_PATH_FOUND"
    assert report["final_selected_route"]["route_id"] == "ROUTE-SOUTH-02"

@pytest.mark.integration
def test_graph_escalates_when_routes_exhausted():
    """
    Verify that when all available routes fail or max retries are reached,
    the incident escalates (CRITICAL_DELAY).
    We can force this by providing an incident with very low maximum tolerable delay
    so that all routes are rejected.
    """

    manifest_text = (
        "Shipment SH-9999 has very critical cargo. Delivery to WH-WEST-202. "
        "Cannot sustain delays exceeding 10 hours."
    )
    initial_state = get_initial_state("INC-FORCE-ESC", manifest_text, "PORT-SEATTLE-02")
    final_state = app.invoke(initial_state)
    
    report = final_state.get("final_report", {})
    metadata = report.get("graph_routing_metadata", {})
    
    assert metadata["final_decision_state"] == "CRITICAL_DELAY"
    assert metadata["loops_executed"] == 2
    assert report["final_selected_route"] == {}

@pytest.mark.integration
def test_final_report_schema():
    """Verify that the generated final report contains all required keys."""
    manifest_text = (
        "Shipment SH-4105 is delayed because the primary port is "
        "temporarily closed. The shipment contains 250 tons of consumer electronics and "
        "is scheduled for WH-SOUTH-303."
    )
    initial_state = get_initial_state("INC-002", manifest_text, "PORT-SEATTLE-02")
    final_state = app.invoke(initial_state)
    
    report = final_state.get("final_report", {})
    
    required_keys = {
        "incident_id",
        "original_incident_summary",
        "parsed_metadata",
        "rag_validation_rules_applied",
        "routes_evaluated",
        "final_selected_route",
        "queried_warehouse_metrics",
        "graph_routing_metadata",
        "final_operations_brief"
    }
    
    for key in required_keys:
        assert key in report
        
    metadata_keys = {
        "loops_executed",
        "final_decision_state",
        "reroute_impact_score"
    }
    for key in metadata_keys:
        assert key in report["graph_routing_metadata"]
        
    parsed_meta_keys = {
        "shipment_id",
        "target_warehouse_id",
        "cargo_weight_tons",
        "cargo_type",
        "has_perishables",
        "maximum_tolerable_delay_hours"
    }
    for key in parsed_meta_keys:
        assert key in report["parsed_metadata"]
