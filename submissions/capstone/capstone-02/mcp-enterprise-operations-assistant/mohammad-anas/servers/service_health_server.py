from fastmcp import FastMCP
from typing import Dict,Any
from pathlib import Path
import json

mcp = FastMCP("service_health_server")

@mcp.tool()
def list_services()->Dict[list,Any]:
    """List all services and their current health status"""
    file_path = Path("data/service_health.json")
    try:
        with open(file_path,"r",encoding="utf-8") as file:
            data = json.load(file)
        original_services = data.get("services",[])
        filtered_service = []
        for s in original_services:
            filtered_service.append({
                "service_name" : s.get("service_name"),
                "status":s.get("status"),
                "region":s.get("region")
            })
        return {
            "count" : len(original_services),
            "services" : filtered_service
        } 
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} contains invalid JSON formatting.")
        return None

@mcp.tool()
def get_service_health(service_name:str)->Dict[str,Any]:
    """Return detailed health information for one service."""
    file_path = Path("data/service_health.json")
    try:
        with open(file_path,"r",encoding="utf-8") as file:
            data = json.load(file)
        original_services = data.get("services",[])
        for s in original_services:
            if s.get("service_name") == service_name:
                return {
                    "found" : "true",
                    "service_name" : s.get("service_name"),
                    "service_id":s.get("service_id"),
                    "status":s.get("status"),
                    "region":s.get("region"),
                    "error_rate_percent":s.get("error_rate_percent"),
                    "average_latency_ms":s.get("average_latency_ms"),
                    "cpu_usage_percent":s.get("cpu_usage_percent"),
                    "memory_usage_percent":s.get("memory_usage_percent"),
                    "last_checked" :s.get("last_checked"),
                    "active_incident_ids":s.get("active_incident_ids")
            }
        return f"service health with this service_name --{service_name}-- is not available"
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} contains invalid JSON formatting.")
        return None
    

@mcp.tool()
def get_active_incidents(service_name:str)->Dict[str,Any]:
    """Return active operational incidents."""
    file_path = Path("data/service_health.json")
    try:
        with open(file_path,"r",encoding="utf-8") as file:
            data = json.load(file)
        original_services = data.get("incidents",[])
        incidents = []
        for s in original_services:
            if s.get("status") == "ACTIVE":
                if service_name is None or s.get("service_name") == service_name:
                    incidents.append(s)
                    return {
                        "count":len(incidents),
                        "incidents":incidents
                    }
            else:
                return original_services
        return f"service health with this service_name --{service_name}-- is not available"
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: The file at {file_path} contains invalid JSON formatting.")
        return None
    
mcp.run()