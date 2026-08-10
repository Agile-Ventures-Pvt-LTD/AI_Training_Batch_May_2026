import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("Enterprise Operations Server")


@mcp.tool()
def list_services() -> dict:
    """
    Get current weather.
    """

    api_key = os.getenv("GROQ_API_KEY")
    data_source = "data/service_health.json"

    return {
        "count": 5,
        "services": [
            {
                "service_name": data_source["service_name"],
                "status": data_source["status"],
                "region": data_source["region"]
            }
        ]
        
    }

@mcp.tool()
def get_service_health(service_name: str) -> dict:
    """
    Return detailed health information for one service.
    """

    api_key = os.getenv("GROQ_API_KEY")
    data_source = "data/service_health.json"


    return{
        "found": True,
        "service": {
            "service_name": data_source["service_name"],
            "service_id": data_source["service_id"],
            "status": data_source["status"],
            "region": data_source["region"],
            "error_rate_percent": data_source["error_rate_percent"],
            "average_latency_ms": data_source["average_latency_ms"],
            "cpu_usage_percent": data_source["cpu_usage_percent"],
            "memory_usage_percent": data_source["memory_usage_percent"],
            "last_checked": data_source["last_checked"],
            "active_incident_ids": [
                data_source["active_incident_ids"]
            ]
        },
        "found": False,
        "message": "Service not found."
        } 


@mcp.tool()
def get_active_incident(service_name: str) -> dict:
    """
    Return active operational incidents.
    """

    api_key = os.getenv("GROQ_API_KEY")

    data_source = "data/service_health.json"


    return{
        "count": 1,
        "incidents": [
            {
                "incident_id": data_source["incident_id"],
                "service_name": data_source["service_name"],
                "severity": data_source["severity"],
                "status": data_source["status"],
                "summary": data_source["summary"],                                                                                
                "customer_impact": data_source["customer_impact"],
                "assigned_group": data_source["assigned_group"]
            }

        ]
        if (service_name == "NULL"):
        return all
        
}
         
if __name__ == "__main__":
    mcp.run(transport="stdio")


