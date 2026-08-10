
import json



def query_warehouse_inventory_tool(warehouse_id) -> str:
    with open('data/inventory_status.json', 'r') as file:
            data = dict(json.load(file))
            
    if warehouse_id in data.keys():
        item = dict(data[warehouse_id])

    return item
 

# warehouse_info=query_warehouse_inventory_tool("WH-EAST-101")
# print(warehouse_info)

# {'warehouse_name': 'East Coast Logistics Hub', 'current_utilization_pct': 92, 'operational_status': 'ACTIVE', 'risk_tier': 'NORMAL'}


def get_alternative_routes_tool(disrupted_port_id):
    with open('data/route_options.json', 'r') as file:
            data2 = dict(json.load(file))
            
    if disrupted_port_id in data2.keys():
        item = data2[disrupted_port_id]

    return item


# print(get_alternative_routes_tool("PORT-SEATTLE-02"))



# [{'route_id': 'ROUTE-WEST-01', 'alternative_port': 'Port-West', 'warehouse_id': 'WH-WEST-202', 'added_delay_hours': 48}, {'route_id': 'ROUTE-SOUTH-02', 'alternative_port': 'Port-South', 'warehouse_id': 'WH-SOUTH-303', 'added_delay_hours': 72}, {}]

