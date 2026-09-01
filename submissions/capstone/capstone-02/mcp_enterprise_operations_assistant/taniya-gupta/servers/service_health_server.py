import json 
from pathlib import Path
from fastmcp import FastMCP

mcp=FastMCP("service-health")

def get_data():
    return Path(__file__).resolve().parent.parent / "data" / "service_health.json"

@mcp.tool
def list_services():
    """List all services and their current health status"""
    try:
        with open (get_data(), "r") as f:
            data=json.load(f)
        services=[]
        for s in data.get("services"):
            services.append({
                "service_name" : s.get("service_name"),
                "status" : s.get("status"),
                "region": s.get("region"),
                }
            )
        return {
            "count" : len(services),
            "services" : services
        }
    except Exception as e:
        return {"error" : str(e)}

@mcp.tool
def get_service_health(service_name:str=""):
    """Return detailed health information for one service, service_name is required"""
    if not service_name:
        return {
            "found" : False,
            "msg" : "Enter service name"
        }
    try:
        with open (get_data(), "r") as f:
            data=json.load(f)
        for s in data.get("services"):
            if s.get("service_name")==service_name:
                return {
                    "found" : True,
                    "service" : s
                }
            
        return {
            "found" : False,
            "msg" : "Could not find service"
                }
    except Exception as e:
        return {"error" : str(e)}
    
@mcp.tool
def get_active_incidents(service_name):
    """Return active operational incidents, the tool filters by services"""
    try:
        with open (get_data(), "r") as f:
            data=json.load(f)
        active_incidents=[]
        for i in data.get("incidents"):
            if i.get("status")=="ACTIVE":
                if not service_name or i.get("service_name")==service_name:
                    active_incidents.append(i)
        return {
            "count" : len(active_incidents),
            "incidents" : active_incidents
        }
    except Exception as e:
        return {"error" : str(e)}
    

if __name__=="__main__":
    mcp.run()