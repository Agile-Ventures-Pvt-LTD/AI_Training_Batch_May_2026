from fastmcp import FastMCP
from pathlib import Path
import json

mcp = FastMCP("change_management_server")

def load_data():
    file_path = Path("data/changes.json")
    try:
        with open(file_path,"r",encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} contains invalid JSON formatting.")
        return None
    

@mcp.tool()
def list_recent_changes(limit:int =10)-> dict:
    """Return recent change records."""
    data = load_data()
    try:
        changes = data.get("changes",[])
        changes.sort(key=lambda x: x.get("implemented_at", ""), reverse=True)
        recent_changes = changes[:limit]
        return {
            "count": len(changes),
            "chnages":recent_changes
        }
    except Exception as e:
        return {
            "error":f"error {e}"
        }
    

@mcp.tool()
def get_change_details(change_id:str)->dict:
    """Return details of a specific change."""
    data = load_data()
    try:
        for s in data.get("changes",[]):
            if s.get("change_id") == change_id:
                return{
                    "found":"true",
                    "changes":s
                }
            return{
                "found":"false",
                "messages" : "change not found"
            }
    except Exception as e:
        return {
            "error":f"error{e}"
        }

@mcp.tool()
def get_changes_for_service(service_name:str)->dict:
    """Find recent changes for a service."""
    data = load_data()
    try:
        changes = []
        for s in data.get("changes",[]):
            if s.get("service_name") == service_name:
                changes.append(s)
            changes.sort(key=lambda x: x.get("implemented_at", ""), reverse=True)
            return{
                    "service_name":service_name,
                    "count":len(changes),
                    "changes":changes
            }
    except Exception as e:
        return {
            "error":f"error{e}"
        }
    
mcp.run()