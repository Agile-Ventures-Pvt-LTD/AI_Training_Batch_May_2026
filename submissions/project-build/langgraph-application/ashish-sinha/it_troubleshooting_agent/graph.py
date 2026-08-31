import json
from typing import Dict, Any, Literal
from groq import Groq

from langgraph.graph import StateGraph, END
from config import settings
from state import TroubleshootingState
from prompts import (
    CLASSIFY_ISSUE_SYSTEM_PROMPT,
    RESOLUTION_PLANNER_SYSTEM_PROMPT,
    SAFETY_REVIEW_SYSTEM_PROMPT
)
from tools import TOOL_MAP

# Initialize Groq client using your configuration
client = Groq(api_key=settings.GROQ_API_KEY)

def call_groq_json(system_prompt: str, user_prompt: str) -> dict:
    """Helper tool to call Groq model and safely enforce raw JSON replies."""
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.1, # Low temperature ensures strict structural adherence
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)

# ==========================================
# 1. GRAPH NODES (Core Execution Logic)
# ==========================================

def classify_issue_node(state: TroubleshootingState) -> Dict[str, Any]:
    """Analyzes user request to categorize the technical issue type."""
    print("🤖 [Node] Classifying user issue...")
    result = call_groq_json(CLASSIFY_ISSUE_SYSTEM_PROMPT, state["user_query"])
    
    # Extract identity if provided in a simple way (e.g., 'Amit')
    user_id_guess = None
    if "amit" in state["user_query"].lower():
        user_id_guess = "U1001"
    elif "rahul" in state["user_query"].lower():
        user_id_guess = "U1002"

    return {
        "issue_type": result.get("issue_type", "UNKNOWN"),
        "confidence": result.get("confidence", "LOW"),
        "requires_clarification": result.get("requires_clarification", False),
        "user_identifier": user_id_guess,
        "reasoning_summary": result.get("reasoning_summary", "")
    }

def gather_context_parallel_node(state: TroubleshootingState) -> Dict[str, Any]:
    """
    Executes multiple tools to pull database metrics and vector snippets.
    Demonstrates the Parallelization Pattern.
    """
    print("⚡ [Node] Gathering context in parallel...")
    uid = state.get("user_identifier")
    issue = state.get("issue_type", "UNKNOWN")
    query = state["user_query"]
    
    # Initialize defaults
    profile = {}
    device = {}
    diagnostics = {}
    incidents = []
    kb_steps = {}

    # Gather data from tool layer if user identifier is known
    if uid:
        profile = json.loads(TOOL_MAP["get_user_profile"](user_id=uid))
        device = json.loads(TOOL_MAP["get_device_status"](user_id=uid))
        diagnostics = json.loads(TOOL_MAP["run_diagnostic_check"](user_id=uid))
    
    # Always pull global incidents and KB articles related to the issue
    incidents = json.loads(TOOL_MAP["check_known_incidents"](service_name=issue))
    kb_steps = json.loads(TOOL_MAP["retrieve_troubleshooting_steps"](issue_type=issue, query=query))

    return {
        "user_profile": profile,
        "device_status": device,
        "diagnostic_snapshot": diagnostics,
        "known_incidents": incidents.get("incidents", []),
        "retrieved_guidance": kb_steps.get("chunks", [])
    }

def clarification_node(state: TroubleshootingState) -> Dict[str, Any]:
    """Executed when the user message lacks vital details."""
    print("💬 [Node] Requesting clarification...")
    return {
        "final_response": "I see you are having an IT issue, but I need a bit more context. Could you please provide your full name, employee ID, or more details about the error you are seeing?"
    }

def resolution_planner_node(state: TroubleshootingState) -> Dict[str, Any]:
    """Synthesizes all gathered data into a structured action strategy."""
    print("🧠 [Node] Designing resolution plan...")
    
    # Construct a comprehensive context dump for the LLM planner
    context_payload = {
        "user_query": state["user_query"],
        "issue_type": state["issue_type"],
        "user_profile": state["user_profile"],
        "device_status": state["device_status"],
        "diagnostic_snapshot": state["diagnostic_snapshot"],
        "known_incidents": state["known_incidents"],
        "kb_guidance": state["retrieved_guidance"]
    }
    
    result = call_groq_json(RESOLUTION_PLANNER_SYSTEM_PROMPT, json.dumps(context_payload))
    return {"resolution_plan": result}

def safety_review_node(state: TroubleshootingState) -> Dict[str, Any]:
    """Audits the generated plan to guarantee safety compliance standards."""
    print("🔒 [Node] Evaluating safety parameters...")
    
    plan_to_check = state["resolution_plan"]
    result = call_groq_json(SAFETY_REVIEW_SYSTEM_PROMPT, json.dumps(plan_to_check))
    
    # If the safety check triggers a content violation, use the safe alternative plan
    final_plan = plan_to_check
    if result.get("unsafe_content_detected", False):
        print("⚠️ Safety violation intercepted! Applying fallback plan rules.")
        final_plan = result.get("safe_alternative_plan", plan_to_check)
        
    # Render the structured technical output clearly into a user-friendly string
    formatted_reply = (
        f"### 🎯 IT Diagnosis & Resolution Plan\n"
        f"**Status/Diagnosis**: {final_plan.get('diagnosis_summary')}\n\n"
        f"**Recommended Fix Steps**:\n" + "\n".join([f"{idx+1}. {step}" for idx, step in enumerate(final_plan.get('recommended_steps', []))]) + "\n\n"
        f"**Escalation Required**: { 'Yes (' + final_plan.get('escalation_group') + ')' if final_plan.get('escalation_required') else 'No' }\n\n"
        f"**Safety Warnings**: {', '.join(final_plan.get('safety_notes', ['None']))}"
    )
    
    return {
        "safety_review": result,
        "final_response": formatted_reply
    }

# ==========================================
# 2. CONDITIONAL ROUTING EDGES
# ==========================================

def routing_after_classification(state: TroubleshootingState) -> Literal["clarify", "gather_context"]:
    """Determines if the flow needs extra basic info or can jump straight into data compilation."""
    if state.get("requires_clarification") or not state.get("user_identifier"):
        return "clarify"
    return "gather_context"

# ==========================================
# 3. GRAPH ORCHESTRATION BUILDER
# ==========================================

workflow = StateGraph(TroubleshootingState)

# Add all building blocks
workflow.add_node("classify", classify_issue_node)
workflow.add_node("clarify", clarification_node)
workflow.add_node("gather_context", gather_context_parallel_node)
workflow.add_node("planner", resolution_planner_node)
workflow.add_node("safety_audit", safety_review_node)

# Set up flow connections
workflow.set_entry_point("classify")

# Add conditional path after classification node
workflow.add_conditional_edges(
    "classify",
    routing_after_classification,
    {
        "clarify": "clarify",
        "gather_context": "gather_context"
    }
)

# Connect sequential lines
workflow.add_edge("gather_context", "planner")
workflow.add_edge("planner", "safety_audit")
workflow.add_edge("clarify", END)
workflow.add_edge("safety_audit", END)

# Compile ready for runtime invocation
app = workflow.compile()
