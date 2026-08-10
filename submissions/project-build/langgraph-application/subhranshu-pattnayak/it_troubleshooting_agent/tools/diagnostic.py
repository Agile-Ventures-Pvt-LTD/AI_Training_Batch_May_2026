from db_utils.db_connection import get_conn
from langchain_core.prompts import ChatPromptTemplate
from utils.gClient import get_client
import sqlite3
from langchain.tools import tool

def make_diagnostic_tool(retrieved, incident, profile, device):
    try:
        diagnostic_system_message = f"""
            You are an expert diagnostics handler. Make a final diagnostics based on retrieved vector docs, incident info, profile info, device status info.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", diagnostic_system_message),
            ("human", "Retrieved documents: {retrieved}, Known Incident information: {incident}, User profile information: {profile}, User device status information: {device}")
        ])
        
        llm = get_client()
        
        chain = prompt | llm
        
        result: str = chain.invoke({"retrieved": retrieved}, {"incident": incident}, {"profile": profile}, {"device": device})
        
        return result
    except Exception as e:
        print(f"Error: {e}")