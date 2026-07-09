import unittest
from unittest.mock import patch, mock_open
from pathlib import Path

from src.tools import (load_json_file,query_warehouse_inventory_tool,get_alternative_routes_tool,get_route_by_id,warehouse_exists,route_exists,tools_health_check,)
class TestTools(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data='{"a": 1}')
    def test_load_json_file_valid(self, mock_file):
        result = load_json_file(Path("dummy.json"))
        self.assertEqual(result, {"a": 1})
    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_json_file_missing(self, mock_file):
        result = load_json_file(Path("missing.json"))
        self.assertEqual(result, {})
    @patch("builtins.open", new_callable=mock_open, read_data="INVALID JSON")
    def test_load_json_file_invalid_json(self, mock_file):
        result = load_json_file(Path("bad.json"))
        self.assertEqual(result, {})
    @patch("src.tools.load_json_file")
    def test_query_warehouse_valid(self, mock_load):
        mock_load.return_value = {
            "WH-1": {"name": "Test Warehouse", "capacity": 100}
        }
        result = query_warehouse_inventory_tool("WH-1")
        self.assertEqual(result["name"], "Test Warehouse")
    @patch("src.tools.load_json_file")
    def test_query_warehouse_missing(self, mock_load):
        mock_load.return_value = {}
        result = query_warehouse_inventory_tool("WH-1")
        self.assertTrue(result["error"])
    @patch("src.tools.load_json_file")
    def test_query_warehouse_not_found(self, mock_load):
        mock_load.return_value = {"WH-2": {"name": "Other"}}
        result = query_warehouse_inventory_tool("WH-1")
        self.assertTrue(result["error"])
    @patch("src.tools.load_json_file")
    def test_get_alternative_routes_tool_valid(self, mock_load):
        mock_load.return_value = {
            "PORT-1": [{"route_id": "R1"}, {"route_id": "R2"}]
        }

        result = get_alternative_routes_tool("PORT-1")
        self.assertEqual(len(result), 2)
    @patch("src.tools.load_json_file")
    def test_get_alternative_routes_tool_no_routes(self, mock_load):
        mock_load.return_value = {}
        result = get_alternative_routes_tool("PORT-1")
        self.assertEqual(result, [])
    @patch("src.tools.load_json_file")
    def test_get_route_by_id_found(self, mock_load):
        mock_load.return_value = {
            "PORT-1": [{"route_id": "R1"}, {"route_id": "R2"}]
        }
        result = get_route_by_id("R2")
        self.assertEqual(result["route_id"], "R2")
    @patch("src.tools.load_json_file")
    def test_get_route_by_id_not_found(self, mock_load):
        mock_load.return_value = {"PORT-1": [{"route_id": "R1"}]}
        result = get_route_by_id("R999")
        self.assertIsNone(result)
    @patch("src.tools.query_warehouse_inventory_tool")
    def test_warehouse_exists_true(self, mock_q):
        mock_q.return_value = {"capacity": 100}
        self.assertTrue(warehouse_exists("WH-1"))
    @patch("src.tools.query_warehouse_inventory_tool")
    def test_warehouse_exists_false(self, mock_q):
        mock_q.return_value = {"error": True}
        self.assertFalse(warehouse_exists("WH-1"))
    @patch("src.tools.get_alternative_routes_tool")
    def test_route_exists_true(self, mock_routes):
        mock_routes.return_value = [{"route_id": "R1"}]
        self.assertTrue(route_exists("PORT-1"))
    @patch("src.tools.get_alternative_routes_tool")
    def test_route_exists_false(self, mock_routes):
        mock_routes.return_value = []
        self.assertFalse(route_exists("PORT-1"))
    @patch("src.tools.load_json_file")
    def test_tools_health_check(self, mock_load):
        mock_load.side_effect = [
            {"W1": {}},   
            {"P1": []},   
        ]
        result = tools_health_check()
        self.assertEqual(result["status"], "healthy")
        self.assertEqual(result["warehouses"], 1)
        self.assertEqual(result["ports"], 1)
if __name__ == "__main__":
    unittest.main()