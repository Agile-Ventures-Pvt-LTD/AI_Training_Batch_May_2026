import json
from typing import Dict, Any, List

def query_warehouse_inventory_tool(warehouse_id:str)-> Dict[str,Any]:
    file_path = "data/inventory_status.json"
    if not file_path:
        return {"error" : f"{ModuleNotFoundError("inventory_status is not present.")}"}
    with open(file_path, "r") as file:
        data = json.load(file)
    info = data.get(warehouse_id)
    if not info:
        return {"error" : f"warehouse not found with id {warehouse_id}"}
    return info

def get_alternative_routes_tool(disrupted_port_id: str) -> List[Dict[str,Any]]:
    file_path = "data/route_options.json"
    if not file_path:
        return {"error" : f"{ModuleNotFoundError("route_options is not present.")}"}
    with open(file_path, "r") as file:
        data = json.load(file)
    info = data.get(disrupted_port_id)
    if not info:
        return {"error" : f"route_options not found with id {disrupted_port_id}"}
    return info