import json
import logging
from pathlib import Path
from typing import Any
LOGGER = logging.getLogger(__name__)
DATA_DIR = Path("data")
INVENTORY_FILE = (DATA_DIR / "inventory_status.json")
ROUTES_FILE = (DATA_DIR / "route_options.json")
def load_json_file(file_path: Path,)-> dict | list:
    """
    JSON .
    """
    try:
        with open(file_path,"r",encoding="utf-8",) as file:
            return json.load(file)
    except FileNotFoundError:
        LOGGER.error("File not found: %s",file_path,)
        return {}
    except json.JSONDecodeError:
        LOGGER.error("Invalid JSON file: %s",file_path,)
        return {}
    except Exception as ex:
        LOGGER.exception(ex)
        return {}
def query_warehouse_inventory_tool(warehouse_id: str,)->dict[str, Any]:
    """
    Input:
    {"warehouse_id": "WH-WEST-202"}
    Output:
    {"warehouse_name": ,}
    Must never crash.
    """
    inventory_db = load_json_file(INVENTORY_FILE)
    if not inventory_db:
        return {"error": True,"message":"Inventory database unavailable.",}
    warehouse = inventory_db.get(warehouse_id)
    if warehouse is None:
        return {"error": True,"warehouse_id": warehouse_id,"message":"Warehouse not found.",}
    return warehouse
def get_alternative_routes_tool(disrupted_port_id: str,) -> list[dict[str, Any]]:
    """
    Input:
    {"disrupted_port_id":"PORT-SEATTLE-02"}
    Output:
    [{"route_id": "...",...}]
    """
    routes_db = load_json_file(ROUTES_FILE)
    if not routes_db:
        return []
    routes = routes_db.get(disrupted_port_id)
    if routes is None:
        return []
    return routes
def get_route_by_id(route_id: str,)->dict[str, Any] | None:
    """
    Find route anywhere in route DB.
    """
    routes_db = load_json_file(ROUTES_FILE)
    for routes in routes_db.values():
        for route in routes:
            if (route.get("route_id")== route_id):
                return route
    return None
def warehouse_exists(warehouse_id: str,) -> bool:
    """
    Validate warehouse existence.
    """
    warehouse = (query_warehouse_inventory_tool(warehouse_id))
    return not warehouse.get("error",False,)
def route_exists(disrupted_port_id: str,) -> bool:
    """
    Validate route presence.
    """
    routes = (get_alternative_routes_tool(disrupted_port_id))
    return len(routes) > 0
def tools_health_check() -> dict:
    """
    Startup validation.
    """
    try:
        inventory = load_json_file(INVENTORY_FILE)
        routes = load_json_file(ROUTES_FILE)
        return {"status": "healthy","warehouses":len(inventory),"ports":len(routes),}
    except Exception as ex:
        return {"status": "unhealthy","error": str(ex),}
if __name__ == "__main__":
    print("\nTOOL HEALTH CHECK\n")
    print(tools_health_check())
    print("\nWAREHOUSE LOOKUP\n")
    print(query_warehouse_inventory_tool("WH-WEST-202"))
    print("\nINVALID WAREHOUSE\n")
    print(query_warehouse_inventory_tool("WH-UNKNOWN-999"))
    print("\nROUTES LOOKUP\n")
    print(get_alternative_routes_tool("PORT-SEATTLE-02"))