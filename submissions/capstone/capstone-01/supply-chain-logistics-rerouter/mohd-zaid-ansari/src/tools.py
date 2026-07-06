from langchain.tools import tool
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
INVENTORY_PATH = BASE_DIR / "data" / "inventory_status.json"
ROUTE_PATH = BASE_DIR / "data" / "route_options.json"

inventory_status_path = INVENTORY_PATH
route_options_path = ROUTE_PATH


@tool
def query_warehouse_inventory_tool(warehouse_id: str):
    """Get the current operational information from the warehouse."""
    try:
        with open(inventory_status_path, mode="r", encoding="utf-8") as file:
            rubric = json.load(file)
        if isinstance(rubric, dict) and warehouse_id in rubric:
            data = rubric[warehouse_id]
        else:
            return {"error": "ID is not valid"}

        return {
            warehouse_id: {
                "warehouse_name": data.get("warehouse_name"),
                "current_utilization_pct": data.get("current_utilization_pct"),
                "operational_status": data.get("operational_status"),
                "risk_tier": data.get("risk_tier"),
            },
        }
    except Exception as e:
        return {"error": "Failed to query warehouse inventory", "details": str(e)}
    
#============================================================================================================================

@tool
def get_alternative_routes_tool(disrupted_port_id:str):
    """It displays alternate route available if any port is disrupted."""
    try:
        with open(route_options_path, mode="r", encoding="utf-8") as file:
            reader=json.load(file)
        if isinstance(reader, dict) and disrupted_port_id in reader:
            info=reader[disrupted_port_id][0]
        else:
            return{"error": "ID is not valid"}
        return{
            disrupted_port_id:[{
                "route_id":info.get("route_id"),
                "alternative_port":info.get("alternative_port"),
                "warehouse_id":info.get("warehouse_id"),
                "added_delay_hours":info.get("added_delay_hours"),
            },]
        }
    except Exception as e:
        return {"error": "Failed to query route options", "details": str(e)}

    



