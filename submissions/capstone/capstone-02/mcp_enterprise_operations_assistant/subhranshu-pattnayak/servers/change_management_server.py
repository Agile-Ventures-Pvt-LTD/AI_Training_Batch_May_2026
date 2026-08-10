# Import required libraries
import os
from fastmcp import FastMCP
from datetime import datetime
from typing import Any, Optional
try:
    from confserver import read_json, CHANGES_MANAGEMENT_PATH
except ImportError:
    from .confserver import read_json, CHANGES_MANAGEMENT_PATH

mcp = FastMCP("Change Management MCP Server")


# Tool: list_recent_changes

@mcp.tool()
async def list_recent_changes(limit: Optional[int] = 10) -> dict[str, Any] :
    """Fetch recent change records with most recent first.

    Args:
        limit (Optional[str], optional): Maximum number of changes to be returned. Defaults to 10.

    Returns:
        dict[str, Any]: Returns list of changes.
    """
    try:
        
        result = read_json(CHANGES_MANAGEMENT_PATH)
        recent_changes = result.get("changes", "")
        
        recent_changes.sort(key=lambda x: datetime.fromisoformat(x.get("implemented_at", "")))
        
        changes = recent_changes[:limit]
        
        return {
            'count': len(changes),
            'changes': changes
        }
    
    except ValueError as v:
        return {'count': 0, 'message': f"VALUE ERROR: {str(v)}"}
    except Exception as e:
        return {'count': 0, 'message': f"ERROR: {str(e)}"}





# Tool: get_change_details

@mcp.tool()
async def get_change_details(change_id: str) -> dict[str, Any] :
    """ Fetches details of a specific change.

    Args:
        change_id (str): Id for a specific change.

    Returns:
        dict[str, Any]: _description_
    """
    try:
        result = read_json(CHANGES_MANAGEMENT_PATH)
        changes = result['changes']
        
        for change in changes:
            if change['change_id'] == change_id:
                return {
                    'found': True,
                    'change': change
                }
    except Exception:
        return {
            'found': False,
            'message': "Change not found."
        }






# Tool: get_changes_for_service

@mcp.tool()
async def get_changes_for_service(service_name: str) -> dict[str, Any] :
    """Find recent changes for a service.

    Args:
        service_name (str): Service name of the change being sought.

    Returns:
        dict[str, Any]: Returns all changes corresponding to a given service name.
    """
    try:
        result = read_json(CHANGES_MANAGEMENT_PATH)
        changes = result['changes']
        changes = list(filter(lambda x: x.get('service_name', '') == service_name, changes))
        return {
            'service_name': service_name,
            'count': len(changes),
            'changes': changes
        }
    except ValueError as v:
        return {'count': 0, 'message': f"VALUE ERROR: {str(v)}"}
    except KeyError as k:
        return {'count': 0, 'message': f"KEY ERROR: {str(k)}"}
    except Exception as e:
        return {'count': 0, 'message': f"ERROR: {str(e)}"}



if __name__ == "__main__":
    mcp.run(transport="stdio")
