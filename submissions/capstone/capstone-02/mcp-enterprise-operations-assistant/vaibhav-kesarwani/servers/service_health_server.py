import json
from fastmcp import FastMCP
from typing import Dict, Optional

mcp = FastMCP(name="service_health_server", instructions="This server will provide the services health information and incident.")


def load_service_health() -> Dict:
    SERVICE_HEALTH_PATH = "./data/service_health.json"

    try:
        with open(SERVICE_HEALTH_PATH, "r") as f:
            data = json.load(f)

    except Exception as e:
        print(f"Error loading the service health file : {e}")

    return data


@mcp.tool(name="list_services", description="List down all the services inside the service health json file")
def list_services() -> Dict:
    """
    List down all the services and their current health status.

    Returns:
        dict: The count of services and the list of services with there current health 
    """

    data = load_service_health()
    
    services = data["services"]

    return {
        "count" : len(services),
        "services" : services
    }


@mcp.tool(name="get_service_health", description="Gives the detailed health information for one servie.")
def get_service_health(service_name: str) -> Dict:
    """
    Give the detailed health information for one service.

    Args:
        service_name: name of the service to serach the health inforamtion

    Returns:
        dict: health information of the asked service
    """

    data = load_service_health()

    for s_name in data["services"]:
        if s_name["service_name"].lower() == service_name.lower():
            service = s_name
            return {
                "found" : True,
                "service" : service
            }
        
    return {
        "found" : False,
        "message" : "Service not found."
    }


@mcp.tool(name="get_active_incidents", description="Returns active operational incidents")
def get_active_incidents(service_name: Optional[str]) -> Dict:
    """
    Returns the active operational incidents according to the service_name if give 
    if not returns the whole list

    Args: 
        service_name (optional) : name of the service which incident you have to find

    Returns:
        dict: the service incidents depends upon the service_name or the whole list 
    """

    data = load_service_health()
    
    if service_name:
        incidents = []
        
        for incident in data["incidents"]:
            if incident["service_name"].lower() == service_name.lower():
                incidents.append(incident)

        return {
            "count" : len(incidents),
            "incidents" : incidents
        }
    
    else:
        return {
            "count" : len(data["incidents"]),
            "incidents" : data["incidents"] 
        }
    

if __name__ == "__main__":
    mcp.run(transport="stdio")