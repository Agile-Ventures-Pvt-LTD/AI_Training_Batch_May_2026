from typing import TypedDict, List, Dict, Optional
import os
from langchain.schema import HumanMessage
from langchain_groq import ChatGroq
from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field
from mermaid import Mermaid
from config import llm

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import START, END, StateGraph

# from google.colab import userdata
from IPython.display import Image, display


def classify_query(user_query: str) -> str:
    """
    Classify the user query into one of the predefined categories"""

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that classifies user queries into one of these categories: HR_LEAVE, TRAVEL, REIMBURSEMENT, IT_SECURITY, AI_USAGE, MULTI_POLICY, UNANSWERABLE, AMBIGUOUS, OTHER. Return only JSON output."),
        ("user", user_query)
    ])

    classifier_chain = prompt_template | llm

    return classifier_chain.invoke({"user_query": user_query})

#=================================================================================================================

def retrieve_hr_policy(query: str, retriever) -> List[Dict[str, str]]:
    """
    Retrieve HR policy documents relevant to the user query.
    
    Args:
        query: The user's HR-related question
        retriever: The vectorstore retriever object
        
    Returns:
        List of relevant policy documents with content and metadata
    """
    try:
        documents = retriever.invoke(query)
        results = []
        for doc in documents:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A")
            })
        
        return results
    except Exception as e:
        return [{"error": f"Failed to retrieve HR policy: {str(e)}"}]


#==================================================================================================

def retrieve_travel_policy(query:str, retriever) -> List[Dict[str,str]]:
    """
    Retrieve travel policy documents relevant to user query and return list of relevant policy.
     Args:
        query: The user's travel policy related query
        retriever: The vectorstore retriever object
        
    Returns:
        List of relevant policy documents with content and metadata
    """
    try:
        documents = retriever.invoke(query)
        results = []
        for doc in documents:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A")
            })
        
        return results
    except Exception as e:
        return [{"error": f"Failed to retrieve travel policy: {str(e)}"}]
    
#===============================================================================

def retrieve_reimbursement_policy(query:str, retriever) -> List[Dict[str,str]]:
    """Retrive reimbursement policy documnets relevant to user query and return the policies in list.
     Args:
        query: The user ask reimbursement policy query
        retriever: The vectorstore retriever object
        
    Returns:
        List of relevant policy documents with content and metadata
    """
    try:
        documents = retriever.invoke(query)
        results = []
        for doc in documents:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A")
            })
        
        return results
    except Exception as e:
        return [{"error": f"Failed to retrieve reimbursement policy: {str(e)}"}]
    
#==================================================================================

def retrieve_it_security_policy(query:str, retriever) -> List[Dict[str, str]]:
    """Get the relevant IT Security policy relevant to user question and return the policies.
    Args:
        query: The user ask IT Security policy
        retriever: The vectorstore retriever object
        
    Returns:
        List of relevant policy documents with content and metadata
    """
    try:
        documents = retriever.invoke(query)
        results = []
        for doc in documents:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A")
            })
        
        return results
    except Exception as e:
        return [{"error": f"Failed to retrieve IT Security policy: {str(e)}"}]
    
#==========================================================================================================

def retrieve_ai_usage_policy(query:str, retriever) -> List[Dict[str, str]]:
    """Get the relevant AI Usage policy relevant to user query and get the policies.
    Args:
        query: The user ask for AI Usage policy
        retriever: The vectorstore retriever object
        
    Returns:
        List of relevant policy documents with content and metadata
    """
    try:
        documents = retriever.invoke(query)
        results = []
        for doc in documents:
            results.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
                "page": doc.metadata.get("page", "N/A")
            })
        
        return results
    except Exception as e:
        return [{"error": f"Failed to retrieve AI Usage policy: {str(e)}"}]
    
#===================================================================================

def generate_grounded_answer(query:str, retrieved_docs:List[Dict[str,str]]) -> str:
    """Generate a well grounded answer to the user question using the retrieved policies from the context."""
    context=" ".join([doc["content"] for doc in retrieved_docs if "content" in doc])

    prompts=f"""
    Your task is to generate grounded answers based on the relevat context provided to you.Always use context to provide answer.If the answer is not found from the context do not hallucinate or give any irrelevant answer, if you do not know the answer just say sorry answer not in the context retrived."""
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompts),
        ("user", f"Policy Context:\n{context}\n\nUser Question: {query}")
    ])
    
    try:
        chain = prompt_template | llm
        response = chain.invoke({"context": context, "query": query})
        return response.content
    except Exception as e:
        return f"Error: {str(e)}"
        



     

