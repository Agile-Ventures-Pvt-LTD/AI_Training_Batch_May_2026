from typing import TypedDict, List, Dict, Optional
import json
import os
from langchain.schema import HumanMessage
from langchain_groq import ChatGroq
from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field
from mermaid import Mermaid
from config import MODEL_NAME, GROQ_API_KEY
from prompts import issue_prompt
from embeddings import get_embedding_model
from retrievers import get_retriever, search_knowledge_base
from vector_store import create_vectorstore
from db_utils import execute_query
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import START, END, StateGraph

# from google.colab import userdata
from IPython.display import Image, display

llm = ChatGroq(model=MODEL_NAME, groq_api_key=GROQ_API_KEY)


def issue_classifiction(user_query: str) -> str:
    """Classify the user query into one of the supported issue categories."""

    prompt_text = issue_prompt()
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", prompt_text),
        ("user", user_query)
    ])

    classifier_chain = prompt_template | llm
    response = classifier_chain.invoke({})
    text = response.content if hasattr(response, "content") else str(response)

    try:
        return json.loads(text)
    except Exception:
        return {"raw_classification": text}

#=====================================================================================================

def classify_and_retrieve(user_query: str, retriever=None) -> Dict[str, object]:
    """Classifies the incoming IT query and immediately fetches matching solutions."""
    raw_classification = issue_classifiction(user_query)
    if isinstance(raw_classification, dict):
        issue_type = raw_classification.get("issue_type", "UNKNOWN")
    else:
        issue_type = raw_classification.strip().upper() if raw_classification else "UNKNOWN"
    if retriever is None:
        embedding_engine = get_embedding_model()
        vector_db = create_vectorstore(embedding_engine)
        retriever = get_retriever(vector_db)
    search_text = f"{issue_type} {user_query}".strip()
    matching_docs = search_knowledge_base(search_text, retriever)
    chunks = []
    for idx, doc in enumerate(matching_docs, start=1):
        source_path = doc.metadata.get("source", "unknown")
        source_file = os.path.basename(source_path)
        base_name = os.path.splitext(source_file)[0]
        chunk_id = doc.metadata.get("chunk_id") or f"{base_name}_chunk_{idx:03d}"
        clean_text = doc.page_content.strip().replace("\n", " ")
        snippet = (clean_text[:197] + "...") if len(clean_text) > 200 else clean_text

        chunks.append({
            "source_file": source_file,
            "chunk_id": chunk_id,
            "snippet": snippet
        })

    return {
        "issue_type": issue_type,
        "chunks": chunks
    }

#=================================================================================================================

def get_user_profile(user_id:str):
    """Find customer information by customer ID, email, phone, name or by card number"""
    
    query="""Select * from users WHERE user_id=?"""

    return execute_query(query,(user_id,))
#=====================================================================================================================

def get_device_status(user_id:str):
    """Find device health,compliance details,device id,vpn clinet version,disk percentage, memory usage"""

    query="""Select * from devices Where user_id=?"""

    return execute_query(query,(user_id,))

#======================================================================================================================

def get_incident_details(incident_id:str):
    """Check active incidents by service name, region, or keyword."""

    query="""Select * from known_incidents Where incident_id=?"""

    return execute_query(query,(incident_id,))

#===========================================================================================================================

def run_diagnostic_check(user_id:str):
    """Return diagnostic snapshot for a user and device."""

    query="""Select * from diagnostic_snapshots Where user_id=?"""

    return execute_query(query,(user_id,))

#===========================================================================================================================

def get_ticket_details(ticket_id:str):
    """Fetch existing IT support ticket details with issue type, priority, status, subjects"""

    query="""Select * from tickets Where ticket_id=?"""

    return execute_query(query,(ticket_id,))

#=============================================================================================================================