from langchain_core.tools import tool

from db_utils import (
    fetch_one,
    fetch_all
)


@tool
def classify_issue_type(query: str):
    """
    Classify IT issue type.
    """

    query = query.lower()

    if "vpn" in query:
        return {
            "issue_type": "VPN",
            "confidence": "HIGH"
        }

    elif "email" in query or "outlook" in query:
        return {
            "issue_type": "OUTLOOK_EMAIL",
            "confidence": "HIGH"
        }

    elif "password" in query or "login" in query:
        return {
            "issue_type": "PASSWORD_RESET",
            "confidence": "HIGH"
        }

    elif "laptop" in query or "slow" in query:
        return {
            "issue_type": "LAPTOP_PERFORMANCE",
            "confidence": "HIGH"
        }

    elif "printer" in query:
        return {
            "issue_type": "PRINTER",
            "confidence": "HIGH"
        }

    elif "network" in query:
        return {
            "issue_type": "NETWORK_CONNECTIVITY",
            "confidence": "HIGH"
        }

    return {
        "issue_type": "UNKNOWN",
        "confidence": "LOW"
    }


@tool
def retrieve_troubleshooting_steps(
    issue_type: str,
    query: str
):
    """
    Retrieve troubleshooting guidance.
    """

    return {
        "issue_type": issue_type,
        "query": query,
        "chunks": []
    }


@tool
def get_user_profile(name: str):
    """
    Get user profile.
    """

    return fetch_one(
        """
        SELECT *
        FROM users
        WHERE full_name = ?
        """,
        (name,)
    )


@tool
def get_device_status(user_id: str):
    """
    Get device status.
    """

    return fetch_one(
        """
        SELECT *
        FROM devices
        WHERE user_id = ?
        """,
        (user_id,)
    )


@tool
def check_known_incidents():
    """
    Get active incidents.
    """

    return fetch_all(
        """
        SELECT *
        FROM known_incidents
        """
    )


@tool
def run_diagnostic_check(user_id: str):
    """
    Get diagnostic snapshot.
    """

    return fetch_one(
        """
        SELECT *
        FROM diagnostic_snapshots
        WHERE user_id = ?
        """,
        (user_id,)
    )


@tool
def get_ticket_details(ticket_id: str):
    """
    Get ticket details.
    """

    return fetch_one(
        """
        SELECT *
        FROM tickets
        WHERE ticket_id = ?
        """,
        (ticket_id,)
    )


@tool
def create_resolution_plan(
    diagnosis: str
):
    """
    Create resolution plan.
    """

    return {
        "diagnosis_summary": diagnosis,
        "recommended_steps": [
            "Check troubleshooting guide",
            "Run diagnostics",
            "Check incidents"
        ],
        "escalation_required": False,
        "confidence": "HIGH"
    }