import json
import config
from typing import TypedDict, List, Dict, Optional
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from retrievers import get_vectorstore, retrieve_hr_policy, retrieve_travel_policy, retrieve_reimbursement_policy, retrieve_it_security_policy, retrieve_ai_usage_policy
from prompts import QUERY_CLASSIFIER_PROMPT, CONTEXT_GRADER_PROMPT, QUERY_REWRITER_PROMPT, ANSWER_GENERATOR_PROMPT, REFLECTION_PROMPT, CLARIFICATION_PROMPT
from output_parser import parse_classifier, parse_grader, parse_answer, parse_reflection, parse_clarification

llm = ChatGroq(api_key=config.GROQ_API_KEY, model=config.GROQ_MODEL, temperature=0)

class PolicyAgentState(TypedDict):
    user_question: str
    query_type: str
    required_policy_domains: List[str]
    rewritten_query: Optional[str]
    retrieved_context: List[Dict]
    context_grade: Dict
    answer: Dict
    reflection: Dict
    retry_count: int
    final_response: str
    clarification_needed: bool
    clarification_question: str

vectorstore = None

def get_vs():
    global vectorstore
    if vectorstore is None:
        vectorstore = get_vectorstore()
    return vectorstore

def query_classifier_node(state: PolicyAgentState) -> PolicyAgentState:
    question = state["user_question"]
    prompt = f"{QUERY_CLASSIFIER_PROMPT}\n\nUser question: {question}\n\nReturn JSON:"
    msg = llm.invoke(prompt)
    data = parse_classifier(msg.content)
    state["query_type"] = data.get("query_type", "OTHER")
    state["required_policy_domains"] = data.get("required_policy_domains", [])
    state["clarification_needed"] = data.get("requires_clarification", False)
    return state

def parallel_retrieval_node(state: PolicyAgentState) -> PolicyAgentState:
    vs = get_vs()
    question = state.get("rewritten_query") or state["user_question"]
    domains = state["required_policy_domains"]
    if not domains:
        domains = [state["query_type"]] if state["query_type"] not in ["MULTI_POLICY", "AMBIGUOUS", "UNANSWERABLE", "OTHER"] else []
    all_results = []
    retriever_map = {
        "HR_LEAVE": retrieve_hr_policy,
        "TRAVEL": retrieve_travel_policy,
        "REIMBURSEMENT": retrieve_reimbursement_policy,
        "IT_SECURITY": retrieve_it_security_policy,
        "AI_USAGE": retrieve_ai_usage_policy,
    }
    for d in domains:
        fn = retriever_map.get(d)
        if fn:
            results = fn(vs, question)
            for doc, score in results:
                all_results.append({
                    "policy_domain": d,
                    "source_file": doc.metadata.get("source_file", ""),
                    "chunk_id": doc.metadata.get("chunk_id", ""),
                    "content": doc.page_content,
                    "relevance_score": float(score),
                })
    state["retrieved_context"] = all_results
    return state

def context_grader_node(state: PolicyAgentState) -> PolicyAgentState:
    question = state.get("rewritten_query") or state["user_question"]
    context = state["retrieved_context"]
    context_str = json.dumps([{"content": c["content"], "source": c["source_file"], "chunk_id": c["chunk_id"]} for c in context], indent=2)
    prompt = f"{CONTEXT_GRADER_PROMPT}\n\nQuestion: {question}\n\nRetrieved context:\n{context_str}\n\nReturn JSON:"
    msg = llm.invoke(prompt)
    grade = parse_grader(msg.content)
    state["context_grade"] = grade
    return state

def query_rewriter_node(state: PolicyAgentState) -> PolicyAgentState:
    question = state["user_question"]
    missing = state["context_grade"].get("missing_information", [])
    prompt = QUERY_REWRITER_PROMPT.format(question=question, missing_info="; ".join(missing) if missing else "query was too vague")
    msg = llm.invoke(prompt)
    state["rewritten_query"] = msg.content.strip()
    state["retry_count"] += 1
    return state

def answer_generator_node(state: PolicyAgentState) -> PolicyAgentState:
    question = state.get("rewritten_query") or state["user_question"]
    context = state["retrieved_context"]
    context_str = json.dumps([{"source_file": c["source_file"], "policy_domain": c["policy_domain"], "chunk_id": c["chunk_id"], "content": c["content"]} for c in context], indent=2)
    prompt = f"{ANSWER_GENERATOR_PROMPT}\n\nQuestion: {question}\n\nRetrieved context:\n{context_str}\n\nReturn JSON:"
    msg = llm.invoke(prompt)
    answer = parse_answer(msg.content)
    state["answer"] = answer
    return state

def reflection_node(state: PolicyAgentState) -> PolicyAgentState:
    answer = state["answer"]
    context = state["retrieved_context"]
    context_str = json.dumps([{"source_file": c["source_file"], "content": c["content"][:200]} for c in context], indent=2)
    prompt = f"{REFLECTION_PROMPT}\n\nAnswer: {json.dumps(answer, indent=2)}\n\nRetrieved context:\n{context_str}\n\nReturn JSON:"
    msg = llm.invoke(prompt)
    reflection = parse_reflection(msg.content)
    state["reflection"] = reflection
    return state

def clarification_response_node(state: PolicyAgentState) -> PolicyAgentState:
    question = state["user_question"]
    prompt = f"{CLARIFICATION_PROMPT}\n\nUser question: {question}\n\nReturn JSON:"
    msg = llm.invoke(prompt)
    cl = parse_clarification(msg.content)
    state["clarification_question"] = cl.get("clarification_question", "Please clarify your question.")
    state["final_response"] = f"Clarification needed: {state['clarification_question']}\n\nPlease provide more specific information so I can help with the right policy."
    return state

def final_response_node(state: PolicyAgentState) -> PolicyAgentState:
    answer = state["answer"]
    reflection = state["reflection"]
    lines = []
    lines.append(f"Answer: {answer.get('answer', 'No answer available.')}")
    lines.append("")
    if answer.get("policy_basis"):
        lines.append("Policy Basis:")
        for pb in answer["policy_basis"]:
            lines.append(f"- {pb}")
        lines.append("")
    if answer.get("sources"):
        lines.append("Sources:")
        for s in answer["sources"]:
            lines.append(f"- {s.get('source_file','')} ({s.get('policy_domain','')}) - {s.get('chunk_id','')}: {s.get('snippet','')[:100]}...")
        lines.append("")
    lines.append(f"Answerability: {answer.get('answerability', 'UNKNOWN')}")
    lines.append(f"Confidence: {answer.get('confidence', 'LOW')}")
    lines.append(f"Recommended Next Step: {answer.get('recommended_next_step', 'Contact relevant policy owner.')}")
    lines.append("")
    if reflection.get("is_grounded") == False:
        lines.append("Note: This answer may not be fully grounded in policy evidence. Please verify with the policy owner.")
    if reflection.get("unsupported_claims"):
        lines.append(f"Unsupported claims identified: {', '.join(reflection['unsupported_claims'])}")
    lines.append("")
    
    state["final_response"] = "\n".join(lines)
    return state

def should_clarify(state: PolicyAgentState) -> str:
    if state.get("clarification_needed", False) or state["query_type"] == "AMBIGUOUS":
        return "clarification"
    return "retrieve"

def should_rewrite(state: PolicyAgentState) -> str:
    decision = state["context_grade"].get("decision", "NOT_FOUND")
    if decision == "REWRITE_QUERY" and state["retry_count"] < 1:
        return "rewrite"
    elif decision == "ASK_CLARIFICATION":
        return "clarify"
    elif decision == "NOT_FOUND":
        return "not_found"
    return "answer"

def should_reflect(state: PolicyAgentState) -> str:
    if state["reflection"].get("needs_revision", False):
        return "revise"
    return "finalize"

def build_graph():
    builder = StateGraph(PolicyAgentState)
    builder.add_node("query_classifier", query_classifier_node)
    builder.add_node("parallel_retrieval", parallel_retrieval_node)
    builder.add_node("context_grader", context_grader_node)
    builder.add_node("query_rewriter", query_rewriter_node)
    builder.add_node("answer_generator", answer_generator_node)
    builder.add_node("reflection", reflection_node)
    builder.add_node("final_response", final_response_node)
    builder.add_node("clarification_response", clarification_response_node)

    builder.set_entry_point("query_classifier")

    builder.add_conditional_edges("query_classifier", should_clarify, {
        "clarification": "clarification_response",
        "retrieve": "parallel_retrieval",
    })
    builder.add_edge("parallel_retrieval", "context_grader")
    builder.add_conditional_edges("context_grader", should_rewrite, {
        "rewrite": "query_rewriter",
        "clarify": "clarification_response",
        "not_found": "final_response",
        "answer": "answer_generator",
    })
    builder.add_edge("query_rewriter", "parallel_retrieval")
    builder.add_edge("answer_generator", "reflection")
    builder.add_conditional_edges("reflection", should_reflect, {
        "revise": "answer_generator",
        "finalize": "final_response",
    })
    builder.add_edge("clarification_response", END)
    builder.add_edge("final_response", END)

    return builder.compile()

def run_policy_assistant(question: str):
    graph = build_graph()
    initial = PolicyAgentState(
        user_question=question,
        query_type="",
        required_policy_domains=[],
        rewritten_query=None,
        retrieved_context=[],
        context_grade={},
        answer={},
        reflection={},
        retry_count=0,
        final_response="",
        clarification_needed=False,
        clarification_question="",
    )
    result = graph.invoke(initial)
    return result["final_response"]