import sqlite3
from pathlib import Path
from config import DB_PATH

def get_db_connection():
    db_file = Path(DB_PATH)
    if not db_file.exists():
        raise FileNotFoundError(f"Database not found: {DB_PATH}")
    conn = sqlite3.connect(str(db_file))
    conn.row_factory = sqlite3.Row
    return conn


def get_user_profile(user_identifier):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT user_id, full_name, department, location, account_status, mfa_status 
        FROM users WHERE user_id = ? OR full_name LIKE ?
        """
        cursor.execute(query, (user_identifier, f"%{user_identifier}%"))
        row = cursor.fetchone()
        if row:
            return {
                "user_id": row["user_id"],
                "full_name": row["full_name"],
                "department": row["department"],
                "location": row["location"],
                "account_status": row["account_status"],
                "mfa_status": row["mfa_status"]
            }
        return None
    finally:
        conn.close()

def get_device_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        SELECT device_id, user_id, compliance_status, vpn_client_version, disk_free_percent, cpu_usage_percent, memory_usage_percent 
        FROM devices WHERE user_id = ?
        """
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                "device_id": row["device_id"],
                "user_id": row["user_id"],
                "compliance_status": row["compliance_status"],
                "vpn_client_version": row["vpn_client_version"],
                "disk_free_percent": row["disk_free_percent"],
                "cpu_usage_percent": row["cpu_usage_percent"],
                "memory_usage_percent": row["memory_usage_percent"]
            }
        return None
    finally:
        conn.close()


def get_ticket_details(ticket_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
        SELECT ticket_id, user_id, issue_type, priority, status, subject, assigned_group 
        FROM tickets WHERE ticket_id = ?
        """
        cursor.execute(query, (ticket_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                "ticket_id": row["ticket_id"],
                "user_id": row["user_id"],
                "issue_type": row["issue_type"],
                "priority": row["priority"],
                "status": row["status"],
                "subject": row["subject"],
                "assigned_group": row["assigned_group"]
            }
        return None
    finally:
        conn.close()


def check_known_incidents(service_name=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if service_name:
            query = """
            SELECT incident_id, service_name, region, severity, status, summary, workaround 
            FROM known_incidents 
            WHERE service_name LIKE ? AND status IN ('ACTIVE', 'INVESTIGATING')
            """
            cursor.execute(query, (f"%{service_name}%",))
        else:
            query = """
            SELECT incident_id, service_name, region, severity, status, summary, workaround 
            FROM known_incidents WHERE status IN ('ACTIVE', 'INVESTIGATING')
            """
            cursor.execute(query)
        
        rows = cursor.fetchall()
        incidents = []
        
        for row in rows:
            incidents.append({
                "incident_id": row["incident_id"],
                "service_name": row["service_name"],
                "region": row["region"],
                "severity": row["severity"],
                "status": row["status"],
                "summary": row["summary"],
                "workaround": row["workaround"]
            })
        return incidents
    finally:
        conn.close()

def get_diagnostic_snapshot(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT user_id, vpn_reachable, internet_reachable, webmail_reachable, internal_apps_reachable, account_locked, mfa_push_success 
        FROM diagnostic_snapshots WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 1
        """
        cursor.execute(query, (user_id,))
        row = cursor.fetchone()
        if row:
            return {
                "user_id": row["user_id"],
                "vpn_reachable": bool(row["vpn_reachable"]),
                "internet_reachable": bool(row["internet_reachable"]),
                "webmail_reachable": bool(row["webmail_reachable"]),
                "internal_apps_reachable": bool(row["internal_apps_reachable"]),
                "account_locked": bool(row["account_locked"]),
                "mfa_push_success": bool(row["mfa_push_success"])
            }
        return None
    finally:
        conn.close()
