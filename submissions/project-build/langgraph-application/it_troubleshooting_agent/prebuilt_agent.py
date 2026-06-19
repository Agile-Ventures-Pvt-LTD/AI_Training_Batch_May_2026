from __future__ import annotations

from typing import Dict, Any, List

import tools
from retrievers import build_default_retriever
from output_parser import format_final_response, create_ticket_summary


retriever = build_default_retriever()


def handle_query(user_query: str, user_identifier: str | None = None) -> Dict[str, Any]:
    
    classification = tools.classify_issue(user_query)
    issue_type = classification.get("issue_type", "UNKNOWN")

    
    kb_results = retriever.retrieve(issue_type, user_query)

    
    user_profile = None
    if user_identifier:
        u = tools.get_user_profile(user_id=user_identifier, email=user_identifier)
        if u.get('found'):
            user_profile = u.get('user')

    device_status = tools.get_device_status(user_id=user_identifier) if user_identifier else {}
    incidents = tools.check_known_incidents(service_name=issue_type)
    diagnostics = tools.run_diagnostic_check(user_id=user_identifier)
    ticket = tools.get_ticket_details(user_id=user_identifier)

    
    plan = tools.generate_resolution_plan(user_query, kb_results, {
        "user_profile": user_profile,
        "device_status": device_status,
        "ticket": ticket,
    }, incidents, diagnostics)

    
    kb_sources = [c.get('source_file') for c in kb_results.get('chunks', [])]
    tools_used = [
        "classify_issue",
        "retrieve_troubleshooting_steps",
        "get_user_profile",
        "get_device_status",
        "check_known_incidents",
        "run_diagnostic_check",
        "get_ticket_details",
    ]
    diagnostic_signals = []
    if diagnostics:
        for k, v in diagnostics.items():
            diagnostic_signals.append(f"{k}={v}")

    final = format_final_response(
        issue_type=issue_type,
        diagnosis=plan.get('diagnosis_summary', ''),
        kb_sources=list(dict.fromkeys([s for s in kb_sources if s])),
        tools_used=tools_used,
        diagnostic_signals=diagnostic_signals,
        recommended_steps=plan.get('recommended_steps', []),
        escalation_required=plan.get('escalation_required', False),
        escalation_group=plan.get('escalation_group', ''),
        safety_notes=plan.get('safety_notes', []),
        confidence=plan.get('confidence', 'LOW'),
    )

    
    final['ticket_summary'] = create_ticket_summary(user_profile or {}, device_status or {}, diagnostics or {}, issue_type, final.get('escalation_group', ''), final.get('recommended_steps', ["See KB"])[0])

    return final
