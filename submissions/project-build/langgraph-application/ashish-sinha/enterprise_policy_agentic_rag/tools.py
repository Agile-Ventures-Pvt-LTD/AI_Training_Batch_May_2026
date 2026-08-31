# from langchain.tools import StructuredTool
# from langchain_core.tools import tool
# from langchain_core.documents import Document
# from retrievers import Retriever
# import os
# from config import llm
# from prompts import *

# retrieve = Retriever(vector_store=os.getenv('VECTOR_STORE_PATH'))


# def retrieve_hr_policy(question:str) -> str:
#     """
#     You have to retrieve the relevant HR Policy from hr_leave_policy 
#     """
#     docs = retrieve.retrieve_policies_chunks(
#         query=question,
#         policy_domain="HR_LEAVE"
#     )

#     return retrieve.formatted_context(docs)

# def retrieve_travel_policy(question: str) -> str:
#     """
#     You have to retrieve relevant travel policy information from travel_policy.
#     """

#     docs = retrieve.retrieve_policies_chunks(query=question,policy_domain="TRAVEL")
#     return retrieve.formatted_docs(docs)


# def retrieve_reimbursement_policy(question: str) -> str:
#     """
#     You have to retrieve relevant reimbursement policy information from the reimbursement_policy.
#     """

#     docs = retrieve.retrieve_policies_chunks(query=question,policy_domain="REIMBURSEMENT")
#     return retrieve.formatted_context(docs)

# def retrieve_it_security_policy(question: str) -> str:
#     """
#     You have to retrieve relevant IT security policy information from the it_security_policy file.
#     """

#     docs = retrieve.retrieve_policies_chunks( query=question,policy_domain="IT_SECURITY")
#     return retrieve.formatted_context(docs)

# def retrieve_ai_usage_policy(question: str) -> str:
#     """
#     you have to retrieve relevant AI usage policy information from the ai_usage_policy file.
#     """

#     docs = retrieve.retrieve_policies_chunks(query=question, policy_domain="AI_USAGE")
#     return retrieve.formatted_context(docs)

# def grade_context(question: str,context: str) -> str:
#     """
#     Grade retrieved context.
#     """

#     prompt = grade_context_prompt

#     return llm.invoke(prompt).content.strip()

# def rewrite_query(question: str) -> str:
#     """
#     Rewrite the query for better retrieval.
#     """
#     prompt = rewrite_query_prompt
#     return llm.invoke(prompt).content.strip()

# def ask_clarification(question: str) -> str:
#     """
#     Generate a clarification question.
#     """

#     prompt = ask_clarification_prompt

#     return llm.invoke(prompt).content.strip()

# def generate_grounded_answer(question: str,context: str) -> str:
#     """
#     Generate answer using retrieved policy context only.
#     """

#     prompt = generate_grounded_answer_promot

#     return llm.invoke(prompt).content.strip()


# def review_answer_grounding(answer: str,context: str) -> str:
#     """
#     Verify whether the answer is grounded in retrieved evidence.
#     """

#     prompt = review_answer_grounding_prompt

#     return llm.invoke(prompt).content.strip()

# retrieve_hr_policy_tool= StructuredTool.from_function(retrieve_hr_policy)
# retrieve_ai_usage_policy_tool = StructuredTool.from_function(retrieve_ai_usage_policy)
# retrieve_it_security_policy_tool = StructuredTool.from_function(retrieve_it_security_policy)
# retrieve_reimbursement_policy_tool = StructuredTool.from_function(retrieve_reimbursement_policy)
# retrieve_travel_policy_tool = StructuredTool.from_function(retrieve_travel_policy)
# grade_context_tool = StructuredTool.from_function(grade_context)
# rewrite_query_tool = StructuredTool.from_function(rewrite_query)
# ask_clarification_tool = StructuredTool.from_function(ask_clarification)
# generate_grounded_answer_tool = StructuredTool.from_function(generate_grounded_answer)
# review_answer_grounding_tool = StructuredTool.from_function(review_answer_grounding)

# tools = [retrieve_ai_usage_policy_tool,retrieve_hr_policy_tool,retrieve_it_security_policy_tool,retrieve_reimbursement_policy_tool,retrieve_travel_policy_tool,grade_context_tool,rewrite_query_tool,ask_clarification_tool,generate_grounded_answer_tool,review_answer_grounding_tool]


import os
from langchain.tools import StructuredTool
from langchain_core.tools import tool
from retrievers import Retriever
from chunking import load_vector_store 
from config import llm
from prompts import (
    grade_context_prompt,
    rewrite_query_prompt,
    ask_clarification_prompt,
    generate_grounded_answer_promot, 
    review_answer_grounding_prompt
)

vector_store_instance = load_vector_store()
retrieve = Retriever(vector_store=vector_store_instance)

def retrieve_hr_policy(question: str) -> str:
    """Retrieve relevant HR and leave policy information from the hr_leave_policy file."""
    docs = retrieve.retrieve_policies_chunks(query=question, policy_domain="HR_LEAVE")
    return retrieve.formatted_context(docs)

def retrieve_travel_policy(question: str) -> str:
    """Retrieve relevant business travel policy information from the travel_policy file."""
    docs = retrieve.retrieve_policies_chunks(query=question, policy_domain="TRAVEL")
    return retrieve.formatted_context(docs)

def retrieve_reimbursement_policy(question: str) -> str:
    """Retrieve relevant reimbursement policy information from the reimbursement_policy file."""
    docs = retrieve.retrieve_policies_chunks(query=question, policy_domain="REIMBURSEMENT")
    return retrieve.formatted_context(docs)

def retrieve_it_security_policy(question: str) -> str:
    """Retrieve relevant IT security and usage policy information from the it_security_policy file."""
    docs = retrieve.retrieve_policies_chunks(query=question, policy_domain="IT_SECURITY")
    return retrieve.formatted_context(docs)

def retrieve_ai_usage_policy(question: str) -> str:
    """Retrieve relevant corporate generative AI usage policy guidelines from the ai_usage_policy file."""
    docs = retrieve.retrieve_policies_chunks(query=question, policy_domain="AI_USAGE")
    return retrieve.formatted_context(docs)

def grade_context(question: str, context: str) -> str:
    """Grade whether the retrieved context contains relevant policy evidence."""
    formatted_prompt = grade_context_prompt.format(question=question, context=context)
    return llm.invoke(formatted_prompt).content.strip()

def rewrite_query(question: str) -> str:
    """Rewrite or optimize the policy query statement for better vector database search precision."""
    formatted_prompt = rewrite_query_prompt.format(question=question)
    return llm.invoke(formatted_prompt).content.strip()

def ask_clarification(question: str) -> str:
    """Generate an explicit, polite clarification response if the user query is missing vital constraints."""
    formatted_prompt = ask_clarification_prompt.format(question=question)
    return llm.invoke(formatted_prompt).content.strip()

def generate_grounded_answer(question: str, context: str) -> str:
    """Generate a structured corporate policy response using strictly verified retrieved context information only."""
    formatted_prompt = generate_grounded_answer_promot.format(question=question, context=context)
    return llm.invoke(formatted_prompt).content.strip()

def review_answer_grounding(answer: str, context: str) -> str:
    """Perform hallucination checking validation loops to ensure claims are grounded in context evidence summaries."""
    formatted_prompt = review_answer_grounding_prompt.format(answer=answer, context=context)
    return llm.invoke(formatted_prompt).content.strip()

retrieve_hr_policy_tool = StructuredTool.from_function(retrieve_hr_policy)
retrieve_ai_usage_policy_tool = StructuredTool.from_function(retrieve_ai_usage_policy)
retrieve_it_security_policy_tool = StructuredTool.from_function(retrieve_it_security_policy)
retrieve_reimbursement_policy_tool = StructuredTool.from_function(retrieve_reimbursement_policy)
retrieve_travel_policy_tool = StructuredTool.from_function(retrieve_travel_policy)
grade_context_tool = StructuredTool.from_function(grade_context)
rewrite_query_tool = StructuredTool.from_function(rewrite_query)
ask_clarification_tool = StructuredTool.from_function(ask_clarification)
generate_grounded_answer_tool = StructuredTool.from_function(generate_grounded_answer)
review_answer_grounding_tool = StructuredTool.from_function(review_answer_grounding)

tools = [
    retrieve_ai_usage_policy_tool,
    retrieve_hr_policy_tool,
    retrieve_it_security_policy_tool,
    retrieve_reimbursement_policy_tool,
    retrieve_travel_policy_tool,
    grade_context_tool,
    rewrite_query_tool,
    ask_clarification_tool,
    generate_grounded_answer_tool,
    review_answer_grounding_tool
]
