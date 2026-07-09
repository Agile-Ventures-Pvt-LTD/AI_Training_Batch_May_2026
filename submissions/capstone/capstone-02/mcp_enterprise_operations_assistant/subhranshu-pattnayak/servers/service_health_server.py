# Import required libraries
import os
from typing import Any, Optional
from fastmcp import FastMCP
try:
    from confserver import read_json, SERVICE_HEALTH_PATH
except ImportError:
    from .confserver import read_json, SERVICE_HEALTH_PATH


mcp = FastMCP("Service Health MCP Server")



# Tool: list_services

@mcp.tool()
async def list_services() -> dict[str, Any] :
    """List all services and their current health status.

    Returns:
        dict[str, Any]: Returns service count and a list of dictionaries of services, region and health status.
    """
    try:
        result = read_json(SERVICE_HEALTH_PATH)
        services = result['services']
        count = len(services)
        keys = ['service_name', 'status', 'region']
        services = [{key: service[key] for key in keys if key in service.keys()} for service in services]
        
        return {
            'count': count,
            'services': services
        }
    except ValueError as v:
        return {'count': 0, 'message': f"VALUE ERROR: {str(v)}"}
    except KeyError as k:
        return {'count': 0, 'message': f"KEY ERROR: {str(k)}"}
    except Exception as e:
        return {'count': 0, 'message': f"ERROR: {str(e)}"}



# Tool: get_service_health

@mcp.tool()
async def get_service_health(service_name: str) -> dict[str, Any] :
    """Fetches detailed health information for one service.

    Args:
        service_name (str): Service name of the target service.

    Returns:
        dict[str, Any]: Return detailed health information.
    """
    try:
        result = read_json(SERVICE_HEALTH_PATH)
        services = result['services']
        target = None
        for service in services:
            if service['service_name'] == service_name:
                target = service
                break
        if not target:
            return {
                'found': False,
                'message': "Service not found."
            }
        return {
            'found': True,
            'service': target
        }
    except Exception:
        return {
            'found': False,
            'message': "Service not found."
        }




# Tool: get_active_incidents

@mcp.tool()
async def get_active_incidents(service_name: Optional[str] = None) -> dict[str, Any] :
    """Fetches active operational incidents and optionally filters incidents by service.

    Args:
        service_name (Optional[str]): Service name to a service, optional to provide. Default to None.

    Returns:
        dict[str, Any]: Returns all active incidents when no service name provided. Returns incidents corresponding to a service when the service name is provided.
    """
    try:
        result = read_json(SERVICE_HEALTH_PATH)
        incidents = result['incidents']
        if service_name:
            inc = [incident for incident in incidents if incident['service_name'] == service_name]
            return {
                'count': len(inc),
                'incidents': inc
            }
        return {
            'count': len(incidents),
            'incidents': incidents
        }
    except ValueError as v:
        return {'count': 0, 'message': f"VALUE ERROR: {str(v)}"}
    except KeyError as k:
        return {'count': 0, 'message': f"KEY ERROR: {str(k)}"}
    except Exception as e:
        return {'count': 0, 'message': f"ERROR: {str(e)}"}



if __name__ == "__main__":
    mcp.run(transport="stdio")