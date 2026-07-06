from langchain.tools import tool
import json

@tool
def query_warehouse_inventory_tool(warehouse_id:str)->dict:
    """tool used to fetch inventory status of an warehouse"""
    file_path="data/inventory_status.json"
    try:
        with open(file_path) as file:
            data=json.load(file)
            keys_list = list(data.keys())
            for key in keys_list:
                if key==warehouse_id:
                    data2=data.get(warehouse_id)
            
            if isinstance(data2,dict):
                return{
                    "warehouse_name":data2.get("warehouse_name"),
                    "current_utilization_pct":data2.get("current_utilization_pct"),
                    "operational_status":data2.get("operational_status"),
                    "risk_tier":data2.get("risk_tier")
                }
            else:
                return{
                    "Error":"data not found"
                }
    except Exception as e:
        return{
            "Error":"Not able to fetch data."
        }


@tool
def get_alternative_routes_tool(disrupted_port_id:str)->list:
    "Tool used to get alternative paths available"
    file_path="data/route_options.json"
    try:
        with open(file_path) as file:
            data=json.load(file)
            keys_list = list(data.keys())
            for key in keys_list:
                if key==disrupted_port_id:
                    data2=data.get(disrupted_port_id)
            
            if isinstance(data2,list):
                return data2
                
    except Exception as e:
        return [f"not able to get data, Pls provide valid id"]
