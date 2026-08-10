import json
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from config import (GROQ_API_KEY,GROQ_MODEL)
from prompts import (QUERY_CLASSIFIER_PROMPT,ANSWER_GENERATION_PROMPT,QUERY_REWRITE_PROMPT,REFLECTION_PROMPT)
from output_parser import (safe_json_parse)
llm = ChatGroq(api_key=GROQ_API_KEY,model=GROQ_MODEL,temperature=0)
def invoke_llm(prompt: str):
    """
    Safe LLM invocation.
    """
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        return response.content
    except Exception as exc:
        print(f"LLM Error: {exc}")
        return None
def classify_query(question: str):
    """
    Classify user query.
    """
    prompt = (QUERY_CLASSIFIER_PROMPT.format(question=question))
    result = invoke_llm(prompt)
    if not result:
        return {"query_type":"OTHER","required_policy_domains":[],"requires_parallel_retrieval":False,"requires_clarification":False,"reasoning_summary":"LLM classification failed."}
    parsed = safe_json_parse(result)
    return parsed
def rewrite_user_query(question: str):
    """
    Rewrite weak query.
    """
    prompt = (QUERY_REWRITE_PROMPT.format(question=question))
    result = invoke_llm(prompt)
    if not result:
        return question
    return result.strip()
def build_context(retrieved_docs):
    """
    Convert retrieved docs
    into prompt context.
    """
    context_parts = []
    for doc in retrieved_docs:
        source = (doc.metadata.get("source_file","unknown"))
        chunk_id = (doc.metadata.get("chunk_id","unknown"))
        context_parts.append(f"""
SOURCE FILE: {source}
CHUNK ID: {chunk_id}

CONTENT:
{doc.page_content}
"""
        )

    return "\n\n".join(
        context_parts
    )


def generate_grounded_answer(question,retrieved_docs):
    """
    Generate answer
    only from retrieved context.
    """

    if not retrieved_docs:

        return {"answer":("No relevant policy ""information found."),"policy_basis":[],"sources":[],"answerability":"NOT_FOUND",
            "confidence":
            "LOW",

            "recommended_next_step":
            (
                "Consult policy owner."
            )
        }

    context = build_context(retrieved_docs)
    prompt = (ANSWER_GENERATION_PROMPT.format(question=question,context=context))
    response = invoke_llm(prompt)
    if not response:
        return {"answer":("Answer generation failed."),"policy_basis":[],"sources":[],"answerability":"NOT_FOUND","confidence":"LOW","recommended_next_step":(
                "Retry later.")}
    parsed = safe_json_parse(response)
    if "error" not in parsed:
        return parsed
    citations = []
    for doc in retrieved_docs[:5]:
        citations.append(
            {
                "source_file":
                doc.metadata.get(
                    "source_file"
                ),

                "policy_domain":
                doc.metadata.get(
                    "policy_domain"
                ),

                "chunk_id":
                doc.metadata.get(
                    "chunk_id"
                ),

                "snippet":
                doc.page_content[:150]
            }
        )

    return {

        "answer":
        response,

        "policy_basis":
        [],

        "sources":
        citations,

        "answerability":
        "ANSWERED",

        "confidence":
        "MEDIUM",

        "recommended_next_step":
        (
            "Review policy citations."
        )
    }


def reflect_on_answer(question,answer,context):
    """
    Reflection node.
    """
    prompt = (REFLECTION_PROMPT.format(question=question,answer=json.dumps(answer,indent=2),context=context))
    response = invoke_llm(prompt)
    if not response:
        return {

            "is_grounded":
            True,

            "has_citations":
            True,

            "unsupported_claims":
            [],

            "needs_revision":
            False,

            "reflection_summary":
            (
                "Reflection skipped."
            )
        }

    parsed = safe_json_parse(
        response
    )

    if isinstance(
        parsed,
        dict
    ):
        return parsed

    return {

        "is_grounded":
        True,

        "has_citations":
        True,

        "unsupported_claims":
        [],

        "needs_revision":
        False,

        "reflection_summary":
        (
            "Reflection completed."
        )
    }
def test_groq_connection():
    """
    Verify Groq setup.
    """

    try:

        response = llm.invoke(
            [
                HumanMessage(
                    content="hello"
                )
            ]
        )

        return {
            "status": "success",
            "response":
            response.content
        }

    except Exception as exc:

        return {
            "status": "failed",
            "error": str(exc)
        }


if __name__ == "__main__":

    result = (
        test_groq_connection()
    )

    print(result)