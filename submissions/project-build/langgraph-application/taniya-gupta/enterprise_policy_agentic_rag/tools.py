import os
import json
from langchain_core.tools import tool
from langchain_groq import ChatGroq
from config import config
import prompts
from output_parser import parse_json

vector_manager=None
def get_vector_store():
    global vector_manager
    if vector_manager is None:
        from loaders import Documentloader
        from chunking import Chunker
        from retrievers import Vectorstore

        loader=Documentloader()
        docs=loader.load()

        chunker=Chunker()
        chunks=chunker.split_documents(docs)

        vector_manager=Vectorstore()
        vector_manager.create_vector(chunks)
    return vector_manager

def get_llm():
    return ChatGroq(
        groq_api_key=config.GROQ_API_KEY,
        model_name=config.GROQ_MODEL,
        temperature=0
    )

def retrieve(query, domain):
    manager=get_vector_store()
    results=manager.retrieve_domain(query,domain)
    formatted=[]
    for i, doc in enumerate(results):
        formatted.append({
            "policy_domain": doc.metadata.get("policy_domain", domain),
            "source_file": doc.metadata.get("source_file", "could not get ource"),
            "chunk_id": doc.metadata.get("chunk_id", f"{domain}_chunk_{i}"),
            "content": doc.page_content,
            "relevance_score": 1.0
        })
    return json.dumps(formatted, indent=2)

@tool
def retrieve_hr(query: str):
    """retrieves context from HR leave policy that is relevant to query"""
    return retrieve(query, "HR_LEAVE")

@tool 
def retrieve_travel(query: str):
    """retrieves context from travel policy that is relevant to query"""
    return retrieve(query, "TRAVEL")

@tool
def retrieve_reimbursement(query: str):
    """retrieves context from reimbursement policy that is relevant to query"""
    return retrieve(query, "REIMBURSEMENT")

@tool 
def retrieve_it(query: str):
    """retrieves context from IT seacurity policy that is relevant to query"""
    return retrieve(query, "IT_SECURITY")

@tool
def retrieve_ai(query: str):
    """retrieves context from AI usage policy that is relevant to query"""
    return retrieve(query, "AI_USAGE")

@tool
def grade_context(query: str, context: str):
    """grades the relevance, acuuracy and ambiguity of the retrieved context for the query.
    returns a JSON containing overall_relevance, relevant_chunks, irrelevant_chunks, missing_information, and decision.
    """
    llm = get_llm()
    prompt = prompts.GRADER_PROMPT.format(query=query, context=context)
    response = llm.invoke(prompt)
    return response.content

@tool
def rewrite_query(query: str, missing_information: str = ""):
    """Rewrites the original query to improve retrieval based on missing information.
    Returns the rewritten query only.
    """
    llm = get_llm()
    prompt = prompts.REWRITER_PROMPT.format(query=query, missing_information=missing_information)
    response = llm.invoke(prompt)
    return response.content.strip()
    
@tool
def generate_answer(query: str, context: str):
    """Generates a structured answer based ONLY on the provided context.
    Returns JSON matching the final response schema that was given.
    """
    llm = get_llm()
    prompt = prompts.GENERATOR_PROMPT.format(query=query, context=context)
    response = llm.invoke(prompt)
    return response.content

@tool
def review_answer(candidate_answer: str, context: str):
    """Reviews the candidate answer with the retrieved context 
    Returns JSON matching the given schema.
    """
    llm = get_llm()
    prompt = prompts.REVIEWER_PROMPT.format(context=context, candidate_answer=candidate_answer)
    response = llm.invoke(prompt)
    return response.content

@tool
def ask_clarification(query: str):
    """Generates a structured clarification request when the query is ambiguous.
    Returns JSON matching the final response schema.
    """
    llm = get_llm()
    prompt = prompts.CLARIFICATION_PROMPT.format(query=query)
    response = llm.invoke(prompt)
    return response.content
