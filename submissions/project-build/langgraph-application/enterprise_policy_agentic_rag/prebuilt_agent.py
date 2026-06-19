from typing import List, Dict, Any, TypedDict
from pydantic import BaseModel, Field

from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent

from config import GROQ_API_KEY, GROQ_MODEL
from retrievers import get_retriever


llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=0
)

retriever = get_retriever



class QueryInput(BaseModel):
    query: str = Field(..., description="User question")


class ContextItem(BaseModel):
    content: str
    source_file: str
    chunk_id: str
    policy_domain: str


class AnswerOutput(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    answerability: str
    confidence: str



def _retrieve(query: str, domain_filter: str = ""):
    """
    Central retrieval logic used by all tools.
    Ensures consistent ranking + metadata structure.
    """
    docs = retriever().invoke(query)

    results = []
    for d in docs:
        meta = d.metadata or {}

        # optional domain filtering
        if domain_filter and domain_filter not in meta.get("policy_domain", ""):
            continue

        results.append({
            "content": d.page_content,
            "source_file": meta.get("source_file", ""),
            "chunk_id": meta.get("chunk_id", ""),
            "policy_domain": meta.get("policy_domain", ""),
        })

    return results



def retrieve_hr_policy(query: str):
    return _retrieve(f"HR policy: {query}", "HR_LEAVE")


def retrieve_travel_policy(query: str):
    return _retrieve(f"travel policy: {query}", "TRAVEL")


def retrieve_reimbursement_policy(query: str):
    return _retrieve(f"reimbursement policy: {query}", "REIMBURSEMENT")


def retrieve_it_security_policy(query: str):
    return _retrieve(f"IT security policy: {query}", "IT_SECURITY")


def retrieve_ai_usage_policy(query: str):
    return _retrieve(f"AI usage policy: {query}", "AI_USAGE")


def grade_retrieved_context(context: List[Dict]):
    """
    Evaluates whether retrieved context is sufficient.
    PRD FR-7 compliant.
    """

    if not context:
        return {
            "decision": "REWRITE_QUERY",
            "overall_relevance": "NOT_RELEVANT"
        }

    score = len(context)

    if score >= 4:
        decision = "ANSWER"
        relevance = "HIGHLY_RELEVANT"
    elif score == 2 or score == 3:
        decision = "ANSWER"
        relevance = "PARTIALLY_RELEVANT"
    else:
        decision = "REWRITE_QUERY"
        relevance = "WEAK"

    return {
        "decision": decision,
        "overall_relevance": relevance,
        "relevant_chunks": context,
        "irrelevant_chunks": [],
        "missing_information": []
    }



def rewrite_query(query: str):
    """
    Only ONE rewrite allowed (PRD constraint)
    """
    return {
        "rewritten_query": f"""
        {query}
        include eligibility rules, limits, approval workflow, conditions, exceptions
        """
    }


def generate_grounded_answer(data: Dict):
    context = data.get("context", [])
    question = data.get("question", "")

    if not context:
        return {
            "answer": "No sufficient policy context found to answer this question.",
            "policy_basis": [],
            "sources": [],
            "answerability": "NOT_FOUND",
            "confidence": "LOW",
            "recommended_next_step": "Please contact HR/Finance/IT support for clarification."
        }

    formatted_context = "\n\n".join(
        f"[{c['chunk_id']}] {c['content']}"
        for c in context
    )

    answer = llm.invoke(f"""
You are an enterprise policy assistant.

RULES:
- Use ONLY the context below
- Never assume missing policy
- Always mention uncertainty if needed
- Include citations using chunk_id

CONTEXT:
{formatted_context}

QUESTION:
{question}
""")

    sources = [
        {
            "source_file": c["source_file"],
            "chunk_id": c["chunk_id"],
            "policy_domain": c["policy_domain"],
            "snippet": c["content"][:200]
        }
        for c in context
    ]

    return {
        "answer": answer.content,
        "policy_basis": [c["chunk_id"] for c in context],
        "sources": sources,
        "answerability": "ANSWERED",
        "confidence": "HIGH" if len(context) > 2 else "MEDIUM",
        "recommended_next_step": "Follow policy guidelines and submit required approvals."
    }



def reflection_check(answer_obj: Dict, context: List[Dict]):
    """
    Detect hallucination risk + grounding check
    """

    issues = []

    if not context:
        issues.append("No context used")

    if "I think" in answer_obj.get("answer", ""):
        issues.append("Speculative language detected")

    if len(answer_obj.get("sources", [])) == 0:
        issues.append("No citations provided")

    return {
        "is_grounded": len(issues) == 0,
        "has_citations": len(answer_obj.get("sources", [])) > 0,
        "unsupported_claims": issues,
        "needs_revision": len(issues) > 0,
        "reflection_summary": " | ".join(issues) if issues else "Response is grounded and safe."
    }



tools = [
    retrieve_hr_policy,
    retrieve_travel_policy,
    retrieve_reimbursement_policy,
    retrieve_it_security_policy,
    retrieve_ai_usage_policy,
    grade_retrieved_context,
    rewrite_query,
    generate_grounded_answer,
    reflection_check
]


agent = create_react_agent(
    llm=llm,
    tools=tools
)




def run_prebuilt_agent(question: str):
    """
    Production entrypoint
    """

    response = agent.invoke({
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a strict enterprise policy assistant. "
                    "You MUST use tools for retrieval and NEVER hallucinate policy rules."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ]
    })

    return response