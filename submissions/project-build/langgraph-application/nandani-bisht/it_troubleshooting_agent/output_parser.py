import json
import re


def extract_json_from_text(text):
    text = text.strip()
    if text.startswith("{") or text.startswith("["):
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

    json_pattern = re.search(r"\{[\s\S]*\}", text)
    if json_pattern:
        try:
            return json.loads(json_pattern.group())
        except json.JSONDecodeError:
            pass

    return None


def parse_classification_output(text):
    result = extract_json_from_text(text)
    if result:
        return result

    return {
        "issue_type": "UNKNOWN",
        "confidence": "LOW",
        "requires_user_lookup": True,
        "requires_device_lookup": True,
        "requires_known_incident_check": True,
        "requires_clarification": True,
        "reasoning_summary": text,
    }


def parse_resolution_plan(text):
    result = extract_json_from_text(text)
    if result:
        return result

    return {
        "diagnosis_summary": text,
        "recommended_steps": [],
        "escalation_required": False,
        "escalation_group": "",
        "safety_notes": ["Do not request password, OTP, or MFA code."],
        "confidence": "LOW",
    }


def parse_safety_review(text):
    result = extract_json_from_text(text)
    if result:
        return result

    return {
        "unsafe_content_detected": False,
        "violations_found": [],
        "safe_version": text,
    }


def parse_final_response(text):
    result = extract_json_from_text(text)
    if result:
        return result

    return {
        "issue_type": "UNKNOWN",
        "diagnosis_summary": text,
        "evidence_used": {
            "kb_sources": [],
            "tools_used": [],
            "diagnostic_signals": [],
        },
        "recommended_steps": [],
        "escalation_required": False,
        "escalation_group": "",
        "safety_notes": ["Do not request password, OTP, or MFA code."],
        "confidence": "LOW",
    }


def parse_ticket_summary(text):
    result = extract_json_from_text(text)
    if result:
        return result

    return {
        "ticket_summary": text,
        "issue_type": "UNKNOWN",
        "observed_signals": [],
        "diagnostics_checked": [],
        "recommended_assignment_group": "",
        "next_action": "",
    }


def format_final_response_for_display(response_dict):
    lines = []
    lines.append("=" * 60)
    lines.append("IT TROUBLESHOOTING AGENT - DIAGNOSIS REPORT")
    lines.append("=" * 60)

    lines.append(f"Issue Type: {response_dict.get('issue_type', 'UNKNOWN')}")
    lines.append(f"Confidence: {response_dict.get('confidence', 'LOW')}")
    lines.append("")

    lines.append("Diagnosis Summary:")
    lines.append(f"  {response_dict.get('diagnosis_summary', '')}")
    lines.append("")

    evidence = response_dict.get("evidence_used", {})
    if evidence:
        lines.append("Evidence Used:")
        kb_sources = evidence.get("kb_sources", [])
        if kb_sources:
            lines.append(f"  Knowledge Base: {', '.join(kb_sources)}")
        tools_used = evidence.get("tools_used", [])
        if tools_used:
            lines.append(f"  Tools Used: {', '.join(tools_used)}")
        signals = evidence.get("diagnostic_signals", [])
        if signals:
            lines.append("  Diagnostic Signals:")
            for signal in signals:
                lines.append(f"    - {signal}")
        lines.append("")

    steps = response_dict.get("recommended_steps", [])
    if steps:
        lines.append("Recommended Steps:")
        for i, step in enumerate(steps, 1):
            lines.append(f"  {i}. {step}")
        lines.append("")

    escalation_required = response_dict.get("escalation_required", False)
    escalation_group = response_dict.get("escalation_group", "")
    lines.append(f"Escalation Required: {'Yes' if escalation_required else 'No'}")
    if escalation_required and escalation_group:
        lines.append(f"Escalation Group: {escalation_group}")
    lines.append("")

    safety_notes = response_dict.get("safety_notes", [])
    if safety_notes:
        lines.append("Safety Notes:")
        for note in safety_notes:
            lines.append(f"  - {note}")
    lines.append("=" * 60)

    return "\n".join(lines)
