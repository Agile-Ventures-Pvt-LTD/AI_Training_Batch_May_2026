from langchain.tools import tool
from db_utils import fetch_one, fetch_all

from langchain.tools import tool

retriever_instance = None


def set_retriever(r):
    global retriever_instance
    retriever_instance = r


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
def get_user_profile(name: str) -> str:
    """Fetch user profile using name from database"""
    row = fetch_one(
        "SELECT user_id, full_name, department, location, account_status, mfa_status FROM users WHERE full_name LIKE ?",
        (f"%{name}%",)
    )

    if not row:
        return "User not found"

    return str({
        "user_id": row[0],
        "name": row[1],
        "department": row[2],
        "location": row[3],
        "account_status": row[4],
        "mfa_status": row[5]
    })


@tool
def get_device_status(user_id: str) -> str:
    """Get device health and performance details for a user"""
    row = fetch_one(
        "SELECT device_id, compliance_status, disk_free_percent, cpu_usage_percent, memory_usage_percent FROM devices WHERE user_id=?",
        (user_id,)
    )

    if not row:
        return "Device not found"

    return str({
        "device_id": row[0],
        "compliance": row[1],
        "disk": row[2],
        "cpu": row[3],
        "memory": row[4]
    })


@tool
def check_known_incidents(service: str) -> str:
    """Check active known incidents for a service"""
    rows = fetch_all(
        "SELECT incident_id, service_name, severity, status, summary FROM known_incidents WHERE service_name LIKE ?",
        (f"%{service}%",)
    )

    return str(rows)


@tool
def run_diagnostic_check(user_id: str) -> str:
    """Run diagnostic checks like VPN, internet, webmail"""
    row = fetch_one(
        "SELECT vpn_reachable, internet_reachable, webmail_reachable FROM diagnostic_snapshots WHERE user_id=?",
        (user_id,)
    )

    if not row:
        return "No diagnostics found"

    return str({
        "vpn": row[0],
        "internet": row[1],
        "webmail": row[2]
    })


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