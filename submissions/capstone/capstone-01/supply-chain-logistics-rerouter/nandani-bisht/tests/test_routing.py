import pytest
from src.nodes import analyze_route, calculate_reroute_impact_score
from src.state import get_initial_state

def test_routing_high_warehouse_utilization():
    """Test that a route with high warehouse utilization (>85%) triggers ROUTE_CLARIFICATION."""
    state = get_initial_state("INC-TEST", "Test manifest", "PORT-TEST")
    state["selected_route"] = {
        "route_id": "ROUTE-TEST",
        "added_delay_hours": 48,
        "warehouse_id": "WH-TEST"
    }
    state["warehouse_db_context"] = {
        "warehouse_name": "Test Warehouse",
        "current_utilization_pct": 92,
        "operational_status": "ACTIVE",
        "risk_tier": "NORMAL"
    }
    state["extracted_metadata"] = {
        "maximum_tolerable_delay_hours": 72
    }
    
    result = analyze_route(state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 30

def test_routing_elevated_risk():
    """Test that an elevated risk warehouse triggers ROUTE_CLARIFICATION."""
    state = get_initial_state("INC-TEST", "Test manifest", "PORT-TEST")
    state["selected_route"] = {
        "route_id": "ROUTE-TEST",
        "added_delay_hours": 48,
        "warehouse_id": "WH-TEST"
    }
    state["warehouse_db_context"] = {
        "warehouse_name": "Test Warehouse",
        "current_utilization_pct": 70,
        "operational_status": "ACTIVE",
        "risk_tier": "ELEVATED"
    }
    state["extracted_metadata"] = {
        "maximum_tolerable_delay_hours": 72
    }
    
    result = analyze_route(state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 25

def test_routing_valid_route():
    """Test that a valid route with acceptable conditions triggers OPTIMAL_PATH_FOUND."""
    state = get_initial_state("INC-TEST", "Test manifest", "PORT-TEST")
    state["selected_route"] = {
        "route_id": "ROUTE-TEST",
        "added_delay_hours": 48,
        "warehouse_id": "WH-TEST"
    }
    state["warehouse_db_context"] = {
        "warehouse_name": "Test Warehouse",
        "current_utilization_pct": 75,
        "operational_status": "ACTIVE",
        "risk_tier": "NORMAL"
    }
    state["extracted_metadata"] = {
        "maximum_tolerable_delay_hours": 72
    }
    
    result = analyze_route(state)
    assert result["routing_decision"] == "OPTIMAL_PATH_FOUND"
    assert result["reroute_impact_score"] == 0

def test_delay_constraint_triggers_clarification():
    """Test that an added delay exceeding maximum tolerable delay triggers ROUTE_CLARIFICATION."""
    state = get_initial_state("INC-TEST", "Test manifest", "PORT-TEST")
    state["selected_route"] = {
        "route_id": "ROUTE-TEST",
        "added_delay_hours": 80,
        "warehouse_id": "WH-TEST"
    }
    state["warehouse_db_context"] = {
        "warehouse_name": "Test Warehouse",
        "current_utilization_pct": 75,
        "operational_status": "ACTIVE",
        "risk_tier": "NORMAL"
    }
    state["extracted_metadata"] = {
        "maximum_tolerable_delay_hours": 72
    }
    
    result = analyze_route(state)
    assert result["routing_decision"] == "ROUTE_CLARIFICATION"
    assert result["reroute_impact_score"] == 25

def test_critical_delay_triggers_escalation():
    """Test that a route with delay exceeding 120 hours triggers CRITICAL_DELAY escalation."""
    state = get_initial_state("INC-TEST", "Test manifest", "PORT-TEST")
    state["selected_route"] = {
        "route_id": "ROUTE-TEST",
        "added_delay_hours": 130,
        "warehouse_id": "WH-TEST"
    }
    state["warehouse_db_context"] = {
        "warehouse_name": "Test Warehouse",
        "current_utilization_pct": 75,
        "operational_status": "ACTIVE",
        "risk_tier": "NORMAL"
    }
    state["extracted_metadata"] = {
        "maximum_tolerable_delay_hours": 150
    }
    
    result = analyze_route(state)
    assert result["routing_decision"] == "CRITICAL_DELAY"
    assert result["reroute_impact_score"] == 50

def test_reroute_impact_score():
    """Verify the reroute impact score calculations and capping at 100."""
    score = calculate_reroute_impact_score(
        current_utilization_pct=90,  
        risk_tier="ELEVATED",        
        operational_status="INACTIVE", 
        added_delay_hours=130, 
        maximum_tolerable_delay_hours=100
    )
    assert score == 100
    
    score_normal = calculate_reroute_impact_score(
        current_utilization_pct=50,
        risk_tier="NORMAL",
        operational_status="ACTIVE",
        added_delay_hours=24,
        maximum_tolerable_delay_hours=72
    )
    assert score_normal == 0
