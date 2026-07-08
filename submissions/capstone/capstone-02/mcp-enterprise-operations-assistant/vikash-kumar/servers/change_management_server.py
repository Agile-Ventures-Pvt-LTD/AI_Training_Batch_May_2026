import os
import json
from typing import Optional, Any
from fastmcp import FastMCP

mcp = FastMCP("Change Management Server")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "changes.json")

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        return data.get("changes", data.get("records", [data]))
    return data if isinstance(data, list) else []

def clean_row(m: dict) -> dict:
    return {"change_id": m.get("change_id", "CHG-2001"),"service_name": m.get("service_name", "Payment API"),"change_type": m.get("change_type", "APPLICATION_RELEASE"),"status": m.get("status", "COMPLETED"),"risk": str(m.get("risk_level", m.get("risk", "LOW"))).upper(),"implemented_at": m.get("scheduled_time", m.get("implemented_at", "")),"implemented_by": m.get("implemented_by", "Payments Engineering"),"summary": m.get("description", m.get("summary", "")),"rollback_available": m.get("rollback_available", True)}

@mcp.tool()
def list_recent_changes(limit: int = 10) -> str:
    """Return recent change records."""
    items = load_data()
    result = [clean_row(m) for m in items if isinstance(m, dict)]
    result.sort(key=lambda x: x["implemented_at"], reverse=True)
    result = result[:limit]
    return json.dumps({"count": len(result), "changes": result})

@mcp.tool()
def get_change_details(change_id: Any) -> str:
    """Return details of a specific change."""
    if isinstance(change_id, list) and change_id:
        change_id = str(change_id[0])
        
    change_str = str(change_id).strip()
    items = load_data()
    
    for m in items:
        if isinstance(m, dict) and str(m.get("change_id")).strip() == change_str:
            return json.dumps({"found": True, "change": clean_row(m)})
    return json.dumps({"found": False, "message": "Change not found."})

@mcp.tool()
def get_changes_for_service(service_name: Any) -> str:
    """Find recent changes for a service."""
    if isinstance(service_name, list) and service_name:
        service_name = str(service_name[0])
        
    service = str(service_name).strip()
    items = load_data()
    result = []
    target = service.lower().replace(" ", "-").replace("_", "-")
    
    for m in items:
        if isinstance(m, dict):
            srv = str(m.get("service_name", "")).lower().replace(" ", "-").replace("_", "-")
            if srv == target or (target in ["payment-api", "payment-gateway"] and srv in ["payment-api", "payment-gateway"]):
                cleaned = clean_row(m)
                result.append({"change_id": cleaned["change_id"],"change_type": cleaned["change_type"],"risk": cleaned["risk"],"implemented_at": cleaned["implemented_at"],"summary": cleaned["summary"],"rollback_available": cleaned["rollback_available"]})
                
    result.sort(key=lambda x: x["implemented_at"], reverse=True)
    return json.dumps({"service_name": service,"count": len(result),"changes": result})

if __name__ == "__main__":
    mcp.run()
