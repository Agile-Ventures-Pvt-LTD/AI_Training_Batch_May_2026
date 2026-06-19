# file: tools.py

from langchain_core.tools import tool

from retrievers import search_policy


@tool
def retrieve_hr_policy(query: str):
    """Search HR leave policy."""
    return search_policy(query, "hr_leave_policy")


@tool
def retrieve_travel_policy(query: str):
    """Search travel policy."""
    return search_policy(query, "travel_policy")


@tool
def retrieve_reimbursement_policy(query: str):
    """Search reimbursement policy."""
    return search_policy(query, "reimbursement_policy")


@tool
def retrieve_it_security_policy(query: str):
    """Search IT security policy."""
    return search_policy(query, "it_security_policy")


@tool
def retrieve_ai_usage_policy(query: str):
    """Search AI usage policy."""
    return search_policy(query, "ai_usage_policy")


@tool
def grade_context(context: str):
    """
    Check whether retrieved context is useful.
    """

    if context and len(str(context)) > 50:
        return "ANSWER"

    return "REWRITE_QUERY"