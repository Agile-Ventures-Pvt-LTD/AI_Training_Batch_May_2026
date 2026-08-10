from typing import Optional
from datetime import datetime, timedelta
from langchain_core.tools import tool

#Tool 1

@tool
def retrieve_hr_policy(query: str):
    """
    Return information about
    leave entitlement, carry forward, approvals, 
    unpaid leave.
    """

    return{
        
             "answer": "",
             "policy_basis": [],
             "sources": [],
             "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
             "confidence": "HIGH | MEDIUM | LOW",
             "recommended_next_step": ""
}

#Tool 2

@tool
def retrieve_travel_policy(query: str):
    """
    Retrieve travel information i.e, domestic travel, international travel 
    and travel approvals.
    """
    return {
             "answer": "",
             "policy_basis": [],
             "sources": [],
             "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
             "confidence": "HIGH | MEDIUM | LOW",
             "recommended_next_step": ""
        
    }

# Tool 3

@tool
def retrieve_reimbursement_policy(query: str):
    """
    Retrieve information about meals, hotel, transport, receipts, claim limit.
    """

    return {
             "answer": "",
             "policy_basis": [],
             "sources": [],
             "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
             "confidence": "HIGH | MEDIUM | LOW",
             "recommended_next_step": ""
        
    
}

# Tool 4

@tool
def retrieve_it_security_policy(
    customer_id: str,
):
    """
    Retrieve information about Laptop usage, password rules, device.
    """

    return {
            "answer": "",
             "policy_basis": [],
             "sources": [],
             "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
             "confidence": "HIGH | MEDIUM | LOW",
             "recommended_next_step": ""
    }


# Tool 5

@tool
def  retrieve_ai_usage_policy(query: str):
    """
    Retrieve information about public AI tool usage, customer data restrictions, approval process.

    """

    return {
             "answer": "",
             "policy_basis": [],
             "sources": [],
             "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
             "confidence": "HIGH | MEDIUM | LOW",
             "recommended_next_step": ""
        
}

# Tool 6

@tool
def  grade_context(query: str):
    """
    Provide grading to the context given.
    """

    return {
             "answer": "",
             "policy_basis": [],
             "sources": [],
             "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
             "confidence": "HIGH | MEDIUM | LOW",
             "recommended_next_step": ""
        
        }

# Tool 7

@tool
def rewrite_query(query: str):
    """
    Rewrite the query given by the user.
    """

    return {
             "answer": "",
             "policy_basis": [],
             "sources": [],
             "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
             "confidence": "HIGH | MEDIUM | LOW",
             "recommended_next_step": ""
    }

# Tool 8

@tool
def generate_grounded_answer(query: str):
    """
    Generate only grounded and truthful answers.
    """
    return {
             "answer": "",
             "policy_basis": [],
             "sources": [],
             "answerability": "ANSWERED | PARTIALLY_ANSWERED | NOT_FOUND | NEEDS_CLARIFICATION",
             "confidence": "HIGH | MEDIUM | LOW",
             "recommended_next_step": ""
    }
    

# Tool Registery

TOOLS = [
    retrieve_hr_policy,
    retrieve_travel_policy,
    retrieve_reimbursement_policy,
    retrieve_it_security_policy,
    retrieve_ai_usage_policy,
    grade_context,
    rewrite_query,
    generate_grounded_answer
    
]

