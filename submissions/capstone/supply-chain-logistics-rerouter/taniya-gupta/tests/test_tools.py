from src.tools import query_warehouse_inventory_tool, query_route_inventory_tool, get_alternative_routes_tool

def test_warehouse_tool_valid_id():
    result = query_warehouse_inventory_tool.invoke({"warehouse_id": "WH-WEST-202"})
    assert result != {}
    assert result["warehouse_name"] == "Pacific Gateway Storage"
    assert result["current_utilization_pct"] == 68
    assert result["operational_status"] == "ACTIVE"
    assert result["risk_tier"] == "ELEVATED"

def test_route_tool_valid_port():
    result = query_route_inventory_tool.invoke({"disrupted_port_id": "PORT-SEATTLE-02"})
    assert isinstance(result, list)
    assert len(result) > 0
    for route in result:
        assert "route_id" in route
        assert "warehouse_id" in route
        assert "added_delay_hours" in route
        assert "alternative_port" in route

def test_get_alternative_routes_tool_valid_port():
    result = get_alternative_routes_tool.invoke({"disrupted_port_id": "PORT-SEATTLE-02"})
    assert isinstance(result, list)
    assert len(result) > 0
