# tools.py

# root_path = Path.cwd().parent.parent
# inventory_path = root_path.joinpath("data/inventory_status.json")
# print(inventory_path)

import json
from pathlib import Path

DATA_DIR = Path("data")

# warehouse  - tool (LangChain)
def query_warehouse_inventory_tool(warehouse_id: str) -> dict:
    """
    Returns warehouse inventory information.
    """

    file_path = DATA_DIR / "inventory_status.json"

    with open(file_path, "r") as f:
        warehouses = json.load(f)

    if warehouse_id not in warehouses:
        return {
            "error": True,
            "message": f"Warehouse '{warehouse_id}' not found."
        }

    return warehouses[warehouse_id]

# Route Tool

def get_alternative_routes_tool(disrupted_port_id: str) -> list:
    """
    Returns all routes for a disrupted port.
    """

    file_path = DATA_DIR / "route_options.json"
    try:
        
        with open(file_path, "r") as f:
            routes = json.load(f)
        return routes.get(disrupted_port_id, [])
    
    except Exception as e:
        return [f"file not found: {e}"]