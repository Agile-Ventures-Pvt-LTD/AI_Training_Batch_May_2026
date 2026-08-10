from db_utils import  get_db
from langchain.tools import tool
import sqlite3
from langchain_core.messages import (SystemMessage, HumanMessage)
from config import TOP_K
from embeddings import get_embedding_model
from langchain_chroma import Chroma
from config import DATABASE
import chromadb
from langchain_groq import ChatGroq

from config import get_api_key



embedding_model = get_embedding_model()
chromadb_client = chromadb.Client()
vectorstore = Chroma(
    collection_name="trouble_shooting",
    collection_metadata={"hnsw:space": "cosine"},
    embedding_function=embedding_model,
    client=chromadb_client,
    persist_directory=DATABASE
)

@tool
def retrieve_troubleshooting_steps(vector_store,query):
    """used to retrive data regarding trouble shooting """
    retriever = vector_store.as_retriever(
        searc_type="similarity",
        search_kwargs={"k": TOP_K})
    return retriever.invoke(query)

@tool
def get_user_profile(user_id: str = None,email: str = None,name: str = None):
    """ This tool is used to get user details .Find users information by user ID, email, or full name"""
    query = None
    params = ()

    if user_id:
        query = "SELECT * FROM users WHERE user_id = ?"
        params = (user_id,)

    elif email:
        query = "SELECT * FROM users WHERE email = ?"
        params = (email,)

    elif name:
        query = " SELECT * FROM users full_name = ?"
        params = ("name",)

    else:
        return {
            "found": False,
            "message": "No search criteria provided."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        user = cursor.fetchone()
        if not user:
            return {
                "found": False,
                "user": None
            }
        return {
            "found": True,
            "user": {
                "user_id": user["user_id"],
                "name": user["full_name"],
                "email": user["email"],
                "department": user["department"],
                "location": user["location"],
                "manager": user["manager"],
                "account_status": user["account_status"],
                "mfa_status": user["mfa_status"]

            }
        }

    finally:
        conn.close()

@tool
def get_device_status(device_id: str = None):
    """ This tool is used to fetch device health and compliance details."""
    query = None
    params = ()

    if device_id:
        query = "SELECT * FROM devices WHERE device_id = ?"
        params = (device_id,)

    else:
        return {
            "found": False,
            "message": "No search criteria provided."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        device = cursor.fetchone()
        if not device:
            return {
                "found": False,
                "device_id": None
            }
        return {
            "found": True,
            "devices": {
                "user_id": device["user_id"],
                "device_id": device["device_id"],
                "compliance_status": device["compliance_status"],
                "vpn_client_version": device["vpn_client_version"],
                "disk_free_percent": device["disk_free_percent"],
                "cpu_usage_percent": device["cpu_usage_percent"],
                "memory_usage_percent": device["memory_usage_percent"]
            }
        }

    finally:
        conn.close()


@tool
def check_known_incidents(service_name: str = None,region: str = None):
    """ This tool is used tocheck active incidents by service name, region."""
    query = None
    params = ()

    if service_name:
        query = "SELECT * FROM known_incidents WHERE service_name = ?"
        params = (service_name,)

    elif region:
        query = "SELECT * FROM known_incidents WHERE region = ?"
        params = (region,)

    else:
        return {
            "found": False,
            "message": "No search criteria provided."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        incidents = []
        for row in rows:
            incident = {
                "incident_id": row["incident_id"],
                "service_name": row["service_name"],
                "region": row["region"],
                "severity": row["severity"],
                "status": row["status"],
                "summary": row["summary"],
                "workaround": row["workaround"],
            }

            incidents.append(incident)

        return {
            "count": len(incidents),
            "Incidents": incidents
        }

    finally:
        conn.close()


@tool
def run_diagnostic_check(user_id: str = None,device_id: str = None,):
    """ This tool is used to Return diagnostic snapshot for a user and device"""
    query = None
    params = ()

    if user_id:
        query = "SELECT * FROM diagnostic_snapshots WHERE user_id = ?"
        params = (user_id,)

    elif device_id:
        query = "SELECT * FROM diagnostic_snapshots WHERE device_id = ?"
        params = (device_id,)

    else:
        return {
            "found": False,
            "message": "No search criteria provided."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        check = cursor.fetchone()
        if not check:
            return {
                "found": False,
                "user": None
            }
        return {
            "found": True,
            "user": {
                "user_id": check["user_id"],
                "vpn_reachable": check["vpn_reachable"],
                "internet_reachable": check["internet_reachable"],
                "webmail_reachable": check["webmail_reachable"],
                "internal_apps_reachable": check["internal_apps_reachable"],
                "account_locked": check["account_locked"],
                "mfa_push_success": check["mfa_push_success"]

            }
        }

    finally:
        conn.close()




@tool
def get_ticket_details(ticket_id: str = None,priority: str = None,):
    """ This tool is used to Fetch existing IT support ticket details"""
    query = None
    params = ()

    if ticket_id:
        query = "SELECT * FROM tickets WHERE ticket_id = ?"
        params = (ticket_id,)

    elif priority:
        query = "SELECT * FROM tickets WHERE priority = ?"
        params = (priority,)

    else:
        return {
            "found": False,
            "message": "No search criteria provided."
        }

    conn = get_db()
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        tickets = []
        for row in rows:
            ticket = {
                "ticket_id": row["ticket_id"],
                "user_id": row["user_id"],
                "issue_type": row["issue_type"],
                "priority": row["priority"],
                "status": row["status"],
                "subject": row["subject"],
                "assigned_group": row["assigned_group"],
            }

            tickets.append(ticket)

        return {
            "count": len(tickets),
            "Incidents": tickets
        }

    finally:
        conn.close()

@tool
def clarification_node(query):
      """This is used to respond to user if query is not recognizable"""
      
      system_prompt=""" User query is not recognisable and understandable.
      query is incomplete or have missing information. ask user to give detailed query."""
      messages=[
           SystemMessage(content=system_prompt),
           HumanMessage(content=query)
 
      ]
      llm = ChatGroq(
     model="openai/gpt-oss-120b",
     groq_api_key=get_api_key(),
    )
      
      response = llm.invoke(messages)
      dict=response
      return{"final_response":dict["final_response"]}

tools = [clarification_node,retrieve_troubleshooting_steps,get_user_profile,get_device_status,check_known_incidents, run_diagnostic_check,get_ticket_details]