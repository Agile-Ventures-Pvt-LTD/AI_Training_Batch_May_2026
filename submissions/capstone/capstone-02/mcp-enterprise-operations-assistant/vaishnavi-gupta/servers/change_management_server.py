import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("Enterprise Operations Server")



@mcp.tool()
def list_recent_changes(limit: int) -> dict:

    """
    Return recent change record.
    """
    api_key = os.getenv("GROQ_API_KEY")
    data_source = "data/changes.db"
    
    return{
        "count": 5,
        "changes": [
            {
                "change_id": data_source["change_id"],
                "service_name": data_source["service_name"],
                "change_type": data_source["change_type"],
                "status": data_source["status"],
                "risk": data_source["risk"],
                "implemented_at": data_source["implemented_at"]
            }
        ]    
    }
@mcp.tool()
def get_change_details(change_id: str) -> dict:

    """
    Return details of a specific change.
    """
    
    api_key = os.getenv("GROQ_API_KEY")
    data_source = "data/changes.db"

    return{
        "found": True,
        "change":{
            "change_id": data_source["change_id"],
            "service_name": data_source["service_name"],
            "change_type": data_source["change_type"],
            "status": data_source["status"],
            "risk": data_source["risk"],
            "implemented_at": data_source["implemented_at"],
            "implemented_by": data_source["implemented_by"],
            "summary": data_source["summary"],
            "rollback_available": True
        }
    }


@mcp.tool()
def get_changes_for_service(service_name: str) -> dict:
    """
    Find recent changes for a service.
    """ 
    api_key = os.getenv("GROQ_API_KEY")
    data_source = "data/changes.db"

    return{
        "service_name": data_source["change_id"],
        "count": data_source["change_id"],
        "changes":[
            {
                "change_id": data_source["change_id"],
                "change_type": data_source["change_type"],
                "risk": data_source["risk"],
                "implemented_at": data_source["implemented_at"],
                "summary": data_source["summary"],
                "rollback_available": data_source["rollback_available"]
            }
        ]
    }    


if __name__ == "__main__":
    mcp.run(transport="stdio")