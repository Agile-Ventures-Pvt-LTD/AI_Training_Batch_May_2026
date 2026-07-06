import json
import os
from config import INVENTORY_STATUS_PATH, ROUTE_OPTIONS_PATH
from langchain_core.tools import StructuredTool

def get_absolute_path(config_path: str) -> str:
    if os.path.isabs(config_path):
        return config_path
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    variants = [
        os.path.join(base_dir, config_path),
        os.path.join(base_dir, "src", "data", os.path.basename(config_path)),
        os.path.join(base_dir, "src", os.path.basename(config_path)),
        os.path.join(base_dir, os.path.basename(config_path))
    ]
    for variant in variants:
        if os.path.exists(variant):
            return variant
    return os.path.join(base_dir, config_path)

def load_inventory_data():
    file_path = get_absolute_path(INVENTORY_STATUS_PATH)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_route_data():
    file_path = get_absolute_path(ROUTE_OPTIONS_PATH)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def query_warehouse_inventory_tool(warehouse_id: str) -> dict:
    if not isinstance(warehouse_id, str) or not warehouse_id.strip():
        return {
            'error': "Invalid Warehouse ID is provided",
            'warehouse_id': warehouse_id if isinstance(warehouse_id, str) else None,
        }
    inventory = load_inventory_data()
    warehouse = inventory.get(warehouse_id)
    if warehouse is None:
        return {
            'error': f'Warehouse {warehouse_id} is not found in inventory',
            'warehouse_id': warehouse_id
        }
    return {
        'warehouse_name': warehouse.get("warehouse_name", ""),
        "current_utilization_pct": warehouse.get('current_utilization_pct', 0),
        "operational_status": warehouse.get('operational_status', 'UNKNOWN'),
        "risk_tier": warehouse.get('risk_tier', 'Unknown')
    }

def get_alternative_route_tool(disrupted_port_id: str) -> list:
    if not isinstance(disrupted_port_id, str) or not disrupted_port_id.strip():
        return [{
            "error": "Invalid Port ID is provided",
            "disrupted_port_id": disrupted_port_id if isinstance(disrupted_port_id, str) else None
        }]
    inventory = load_route_data()
    routes = inventory.get(disrupted_port_id)
    if routes is None:
        return [{
            "error": f"Disrupted port {disrupted_port_id} is not found in inventory",
            "disrupted_port_id": disrupted_port_id
        }]
    if isinstance(routes, dict):
        routes = [routes]
    cleaned_routes = []
    for route in routes:
        cleaned_routes.append({
            "route_id": route.get("route_id", ""),
            "alternative_port": route.get("alternative_port", ""),
            "warehouse_id": route.get("warehouse_id", ""),
            "added_delay_hours": route.get("added_delay_hours", 0)
        })
    return cleaned_routes
