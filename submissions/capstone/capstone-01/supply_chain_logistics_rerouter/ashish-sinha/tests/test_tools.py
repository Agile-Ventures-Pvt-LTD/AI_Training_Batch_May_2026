import pytest
from src.tools import get_alternative_route_tool,query_warehouse_inventory_tool

def test_warehouse_tool_valid_id():
    result = query_warehouse_inventory_tool('WH-WEST-202')
    assert result is not None
    assert isinstance(result,dict)
    assert "warehouse_name" in result
    assert result['warehouse_name']=='Pacific Gateway Storage'
    assert result["current_utilization_pct"]==68
    assert "operational_status" in result
    assert result["operational_status"]=="ACTIVE"
    assert "risk_tier" in result
    assert result['risk_tier']=='ELEVATED'

def test_warehouse_tool_invalid_id():
    result = query_warehouse_inventory_tool('WH-UNKNOWN-999')
    assert isinstance(result,dict)
    assert "error" in result
    assert "WH-UNKNOWN-999" in result['error']
    assert result.get('warehouse_id') =="WH-UNKNOWN-999"

def test_route_tool_valid_port():
    result = get_alternative_route_tool("PORT-SEATTLE-02")
    assert isinstance(result,list)
    assert len(result)==0


