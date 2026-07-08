import json
from pathlib import Path
from fastmcp import FastMCP

mcp=FastMCP("change-management")

def get_data():
    return Path(__file__).resolve().parent.parent / "data" / "changes.json"

@mcp.tool
def list_recent_changes(limit:int=10):
    """List recent change records sorted by implemented_at in descending order"""
    try:
        with open (get_data(), "r") as f:
            data=json.load(f)
        changes=data.get("changes")
        sorted_changes= sorted(changes,key=lambda x :x.get("implemented_at"),reverse=True)
        limited=sorted_changes[:limit]
        result=[]
        for chg in limited:
            result.append({
                "change_id" : chg.get("change_id"),
                "service_name":chg.get("service_name"),
                "change_type":chg.get("change_type"),
                "status":chg.get("status"),
                "risk": chg.get("risk"),
                "implemented_at":chg.get("implemented_at")
            })
        return {
            "count" : len(result),
            "changes" : result
        }
    except Exception as e:
        return {"error" : str(e)}
    
@mcp.tool
def get_change_details(change_id:str=""):
    """Return details of a specific change"""
    if not change_id:
        return {
            "found" : False,
            "msg" : "Enter change id"
        }
    try:
        with open (get_data(), "r") as f:
            data=json.load(f)
        for chg in data.get("changes"):
            if chg.get("change_id")==change_id:
                return {
                    "found" :True,
                    "change": chg
                }
        return {
                "found" : False,
                "msg" : "Could not find change"
            }
    except Exception as e:
        return {"error" : str(e)}
    
@mcp.tool
def get_changes_for_service(service_name: str) -> dict:
    """Get recent changes for a service, it is sorted by implemented_at by descending order"""
    if not service_name:
        return {
            "found" : False,
            "msg" : "Enter service name"
        }
    try:
        with open (get_data(), "r") as f:
            data=json.load(f)
        changes=[]
        for chg in data.get("changes"):
            if chg.get("service_name")==service_name:
                changes.append(chg)
        sorted_changes= sorted(changes,key=lambda x :x.get("implemented_at"),reverse=True)
        result=[]
        for chg in sorted_changes:
            result.append({
                "change_id" : chg.get("change_id"),
                "service_name":chg.get("service_name"),
                "change_type":chg.get("change_type"),
                "status":chg.get("status"),
                "risk": chg.get("risk"),
                "implemented_at":chg.get("implemented_at"),
                "summary":chg.get("summary"),
                "rollback_available":chg.get("rollback_available")
            })
        return {
            "service_name": service_name,
            "count" : len(result),
            "changes" : result
        }
    except Exception as e:
        return {"error" : str(e)}

@mcp.tool
def get_changes_for_services(service_name: str) -> dict:
    """Get recent changes for a service, it is sorted by implemented_at by descending order"""
    return get_changes_for_service(service_name)
    

if __name__=="__main__":
    mcp.run()