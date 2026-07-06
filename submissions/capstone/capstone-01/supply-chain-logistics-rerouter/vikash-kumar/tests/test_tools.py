from src.tools import query_warehouse_inventory_tool, get_alternative_routes_tool

def test_warehouse_tool_valid_id():
    result = query_warehouse_inventory_tool("WH-WEST-202")
    assert "error" not in result
    assert result["warehouse_name"] == "Pacific Gateway Storage"
    assert "current_utilization_pct" in result
    assert result["operational_status"] == "ACTIVE"
    assert result["risk_tier"] == "ELEVATED"

def test_warehouse_tool_invalid_id():
    result = query_warehouse_inventory_tool("WH-UNKNOWN-999")
    assert "error" in result

def test_route_tool_valid_port():
    result = get_alternative_routes_tool("PORT-SEATTLE-02")
    assert isinstance(result, list)
    assert len(result) > 0
    for route in result:
        assert "route_id" in route
        assert "warehouse_id" in route
        assert "added_delay_hours" in route
