import json
import logging
from typing import List

from langchain_core.tools import tool
from langchain_groq import ChatGroq

import config
import retrievers
import prompts
import output_parser as op

logger = logging.getLogger(__name__)

llm = ChatGroq(model=config.GROQ_MODEL, api_key=config.GROQ_API_KEY, temperature=0)

def format_chunks(chunks: List[dict]) -> str:
    if not chunks:
        return "No relevant policy content retrieved."
    parts = []
    for c in chunks:
        header = f"[{c.get('policy_domain', 'UNKNOWN')} | {c.get('source_file', '')} | {c.get('chunk_id', '')}]"
        content = c.get('content', '').strip()[:600]
        parts.append(f"{header}\n{content}")
    return "\n\n---\n\n".join(parts)


def extract_chunks(raw) -> List[dict]:
    try:
        data = json.loads(raw) if isinstance(raw, str) else raw
        if isinstance(data, dict):
            return data.get("chunks", [])
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, TypeError):
        return []


@tool
def retrieve_hr_policy(query: str) -> str:
    """Search the HR leave policy. Use for questions about annual leave, sick leave, carry forward, unpaid leave, or leave approvals."""
    chunks = retrievers.retrieve_by_domain(query, "HR_LEAVE")
    if not chunks:
        return json.dumps({"chunks": [], "message": "No matching content in HR leave policy."})
    return json.dumps({"chunks": chunks})


@tool
def retrieve_travel_policy(query: str) -> str:
    """Search the travel policy. Use for questions about business travel approvals, domestic or international travel, same-day travel."""
    chunks = retrievers.retrieve_by_domain(query, "TRAVEL")
    if not chunks:
        return json.dumps({"chunks": [], "message": "No matching content in travel policy."})
    return json.dumps({"chunks": chunks})


@tool
def retrieve_reimbursement_policy(query: str) -> str:
    """Search the reimbursement policy. Use for questions about expense claims, meal limits, hotel reimbursement, receipts, or claim timelines."""
    chunks = retrievers.retrieve_by_domain(query, "REIMBURSEMENT")
    if not chunks:
        return json.dumps({"chunks": [], "message": "No matching content in reimbursement policy."})
    return json.dumps({"chunks": chunks})


@tool
def retrieve_it_security_policy(query: str) -> str:
    """Search the IT security policy. Use for questions about laptop usage, personal devices, passwords, public Wi-Fi, or data storage."""
    chunks = retrievers.retrieve_by_domain(query, "IT_SECURITY")
    if not chunks:
        return json.dumps({"chunks": [], "message": "No matching content in IT security policy."})
    return json.dumps({"chunks": chunks})


@tool
def retrieve_ai_usage_policy(query: str) -> str:
    """Search the AI usage policy. Use for questions about public AI tools, customer data in AI, approved AI tools, or AI governance."""
    chunks = retrievers.retrieve_by_domain(query, "AI_USAGE")
    if not chunks:
        return json.dumps({"chunks": [], "message": "No matching content in AI usage policy."})
    return json.dumps({"chunks": chunks})


@tool
def rewrite_query(original_question: str, missing_info: str, domains: str) -> str:
    """Rewrite a weak query to improve retrieval. Pass original question, what was missing, and target domains as plain strings."""
    prompt = prompts.QUERY_REWRITER_PROMPT.format(
        question=original_question,
        missing_info=missing_info or "not specified",
        domains=domains or "general policy",
    )
    response = llm.invoke(prompt)
    return json.dumps({"rewritten_query": response.content.strip()})


@tool
def generate_grounded_answer(question: str, context_json: str) -> str:
    """Generate a policy answer using only retrieved context. Pass the question and the JSON output from retrieve tools."""
    chunks = extract_chunks(context_json)
    context_text = format_chunks(chunks)

    if context_text == "No relevant policy content retrieved.":
        return json.dumps({
            "answer": "The policy documents do not contain information that covers this question.",
            "policy_basis": [],
            "sources": [],
            "answerability": "NOT_FOUND",
            "confidence": "LOW",
            "recommended_next_step": "Contact the relevant policy owner — HR, Finance, IT Security, or AI Governance.",
        })

    prompt = prompts.ANSWER_GENERATOR_PROMPT.format(question=question, context=context_text)
    response = llm.invoke(prompt)
    result = op.parse_json_response(response.content, "generate_grounded_answer")

    if not result:
        return json.dumps({
            "answer": response.content.strip(),
            "policy_basis": [],
            "sources": [],
            "answerability": "PARTIALLY_ANSWERED",
            "confidence": "LOW",
            "recommended_next_step": "Review the source policy document directly.",
        })

    return json.dumps(result)

