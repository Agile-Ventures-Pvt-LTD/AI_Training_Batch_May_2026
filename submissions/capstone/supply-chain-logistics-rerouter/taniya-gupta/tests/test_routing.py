from src.nodes import analyze_route

def test_routing_high_warehouse_utilization():
    """Test 5: Warehouse utilization above 85% triggers ROUTE_CLARIFICATION."""
    state = {
        "selected_route": {"route_id": "ROUTE-1", "added_delay_hours": 40},
        "warehouse_db_context": {
            "current_utilization_pct": 92,
            "operational_status": "ACTIVE",
            "risk_tier": "NORMAL"
        },
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},
        "routes_evaluated": [],
        "logs": []
    }
    res = analyze_route(state)
    assert res["routing_decision"] == "ROUTE_CLARIFICATION"
    assert res["reroute_impact_score"] == 30

def test_routing_elevated_risk():
    """Test 6: Warehouse with ELEVATED risk triggers ROUTE_CLARIFICATION."""
    state = {
        "selected_route": {"route_id": "ROUTE-1", "added_delay_hours": 40},
        "warehouse_db_context": {
            "current_utilization_pct": 50,
            "operational_status": "ACTIVE",
            "risk_tier": "ELEVATED"
        },
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},
        "routes_evaluated": [],
        "logs": []
    }
    res = analyze_route(state)
    assert res["routing_decision"] == "ROUTE_CLARIFICATION"
    assert res["reroute_impact_score"] == 25



def test_delay_constraint_triggers_clarification():
    state = {
        "selected_route": {"route_id": "ROUTE-1", "added_delay_hours": 80},
        "warehouse_db_context": {
            "current_utilization_pct": 70,
            "operational_status": "ACTIVE",
            "risk_tier": "NORMAL"
        },
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},
        "routes_evaluated": [],
        "logs": []
    }
    res = analyze_route(state)
    assert res["routing_decision"] == "ROUTE_CLARIFICATION"
    assert res["reroute_impact_score"] == 25


def test_reroute_impact_score():
    state = {
        "selected_route": {"route_id": "ROUTE-1", "added_delay_hours": 130},
        "warehouse_db_context": {
            "current_utilization_pct": 92, # +30
            "operational_status": "INACTIVE", # +30
            "risk_tier": "ELEVATED" # +25
        },
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72}, 
        "routes_evaluated": [],
        "logs": []
    }
    res = analyze_route(state)
    # Sum: 30 + 30 + 25 + 25 + 50 = 160 -> so 100
    assert res["reroute_impact_score"] == 100
