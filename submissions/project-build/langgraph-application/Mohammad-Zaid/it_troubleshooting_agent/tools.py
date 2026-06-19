from db_utils import run_query
from retrievers import get_vector_store
import json

try:
    retriever = get_vector_store()
except Exception as e:
    print(f"Warning: Vector store not initialized: {e}")
    retriever = None

def retrieve_troubleshooting_steps(query: str):
    """Retrieve troubleshooting steps from knowledge base"""
    if not retriever:
        return "No KB available"
    docs = retriever.invoke(query)
    response = "\n\n".join([f"Source: {doc.metadata.get('source_file', 'unknown')}\n{doc.page_content[:400]}" for doc in docs])
    return response if response else "No matching documents found"


def get_user_profile(user_id: str):
    """Get user profile and device information"""
    query = "SELECT user_id, full_name, email, department, account_status, mfa_status FROM users WHERE user_id = ?"
    return run_query(query, (user_id,))


def get_device_status(user_id: str):
    """Get device status and compliance information"""
    query = """SELECT device_id, device_type, os, compliance_status, 
               vpn_client_version, disk_free_percent, cpu_usage_percent, 
               memory_usage_percent FROM devices WHERE user_id = ?"""
    return run_query(query, (user_id,))


def check_known_incidents():
    """Check for known incidents"""
    query = "SELECT service_name, severity, status, summary, workaround FROM known_incidents WHERE status != 'resolved' LIMIT 5"
    return run_query(query)


def run_diagnostic_check(user_id: str):
    """Run diagnostic check on user's device"""
    query = """SELECT user_id, device_id, vpn_reachable, internet_reachable, 
               webmail_reachable, internal_apps_reachable, mailbox_quota_percent, account_locked, mfa_push_success 
               FROM diagnostic_snapshots WHERE user_id = ? ORDER BY created_at DESC LIMIT 1"""
    return run_query(query, (user_id,))


def get_ticket_details(user_id: str):
    """Get ticket details for user"""
    query = """SELECT ticket_id, issue_type, priority, status, subject, description FROM tickets WHERE user_id = ? ORDER BY created_at DESC LIMIT 3"""
    return run_query(query, (user_id,))


def create_resolution_plan(user_id: str, issue: str):
    """Create resolution plan based on user context and issue"""
    profile = get_user_profile(user_id)
    devices = get_device_status(user_id)
    diagnostics = run_diagnostic_check(user_id)
    steps = retrieve_troubleshooting_steps(issue)
    
    return {
        "user_profile": profile,
        "device_status": devices,
        "diagnostics": diagnostics,
        "troubleshooting_steps": steps,
        "issue": issue
    }
