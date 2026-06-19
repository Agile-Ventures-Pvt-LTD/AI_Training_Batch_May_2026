from typing import Literal

from langgraph.graph import END, START, StateGraph

from tools import (
    TroubleshootingState,
    classify_issue_node,
    clarification_node,
    diagnostic_decision_node,
    escalation_node,
    final_response_node,
    parallel_context_node,
    resolution_planner_node,
    retrieve_guidance_node,
    safety_review_node,
)

import re
from typing import Dict, List, Optional, TypedDict

from retrievers import retriever


class TroubleshootingState(TypedDict):
    user_query: str
    issue_type: str
    user_identifier: Optional[str]
    retrieved_guidance: List[Dict]
    user_profile: Dict
    device_status: Dict
    known_incidents: List[Dict]
    diagnostic_snapshot: Dict
    resolution_plan: Dict
    safety_review: Dict
    final_response: str



def classify_issue_node(state: TroubleshootingState) -> TroubleshootingState:

    """It classify the user query according to below conditions"""
    text = state["user_query"].lower()

    if "vpn" in text or "network" in text:
        issue_type = "network"
    elif "outlook" in text or "email" in text:
        issue_type = "email"
    elif "password" in text or "login" in text:
        issue_type = "password"
    elif "printer" in text:
        issue_type = "printer"
    elif "slow" in text or "performance" in text or "laptop" in text:
        issue_type = "performance"
    else:
        issue_type = "unknown"

    return {"issue_type":issue_type}


def retrieve_guidence_node(state: TroubleshootingState):
    """This node helps to retrieve the relevant information from the knowledge base """
    query = state["user_query"]
    docs=retriever.invoke(query)

    return {"retrieved_guidance" : [
        {
            "content": doc.page_content
        }
        for doc in docs
    ]
    }

def parallel_context_node(state: TroubleshootingState):

    """This node helps to retrieve the data from sql database"""

    query="""
        select * from users;

"""

def diagnostic_decision_node(state: TroubleshootingState) -> TroubleshootingState:
    issue = state["issue_type"]
    text = state["user_query"]
    missing_info = state["diagnostic_snapshot"].get("missing_info", [])

    if issue == "network":
        likely_cause = "possible connectivity or VPN configuration issue"
        next_step = "check internet access, VPN status, and network settings"
    elif issue == "email":
        likely_cause = "possible Outlook or mailbox sync issue"
        next_step = "verify email settings and account sync status"
    elif issue == "password":
        likely_cause = "possible account access or reset issue"
        next_step = "verify account status and reset instructions"
    elif issue == "printer":
        likely_cause = "possible printer connection or queue problem"
        next_step = "check printer connection and print queue"
    elif issue == "performance":
        likely_cause = "possible device slowdown or resource issue"
        next_step = "check system performance and startup apps"
    else:
        likely_cause = "issue is not clear yet"
        next_step = "collect more details from the user"

    return {"diagnostic_snapshot": {
        "likely_cause": likely_cause,
        "next_step": next_step,
        "missing_info": missing_info,
        "evidence": text,
    }
    }

def clarification_node(state: TroubleshootingState) -> TroubleshootingState:
    missing = state["diagnostic_snapshot"].get("missing_info", [])

    if missing:
        state["final_response"] = (
            "Please share these details to continue safely: " + ", ".join(missing)
        )
    else:
        state["final_response"] = "Please provide any missing details you can."

    return state


def resolution_planner_node(state: TroubleshootingState) -> TroubleshootingState:
    steps = [
        state["diagnostic_snapshot"].get("next_step", "review the troubleshooting guide"),
        "confirm the affected device and user account",
        "follow the relevant KB steps",
    ]

    state["resolution_plan"] = {
        "steps": steps,
        "reason": "This follows the likely cause and avoids risky steps.",
    }
    return state




workflow = StateGraph(TroubleshootingState)

workflow.add_node("classify_issue_node", classify_issue_node)
workflow.add_node("retrieve_guidance_node", retrieve_guidance_node)
workflow.add_node("parallel_context_node", parallel_context_node)
workflow.add_node("diagnostic_decision_node", diagnostic_decision_node)
workflow.add_node("clarification_node", clarification_node)
workflow.add_node("resolution_planner_node", resolution_planner_node)
workflow.add_node("escalation_node", escalation_node)
workflow.add_node("safety_review_node", safety_review_node)
workflow.add_node("final_response_node", final_response_node)

workflow.set_entry_point(START)
workflow.add_edge("classify_issue_node", "retrieve_guidance_node")
workflow.add_edge("retrieve_guidance_node", "parallel_context_node")
workflow.add_edge("parallel_context_node", "diagnostic_decision_node")


def route_after_diagnostic(state: TroubleshootingState) -> Literal["clarification_node", "resolution_planner_node", "escalation_node"]:
    if state.get("diagnostic_snapshot", {}).get("missing_info"):
        return "clarification_node"
    if state.get("issue_type") in {"network", "email", "password", "printer", "performance"}:
        return "resolution_planner_node"
    return "resolution_planner_node"


workflow.add_conditional_edges(
    "diagnostic_decision_node",
    route_after_diagnostic,
    {
        "clarification_node": "clarification_node",
        "resolution_planner_node": "resolution_planner_node",
        "escalation_node": "escalation_node",
    },
)
workflow.add_edge("clarification_node", "final_response_node")
workflow.add_edge("resolution_planner_node", "safety_review_node")
workflow.add_edge("escalation_node", "safety_review_node")
workflow.add_edge("safety_review_node", "final_response_node")
workflow.add_edge("final_response_node", END)

graph = workflow.compile()