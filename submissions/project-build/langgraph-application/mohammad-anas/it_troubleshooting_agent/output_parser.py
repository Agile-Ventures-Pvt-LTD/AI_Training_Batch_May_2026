
def create_final_response(
    issue_type="UNKNOWN",
    diagnosis_summary="",
    kb_sources=None,
    tools_used=None,
    diagnostic_signals=None,
    recommended_steps=None,
    escalation_required=False,
    escalation_group="",
    confidence="MEDIUM"
):
    """
    Standard response format.
    """

    if kb_sources is None:
        kb_sources = []

    if tools_used is None:
        tools_used = []

    if diagnostic_signals is None:
        diagnostic_signals = []

    if recommended_steps is None:
        recommended_steps = []

    return {
        "issue_type": issue_type,

        "diagnosis_summary": diagnosis_summary,

        "evidence_used": {
            "kb_sources": kb_sources,
            "tools_used": tools_used,
            "diagnostic_signals": diagnostic_signals
        },

        "recommended_steps": recommended_steps,

        "escalation_required": escalation_required,

        "escalation_group": escalation_group,

        "safety_notes": [
            "Never ask users for passwords",
            "Never ask users for OTPs",
            "Never ask users for MFA codes"
        ],

        "confidence": confidence
    }