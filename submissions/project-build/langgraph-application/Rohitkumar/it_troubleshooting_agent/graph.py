from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END


from tools import (
    classify_issue_type,
    retrieve_troubleshooting_steps,
    get_user_profile,
    get_device_status,
    check_known_incidents,
    run_diagnostic_check,
    create_resolution_plan,
)

class TroubleshootingState(TypedDict):
    user_query: str

    issue_type: Optional[str]
    classification: Dict

    user_identifier: Optional[str]

    retrieved_guidance: List[Dict]

    user_profile: Dict
    device_status: Dict
    known_incidents: List[Dict]
    diagnostic_snapshot: Dict

    severity: Optional[str]
    requires_clarification: bool

    resolution_plan: Dict
    safety_review: Dict

    final_response: str

def classify_issue_node(state: TroubleshootingState):
    result = classify_issue_type(state["user_query"])

    return {
        "issue_type": result["issue_type"],
        "classification": result,
        "requires_clarification": result.get("requires_clarification", False),
    }



def retrieve_kb_node(state: TroubleshootingState):
    result = retrieve_troubleshooting_steps(
        issue_type=state["issue_type"],
        query=state["user_query"]
    )

    return {
        "retrieved_guidance": result.get("chunks", [])
    }



def parallel_context_node(state: TroubleshootingState):
    """
    Simulated parallel execution:
    - user profile
    - device status
    - incidents
    - diagnostics
    """

    user_profile = {}
    device_status = {}
    incidents = []
    diagnostics = {}

  
    user_identifier = state.get("user_identifier")

    if user_identifier:
        user_profile = get_user_profile(user_identifier)
        device_status = get_device_status(user_identifier)
        diagnostics = run_diagnostic_check(user_identifier)

   
    incidents = check_known_incidents(state["issue_type"])

    return {
        "user_profile": user_profile,
        "device_status": device_status,
        "known_incidents": incidents.get("incidents", []),
        "diagnostic_snapshot": diagnostics,
    }



def diagnostic_decision_node(state: TroubleshootingState):
    """
    Decide:
    - Missing info?
    - Severity?
    """

    severity = "LOW"
    requires_clarification = state.get("requires_clarification", False)

   
    if not state.get("user_profile"):
        requires_clarification = True

   
    if state.get("known_incidents"):
        severity = "HIGH"

    device = state.get("device_status", {})

    if device:
        if device.get("disk_free_percent", 100) < 10:
            severity = "HIGH"
        if device.get("cpu_usage_percent", 0) > 85:
            severity = "HIGH"
        if device.get("memory_usage_percent", 0) > 85:
            severity = "HIGH"

    return {
        "severity": severity,
        "requires_clarification": requires_clarification
    }



def clarification_node(state: TroubleshootingState):
    return {
        "final_response": "Please provide more details such as user name, device issue specifics, error messages, and system behavior."
    }




def resolution_planner_node(state: TroubleshootingState):

    plan = create_resolution_plan({
        "issue_type": state["issue_type"],
        "user_query": state["user_query"],
        "kb": state.get("retrieved_guidance", []),
        "user_profile": state.get("user_profile", {}),
        "device_status": state.get("device_status", {}),
        "incidents": state.get("known_incidents", []),
        "diagnostics": state.get("diagnostic_snapshot", {})
    })

    return {
        "resolution_plan": plan
    }
def safety_review_node(state: TroubleshootingState):
    plan = state.get("resolution_plan", {})

    safety_notes = []

    
    for step in plan.get("recommended_steps", []):
        if "password" in step.lower():
            safety_notes.append("Do not request password.")
        if "otp" in step.lower():
            safety_notes.append("Do not request OTP.")
        if "mfa" in step.lower():
            safety_notes.append("Do not request MFA code.")

    plan["safety_notes"] = list(set(safety_notes))

    return {
        "resolution_plan": plan,
        "safety_review": {"status": "checked"}
    }

def final_response_node(state: TroubleshootingState):
    plan = state.get("resolution_plan", {})

    response = {
        "issue_type": state.get("issue_type"),
        "diagnosis_summary": plan.get("diagnosis_summary"),
        "evidence_used": {
            "kb_sources": [c["source_file"] for c in state.get("retrieved_guidance", [])],
            "tools_used": [
                "get_user_profile",
                "get_device_status",
                "check_known_incidents",
                "run_diagnostic_check"
            ],
            "diagnostic_signals": plan.get("diagnostic_signals", [])
        },
        "recommended_steps": plan.get("recommended_steps", []),
        "escalation_required": plan.get("escalation_required", False),
        "escalation_group": plan.get("escalation_group", ""),
        "safety_notes": plan.get("safety_notes", []),
        "confidence": plan.get("confidence", "MEDIUM")
    }

    return {
        "final_response": response
    }



def build_graph():

    builder = StateGraph(TroubleshootingState)

   
    builder.add_node("classify_issue", classify_issue_node)
    builder.add_node("retrieve_kb", retrieve_kb_node)
    builder.add_node("parallel_context", parallel_context_node)
    builder.add_node("diagnostic_decision", diagnostic_decision_node)
    builder.add_node("clarification", clarification_node)
    builder.add_node("resolution_planner", resolution_planner_node)
    builder.add_node("safety_review", safety_review_node)
    builder.add_node("final_response", final_response_node)

    builder.set_entry_point("classify_issue")
    builder.add_edge("classify_issue", "retrieve_kb")
    builder.add_edge("retrieve_kb", "parallel_context")
    builder.add_edge("parallel_context", "diagnostic_decision")

  
    def decision_router(state: TroubleshootingState):
        if state["requires_clarification"]:
            return "clarification"
        elif state["severity"] == "HIGH":
            return "resolution_planner"
        else:
            return "resolution_planner"

    builder.add_conditional_edges(
        "diagnostic_decision",
        decision_router,
        {
            "clarification": "clarification",
            "resolution_planner": "resolution_planner"
        }
    )

    builder.add_edge("resolution_planner", "safety_review")
    builder.add_edge("safety_review", "final_response")

    builder.add_edge("clarification", END)
    builder.add_edge("final_response", END)

    return builder.compile()

