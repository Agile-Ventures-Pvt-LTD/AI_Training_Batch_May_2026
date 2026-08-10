from src.tools import get_alternative_routes_tool, query_warehouse_inventory_tool


def test_warehouse_tool_valid_id():
    result=query_warehouse_inventory_tool("WH-WEST-202")
    assert result
    assert result["warehouse_name"]=="Pacific Gateway Storage"
    assert result["current_utilization_pct"]==68
    assert result["operational_status"]=="ACTIVE"
    assert result["risk_tier"]=="ELEVATED"



def test_warehouse_tool_invalid_id():
    result=query_warehouse_inventory_tool("WH-UNKNOWN-999")
    assert result["error"]== 'Not able to fetch data.'



def test_route_tool_valid_port():
    result=get_alternative_routes_tool("PORT-SEATTLE-02")
    assert result is list












