import json
import os

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))

def query_warehouse_inventory_tool(warehouse_id: str) -> dict:
    try:
        path = os.path.join(DATA_DIR, "inventory_status.json")
        if not os.path.exists(path):
            return {f"error found: {path}"}
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        if warehouse_id in data:
            return data[warehouse_id]
        return {f"Warehouse_id {warehouse_id} is not found"}
    except Exception as e:
        return {f"Tool execution is failed and the error is: {str(e)}"}


def get_alternative_routes_tool(disrupted_port_id: str) -> list:
    try:
        path = os.path.join(DATA_DIR, "route_options.json")
        if not os.path.exists(path):
            return []
            
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        return data.get(disrupted_port_id, [])
    except Exception:
        return []

