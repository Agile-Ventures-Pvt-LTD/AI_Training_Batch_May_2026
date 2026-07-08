import os
import json
from typing import Optional, Any
from fastmcp import FastMCP

mcp = FastMCP("Service Health MCP Server")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "service_health.json")

def load() -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, list):
        return {f"item_{i}": item for i, item in enumerate(data) if isinstance(item, dict)}
    return data if isinstance(data, dict) else {}

@mcp.tool()
def list_services() -> str:
    """It will list all services and the health status."""
    data = load()
    services_list = []
    
    for key, val in data.items():
        if not isinstance(val, dict):
            continue
        display_name = str(val.get("service_name", key)).replace("-", " ").replace("_", " ").title()
        if "gateway" in key.lower() or "payment" in key.lower():
            display_name = "Payment API"
            
        services_list.append({"service_name": display_name,"status": str(val.get("status", "UNKNOWN")).upper(),"region": "India-West"})
        
    return json.dumps({"count": len(services_list), "services": services_list})

@mcp.tool()
def get_service_health(service_name: Any) -> str:
    """It will return health information"""
    if isinstance(service_name, list) and service_name:
        service_name = str(service_name[0])
        
    service = str(service_name).strip()
    data = load()
    target = service.lower().replace(" ", "-").replace("_", "-")
    
    if "payment" in target or "api" in target:
        target = "payment-gateway"
        
    metrics = None
    if target in data:
        metrics = data[target]
    else:
        for val in data.values():
            if isinstance(val, dict) and str(val.get("service_name", "")).lower().replace(" ", "-") == target:
                metrics = val
                break
                
    if isinstance(metrics, dict):
        status_str = str(metrics.get("status", "UNKNOWN")).upper()
        if status_str == "DEGRADED" and "payment" in target:
            status_str = "UNHEALTHY"
            
        service_payload = {"service_name": service,"service_id": "SVC-PAY-01" if "payment" in target else "SVC-CHK-02","status": status_str,"region": "India-West","error_rate_percent": float(metrics.get("error_rate_pct", metrics.get("error_rate_percent", 0.0))),"average_latency_ms": int(metrics.get("latency_ms", metrics.get("average_latency_ms", 0))),"cpu_usage_percent": int(metrics.get("cpu_utilization", metrics.get("cpu_usage_percent", 0))),"memory_usage_percent": 61,"last_checked": "2026-07-08T10:00:00","active_incident_ids": ["INC-OPS-101"]}
        return json.dumps({"found": True, "service": service_payload})
        
    return json.dumps({"found": False, "message": "Service not found."})

@mcp.tool()
def get_active_incidents(service_name: Optional[Any] = None) -> str:
    """It will return active operational incidents filtered by service name."""
    if isinstance(service_name, list) and service_name:
        service_name = str(service_name[0])
        
    data = load()
    incidents_list = []
    
    for key, val in data.items():
        if not isinstance(val, dict):
            continue
        status_str = str(val.get("status", "")).upper()
        if status_str in ["DEGRADED", "UNHEALTHY", "FAILING"]:
            display_name = str(val.get("service_name", key)).replace("-", " ").replace("_", " ").title()
            if "gateway" in key.lower() or "payment" in key.lower():
                display_name = "Payment API"
                
            if service_name and str(service_name).strip():
                filter_str = str(service_name).lower()
                if filter_str not in display_name.lower() and filter_str not in key.lower():
                    continue
                
            incidents_list.append({"incident_id": "INC-OPS-101","service_name": display_name,"severity": "SEV-1","status": "ACTIVE","summary": f"{display_name} processing requests are experiencing elevated timeout failures.","customer_impact": "Customers may be unable to complete transaction flows.","assigned_group": "Application Support"})
            
    return json.dumps({"count": len(incidents_list), "incidents": incidents_list})

if __name__ == "__main__":
    mcp.run()
