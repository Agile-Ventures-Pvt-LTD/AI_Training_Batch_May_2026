from src.tools import ( query_warehouse_inventory_tool, get_alternative_routes_tool, )
def test_warehouse_tool_valid_id(): 
    result = query_warehouse_inventory_tool("WH-WEST-202") 
    assert result["success"] is True 
    assert result["warehouse_name"] == "Pacific Gateway Storage" 
    assert "current_utilization_pct" in result 
    assert "operational_status" in result 
    assert "risk_tier" in result
def test_warehouse_tool_invalid_id(): 
    result = query_warehouse_inventory_tool("WH-UNKNOWN-999") 
    assert result["success"] is False 
    assert "error" in result 
def test_route_tool_valid_port(): 
    routes = get_alternative_routes_tool("PORT-SEATTLE-02") 
    assert isinstance(routes, list) 
    assert len(routes) > 0 
    assert "route_id" in routes[0] 
    assert "warehouse_id" in routes[0] 
    assert "added_delay_hours" in routes[0]