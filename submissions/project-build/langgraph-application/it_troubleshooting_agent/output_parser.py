from __future__ import annotations

from typing import Dict, Any, List


def format_final_response(issue_type: str, diagnosis: str, kb_sources: List[str], tools_used: List[str], diagnostic_signals: List[str], recommended_steps: List[str], escalation_required: bool, escalation_group: str, safety_notes: List[str], confidence: str) -> Dict[str, Any]:
    return {
        "issue_type": issue_type,
        "diagnosis_summary": diagnosis,
        "evidence_used": {
            "kb_sources": kb_sources,
            "tools_used": tools_used,
            "diagnostic_signals": diagnostic_signals,
        },
        "recommended_steps": recommended_steps,
        "escalation_required": escalation_required,
        "escalation_group": escalation_group,
        "safety_notes": safety_notes,
        "confidence": confidence,
    }


def create_ticket_summary(user: Dict[str, Any], device: Dict[str, Any], diagnostics: Dict[str, Any], issue_type: str, recommended_assignment_group: str, next_action: str) -> Dict[str, Any]:
    observed = []
    if device:
        if device.get('disk_free_percent') is not None:
            observed.append(f"disk_free_percent={device.get('disk_free_percent')}")
        if device.get('cpu_usage_percent') is not None:
            observed.append(f"cpu_usage_percent={device.get('cpu_usage_percent')}")
        if device.get('memory_usage_percent') is not None:
            observed.append(f"memory_usage_percent={device.get('memory_usage_percent')}")

    diagnostics_checked = []
    if diagnostics:
        for k, v in diagnostics.items():
            diagnostics_checked.append(f"{k}={v}")

    return {
        "ticket_summary": f"Ticket for {user.get('full_name') if user else 'Unknown user'}: {issue_type}",
        "issue_type": issue_type,
        "observed_signals": observed,
        "diagnostics_checked": diagnostics_checked,
        "recommended_assignment_group": recommended_assignment_group,
        "next_action": next_action,
    }
