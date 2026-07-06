import json
from config import *

INVENTORY_PATH = Config.BASE_DIR/"data"/"inventory_status.json"
ROUTES_PATH = Config.BASE_DIR/"data"/"route_options.json"

def query_warehouse_inventory_tool(warehouse_id: str):
    try:
        with open(INVENTORY_PATH) as f:
            data = json.load(f)

        if warehouse_id not in data:
            return{
                "error": "warehouse not found",
                "warehouse_id": warehouse_id
            }
        
        return data[warehouse_id]
    
    except Exception as e:
        return{
            "error": str(e)
        }
    

def get_alternative_routes_tool(disrupted_port_id: str):
    try:
        with open(ROUTES_PATH) as f:
            routes = json.load(f)

        return routes.get(
            disrupted_port_id,
            []
        )
    
    except Exception as e:
        return [
            {
                "error": str(e)
            }
        ]