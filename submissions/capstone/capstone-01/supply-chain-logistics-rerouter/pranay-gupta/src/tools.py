import json
from typing import List
from src.config import (INVENTORY_STATUS_PATH, ROUTE_OPTIONS_PATH)

def load_json_file(file_path) -> dict:
    with open(file_path,"r",encoding="utf-8") as data:
        return json.load(data)

def query_warehouse_inventory_tool(warehouse_id:str)-> dict:
    try:
        route_data = load_json_file(INVENTORY_STATUS_PATH)
    except(FileNotFoundError,json.JSONDecodeError):
        return {
            "error": f"The json file is not found in directory",
            "warehouse_id": warehouse_id,
        }
    
    warehouse_data = route_data.get(warehouse_id)
    if warehouse_data is None:
        return {
            "error": f"Warehouse {warehouse_id} not found in inventory",
            "warehouse_id": warehouse_id,
        }
    
    return warehouse_data

def get_alternative_routes_tool(disrupted_port_id:str) -> List:
    try:
        route_data = load_json_file(ROUTE_OPTIONS_PATH)
    except (FileNotFoundError,json.JSONDecodeError):
        return []
    
    return route_data.get(disrupted_port_id,[])
    