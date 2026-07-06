import pytest
from src.nodes import analyze_route

def test_routing_high_warehouse_utilization():
    # Test case: warehouse utilization is 92% (>85%) -> ROUTE_CLARIFICATION
    state = {
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},
        "selected_route": {"route_id": "ROUTE-WEST-01", "added_delay_hours": 48},
        "warehouse_db_context": {
            "warehouse_name": "Test Hub",
            "current_utilization_pct": 92,
            "operational_status": "ACTIVE",
            "risk_tier": "NORMAL"
        },
        "logs": []
    }
    result = analyze_route(state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 30 # +30 for utilization > 85%

def test_routing_elevated_risk():
    # Test case: warehouse risk tier is ELEVATED -> ROUTE_CLARIFICATION
    state = {
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},
        "selected_route": {"route_id": "ROUTE-WEST-01", "added_delay_hours": 48},
        "warehouse_db_context": {
            "warehouse_name": "Test Hub",
            "current_utilization_pct": 50,
            "operational_status": "ACTIVE",
            "risk_tier": "ELEVATED"
        },
        "logs": []
    }
    result = analyze_route(state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 25 # +25 for elevated risk

def test_routing_valid_route():
    # Test case: valid route, utilization <= 85, active status, risk NORMAL, delay <= limit -> OPTIMAL_PATH_FOUND
    state = {
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},
        "selected_route": {"route_id": "ROUTE-WEST-01", "added_delay_hours": 48},
        "warehouse_db_context": {
            "warehouse_name": "Test Hub",
            "current_utilization_pct": 60,
            "operational_status": "ACTIVE",
            "risk_tier": "NORMAL"
        },
        "logs": []
    }
    result = analyze_route(state)
    assert result["routing_decision"] == "OPTIMAL_PATH_FOUND"
    assert result["reroute_impact_score"] == 0

def test_delay_constraint_triggers_clarification():
    # Test case: delay (80 hours) > tolerable limit (72 hours) -> ROUTE_CLARIFICATION
    state = {
        "extracted_metadata": {"maximum_tolerable_delay_hours": 72},
        "selected_route": {"route_id": "ROUTE-WEST-01", "added_delay_hours": 80},
        "warehouse_db_context": {
            "warehouse_name": "Test Hub",
            "current_utilization_pct": 60,
            "operational_status": "ACTIVE",
            "risk_tier": "NORMAL"
        },
        "logs": []
    }
    result = analyze_route(state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 25 # +25 for delay limit exceeded

def test_critical_delay_triggers_escalation():
    # Test case: delay (130 hours) > 120 hours limit -> CRITICAL_DELAY
    state = {
        "extracted_metadata": {"maximum_tolerable_delay_hours": 150},
        "selected_route": {"route_id": "ROUTE-WEST-01", "added_delay_hours": 130},
        "warehouse_db_context": {
            "warehouse_name": "Test Hub",
            "current_utilization_pct": 60,
            "operational_status": "ACTIVE",
            "risk_tier": "NORMAL"
        },
        "logs": []
    }
    result = analyze_route(state)
    assert result["routing_decision"] == "CRITICAL_DELAY"
    assert result["reroute_impact_score"] == 50 # +50 for delay > 120 hours



### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026