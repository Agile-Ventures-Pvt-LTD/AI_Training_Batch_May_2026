import json
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from retriever import retrieve_by_domain
from config import GROQ_MODEL
from prompts import CLASSIFY_PROMPT, GROUNDED_ANSWER_PROMPT

llm = ChatGroq(model=GROQ_MODEL, temperature=0)

#Tool 1
@tool
def search_policies(query: str) -> dict:
    """
    Searches enterprise policy documents for content relevant to the user's
    question. Use this tool for any and only questions about HR leave, travel,
    reimbursement, IT security, or AI usage policy.
    Classifies the question into one or more policy domains, then retrieves
    matching policy chunks from each relevant domain. If the question is
    too ambiguous to classify, returns requires_clarification=true instead
    of guessing and ask the user to clarify rather than
    answering.
    """
    print(f"Input: {query=}")

    response = llm.invoke(CLASSIFY_PROMPT.format(query=query))

    try:
        classification = json.loads(response.content)
    except json.JSONDecodeError:
        classification = {
            "query_type": "AMBIGUOUS",
            "required_policy_domains": [],
            "requires_parallel_retrieval": False,
            "requires_clarification": True,
            "reasoning_summary": "Failed to parse classifier output as JSON.",
        }

    if classification.get("requires_clarification") or not classification.get("required_policy_domains"):
        return {
            "classification": classification,
            "chunks": [],
            "status": "NEEDS_CLARIFICATION",
        }

    chunks = []
    for domain in classification["required_policy_domains"]:
        domain_chunks = retrieve_by_domain(query, domain)
        chunks.extend(domain_chunks)

    return {
        "classification": classification,
        "chunks": chunks,
        "status": "OK",
    }

#TOOL 2
@tool 

def generate_grounded_answer(query: str, retrieved_chunks: list) -> dict:
    """
    Generates a final answer to the user's policy question using only the
    provided retrieved policy chunks. Use this tool after search_policies
    has returned relevant chunks. The answer must include source citations
    for every claim. Never call this with an empty chunk list 
    If there are no chunks, the result will correctly report
    NOT_FOUND instead of guessing.
    """

    print(f"Input: {query=}, chunks={len(retrieved_chunks)}")

    if not retrieved_chunks:
        result = {
            "answer": "I could not find relevant policy information to answer this question.",
            "policy_basis": [],
            "sources": [],
            "answerability": "NOT_FOUND",
            "confidence": "LOW",
            "recommended_next_step": "Contact the relevant policy owner for guidance.",
        }
        print(f"\n*** Grounded Answer (no chunks, short-circuited) ***")
        return result

    prompt = GROUNDED_ANSWER_PROMPT.format(
        query=query,
        chunks_json=json.dumps(retrieved_chunks, indent=2),
    )
    response = llm.invoke(prompt)

    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        result = {
            "answer": "",
            "policy_basis": [],
            "sources": [],
            "answerability": "NOT_FOUND",
            "confidence": "LOW",
            "recommended_next_step": "Answer generation failed to parse; please retry the question.",
        }

    if result.get("answer") and not result.get("sources"):
        result["confidence"] = "LOW"
        result["answerability"] = "PARTIALLY_ANSWERED"

    print(f"\n*** Grounded Answer ***")
    return result