
import pytest
from src.tools import query_warehouse_inventory_tool,get_alternative_routes_tool

def test_query_warehouse():
    warehouse_id="WH-EAST-101"
    assert query_warehouse_inventory_tool(warehouse_id) is not None



def test_get_alternative_routes():
    disrupted_id="PORT-SEATTLE-02"
    assert get_alternative_routes_tool(disrupted_id) is not None