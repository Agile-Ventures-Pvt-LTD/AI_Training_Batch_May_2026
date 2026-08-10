import json
import os
from typing import Dict, Any, List, Union

def query_warehouse_inventory_tool(warehouse_id: str) -> Dict[str, Any]:
    """
    Retrieve current operational information for a given warehouse.
    
    Args:
        warehouse_id: The ID of the warehouse (e.g., 'WH-WEST-202').
        
    Returns:
        A dictionary containing warehouse_name, current_utilization_pct,
        operational_status, and risk_tier, or a structured error dictionary.
    """
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "inventory_status.json")
        if not os.path.exists(data_path):
            return {"error": "Inventory status database file not found."}
            
        with open(data_path, "r") as f:
            inventory = json.load(f)
            
        if warehouse_id in inventory:
            return inventory[warehouse_id]
        else:
            return {"error": f"Warehouse with ID '{warehouse_id}' not found."}
    except Exception as e:
        return {"error": f"An error occurred while querying the warehouse database: {str(e)}"}

def get_alternative_routes_tool(disrupted_port_id: str) -> List[Dict[str, Any]]:
    """
    Retrieve alternative routes available when a port is disrupted.
    
    Args:
        disrupted_port_id: The ID of the disrupted port (e.g., 'PORT-SEATTLE-02').
        
    Returns:
        A list of dictionaries, where each dictionary contains route_id,
        alternative_port, warehouse_id, and added_delay_hours.
    """
    try:
        data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "route_options.json")
        if not os.path.exists(data_path):
            return []
            
        with open(data_path, "r") as f:
            routes = json.load(f)
            
        return routes.get(disrupted_port_id, [])
    except Exception:
        return []
    
    
    
    