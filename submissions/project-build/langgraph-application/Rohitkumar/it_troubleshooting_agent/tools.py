from langchain.tools import tool
from db_utils import execute_query
from datetime import datetime, timedelta

@tool
def get_user_profile(
    user_id: str | str = None,
    email: str = None,
    full_name: str = None
):
    """find user by User ID, email,or fullname"""

    query = """
    SELECT *
    FROM user
    WHERE 1=1
    """

    params = []

    if user_id is not None:
        try:
            user_id = str(user_id)
        except (ValueError, TypeError):
            pass
        query += " AND user_id = ?"
        params.append(user_id)

    if email:
        query += " AND email = ?"
        params.append(email)

    

    if full_name:
        query += " AND (full_name) LIKE ?"
        params.append(f"%{full_name}%")

    result = execute_query(query, tuple(params))

    if not result:
        return {"found": False, "user": None}

    row = result[0]

    email_val = row["email"]
   

    masked_email = email_val[:2] + "***" if email_val else None
   
    return {
        "found": True,
        "user": {
            "user_id": row["user_id"],
            "full_name": row["full_name"],
            "department": row["department"],
            "location": row["location"],
            "account_status":row["account_status"],
            "mfa_status" :row["mfa_status"]
           
        }
    }

@tool
def get_device_status(user_id: str ,device_id: str ):
    """get device status info by user ID or device id."""

    query = """
    SELECT *
    FROM devices
    WHERE 1=1
    """

    params = []

    if user_id is not None:
        try:
            user_id = str(user_id)
        except (ValueError, TypeError):
            pass
        query += " AND user_id = ?"
        params.append(user_id)

    if device_id:
        query += " AND device_id = ?"
        params.append(device_id)

    result = execute_query(query, tuple(params))

    if not result:
        return {"found": False, "devices": []}

    devices = []

    for row in result:
        number = str(row["device_id"])
        
        devices.append({
            "user_id":row["user_id"],
            "device_id": row["device_id"],
            "compliance_status": row["compliance_status"],
            "vpn_client_version": row["vpn_client_version"],
            "disk_free_percent": row["disk_free_percent"],
            "cpu_ussage_percent": row["cpu_usage_percent"],
            "memory_usage_percent" : row["memory_usage_percent"]

        })

    return {"found": True, "devices": devices}

@tool
def retrieve_troubleshooting_steps(query: str) -> str:
    """Retrieve troubleshooting steps from knowledge base for a given issue"""
   
    if retriever_instance is None:
        return "Retriever not initialized"
 
    docs = retriever_instance.invoke(query)
 
 
    results = []
    for d in docs:
        results.append({
            "source": d.metadata.get("source_file"),
            "content": d.page_content[:200]
        })
 
    return str(results)

@tool
def check_known_incidents(
    service_name: str,
    status: str 
):
    """check active incidents by service name or region"""

    query = """
    SELECT *
    FROM incidents
    WHERE 1=1
    """

    params = []

    if service_name is not None:
        try:
            service_name = str(service_name)
        except (ValueError, TypeError):
            pass
        query += " AND service_name = ?"
        params.append(service_name)

    if status:
        query += " AND email = ?"
        params.append(status)

    

    

    result = execute_query(query, tuple(params))

    if not result:
        return {"found": False, "user": None}

    row = result[0]
   
    return {
        "incidents": {
            "incident_id": row["incident_id"],
            "service_name": row["service_name"],
            "region": row["region"],
            "severity": row["severity"],
            "status":row["status"],
            "workaround" :row["work_around"]
           
        }
    }

@tool
def get_ticket_details(user_id: str) -> str:
    """Fetch support ticket details for a user"""
    row = fetch_one(
        "SELECT ticket_id, issue_type, priority, status FROM tickets WHERE user_id=?",
        (user_id,)
    )
 
    return str(row)

@tool
def classify_issue_type(query: str) -> str:
    """Classify user query into issue type"""
    q = query.lower()
 
    if "vpn" in q:
        return "VPN"
    elif "outlook" in q or "email" in q:
        return "OUTLOOK_EMAIL"
    elif "slow" in q or "laptop" in q:
        return "LAPTOP_PERFORMANCE"
    elif "password" in q or "login" in q:
        return "PASSWORD_RESET"
    elif "network" in q:
        return "NETWORK_CONNECTIVITY"
    elif "printer" in q:
        return "PRINTER"
    else:
        return "UNKNOWN"

@tool
def run_diagnostic_check(
    user_id:  str,
    device_id: str,
    
):
    """ return diagnostic snapshot for a user and device"""

    

    try:
        if user_id is not None:
            user_id = str(user_id)
    except:
        user_id = None

    try:
        if device_id is not None:
            device_id = str(device_id)
    except:
        device_id = None

    query = """
    SELECT
        user_id,
        vpn_reachable,
        internet_reachable,
        webmail_reachable,
        internal_apps_reachable,
        mfa_push_success
    FROM diagnostic_snapshots
    WHERE 1=1
    """

    params = []

    if user_id is not None:
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            pass
        diagnostic_snapshots= execute_query(
            "SELECT device_id FROM diagnostic_snapshots WHERE device_id = ?",
            (device_id,)
        )

        

        user_ids = [c["device_id"] for c in diagnostic_snapshots]

        placeholders = ",".join(["?"] * len(user_id))
        query += f" AND t.user_id IN ({placeholders})"
        params.extend(user_id)

    if user_id:
        query += " AND user_id = ?"
        params.append(user_id)

    

    if device_id:
        query += " AND device_id = ?"
        params.append(device_id)


    

    result = execute_query(query, tuple(params))

    
    collection = []

    for row in result:
        diagnostic_snapshots = str(row["user_id"])
       
        collection.append({
            "user_id": row["user_id"],
            "device_id": row["device_id"],
            "vpn_reachable": row["vpn_reachable"],
            "internet_reachable": row["internet_reachable"],
            "webmail_reachable": row["webmail_reachable"],
            "internal_apps_reachable": row["internal_apps_reachable"],
            "mfa_push_success":row["mfa_push_success""]
        })

    return {collection}




