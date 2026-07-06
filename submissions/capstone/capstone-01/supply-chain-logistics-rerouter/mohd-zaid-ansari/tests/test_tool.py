import pytest
from src.tools import query_warehouse_inventory_tool, get_alternative_routes_tool

def test_warehouse_tool_valid_id():
    res=query_warehouse_inventory_tool("WH-WEST-202")
    assert res["success"] is True
    assert res["original_warehouse_id"] == "WH-WEST-202"


def test_warehouse_tool_invalid_id():
    res=query_warehouse_inventory_tool("WH-UNKNOWN-999")
    assert res["success"] is True
    assert res["original_warehouse_id"] == "WH-WEST-202"


def test_route_tool_valid_port():
    res=get_alternative_routes_tool("PORT-SEATTLE-02")
    assert res["success"] is True
    assert res["original_port_id"] == "PORT-SEATTLE-02"



