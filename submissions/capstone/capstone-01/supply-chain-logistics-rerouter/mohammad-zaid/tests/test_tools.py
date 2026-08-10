# test_tools.py
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.tools import (
    query_warehouse_inventory_tool,
    get_alternative_routes_tool,
)


def test_warehouse_tool_valid_id():
    result = query_warehouse_inventory_tool("WH-WEST-202")

    assert "warehouse_name" in result
    assert "current_utilization_pct" in result
    assert "operational_status" in result
    assert "risk_tier" in result

# Should pass
def test_warehouse_tool_invalid_id():
    result = query_warehouse_inventory_tool("WH-UNKNOWN-999")
    assert result["error"] is True


def test_route_tool_valid_port():
    routes = get_alternative_routes_tool("PORT-SEATTLE-02")
    assert isinstance(routes, list)
    assert len(routes) > 0
    route = routes[0]
    assert "route_id" in route
    assert "warehouse_id" in route
    assert "added_delay_hours" in route