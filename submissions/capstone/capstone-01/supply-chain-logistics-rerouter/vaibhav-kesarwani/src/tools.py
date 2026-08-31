import json
from langchain.tools import tool


def query_warehouse_inventory_tool(wearhouse_id: str) -> dict:
    """
    This tool is used to query the wearhouse inventory tool.

    Args:
        wearhouse_id: The wearhouse id which will used to fetch the details of the wearhouse.

    Returns:
        dict: The fetched details of the wearhouse
    """

    INVENTORY_PATH = "./data/inventory_status.json"

    try:
        with open(INVENTORY_PATH, "r") as f:
            data = json.load(f)
    
    except Exception as e:
        print(f"Error loading the inventory file : {e}")

    result = data[wearhouse_id]

    return result


@tool
def get_alternative_routes_tool(port_name = "PORT-SEATTLE-02") -> list:
    """
    This tool is used to fetch all the alternative routes from PORT-SEATTLE-02. 

    Returns:
        list: The list of alternative routes from the PORT-SEATTLE-02
    """

    ALTERNATIVE_ROUTE_PATH = "./data/route_options.json"

    try: 
        with open(ALTERNATIVE_ROUTE_PATH, "r") as f:
            data = json.load(f)

    except Exception as e:
        print(f"Error loading the alternative routes file : {e}")

    result = data[port_name]

    return result


tools = [query_warehouse_inventory_tool, get_alternative_routes_tool]