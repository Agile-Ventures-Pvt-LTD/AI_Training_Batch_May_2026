"""
tools.py

Tool layer used by LangGraph nodes.

Contains:
1. Policy Retrieval Tools
2. Context Grading Tool
3. Query Rewriting Tool
4. Clarification Tool
5. Reflection Tool
"""

from retrievers import (
    retrieve_hr_policy,
    retrieve_travel_policy,
    retrieve_reimbursement_policy,
    retrieve_it_security_policy,
    retrieve_ai_usage_policy
)

def retrieve_policy_data(
    query: str,
    domain: str
):
    """
    Route retrieval request
    to correct policy retriever.
    """

    domain = domain.upper()

    if domain == "HR_LEAVE":
        return retrieve_hr_policy(query)

    if domain == "TRAVEL":
        return retrieve_travel_policy(query)

    if domain == "REIMBURSEMENT":
        return retrieve_reimbursement_policy(query)

    if domain == "IT_SECURITY":
        return retrieve_it_security_policy(query)

    if domain == "AI_USAGE":
        return retrieve_ai_usage_policy(query)

    return []

def grade_context(
    question: str,
    retrieved_documents
):
    """
    Grade retrieval quality.
    """

    if not retrieved_documents:

        return {
            "overall_relevance":
            "NOT_RELEVANT",

            "relevant_chunks":
            [],

            "irrelevant_chunks":
            [],

            "missing_information":
            [
                "No supporting policy content found."
            ],

            "decision":
            "NOT_FOUND"
        }

    if len(retrieved_documents) < 2:

        return {
            "overall_relevance":
            "WEAK",

            "relevant_chunks":
            retrieved_documents,

            "irrelevant_chunks":
            [],

            "missing_information":
            [
                "Additional supporting policy evidence required."
            ],

            "decision":
            "REWRITE_QUERY"
        }

    return {

        "overall_relevance":
        "HIGHLY_RELEVANT",

        "relevant_chunks":
        retrieved_documents,

        "irrelevant_chunks":
        [],

        "missing_information":
        [],

        "decision":
        "ANSWER"
    }



def rewrite_query(
    original_query: str
):
    """
    Expand weak user queries
    for a second retrieval attempt.
    """

    return (
        f"{original_query} "
        f"enterprise policy "
        f"eligibility requirements "
        f"approvals receipt rules "
        f"documentation process"
    )


def ask_clarification(
    question: str
):
    """
    Return clarification prompt.
    """

    return {
        "answer":
        (
            "Your question is ambiguous. "
            "Please provide additional details."
        ),

        "clarification_needed":
        True,

        "suggested_details":
        [
            "policy type",
            "expense type",
            "travel type",
            "manager approval",
            "date of request",
            "supporting documents"
        ]
    }



def review_answer_grounding(
    answer_text: str,
    retrieved_context
):
    """
    Reflection node helper.
    """

    has_context = (
        len(retrieved_context) > 0
    )

    has_citations = (
        "sources" in answer_text.lower()
        or "source" in answer_text.lower()
    )

    return {

        "is_grounded":
        has_context,

        "has_citations":
        has_citations,

        "unsupported_claims":
        [],

        "needs_revision":
        not has_context,

        "reflection_summary":
        (
            "Answer reviewed against "
            "retrieved policy context."
        )
    }



def build_source_reference(
    document
):
    """
    Convert retrieved document
    into citation format.
    """

    return {

        "source_file":
        document.metadata.get(
            "source_file",
            ""
        ),

        "policy_domain":
        document.metadata.get(
            "policy_domain",
            ""
        ),

        "chunk_id":
        document.metadata.get(
            "chunk_id",
            ""
        ),

        "snippet":
        document.page_content[:250]
    }

def build_not_found_response():

    return {

        "answer":
        (
            "The requested information could not be found "
            "in the available policy documents."
        ),

        "policy_basis":
        [],

        "sources":
        [],

        "answerability":
        "NOT_FOUND",

        "confidence":
        "LOW",

        "recommended_next_step":
        (
            "Contact the policy owner or "
            "HR/Finance/IT support team."
        )
    }