from fastmcp import FastMCP
import os
import json

mcp = FastMCP("Service Health MCP Server")
@mcp.tool
def list_services()-> dict:
    """List enterprise services and current health status."""
    file_path=os.path.join(os.path.dirname(__file__),"..","data","service_health.json")
    try:
        with open(file_path) as f:
            data=json.load(f)
            services=data.get("services")
            return{
                "count":len(services),
                "services":services
            }
    except Exception as e:
        return{
            "Can not find data":{e}
        }
    

@mcp.tool
def get_service_health(service_name: str)-> dict:
    """Return detailed health information for a service."""
    file_path=os.path.join(os.path.dirname(__file__),"..","data","service_health.json")
    try:
        with open(file_path) as f:
            data=json.load(f)
            services=data.get("services")
            for s in services:
                if service_name==s.get("service_name"):
                    return{
                        "found":True,
                        "service":s
                    }
            
            return{
                "found":False,
                "message": "Service not found."
            }
    except Exception as e:
        return{
            "Can not find data":{e}
        }
    

@mcp.tool
def get_active_incidents(service_name:str="all_incident")->dict:
    """This tool is use to get active incidents based on service name"""
    file_path=os.path.join(os.path.dirname(__file__),"..","data","service_health.json")
    try:
        with open(file_path) as f:
            data=json.load(f)
            incidents=data.get("incidents")
            if service_name== "all_incident":
                return{
                "count":len(incidents),
                "incidents":incidents
            }
            incident_list=[]
            for s in incidents:
                if service_name==s.get("service_name"):
                    incident_list.append(s)
            if len(incident_list)>0:
                return{
                    "count":len(incident_list),
                    "incidents":incident_list
                    }
            return{
                    "Message":"Provide a valid service name"
                    }
            
    except Exception as e:
        return{
            "can not get data":{e}
        }



if __name__ == "__main__":
    mcp.run()