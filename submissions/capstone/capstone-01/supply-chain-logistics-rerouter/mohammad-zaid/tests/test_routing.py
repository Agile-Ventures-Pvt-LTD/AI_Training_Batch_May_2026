
def routing_logic(warehouse, delay, shipment_delay=None,):
    if delay > 120:
        return "CRITICAL_DELAY"
    if warehouse["current_utilization_pct"] > 85:
        return "ROUTE_CLARIFICATION"
    if warehouse["operational_status"] != "ACTIVE":
        return "ROUTE_CLARIFICATION"
    if warehouse["risk_tier"] == "ELEVATED":
        return "ROUTE_CLARIFICATION"
    if (shipment_delay is not None and delay > shipment_delay):
        return "ROUTE_CLARIFICATION"
    return "OPTIMAL_PATH_FOUND"


def test_routing_high_warehouse_utilization():
    warehouse = {
        "current_utilization_pct": 92,
        "operational_status": "ACTIVE",
        "risk_tier": "NORMAL",
    }
    decision = routing_logic(warehouse, 40, 72,)
    assert decision == "ROUTE_CLARIFICATION"


def test_routing_elevated_risk():
    warehouse = {
        "current_utilization_pct": 60,
        "operational_status": "ACTIVE",
        "risk_tier": "ELEVATED",
    }
    decision = routing_logic(warehouse, 40, 72,)
    assert decision == "ROUTE_CLARIFICATION"


def test_routing_valid_route():

    warehouse = {
        "current_utilization_pct": 60,
        "operational_status": "ACTIVE",
        "risk_tier": "NORMAL",
    }

    decision = routing_logic(warehouse, 40, 72,)

    assert decision == "OPTIMAL_PATH_FOUND"
