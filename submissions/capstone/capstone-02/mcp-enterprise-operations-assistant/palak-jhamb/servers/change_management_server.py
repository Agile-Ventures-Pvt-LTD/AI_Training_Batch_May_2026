from fastmcp import FastMCP
import os
import json

mcp = FastMCP("Change Management MCP Server")
@mcp.tool
def list_recent_changes(limit=10)-> dict:
    """Return all recent change records."""
    file_path=os.path.join(os.path.dirname(__file__),"..","data","changes.json")
    try:
        with open(file_path) as f:
            data=json.load(f)
            changes=data.get("changes")
            sorted_list = sorted(changes, key=lambda item: item['implemented_at'],reverse=True)
            return{
                "count":len(sorted_list),
                "changes":sorted_list
            }
    except Exception as e:
        return{
            "Can not find data":{e}
        }
    

@mcp.tool
def get_change_details(change_id: str)-> dict:
    """Return details of a specific recent change by id."""
    file_path=os.path.join(os.path.dirname(__file__),"..","data","changes.json")
    try:
        with open(file_path) as f:
            data=json.load(f)
            changes=data.get("changes")
            for s in changes:
                if change_id==s.get("change_id"):
                    return{
                        "found":True,
                        "change":s
                    }
            
            return{
                "found":False,
                "message": "change_id not found."
            }
    except Exception as e:
        return{
            "Can not find data":{e}
        }
    

@mcp.tool
def get_changes_for_service(service_name:str)->dict:
    """This tool is use to Find recent changes for a service bsed on its service name"""
    file_path=os.path.join(os.path.dirname(__file__),"..","data","changes.json")
    try:
        with open(file_path) as f:
            data=json.load(f)
            changes=data.get("changes")
            changes_list=[]
            for s in changes:
                if service_name==s.get("service_name"):
                    changes_list.append(s)
            if len(changes_list)>0:
                return{
                    "service_name":service_name,
                    "count":len(changes_list),
                    "changes":changes_list
                }
            return{
                "service_name":service_name,
                "count":len(changes_list),
                "changes":changes_list
            }   
    except Exception as e:
        return{
            "can not get data":{e}
        }


if __name__ == "__main__":
    mcp.run()