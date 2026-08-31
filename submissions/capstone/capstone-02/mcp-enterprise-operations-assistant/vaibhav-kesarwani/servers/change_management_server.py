import json
from fastmcp import FastMCP
from typing import Dict

mcp = FastMCP(name="change_management_server", instructions="This server gives the information about the last changes whcih has been done")


def load_changes():
    CHANGES_PATH = "./data/changes.json"

    try:
        with open(CHANGES_PATH, "r") as f:
            data = json.load(f)

    except Exception as e:
        print(f"Error loading the changes file : {e}")

    return data

         
@mcp.tool(name="list_recent_changes", description="List all the recent changes and return the most recent change first")
def list_recent_changes(limit: int = 10) -> Dict:
    """
    List all the recent changes and return the most recent change first

    Args:
        limit : limit value set 10 by default

    Returns:
        dict: the count of changes and the list of recent changes
    """
    
    data = load_changes()

    changes = sorted(data["changes"], key=lambda x : x["implemented_at"], reverse=True)

    if len(changes) > limit:
        changes = changes[:limit]

    return {
        "count" : len(changes),
        "changes" : changes
    }


@mcp.tool(name="get_change_details", description="Returns the details of specific change details using the change_id")
def get_change_details(change_id: str) -> Dict:
    """
    Returns the details of specific change details using the change_id

    Args:
        change_id: id to find the specific change details

    Returns:
        dict: gives the details of changes using the soecific id with the found boolean
    """

    data = load_changes()

    for change in data["changes"]:
        if change["change_id"].upper() == change_id.upper():
            return {
                "found" : True,
                "change" : change
            }
            
    return {
        "found" : False,
        "message" : "No change id found"
    }


@mcp.tool(name="", description="")
def get_changes_for_service(service_name: str):
    data = load_changes()
    changes = []

    for change in data["changes"]:
        if change["service_name"].lower() == service_name.lower():
            changes.append(change)

    return {
        "service_name" : service_name,
        "count" : len(changes),
        "changes" : changes
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")