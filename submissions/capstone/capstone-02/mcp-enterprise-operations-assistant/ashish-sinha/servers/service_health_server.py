import os
import json
from typing import Dict, List, Any, Optional
from fastmcp import FastMCP
from src.config import SERVICE_HEALTH_JSON_PATH

mcp = FastMCP("Service_Health_MCP_Server")

def load_health_json() -> Dict[str, Any]:
        
    with open(SERVICE_HEALTH_JSON_PATH, "r") as data_file:
        return json.load(data_file)


@mcp.tool
def list_services() -> Dict[str, Any]:
    records = load_health_json()
    extracted_output = []
    for item in records.get("services", []):
        extracted_output.append({
            "service_name": item.get("service_name"),
            "status": item.get("status"),
            "region": item.get("region")
        })
    return {"count": len(extracted_output), "services": extracted_output}

@mcp.tool
def get_service_health(service_name: str) -> Dict[str, Any]:
    records = load_health_json()
    for item in records.get("services", []):
        if item.get("service_name") == service_name:
            return {"found": True, "service": item}
    return {"found": False, "message": "Service not Found"}

@mcp.tool
def get_active_incidents(service_name: Optional[str] = None) -> Dict[str, Any]:
    records = load_health_json()
    extracted_output = []
    for item in records.get("incidents", []):
        if item.get("status") == "ACTIVE":
            if service_name is None or item.get("service_name") == service_name:
                extracted_output.append(item)
    return {"count": len(extracted_output), "incidents": extracted_output}

if __name__ == "__main__":
    mcp.run()
