from typing import TypedDict,List, Dict, Optional
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from config import GROQ_API_KEY,GROQ_MODEL
from prompts import SYSTEM_PROMPT,TROUBLESHOOTING_RETERIVAL_TOOL,ISSUE_CLASSIFICATION
from tools import safety_review_node,final_response_node,classify_issue_node,retrieve_guidance_node,parallel_context_node,diagnostic_decision_node,clarification_node,escalation_node,resolution_planner_node

llm = ChatGroq(api_key=GROQ_API_KEY,model=GROQ_MODEL,temperature=0)

from typing import TypedDict, List, Dict, Optional
class TroubleshootingState(TypedDict):
    """
    Represents the state of our query routing workflow.
    """
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

workflow = StateGraph(TroubleshootingState)
workflow.add_node("classify_issue_node",classify_issue_node)
workflow.add_node("retrieve_guidance_node",retrieve_guidance_node)
workflow.add_node("parallel_context_node",parallel_context_node)
workflow.add_node("diagnostic_decision_node",diagnostic_decision_node)
workflow.add_node("clarification_node",clarification_node)
workflow.add_node("resolution_planner_node",resolution_planner_node)
workflow.add_node("escalation_node",escalation_node)
workflow.add_node("safety_review_node",safety_review_node)
workflow.add_node("final_response_node",final_response_node)

workflow.add_edge(START,"classify_issue_node")
workflow.add_conditional_edges("clarification_node",clarification_node,{
        "parallel_context_node":"parallel_context_node",})
workflow.add_edge("parallel_retrieval","context_grader")
workflow.add_conditional_edges("diagnostic_decision_node",escalation_node,{
        "ansclarification_nodeer":"clarification_node",})


graph = workflow.compile()