from typing import Optional
from datetime import datetime, timedelta
from langchain_core.tools import tool

from db_utils import (
    execute_query,
    execute_single,
    get_all_tables,
    get_table_schema
)

@tool
def issue_classfication_tool(query: str):
    """
    Classify the category of the issue.
    """
    

@tool
def rag_retrieval_tool(query: str):
    """
    Solves the problem of retrieval of documents from RAG.
    """

@tool
def user_profile_tool(query: str):
    """
    Solves issues regarding user's profile.
    """

@tool
def device_status_tool(query: str):
    """
    States the condition of the device.
    """

@tool
def known_incident_tool(query: str):
    """
    Tells if an incident is already known.
    """

@tool
def diagnostic_tool(query: str):
    """
    Diagnose the issue completely.
    """



TOOLS = [
    issue_classfication_tool,
    rag_retrieval_tool,
    user_profile_tool,
    device_status_tool,
    known_incident_tool,
    diagnostic_tool
    
]