"""IT Troubleshooting tool helpers.

This module implements a set of helper functions used by the troubleshooting
agent: issue classification, knowledge-base retrieval, SQLite-backed lookups
for users/devices/tickets/incidents, a basic diagnostic snapshot reader,
and a resolution-plan generator.

Functions are written to be defensive: if the expected database or tables are
not present they return `found: False` (for lookups) or reasonable default
structures so the caller can handle missing data.
"""
from __future__ import annotations

import os
import glob
import sqlite3
from typing import Dict, Any, List, Optional


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_DIR = os.path.join(BASE_DIR, "data", "knowledge_base")
DB_PATH = os.path.join(BASE_DIR, "data", "database", "it_support.db")


def classify_issue(text: str) -> Dict[str, Any]:
    """Classify a freeform issue description into a supported issue type.

    Returns the FR-4 required structure.
    The classifier is a lightweight keyword matcher with conservative confidences.
    """
    t = (text or "").lower()
    # simple keyword mapping
    mappings = [
        ("vpn", "VPN"),
        ("mfa", "VPN"),
        ("outlook", "OUTLOOK_EMAIL"),
        ("email", "OUTLOOK_EMAIL"),
        ("slow", "LAPTOP_PERFORMANCE"),
        ("battery", "LAPTOP_PERFORMANCE"),
        ("password", "PASSWORD_RESET"),
        ("forgot", "PASSWORD_RESET"),
        ("network", "NETWORK_CONNECTIVITY"),
        ("wifi", "NETWORK_CONNECTIVITY"),
        ("printer", "PRINTER"),
    ]

    found_types = []
    for kw, typ in mappings:
        if kw in t:
            found_types.append(typ)

    if not found_types:
        issue_type = "UNKNOWN"
        confidence = "LOW"
        requires_clarification = True
        reasoning = "No clear keyword match found."
    else:
        # pick the most frequent match (first in this simple list)
        issue_type = found_types[0]
        # confidence heuristic
        if any(k in t for k, _ in mappings[:3]):
            confidence = "HIGH"
        else:
            confidence = "MEDIUM"
        requires_clarification = False
        reasoning = f"Matched keywords suggesting {issue_type}."

    # conservative defaults for required lookups
    requires_user_lookup = True
    requires_device_lookup = issue_type in ("VPN", "LAPTOP_PERFORMANCE", "PRINTER")
    requires_known_incident_check = issue_type in ("VPN", "NETWORK_CONNECTIVITY")

    return {
        "issue_type": issue_type,
        "confidence": confidence,
        "requires_user_lookup": requires_user_lookup,
        "requires_device_lookup": requires_device_lookup,
        "requires_known_incident_check": requires_known_incident_check,
        "requires_clarification": requires_clarification,
        "reasoning_summary": reasoning,
    }


def retrieve_troubleshooting_steps(issue_type: str, query: str) -> Dict[str, Any]:
    """Search knowledge base markdown files for relevant snippets.

    Returns a structure matching FR-5. The search is a simple substring search
    across the KB files that include the `issue_type` in their filename or
    contain the query text.
    """
    results: List[Dict[str, str]] = []

    if not os.path.isdir(KB_DIR):
        return {"issue_type": issue_type, "chunks": []}

    md_files = glob.glob(os.path.join(KB_DIR, "*.md"))
    q = (query or "").lower()
    for path in md_files:
        name = os.path.basename(path)
        try:
            with open(path, "r", encoding="utf-8") as fh:
                contents = fh.read()
        except Exception:
            continue

        lowered = contents.lower()
        match = False
        snippet = None
        # Prefer files that match the issue_type name (vpn -> vpn_troubleshooting_guide.md)
        if issue_type and issue_type.lower() in name.lower():
            match = True
        if q and q in lowered:
            match = True
            # extract a short snippet: the first matching line
            for line in contents.splitlines():
                if q in line.lower():
                    snippet = line.strip()
                    break

        if match:
            if not snippet:
                # take the first non-empty line as a fallback snippet
                for line in contents.splitlines():
                    if line.strip():
                        snippet = line.strip()
                        break

            chunk_id = f"{name}::1"
            results.append({
                "source_file": name,
                "chunk_id": chunk_id,
                "snippet": snippet or "",
            })

    return {"issue_type": issue_type, "chunks": results}


def _connect(db_path: Optional[str] = None) -> sqlite3.Connection:
    if not db_path:
        db_path = DB_PATH
    return sqlite3.connect(db_path)


def get_user_profile(user_id: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
    """Lookup a user in the `it_support.db` SQLite database.

    Looks for a `users` table with columns like user_id, full_name, department,
    location, account_status, mfa_status. If the database/table/row is missing
    the function returns `found: False`.
    """
    try:
        conn = _connect()
        cur = conn.cursor()
        # prefer user_id lookup
        if user_id:
            cur.execute("SELECT user_id, full_name, department, location, account_status, mfa_status FROM users WHERE user_id = ?", (user_id,))
        elif email:
            cur.execute("SELECT user_id, full_name, department, location, account_status, mfa_status FROM users WHERE email = ?", (email,))
        else:
            return {"found": False}

        row = cur.fetchone()
        conn.close()
        if not row:
            return {"found": False}

        return {
            "found": True,
            "user": {
                "user_id": row[0],
                "full_name": row[1],
                "department": row[2],
                "location": row[3],
                "account_status": row[4],
                "mfa_status": row[5],
            },
        }
    except Exception as e:
        return {"found": False, "error": str(e)}


def get_device_status(user_id: Optional[str] = None, device_id: Optional[str] = None) -> Dict[str, Any]:
    """Fetch device health details from the `devices` table.

    Returns a dictionary with device and resource usage details. If lookup
    fails returns an empty structure with `found: False`.
    """
    try:
        conn = _connect()
        cur = conn.cursor()
        if device_id:
            cur.execute("SELECT user_id, device_id, compliance_status, vpn_client_version, disk_free_percent, cpu_usage_percent, memory_usage_percent FROM devices WHERE device_id = ?", (device_id,))
        elif user_id:
            cur.execute("SELECT user_id, device_id, compliance_status, vpn_client_version, disk_free_percent, cpu_usage_percent, memory_usage_percent FROM devices WHERE user_id = ? LIMIT 1", (user_id,))
        else:
            return {"found": False}

        row = cur.fetchone()
        conn.close()
        if not row:
            return {"found": False}

        return {
            "found": True,
            "user_id": row[0],
            "device_id": row[1],
            "compliance_status": row[2],
            "vpn_client_version": row[3],
            "disk_free_percent": row[4],
            "cpu_usage_percent": row[5],
            "memory_usage_percent": row[6],
        }
    except Exception as e:
        return {"found": False, "error": str(e)}


def check_known_incidents(service_name: Optional[str] = None, region: Optional[str] = None, keyword: Optional[str] = None) -> Dict[str, Any]:
    """Query `incidents` table for active incidents.

    Returns count and list of incidents. Each incident is expected to contain
    fields similar to the FR-8 example. If the table is missing returns an
    empty result.
    """
    try:
        conn = _connect()
        cur = conn.cursor()
        q = "SELECT incident_id, service_name, region, severity, status, summary, workaround FROM incidents WHERE 1=1"
        params: List[Any] = []
        if service_name:
            q += " AND service_name LIKE ?"
            params.append(f"%{service_name}%")
        if region:
            q += " AND region LIKE ?"
            params.append(f"%{region}%")
        if keyword:
            q += " AND (summary LIKE ? OR workaround LIKE ? OR service_name LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"])

        q += " AND status IN ('Active','active','OPEN','Open')"
        cur.execute(q, tuple(params))
        rows = cur.fetchall()
        conn.close()

        incidents = []
        for r in rows:
            incidents.append({
                "incident_id": r[0],
                "service_name": r[1],
                "region": r[2],
                "severity": r[3],
                "status": r[4],
                "summary": r[5],
                "workaround": r[6],
            })

        return {"count": len(incidents), "incidents": incidents}
    except Exception as e:
        return {"count": 0, "incidents": [], "error": str(e)}


def run_diagnostic_check(user_id: Optional[str] = None, device_id: Optional[str] = None) -> Dict[str, Any]:
    """Return a diagnostic snapshot for a user/device.

    This function looks up a `diagnostics` table for the latest snapshot. If
    the table is not available a conservative simulated snapshot is returned.
    """
    try:
        conn = _connect()
        cur = conn.cursor()
        q = "SELECT user_id, vpn_reachable, internet_reachable, webmail_reachable, internal_apps_reachable, account_locked, mfa_push_success FROM diagnostics WHERE 1=1"
        params: List[Any] = []
        if user_id:
            q += " AND user_id = ?"
            params.append(user_id)
        if device_id:
            q += " AND device_id = ?"
            params.append(device_id)
        q += " ORDER BY timestamp DESC LIMIT 1"
        cur.execute(q, tuple(params))
        row = cur.fetchone()
        conn.close()
        if row:
            return {
                "user_id": row[0],
                "vpn_reachable": bool(row[1]),
                "internet_reachable": bool(row[2]),
                "webmail_reachable": bool(row[3]),
                "internal_apps_reachable": bool(row[4]),
                "account_locked": bool(row[5]),
                "mfa_push_success": bool(row[6]),
            }
    except Exception:
        # fall through to simulated snapshot
        pass

    # conservative defaults if no diagnostics table is present
    return {
        "user_id": user_id or "",
        "vpn_reachable": False,
        "internet_reachable": True,
        "webmail_reachable": True,
        "internal_apps_reachable": False,
        "account_locked": False,
        "mfa_push_success": True,
    }


def get_ticket_details(ticket_id: Optional[str] = None, user_id: Optional[str] = None) -> Dict[str, Any]:
    """Fetch ticket details from `tickets` table.

    Returns a single ticket matching `ticket_id` or the most recent ticket for
    `user_id` when `ticket_id` is not provided.
    """
    try:
        conn = _connect()
        cur = conn.cursor()
        if ticket_id:
            cur.execute("SELECT ticket_id, user_id, issue_type, priority, status, subject, assigned_group FROM tickets WHERE ticket_id = ?", (ticket_id,))
        elif user_id:
            cur.execute("SELECT ticket_id, user_id, issue_type, priority, status, subject, assigned_group FROM tickets WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", (user_id,))
        else:
            return {}

        row = cur.fetchone()
        conn.close()
        if not row:
            return {}

        return {
            "ticket_id": row[0],
            "user_id": row[1],
            "issue_type": row[2],
            "priority": row[3],
            "status": row[4],
            "subject": row[5],
            "assigned_group": row[6],
        }
    except Exception as e:
        return {"error": str(e)}


def generate_resolution_plan(issue_text: str, kb_results: Dict[str, Any], tool_outputs: Dict[str, Any], known_incidents: Dict[str, Any], diagnostics: Dict[str, Any]) -> Dict[str, Any]:
    """Create a resolution plan (FR-11) based on inputs.

    The function synthesizes a short diagnosis, recommended steps and whether
    escalation is required. Logic is heuristic-driven and conservative.
    """
    cls = classify_issue(issue_text)
    issue_type = cls.get("issue_type", "UNKNOWN")

    diagnosis = f"Issue classified as {issue_type} (confidence={cls.get('confidence')})."

    recommended: List[str] = []
    escalation_required = False
    escalation_group = ""
    safety_notes: List[str] = []

    # include top KB snippets as first steps
    chunks = kb_results.get("chunks", []) if isinstance(kb_results, dict) else []
    for c in chunks[:3]:
        snip = c.get("snippet") or f"See {c.get('source_file')}"
        recommended.append(f"Consult KB: {snip}")

    # incorporate diagnostics
    if diagnostics:
        if diagnostics.get("vpn_reachable") is False:
            recommended.append("Verify VPN gateway reachability and ask user to switch networks.")
        if diagnostics.get("account_locked"):
            recommended.append("Unlock account or escalate to Identity Access Management.")
            escalation_required = True
            escalation_group = "Identity Access Management"

    # known incidents influence escalation
    if known_incidents and known_incidents.get("count", 0) > 0:
        recommended.append("Known service incident detected; follow incident workaround and inform the user.")
        escalation_required = True
        # prefer Network Support for VPN/network incidents
        if issue_type in ("VPN", "NETWORK_CONNECTIVITY"):
            escalation_group = "Network Support"

    # default first-level steps if nothing found
    if not recommended:
        recommended.extend([
            "Ask user for exact error message and recent changes.",
            "Collect user and device identifiers for deeper lookup.",
        ])

    # safety notes from KB (if present)
    for c in chunks:
        if "Do not" in (c.get("snippet") or "") or "Do not ask" in (c.get("snippet") or ""):
            safety_notes.append(c.get("snippet"))

    # determine confidence
    confidence = cls.get("confidence", "LOW")

    return {
        "diagnosis_summary": diagnosis,
        "recommended_steps": recommended,
        "escalation_required": escalation_required,
        "escalation_group": escalation_group,
        "safety_notes": safety_notes,
        "confidence": confidence,
    }


if __name__ == "__main__":
    # simple self-check when run directly
    print("tools.py: available functions:\n - classify_issue(text)\n - retrieve_troubleshooting_steps(issue_type, query)\n - get_user_profile(user_id=None, email=None)\n - get_device_status(user_id=None, device_id=None)\n - check_known_incidents(service_name=None, region=None, keyword=None)\n - run_diagnostic_check(user_id=None, device_id=None)\n - get_ticket_details(ticket_id=None, user_id=None)\n - generate_resolution_plan(issue_text, kb_results, tool_outputs, known_incidents, diagnostics)")