import json
import os
import pytest
from src.tools import query_warehouse_inventory_tool, get_alternative_routes_tool

def _prepare_data(tmp_path):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    inventory = {"WH-001": {"warehouse_utilization": 80, "operational_status": "ACTIVE", "risk_tier": "LOW"}}
    routes = {"PORT-001": [{"route_id": "R1"}, {"route_id": "R2"}]}
    (data_dir / "inventory_status.json").write_text(json.dumps(inventory))
    (data_dir / "route_options.json").write_text(json.dumps(routes))
    return data_dir

@pytest.fixture
def change_cwd(tmp_path):
    _prepare_data(tmp_path)
    original = os.getcwd()
    os.chdir(tmp_path)
    yield
    os.chdir(original)

def test_query_warehouse_inventory_valid(change_cwd):
    result = query_warehouse_inventory_tool("WH-001")
    assert isinstance(result, dict)
    assert result["warehouse_utilization"] == 80
    assert result["operational_status"] == "ACTIVE"
    assert result["risk_tier"] == "LOW"

def test_query_warehouse_inventory_invalid(change_cwd):
    result = query_warehouse_inventory_tool("WH-999")
    assert isinstance(result, dict)
    assert "error" in result
    assert "warehouse not found" in result["error"]

def test_get_alternative_routes_valid(change_cwd):
    result = get_alternative_routes_tool("PORT-001")
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["route_id"] == "R1"
    assert result[1]["route_id"] == "R2"

def test_get_alternative_routes_invalid(change_cwd):
    result = get_alternative_routes_tool("PORT-999")
    assert isinstance(result, dict)
    assert "error" in result
    assert "route_options not found" in result["error"]