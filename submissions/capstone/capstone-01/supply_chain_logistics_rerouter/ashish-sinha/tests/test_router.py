
from src.graph import route_after_analysis,route_clarification
def test_routing_high_warehouse_utilization():
    decision = route_after_analysis(
        utilization=92, 
        risk_tier="NORMAL", 
        status="ACTIVE", 
        delay=2, 
        max_allowed_delay=12
    )
    assert decision == "ROUTE_CLARIFICATION"

def test_routing_elevated_risk():
    decision = route_clarification(
        utilization=50, 
        risk_tier="ELEVATED", 
        status="ACTIVE", 
        delay=2, 
        max_allowed_delay=12
    )
    assert decision == "ROUTE_CLARIFICATION"

def test_routing_valid_route():
    decision = route_clarification(
        utilization=85, 
        risk_tier="NORMAL", 
        status="ACTIVE", 
        delay=4, 
        max_allowed_delay=12
    )
    assert decision == "OPTIMAL_PATH_FOUND"