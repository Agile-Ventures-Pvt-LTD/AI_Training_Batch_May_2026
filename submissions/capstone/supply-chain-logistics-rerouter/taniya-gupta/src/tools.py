from langchain_core.tools import tool
import json

class ToolWrapper:
    def __init__(self, tool):
        self._tool = tool
    def invoke(self, *args, **kwargs):
        return self._tool.invoke(*args, **kwargs)
    def __getattr__(self, name):
        return getattr(self._tool, name)

@tool
def _query_warehouse_inventory_tool(warehouse_id):
    """The tool shows warehouse details (name, utilization, status and risk teir) for a particular warehouse id    """
    file_path = "data/inventory_status.json"
    try:
        with open(file_path, "r") as f:
            file_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    results = {}
    if warehouse_id in file_data:
        warehouse_data = file_data[warehouse_id]
        parsed_entry = {
            "warehouse_name": warehouse_data.get("warehouse_name"),
            "current_utilization_pct": warehouse_data.get("current_utilization_pct"),
            "operational_status": warehouse_data.get("operational_status"),
            "risk_tier": warehouse_data.get("risk_tier")
        }
        results.update(parsed_entry)
    else:
        print(f"Warning:'{warehouse_id}' not found.")
    return results   

query_warehouse_inventory_tool = ToolWrapper(_query_warehouse_inventory_tool)


@tool
def _query_route_inventory_tool(disrupted_port_id, file_path="data/route_options.json"):
    """This tool shows all routes available for disrupted port id"

    Args:
        disrupted_port_id (str)
        file_path (str, optional)
    """
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    result = []
    if isinstance(data, dict) and disrupted_port_id in data:
        routes_list = data[disrupted_port_id]
        
        if isinstance(routes_list, list):
            result = routes_list
    return result

query_route_inventory_tool = ToolWrapper(_query_route_inventory_tool)
    
@tool
def _get_alternative_routes_tool(disrupted_port_id):
    """This tool return the routes avaiable for disrupted port id"""
    return query_route_inventory_tool.invoke({"disrupted_port_id": disrupted_port_id})

get_alternative_routes_tool = ToolWrapper(_get_alternative_routes_tool)