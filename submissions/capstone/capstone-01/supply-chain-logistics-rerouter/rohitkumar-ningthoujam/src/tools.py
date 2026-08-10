import json 
from pathlib import Path 
BASE_DIR = Path(__file__).resolve().parent.parent 
INVENTORY_FILE = BASE_DIR / "data" / "inventory_status.json" 
ROUTES_FILE = BASE_DIR / "data" / "route_options.json" 

def load_json(file_path: Path): 
    """Read a JSON file.""" 
    with open(file_path, "r", encoding="utf-8") as file: 
        return json.load(file) 
    
def query_warehouse_inventory_tool(warehouse_id: str) -> dict: 
    """Return warehouse details for a warehouse ID.""" 
    inventory_data = load_json(INVENTORY_FILE) 
    warehouse = inventory_data.get(warehouse_id) 
    if not warehouse: 
        return { "success": False, 
                    "error": f"Warehouse ID '{warehouse_id}' was not found." } 
    return { "success": True, "warehouse_id": warehouse_id, **warehouse } 
    
    
def get_alternative_routes_tool(disrupted_port_id: str) -> list: 
    """Return all available routes for a disrupted port.""" 
    route_data = load_json(ROUTES_FILE) 
    routes = route_data.get(disrupted_port_id) 
    if not routes: 
        
        return [] 
    return routes