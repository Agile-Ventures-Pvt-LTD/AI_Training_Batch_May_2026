from langchain_core.tools import tool


@tool
def query_warehouse_inventory_tool(warehouse_id: str):
    """
    Handle an invalid warehouse ID without crashing the application.
    """

    return {
        "warehouse_name": str,
        "current_utilization_pct": int,
        "operational_status": str,
        "risk_tier": str
}


@tool
def get_alternative_routes_tool(disrupter_port_id: str):
    """
    Gives alternative tools when a port is disrupted.
    """

    return {
        "PORT-SEATTLE-02": [
            {
                "route_id": str,
                "alternative_port": str,
                "warehouse_id": str,
                "added_delay_hours": int

            },
            {
                "route_id": str,
                "alternative_port": str,
                "warehouse_id": str,
                "added_delay_hours": int
            },
            {
                "route_id": str,
                "alternative_port": str,
                "warehouse_id": str,
                "added_delay_hours": int

            }
    ]
}

    





