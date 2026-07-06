import ast
import os, json
from typing import Any
from langchain_core.tools import StructuredTool
try:
    from utils.config import ROUTE_DIR, WAREHOUSE_DIR
except ImportError:
    from .utils.config import ROUTE_DIR, WAREHOUSE_DIR

def _read(file_path: str):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def get_alternative_routes(disrupted_port_id: str) -> list[dict[str, Any]]:
    """Fetches and loads all routes available for the requested disrupted port.

    Args:
        disrupted_port_id (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        list[dict[str, Any]]
    """
    try:
        routes = _read(ROUTE_DIR)
    
        if not routes:
            print(f"No alternate routes available at {os.path.basename(ROUTE_DIR)}")
        return routes[disrupted_port_id]
    except KeyError:
        print(f"KeyError: No alternate routes available for port: {disrupted_port_id}.")


def query_warehouse_inventory(warehouse_id: str) -> dict[str, Any]:
    """Fetches warehouse information correspoding to a warehouse id.

    Args:
        warehouse_id (str): Warehouse id of the target warehouse.

    Returns:
        dict[str, Any]
    """
    try:
        warehouses = _read(WAREHOUSE_DIR)
    
        if not warehouses:
            print(f"No warehouses available at {os.path.basename(WAREHOUSE_DIR)}")
        
        return warehouses[warehouse_id]
    
    except KeyError:
        print(f"KeyError: No warehouse exist by the id: {warehouse_id}.")



get_alternative_routes_tool = StructuredTool.from_function(func=get_alternative_routes)

query_warehouse_inventory_tool = StructuredTool.from_function(func=query_warehouse_inventory)