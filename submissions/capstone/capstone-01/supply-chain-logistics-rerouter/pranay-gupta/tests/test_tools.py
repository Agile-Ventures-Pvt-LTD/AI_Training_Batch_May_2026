from src.tools import query_warehouse_inventory_tool, get_alternative_routes_tool


def test_warehouse_tool_valid_id():
    result = query_warehouse_inventory_tool("WH-WEST-202")

    assert "error" not in result
    assert result["warehouse_name"] == "Pacific Gateway Storage"
    assert "current_utilization_pct" in result
    assert isinstance(result["current_utilization_pct"], int)
    assert "operational_status" in result
    assert result["operational_status"] == "ACTIVE"
    assert "risk_tier" in result
    assert result["risk_tier"] == "ELEVATED"


def test_warehouse_tool_invalid_id():
    result = query_warehouse_inventory_tool("WH-UNKNOWN-999")

    assert "error" in result
    assert "WH-UNKNOWN-999" in result["error"]
    assert result["warehouse_id"] == "WH-UNKNOWN-999"


def test_warehouse_tool_returns_all_fields():
    result = query_warehouse_inventory_tool("WH-EAST-101")

    assert "warehouse_name" in result
    assert "current_utilization_pct" in result
    assert "operational_status" in result
    assert "risk_tier" in result


def test_route_tool_valid_port():
    result = get_alternative_routes_tool("PORT-SEATTLE-02")

    assert isinstance(result, list)
    assert len(result) >= 1

    for route in result:
        assert "route_id" in route
        assert "warehouse_id" in route
        assert "added_delay_hours" in route
        assert "alternative_port" in route


def test_route_tool_invalid_port():
    result = get_alternative_routes_tool("PORT-UNKNOWN-999")

    assert isinstance(result, list)
    assert len(result) == 0


def test_route_tool_returns_expected_routes():
    result = get_alternative_routes_tool("PORT-SEATTLE-02")

    route_ids = [r["route_id"] for r in result]
    assert "ROUTE-WEST-01" in route_ids
    assert "ROUTE-SOUTH-02" in route_ids
    assert "ROUTE-CENTRAL-03" in route_ids


def test_route_tool_route_delays():
    result = get_alternative_routes_tool("PORT-SEATTLE-02")

    delays = [r["added_delay_hours"] for r in result]
    assert all(isinstance(d, int) for d in delays)
    assert all(d > 0 for d in delays)