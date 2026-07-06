from src.nodes import analyze_route

def test_routing_high_warehouse_utilization():
    mock_state = {"selected_route": {"route_id": "R1", "warehouse_id": "W1", "added_delay_hours": 24},
        "warehouse_db_context": {"current_utilization_pct": 92, "operational_status": "ACTIVE", "risk_tier": "NORMAL"},
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},
        "logs": []}
    result = analyze_route(mock_state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 30

def test_routing_elevated_risk():
    mock_state = {"selected_route": {"route_id": "R1", "warehouse_id": "W1", "added_delay_hours": 24},"warehouse_db_context": {"current_utilization_pct": 70, "operational_status": "ACTIVE", "risk_tier": "ELEVATED"},
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},"logs": []}
    result = analyze_route(mock_state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 25

def test_routing_valid_route():
    mock_state = {"selected_route": {"route_id": "R1", "warehouse_id": "W1", "added_delay_hours": 24},"warehouse_db_context": {"current_utilization_pct": 70, "operational_status": "ACTIVE", "risk_tier": "NORMAL"},"extracted_metadata": {"maximum_tolerable_delay_hours": 72},"logs": []}
    result = analyze_route(mock_state)
    assert result["routing_decision"] == "OPTIMAL_PATH_FOUND"
    assert result["reroute_impact_score"] == 0

def test_routing_critical_route_delay():
    mock_state = {"selected_route": {"route_id": "R1", "warehouse_id": "W1", "added_delay_hours": 130},"warehouse_db_context": {"current_utilization_pct": 70, "operational_status": "ACTIVE", "risk_tier": "NORMAL"},"extracted_metadata": {"maximum_tolerable_delay_hours": 140},"logs": []}
    result = analyze_route(mock_state)
    assert result["routing_decision"] == "CRITICAL_DELAY"
    assert result["reroute_impact_score"] == 50

def test_routing_exceeds_shipment_delay_limit():
    mock_state = {"selected_route": {"route_id": "R1", "warehouse_id": "W1", "added_delay_hours": 80},"warehouse_db_context": {"current_utilization_pct": 70, "operational_status": "ACTIVE", "risk_tier": "NORMAL"},"extracted_metadata": {"maximum_tolerable_delay_hours": 72},"logs": []}
    result = analyze_route(mock_state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 25
