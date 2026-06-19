from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, TypedDict, Literal
from pathlib import Path

from langgraph.graph import StateGraph, END

import tools
from retrievers import build_default_retriever
from output_parser import format_final_response


retriever = build_default_retriever()



def classify_issue_node(query: str) -> Dict[str, Any]:
    """Classify the issue type from the query."""
    return tools.classify_issue(query)


def retrieve_guidance_node(issue_type: str, query: str) -> Dict[str, Any]:
    """Retrieve KB guidance for the classified issue."""
    return retriever.retrieve(issue_type, query)


def parallel_context_node(user_identifier: str | None, issue_type: str, query: str) -> Dict[str, Any]:
    """Fetch user profile, device status, incidents, diagnostics in parallel."""
    results = {}
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = {
            ex.submit(tools.get_user_profile, user_id=user_identifier): 'user_profile',
            ex.submit(tools.get_device_status, user_id=user_identifier): 'device_status',
            ex.submit(tools.check_known_incidents, service_name=issue_type): 'known_incidents',
            ex.submit(tools.run_diagnostic_check, user_id=user_identifier): 'diagnostics',
            ex.submit(tools.get_ticket_details, user_id=user_identifier): 'ticket',
        }
        for fut in as_completed(futures):
            key = futures[fut]
            try:
                results[key] = fut.result()
            except Exception as e:
                results[key] = {'error': str(e)}

    return results


def diagnostic_decision_node(diagnostics: Dict[str, Any], known_incidents: Dict[str, Any]) -> Dict[str, Any]:
    """Determine severity based on diagnostics and incidents."""
    severity = 'LOW'
    if diagnostics.get('vpn_reachable') is False and known_incidents.get('count', 0) > 0:
        severity = 'HIGH'
    elif diagnostics.get('cpu_usage_percent', 0) > 85 or diagnostics.get('disk_free_percent', 100) < 10:
        severity = 'HIGH'

    return {'severity': severity}


def resolution_planner_node(query: str, kb_results: Dict[str, Any], tools_outputs: Dict[str, Any], known_incidents: Dict[str, Any], diagnostics: Dict[str, Any]) -> Dict[str, Any]:
    """Generate resolution plan based on all context."""
    return tools.generate_resolution_plan(query, kb_results, tools_outputs, known_incidents, diagnostics)


def safety_review_node(plan: Dict[str, Any]) -> Dict[str, Any]:
    """Review plan for safety issues (password/OTP/MFA requests)."""
    unsafe = False
    notes = []
    for step in plan.get('recommended_steps', []):
        lower = step.lower()
        if 'password' in lower or 'otp' in lower or 'mfa' in lower:
            unsafe = True
            notes.append(step)

    return {'unsafe': unsafe, 'notes': notes}


def final_response_node(issue_type: str, query: str, plan: Dict[str, Any], kb_results: Dict[str, Any], diagnostics: Dict[str, Any]) -> Dict[str, Any]:
    """Format final response for the user."""
    kb_sources = [c.get('source_file') for c in kb_results.get('chunks', [])]
    diagnostic_signals = [f"{k}={v}" for k, v in diagnostics.items()]
    return format_final_response(
        issue_type=issue_type,
        diagnosis=plan.get('diagnosis_summary', ''),
        kb_sources=list(dict.fromkeys([s for s in kb_sources if s])),
        tools_used=['classify_issue', 'retrieve_troubleshooting_steps', 'get_user_profile', 'get_device_status', 'check_known_incidents', 'run_diagnostic_check'],
        diagnostic_signals=diagnostic_signals,
        recommended_steps=plan.get('recommended_steps', []),
        escalation_required=plan.get('escalation_required', False),
        escalation_group=plan.get('escalation_group', ''),
        safety_notes=plan.get('safety_notes', []),
        confidence=plan.get('confidence', 'LOW'),
    )



class State(TypedDict):
    """State object for troubleshooting workflow."""
    query: str
    user_identifier: str | None
    classification: Dict[str, Any]
    kb_results: Dict[str, Any]
    parallel_context: Dict[str, Any]
    decision: Dict[str, Any]
    plan: Dict[str, Any]
    safety_check: Dict[str, Any]
    final_response: Dict[str, Any]
    route: Literal["SAFE", "ESCALATE", "END"]


def classify(state: State) -> State:
    """Classify the issue from the query."""
    result = classify_issue_node(state["query"])
    state["classification"] = result
    return state


def retrieve(state: State) -> State:
    """Retrieve KB guidance for the classified issue."""
    issue_type = state["classification"].get("issue_type", "UNKNOWN")
    result = retrieve_guidance_node(issue_type, state["query"])
    state["kb_results"] = result
    return state


def parallel_context(state: State) -> State:
    """Fetch user profile, device status, incidents, diagnostics in parallel."""
    issue_type = state["classification"].get("issue_type", "UNKNOWN")
    result = parallel_context_node(state["user_identifier"], issue_type, state["query"])
    state["parallel_context"] = result
    return state


def grade(state: State) -> State:
    """Diagnostic decision node to determine severity."""
    diagnostics = state["parallel_context"].get("diagnostics", {})
    known_incidents = state["parallel_context"].get("known_incidents", {})
    result = diagnostic_decision_node(diagnostics, known_incidents)
    state["decision"] = result
    return state


def generate_plan(state: State) -> State:
    """Generate resolution plan based on all context."""
    result = resolution_planner_node(
        state["query"],
        state["kb_results"],
        state["parallel_context"],
        state["parallel_context"].get("known_incidents", {}),
        state["parallel_context"].get("diagnostics", {})
    )
    state["plan"] = result
    return state


def safety_check(state: State) -> State:
    """Review plan for safety issues."""
    result = safety_review_node(state["plan"])
    state["safety_check"] = result
    # Determine route based on safety
    if result.get("unsafe"):
        state["route"] = "ESCALATE"
        state["plan"]["safety_notes"] = result.get("notes", [])
    else:
        state["route"] = "SAFE"
    return state


def answer(state: State) -> State:
    """Generate final response."""
    result = final_response_node(
        state["classification"].get("issue_type", "UNKNOWN"),
        state["query"],
        state["plan"],
        state["kb_results"],
        state["parallel_context"].get("diagnostics", {})
    )
    state["final_response"] = result
    return state


def build_graph():
    """Build a LangGraph StateGraph for the troubleshooting workflow.
    
    Returns the compiled graph object.
    """
    g = StateGraph(State)

    # Add nodes
    g.add_node("classify", classify)
    g.add_node("retrieve", retrieve)
    g.add_node("parallel_context", parallel_context)
    g.add_node("grade", grade)
    g.add_node("generate_plan", generate_plan)
    g.add_node("safety_check", safety_check)
    g.add_node("answer", answer)

    g.set_entry_point("classify")

    g.add_edge("classify", "retrieve")
    g.add_edge("retrieve", "parallel_context")
    g.add_edge("parallel_context", "grade")
    g.add_edge("grade", "generate_plan")
    g.add_edge("generate_plan", "safety_check")

    
    g.add_conditional_edges(
        "safety_check",
        lambda x: x["route"],
        {
            "SAFE": "answer",
            "ESCALATE": "answer",
        }
    )

    g.add_edge("answer", END)

    return g.compile()



# Below is the commented code for creating the graph.
#graph = build_graph()

#graph.get_graph(xray=True).draw_mermaid_png(output_file_path='troubleshooting_graph.png')




def run_troubleshooting_graph(query: str, user_identifier: str | None = None) -> Dict[str, Any]:
    """Legacy function: run troubleshooting without StateGraph.
    
    For backward compatibility. Use build_graph() + .invoke() for new code.
    """
    cls = classify_issue_node(query)
    if cls.get('requires_clarification'):
        return {'clarify': True, 'question': 'Please provide the affected user and more details.'}

    kb = retrieve_guidance_node(cls.get('issue_type'), query)
    parallel = parallel_context_node(user_identifier, cls.get('issue_type'), query)
    decision = diagnostic_decision_node(parallel.get('diagnostics', {}), parallel.get('known_incidents', {}))
    plan = resolution_planner_node(query, kb, parallel, parallel.get('known_incidents', {}), parallel.get('diagnostics', {}))
    safety = safety_review_node(plan)
    if safety.get('unsafe'):
        plan['safety_notes'] = safety.get('notes')

    final = final_response_node(cls.get('issue_type', 'UNKNOWN'), query, plan, kb, parallel.get('diagnostics', {}))
    return final
