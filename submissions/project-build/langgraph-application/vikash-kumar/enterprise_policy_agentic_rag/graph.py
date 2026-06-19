from typing import TypedDict,List, Dict, Optional
from langgraph.graph import StateGraph,START,END
from langchain_groq import ChatGroq
from config import GROQ_API_KEY,GROQ_MODEL
from prompts import CLASSIFIER_PROMPT,CONTEXT_GRADER_PROMPT,QUERY_REWRITE_PROMPT,ANSWER_PROMPT,REFLECTION_PROMPT
from tools import query_classifier_node,parallel_retrieval_node,context_grader_node,query_rewriter_node,answer_generator_node,reflection_node,final_response_node,route_after_classifier,route_after_grader,route_after_reflection

llm = ChatGroq(api_key=GROQ_API_KEY,model=GROQ_MODEL,temperature=0)

class PolicyAgentState(TypedDict):
    """
    Represents the state of the query routing workflow.
    """
    user_question: str
    query_type: str
    required_policy_domains: list
    requires_clarification: bool
    rewritten_query: str
    retrieved_context: list
    context_grade: dict
    answer: dict
    reflection: dict
    retry_count: int
    final_response: str


workflow = StateGraph(PolicyAgentState)
workflow.add_node("query_classifier",query_classifier_node)
workflow.add_node("parallel_retrieval",parallel_retrieval_node)
workflow.add_node("context_grader",context_grader_node)
workflow.add_node("query_rewriter",query_rewriter_node)
workflow.add_node("answer_generator",answer_generator_node)
workflow.add_node("reflection",reflection_node)
workflow.add_node("final_response",final_response_node)

workflow.add_edge(START,"query_classifier")
workflow.add_conditional_edges("query_classifier",route_after_classifier,{
        "clarification":"final_response",
        "retrieve":"parallel_retrieval"})
workflow.add_edge("parallel_retrieval","context_grader")
workflow.add_conditional_edges("context_grader",route_after_grader,{
        "answer":"answer_generator",
        "rewrite":"query_rewriter",
        "final":"final_response"})

workflow.add_edge("query_rewriter","parallel_retrieval")
workflow.add_edge("answer_generator","reflection")
workflow.add_conditional_edges("reflection",route_after_reflection,{"final":"final_response"})
workflow.add_edge("final_response",END)

graph = workflow.compile()