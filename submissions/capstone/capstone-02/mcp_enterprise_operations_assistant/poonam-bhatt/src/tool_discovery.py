import os
import json
import sqlite3
from typing import Dict, Any, List, Optional

# Helper function to get database paths
def get_service_health_path() -> str:
    return os.path.join("data", "service_health.json")

def get_tickets_db_path() -> str:
    return os.path.join("data", "tickets.db")

def get_changes_path() -> str:
    return os.path.join("data", "changes.json")

# Tool - 01 list_services
def list_services() -> dict:
    """List all services and their current health status."""
    path = get_service_health_path()
    if not os.path.exists(path):
        return {"error": "Service health data file not found."}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        services = data.get("services", [])
        result = []
        for s in services:
            result.append({
                "service_name": s.get("service_name"),
                "status": s.get("status"),
                "region": s.get("region")
            })
        return {"count": len(result), "services": result}
    except Exception as e:
        return {"error": str(e)}

# Tool - 02 get_service_health
def get_service_health(service_name: str) -> dict:
    """Return detailed health information for one service."""
    path = get_service_health_path()
    if not os.path.exists(path):
        return {"found": False, "message": "Service health data file not found."}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        services = data.get("services", [])
        for s in services:
            if s.get("service_name") == service_name:
                return {"found": True, "service": s}
        return {"found": False, "message": "Service not found."}
    except Exception as e:
        return {"found": False, "message": str(e)}

# Tool - 03 get_active_incidents
def get_active_incidents(service_name: str = None) -> dict:
    """Return active operational incidents, optionally filtered by service name."""
    path = get_service_health_path()
    if not os.path.exists(path):
        return {"error": "Service health data file not found."}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        incidents = data.get("incidents", [])
        active_incidents = []
        for inc in incidents:
            if inc.get("status") == "ACTIVE":
                if service_name is None or inc.get("service_name") == service_name:
                    active_incidents.append(inc)
        return {"count": len(active_incidents), "incidents": active_incidents}
    except Exception as e:
        return {"error": str(e)}

# Tool - 04 search_tickets
def search_tickets(service_name: str = None, priority: str = None, status: str = None, limit: int = 50) -> dict:
    """Search support tickets using predefined filters."""
    db_path = get_tickets_db_path()
    if not os.path.exists(db_path):
        return {"error": "Tickets database not found."}
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT ticket_id, service_name, priority, status, subject, customer_impact, assigned_group FROM tickets"
        conditions = []
        params = []
        
        if service_name:
            conditions.append("service_name = ?")
            params.append(service_name)
        if priority:
            conditions.append("priority = ?")
            params.append(priority)
        if status:
            conditions.append("status = ?")
            params.append(status)
            
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        tickets = []
        for r in rows:
            tickets.append({
                "ticket_id": r["ticket_id"],
                "service_name": r["service_name"],
                "priority": r["priority"],
                "status": r["status"],
                "subject": r["subject"],
                "customer_impact": r["customer_impact"],
                "assigned_group": r["assigned_group"]
            })
            
        conn.close()
        return {"count": len(tickets), "tickets": tickets}
    except Exception as e:
        return {"error": str(e)}

# Tool - 05 get_ticket_details
def get_ticket_details(ticket_id: str) -> dict:
    """Get full details of one support ticket."""
    db_path = get_tickets_db_path()
    if not os.path.exists(db_path):
        return {"found": False, "message": "Tickets database not found."}
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT ticket_id, service_name, priority, status, subject, description, created_at, customer_impact, assigned_group FROM tickets WHERE ticket_id = ?", (ticket_id,))
        row = cursor.fetchone()
        
        if row:
            ticket = {
                "ticket_id": row["ticket_id"],
                "service_name": row["service_name"],
                "priority": row["priority"],
                "status": row["status"],
                "subject": row["subject"],
                "description": row["description"],
                "created_at": row["created_at"],
                "customer_impact": row["customer_impact"],
                "assigned_group": row["assigned_group"]
            }
            conn.close()
            return {"found": True, "ticket": ticket}
        else:
            conn.close()
            return {"found": False, "message": "Ticket not found."}
    except Exception as e:
        return {"found": False, "message": str(e)}

# Tool - 06 get_high_priority_tickets
def get_high_priority_tickets(service_name: str = None) -> dict:
    """Return open P1 and P2 tickets, optionally filtered by service name."""
    db_path = get_tickets_db_path()
    if not os.path.exists(db_path):
        return {"error": "Tickets database not found."}
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT ticket_id, service_name, priority, status, subject FROM tickets WHERE status = 'OPEN' AND (priority = 'P1' OR priority = 'P2')"
        params = []
        if service_name:
            query += " AND service_name = ?"
            params.append(service_name)
            
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        tickets = []
        for r in rows:
            tickets.append({
                "ticket_id": r["ticket_id"],
                "service_name": r["service_name"],
                "priority": r["priority"],
                "status": r["status"],
                "subject": r["subject"]
            })
            
        conn.close()
        return {"count": len(tickets), "tickets": tickets}
    except Exception as e:
        return {"error": str(e)}

# Tool - 07 list_recent_changes
def list_recent_changes(limit: int = 10) -> dict:
    """Return recent change records, ordered from most recent to oldest."""
    path = get_changes_path()
    if not os.path.exists(path):
        return {"error": "Changes data file not found."}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        changes = data.get("changes", [])
        
        # Sort by implemented_at descending
        sorted_changes = sorted(changes, key=lambda x: x.get("implemented_at", ""), reverse=True)
        sliced_changes = sorted_changes[:limit]
        
        result = []
        for c in sliced_changes:
            result.append({
                "change_id": c.get("change_id"),
                "service_name": c.get("service_name"),
                "change_type": c.get("change_type"),
                "status": c.get("status"),
                "risk": c.get("risk"),
                "implemented_at": c.get("implemented_at")
            })
        return {"count": len(result), "changes": result}
    except Exception as e:
        return {"error": str(e)}

# Tool - 08 get_change_details
def get_change_details(change_id: str) -> dict:
    """Return details of a specific change."""
    path = get_changes_path()
    if not os.path.exists(path):
        return {"found": False, "message": "Changes data file not found."}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        changes = data.get("changes", [])
        for c in changes:
            if c.get("change_id") == change_id:
                return {"found": True, "change": c}
        return {"found": False, "message": "Change not found."}
    except Exception as e:
        return {"found": False, "message": str(e)}

# Tool - 09 get_changes_for_service
def get_changes_for_service(service_name: str) -> dict:
    """Find recent changes for a service, ordered from most recent to oldest."""
    path = get_changes_path()
    if not os.path.exists(path):
        return {"error": "Changes data file not found."}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        changes = data.get("changes", [])
        
        service_changes = [c for c in changes if c.get("service_name") == service_name]
        sorted_changes = sorted(service_changes, key=lambda x: x.get("implemented_at", ""), reverse=True)
        
        result = []
        for c in sorted_changes:
            result.append({
                "change_id": c.get("change_id"),
                "change_type": c.get("change_type"),
                "risk": c.get("risk"),
                "implemented_at": c.get("implemented_at"),
                "summary": c.get("summary"),
                "rollback_available": c.get("rollback_available")
            })
        return {"service_name": service_name, "count": len(result), "changes": result}
    except Exception as e:
        return {"error": str(e)}