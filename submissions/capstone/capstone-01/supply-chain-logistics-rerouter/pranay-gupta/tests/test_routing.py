from src.routing_rules import evaluate_route, calculate_reroute_impact_score


def _make_metadata(max_delay=None):
    return {
        "shipment_id": "SH-TEST",
        "cargo_weight_tons": 500,
        "cargo_type": "electronics",
        "target_warehouse_id": "WH-TEST",
        "has_perishables": False,
        "maximum_tolerable_delay_hours": max_delay,
    }


def _make_route(delay=48):
    return {
        "route_id": "ROUTE-TEST",
        "alternative_port": "Port-Test",
        "warehouse_id": "WH-TEST",
        "added_delay_hours": delay,
    }


def _make_warehouse(utilization=70, status="ACTIVE", risk="NORMAL"):
    return {
        "warehouse_name": "Test Hub",
        "current_utilization_pct": utilization,
        "operational_status": status,
        "risk_tier": risk,
    }


def test_routing_high_warehouse_utilization():
    metadata = _make_metadata()
    route = _make_route(delay=48)
    warehouse = _make_warehouse(utilization=92)

    decision, reason, score = evaluate_route(metadata, route, warehouse)

    assert decision == "ROUTE_CLARIFICATION"
    assert "utilization" in reason.lower()
    assert score >= 30


def test_routing_elevated_risk():
    metadata = _make_metadata()
    route = _make_route(delay=48)
    warehouse = _make_warehouse(utilization=70, risk="ELEVATED")

    decision, reason, score = evaluate_route(metadata, route, warehouse)

    assert decision == "ROUTE_CLARIFICATION"
    assert "elevated" in reason.lower()
    assert score >= 25


def test_routing_valid_route():
    metadata = _make_metadata(max_delay=72)
    route = _make_route(delay=48)
    warehouse = _make_warehouse(utilization=70, status="ACTIVE", risk="NORMAL")

    decision, reason, score = evaluate_route(metadata, route, warehouse)

    assert decision == "OPTIMAL_PATH_FOUND"
    assert score == 0


def test_routing_inactive_warehouse():
    metadata = _make_metadata()
    route = _make_route(delay=48)
    warehouse = _make_warehouse(utilization=70, status="MAINTENANCE")

    decision, reason, score = evaluate_route(metadata, route, warehouse)

    assert decision == "ROUTE_CLARIFICATION"
    assert "status" in reason.lower() or "active" in reason.lower()
    assert score >= 30

