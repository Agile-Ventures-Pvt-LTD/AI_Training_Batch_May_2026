
from db_utils import get_connection
from langchain.tools import tool
from retrievers import printer_troubleshooting_guide_retriever,get_retriever

from db_utils import get_connection
import sqlite3
from pprint import pprint

def inspect_database_schema():

    """
    It will inspect the schema of ccms.db database
    """
    conn=get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table';
    """)

    tables = cursor.fetchall()

    schema_info = {
        "tables": [],
        "schema": {}
    }

    for table in tables:
        table_name = table[0]

        # Add table name to tables list
        schema_info["tables"].append(table_name)

        # Get column information
        cursor.execute(f'PRAGMA table_info("{table_name}")')

        columns = cursor.fetchall()

        schema_info["schema"][table_name] = [
            column[1] for column in columns
        ]

    conn.close()
    return schema_info




def classify_issue_type(user_query: str):
    """Classify the IT issue type.Supported issue types: VPN,OUTLOOK_EMAIL,LAPTOP_PERFORMANCE,PASSWORD_RESET,NETWORK_CONNECTIVITY,PRINTER,UNKNOWN """
    retriever=get_retriever()
    return {
        "issue_type": "VPN",  
        "confidence": "HIGH",
        "requires_user_lookup": True,
        "requires_device_lookup": True,
        "requires_known_incident_check": True,
        "requires_clarification": False,
        "reasoning_summary": "Issue appears to be VPN-related"
    }


#================================TOOL=========================================
def retrieve_troubleshooting_steps(issue_type: str=None, query: str=None):
    """Retrieve relevant troubleshooting guidance from knowledge base
    Input:
        {
        "issue_type": "VPN",
        "query": "VPN times out after MFA approval"
        }

    Expected output:
        {
            "issue_type": "VPN",
            "chunks": [
                {
                    "source_file": "vpn_troubleshooting_guide.md",
                    "chunk_id": "vpn_chunk_002",
                    "snippet": "If VPN shows timeout...
                }
            ]
        }"""
    

    return {
        "issue_type": issue_type,
        "chunks": [
            {
                "source_file": f"{issue_type.lower()}_troubleshooting_guide.md",
                "chunk_id": f"{issue_type.lower()}_chunk_001",
                "snippet": f"Basic troubleshooting steps for {issue_type}"
            }
        ]
    }



#====================TOOL: PROFILE INFO=======================
def get_user_profile(
    
    user_id=None,
    full_name=None,
    email=None,
):
    """
    this tool is used to find customer information by customer ID, email, phone, or name.
    It take input as 

    {

    "user_id": "USR-1003"

    }
    If user query mentions CUST-1001 it means 1001
    
    Output should strictly be in this form where found=true if value exist and found=false is value not exist

        }
    Expected output:
        {

        "found": true,
        "user": {
        "user_id": "USR-1001",
        "full_name": "Amit Sharma",
        "department": "Sales",
        "location": "Pune",
        "account_status": "Active",
        "mfa_status": "Enabled"
        }
 
    """

    filters = {}

    if user_id:
        filters["user_id"] = user_id

    if full_name:
        filters["full_name"] = full_name

    if email:
        filters["email"] = email


    conn=get_connection()

    conn.row_factory=sqlite3.Row

    cursor=conn.cursor()

    column_name, column_value = next(iter(filters.items()))

    #-------check whether column value exist------
    cursor.execute(f"""SELECT EXISTS(SELECT 1
                    FROM customer ct
                    WHERE {column_name}=?)""",(column_value,))

    found = bool(cursor.fetchone()[0])

    if not found:
        conn.close()

        return {
            "found": False,
            "user": None
        }

    cursor.execute(f"""
                    SELECT 
                        user_id,
                        full_name,
                        department,
                        location,
                        account_status,
                        mfa_status
                    from users
                    where {column_name}=?
                        """,(column_value,))
        
    user_info=dict(cursor.fetchone())

    conn.close()
    return {"found":True,
            "customer":user_info}

#===================TOOL: DEVICE STATUS TOOL====================

def get_device_status(
    user_id=None,device_id=None
):

    """
    {
    Purpose:
    Fetch device health and compliance details.

    Expected output:
        "user_id": "USR-1002",
        "device_id": "DEV-2002",
        "compliance_status": "Compliant",
        "vpn_client_version": "5.8",
        "disk_free_percent": 8,
        "cpu_usage_percent": 78,
        "memory_usage_percent": 84
    }
    """
    
    filters = {}

    if user_id:
        filters["user_id"] = user_id

    if device_id:
        filters["device_id"] = device_id



    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    column_name,column_value=next(iter(filters.items()))
    cursor.execute("""
                    SELECT 
                        user_id,
                        device_id,
                        compliance_status,
                        vpn_client_version,
                        disk_free_percent,
                        cpu_usage_percent,
                        memory_usage_percent
                    FROM devices
                    WHERE 
                   """,(column_value,))
    
    result=dict(cursor.fetchone())
    # count=len(result)

    return {}
    

#==============TOOL  Known Incident Tool===================

def check_known_incidents(
    service_name=None,
    status=None
):
    """
        Purpose:
        Check active incidents by service name, region, or keyword.
        Example:
        {
    
        "service_name": "VPN Gateway",
        "status": "Active"

        Purpose:

        Check active incidents by service name, region, or keyword.
        Example:
            {
            "service_name": "VPN Gateway",
            "status": "Active"
            }
        Expected output:
    
        {
        "count": 1,
        "incidents": [
            {
            "incident_id": "INC-4001",
            "service_name": "VPN Gateway",
            "region": "India-West",
            "severity": "High",
            "status": "Active",
            "summary": "VPN gateway latency causing timeout...",
            "workaround": "Ask users to switch to India-South gateway if available."
            }
            ]
        }
    """

    filters = {}

    if service_name is not None:
        filters["service_name"] = service_name

    if status is not None:
        filters["status"] = status

    
    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    values=[]

    query="""
        SELECT 
            incident_id,
            service_name,
            region,
            severity,
            status,
            summary,
            workaround
        FROM known_incidents
        where 1=1 """

    
    if "service_name" in filters:
        query += " AND service_name = ?"
        values.append(filters["service_name"])

    if "status" in filters:
        query += " AND status = ?"
        values.append(filters["status"])


    cursor.execute(query,tuple(values))
        
    rows=cursor.fetchall()


    conn.close()

    count_incident=len(rows)

    incident_info=[dict(row) for row in rows]



    return {"count":count_incident,
            "incidents":incident_info}


#========================TOOL Diagnostic Check Tool============

def run_diagnostic_check(
    user_id=None,
    device_id=None
):
    """
        Purpose:
        Return diagnostic snapshot for a user and device.
        Expected output:
        {
        
            "user_id": "USR-1001",
            "vpn_reachable": false,
            "internet_reachable": true,
            "webmail_reachable": true,
            "internal_apps_reachable": false,
            "account_locked": false,
            "mfa_push_success": true
        }
    """

    filters = {}

    if user_id is not None:
        filters["user_id"] = user_id

    if device_id is not None:
        filters["device_id"] = device_id

    
    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    values=[]

    query="""
        SELECT 
            user_id,
            vpn_reachable,
            internet_reachable,
            webmail_reachable,
            internal_apps_reachable,
            account_locked,
            mfa_push_success
        FROM diagnostic_snapshots
        where 1=1 """

    
    if "user_id" in filters:
        query += " AND user_id = ?"
        values.append(filters["user_id"])

    if "device_id" in filters:
        query += " AND device_id = ?"
        values.append(filters["device_id"])


    cursor.execute(query,tuple(values))
        
    rows=cursor.fetchall()


    conn.close()

 

    diagnostic_info=[dict(row) for row in rows]



    return diagnostic_info

#=====================================TOOL Ticket Lookup Tool======================


def get_ticket_details(
    user_id=None,
    ticket_id=None
):
    """
    Purpose:
    Fetch existing IT support ticket details.
    Expected output:
    {
        "ticket_id": "IT-3001",
        "user_id": "USR-1001",
        "issue_type": "VPN",
        "priority": "High",
        "status": "Open",
        "subject": "VPN timeout on home Wi-Fi",
        "assigned_group": "Network Support"
    }
    """

    filters = {}

    if user_id is not None:
        filters["user_id"] = user_id

    if ticket_id is not None:
        filters["ticket_id"] = ticket_id

    
    conn=get_connection()
    conn.row_factory=sqlite3.Row
    cursor=conn.cursor()
    values=[]

    query="""
        SELECT 
            ticket_id
            user_id,
            issue_type,
            priority,
            status,
            subject,
            assigned_group,
         
        FROM tickets
        where 1=1 """

    
    if "user_id" in filters:
        query += " AND user_id = ?"
        values.append(filters["user_id"])

    if "ticket_id" in filters:
        query += " AND ticket_id = ?"
        values.append(filters["ticket_id"])


    cursor.execute(query,tuple(values))
        
    rows=cursor.fetchall()


    conn.close()


    diagnostic_info=[dict(row) for row in rows]

    return diagnostic_info


