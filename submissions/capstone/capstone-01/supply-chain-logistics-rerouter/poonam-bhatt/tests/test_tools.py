import pytest
from src.tools import query_warehouse_inventory_tool, get_alternative_routes_tool

def test_warehouse_tool_valid_id():
    warehouse_id = "WH-WEST-202"
    result = query_warehouse_inventory_tool(warehouse_id)
    
    assert "error" not in result
    assert result["warehouse_name"] == "Pacific Gateway Storage"
    assert result["current_utilization_pct"] == 68
    assert result["operational_status"] == "ACTIVE"
    assert result["risk_tier"] == "ELEVATED"

def test_warehouse_tool_invalid_id():
    warehouse_id = "WH-UNKNOWN-999"
    result = query_warehouse_inventory_tool(warehouse_id)
    
    assert "error" in result
    assert "not found" in result["error"].lower()

def test_route_tool_valid_port():
    port_id = "PORT-SEATTLE-02"
    routes = get_alternative_routes_tool(port_id)
    
    assert isinstance(routes, list)
    assert len(routes) == 3
    for route in routes:
        assert "route_id" in route
        assert "warehouse_id" in route
        assert "added_delay_hours" in route




### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026