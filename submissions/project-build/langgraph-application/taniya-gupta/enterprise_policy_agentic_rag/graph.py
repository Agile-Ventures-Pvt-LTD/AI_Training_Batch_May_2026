import json
from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END
import tools
import prompts
from output_parser import parse_json

class PolicyAgentState(TypedDict):
    user_question: str
    query_type: str
    required_policy_domains: List[str]
    requires_clarification: bool
    rewritten_query: Optional[str]
    retrieved_context: List[Dict]
    context_grade: Dict
    answer: Dict
    reflection: Dict
    final_response: str

# Helper function to format the chunk context, this maintains consistency
def format_context(chunks):
    return "".join(f"Source File: {c.get('source_file')} | Domain: {c.get('policy_domain')} | Chunk ID: {c.get('chunk_id')}\nContent: {c.get('content')}\n"for c in chunks)

def query_classifier_node(state: PolicyAgentState):
    llm = tools.get_llm()
    prompt = prompts.CLASSIFICATION_PROMPT.format(question=state["user_question"])
    res = llm.invoke(prompt)
    parsed = parse_json(res.content)
    return {
        "query_type": parsed.get("query_type", "general"),
        "required_policy_domains": list(set(parsed.get("required_policy_domains", []))),
        "requires_clarification": parsed.get("requires_clarification", False)
    }

def parallel_retrieval_node(state: PolicyAgentState):
    query = state.get("rewritten_query") or state["user_question"]
    retrieved_chunks = []
    for domain in state["required_policy_domains"]:
        res_json = tools.retrieve(query, domain)
        retrieved_chunks.extend(json.loads(res_json))
    return {"retrieved_context": retrieved_chunks}

def context_grader_node(state: PolicyAgentState):
    query = state.get("rewritten_query") or state["user_question"]
    llm = tools.get_llm()
    prompt = prompts.GRADER_PROMPT.format(query=query, context=format_context(state["retrieved_context"]))
    res = llm.invoke(prompt)
    return {"context_grade": parse_json(res.content)}

def query_rewriter_node(state: PolicyAgentState):
    query = state.get("rewritten_query") or state["user_question"]
    missing_info = ", ".join(state["context_grade"].get("missing_information", []))
    llm = tools.get_llm()
    prompt = prompts.REWRITER_PROMPT.format(query=query, missing_information=missing_info)
    res = llm.invoke(prompt)
    return {
        "rewritten_query": res.content.strip()
    }

def answer_generator_node(state: PolicyAgentState):
    query = state.get("rewritten_query") or state["user_question"]
    reflection = state.get("reflection", {})
    llm = tools.get_llm()
    if reflection.get("needs_revision", False):
        prompt = prompts.REVISER_PROMPT.format(
            query=query,
            context=format_context(state["retrieved_context"]),
            candidate_answer=json.dumps(state.get("answer", {})),
            feedback=reflection.get("reflection_summary", "")
        )
    else:
        prompt = prompts.GENERATOR_PROMPT.format(query=query, context=format_context(state["retrieved_context"]))
    res = llm.invoke(prompt)
    return {
        "answer": parse_json(res.content)
    }

def reflection_node(state: PolicyAgentState):
    llm = tools.get_llm()
    prompt = prompts.REVIEWER_PROMPT.format(
        context=format_context(state["retrieved_context"]),
        candidate_answer=json.dumps(state["answer"]))
    res = llm.invoke(prompt)
    return {"reflection": parse_json(res.content)}

def clarification_response_node(state: PolicyAgentState):
    llm = tools.get_llm()
    prompt = prompts.CLARIFICATION_PROMPT.format(query=state["user_question"])
    res = llm.invoke(prompt)
    return {"final_response": res.content}

def final_response_node(state: PolicyAgentState):
    grade = state.get("context_grade", {})
    if grade.get("decision") == "NOT_FOUND":
        fallback = {
            "answer": "I could not find any company policies matching your request.",
            "policy_basis": [],
            "sources": [],
            "answerability": "NOT_FOUND",
            "confidence": "LOW",
            "recommended_next_step": "Verify terms or contact HR for direct guidance."}
        return {"final_response": json.dumps(fallback, indent=2)}
    return {"final_response": json.dumps(state.get("answer", {}), indent=2)}

def route_after_classifier(state: PolicyAgentState):
    if state.get("requires_clarification", False):
        return "clarification_response_node"
    return "parallel_retrieval_node"

def route_after_grader(state: PolicyAgentState):
    grade = state.get("context_grade", {})
    decision = grade.get("decision", "ANSWER")
    if decision == "ANSWER":
        return "answer_generator_node"
    elif decision == "REWRITE_QUERY":
        return "query_rewriter_node"
    elif decision == "ASK_CLARIFICATION":
        return "clarification_response_node"
    else: 
        return "final_response_node"

def route_after_reflection(state: PolicyAgentState):
    reflection = state.get("reflection", {})
    if reflection.get("needs_revision", False):
        return "answer_generator_node"
    return "final_response_node"

def custom_agent():
    workflow = StateGraph(PolicyAgentState)
    
    workflow.add_node("query_classifier_node", query_classifier_node)
    workflow.add_node("parallel_retrieval_node", parallel_retrieval_node)
    workflow.add_node("context_grader_node", context_grader_node)
    workflow.add_node("query_rewriter_node", query_rewriter_node)
    workflow.add_node("answer_generator_node", answer_generator_node)
    workflow.add_node("reflection_node", reflection_node)
    workflow.add_node("clarification_response_node", clarification_response_node)
    workflow.add_node("final_response_node", final_response_node)
    
    workflow.set_entry_point("query_classifier_node")
    workflow.add_edge("parallel_retrieval_node", "context_grader_node")
    workflow.add_edge("query_rewriter_node", "parallel_retrieval_node")
    workflow.add_edge("answer_generator_node", "reflection_node")
    
    workflow.add_conditional_edges(
        "query_classifier_node",
        route_after_classifier,
        {
            "clarification_response_node": "clarification_response_node",
            "parallel_retrieval_node": "parallel_retrieval_node"})
    
    workflow.add_conditional_edges(
        "context_grader_node",
        route_after_grader,
        {
            "answer_generator_node": "answer_generator_node",
            "query_rewriter_node": "query_rewriter_node",
            "clarification_response_node": "clarification_response_node",
            "final_response_node": "final_response_node"})
    
    workflow.add_conditional_edges(
        "reflection_node",
        route_after_reflection,
        {
            "answer_generator_node": "answer_generator_node",
            "final_response_node": "final_response_node"})
    
    workflow.add_edge("clarification_response_node", END)
    workflow.add_edge("final_response_node", END)
    return workflow.compile()

def run_agent(query):
    agent = custom_agent()
    initial_state = {
        "user_question": query,
        "query_type": "",
        "required_policy_domains": [],
        "requires_clarification": False,
        "rewritten_query": None,
        "retrieved_context": [],
        "context_grade": {},
        "answer": {},
        "reflection": {},
        "final_response": ""
    }
    
    res = agent.invoke(initial_state)
    return parse_json(res["final_response"])