import pytest
from src.tools import query_warehouse_inventory_tool, get_alternative_routes_tool

def test_warehouse_tool_valid_id():
    """Test query_warehouse_inventory_tool with a valid warehouse ID."""
    warehouse_id = "WH-WEST-202"
    result = query_warehouse_inventory_tool(warehouse_id)
    
    assert "error" not in result
    assert result["warehouse_name"] == "Pacific Gateway Storage"
    assert result["current_utilization_pct"] == 68
    assert result["operational_status"] == "ACTIVE"
    assert result["risk_tier"] == "ELEVATED"

def test_warehouse_tool_invalid_id():
    """Test query_warehouse_inventory_tool with an invalid warehouse ID."""
    warehouse_id = "WH-UNKNOWN-999"
    result = query_warehouse_inventory_tool(warehouse_id)
    
    assert "error" in result
    assert "not found" in result["error"].lower()
    
    
def test_route_tool_valid_port():
    """Test get_alternative_routes_tool with a valid disrupted port ID."""
    port_id = "PORT-SEATTLE-02"
    result = get_alternative_routes_tool(port_id)
    
    assert isinstance(result, list)
    assert len(result) > 0
    
    for route in result:
        assert "route_id" in route
        assert "warehouse_id" in route
        assert "added_delay_hours" in route
        assert "alternative_port" in route
        
