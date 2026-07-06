import json
import os

def query_warehouse_inventory_tool(warehouse_id: str) -> dict:
    """Queries warehouse inventory database to retrieve utilization, status, and risk tier.
    
    Args:
        warehouse_id: The ID of the warehouse (e.g., WH-WEST-202).
        
    Returns:
        A dict containing warehouse operational metrics, or an error dict if not found.
    """
    db_path = "data/inventory_status.json"
    if not os.path.exists(db_path):
        return {"error": "Warehouse database file not found."}
        
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if warehouse_id in data:
            return data[warehouse_id]
        else:
            return {"error": f"Warehouse ID '{warehouse_id}' not found."}
    except Exception as e:
        return {"error": f"Error querying warehouse database: {str(e)}"}

def get_alternative_routes_tool(disrupted_port_id: str) -> list:
    """Queries alternative routes database to retrieve available routes for a disrupted port.
    
    Args:
        disrupted_port_id: The ID of the disrupted port (e.g., PORT-SEATTLE-02).
        
    Returns:
        A list of available routes, or an empty list if none are found or on error.
    """
    db_path = "data/route_options.json"
    if not os.path.exists(db_path):
        return []
        
    try:
        with open(db_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if disrupted_port_id in data:
            return data[disrupted_port_id]
        else:
            return []
    except Exception:
        return []




### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026