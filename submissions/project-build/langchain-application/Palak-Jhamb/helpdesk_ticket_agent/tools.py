from langchain.tools import tool
from langchain_core.tools import tool
from pathlib import Path
from connection import get_db
import json

    
@tool
def search_tickets(sql_query: str) -> str:
    """
    Use this tool to search for tickets based on a SQL query. The input is a SQL query string,
     and the output should be a list of matching tickets.
     If no tickets are found, return a message indicating that no matches were found.
    When using this tool
    - Generate a valid SQLite  query.
    - Pass ONLY the SQL query to the tool.
    - Do not pass natural language.
    """

    try:
        db=get_db()
        result = db.run(sql_query)
        return str(result)

    except Exception as e:
        return f"Database Error: {str(e)}"

@tool
def get_ticket_details(sql_query: str) -> str:
    """
    Use this tool to get detailed information about a specific ticket based on a SQL query. The input is a SQL query string,
     and the output should be the details of the matching ticket.
     If the ticket is not found, return a message indicating that no matching ticket was found.
         When using this tool
    - Generate a valid SQLite  query.
    - Pass ONLY the SQL query to the tool.
    - Do not pass natural language.
    """

    try:
        db=get_db()
        result = db.run(sql_query)
        return str(result)

    except Exception as e:
        return f"Database Error: {str(e)}" 

@tool
def ticket_comment_tools(sql_query: str) -> str:
    """
    Use this tool to add an internal comment to a ticket based on a SQL query. The input is a SQL query string,
     and the output should indicate whether the comment was successfully added or if there was an error.
        When using this tool
    - Generate a valid SQLite  query.
    - Pass ONLY the SQL query to the tool.
    - Do not pass natural language.
    """

    try:
        db=get_db()
        result = db.run(sql_query)
        return "Comment added successfully." if result else "Failed to add comment."

    except Exception as e:
        return f"Database Error: {str(e)}"

@tool
def calculate_sla_status(sql_query: str) -> str:
    """
    Determine whether a ticket is overdue, due today, or within SLA
        When using this tool
    - Generate a valid SQLite  query.
    - Pass ONLY the SQL query to the tool.
    - Do not pass natural language.
    """
    try:
        db=get_db()
        result = db.run(sql_query)
        return result

    except Exception as e:
        return f"Database Error: {str(e)}"
    
@tool
def prioritization(sql_query: str) -> str:
    """
    set priority of ticket 
    Rank tickets based on:
    Priority
    SLA status
    Customer tier
    Ticket status
    User’s archival memory preferences
    """
    try:
        db=get_db()
        result = db.run(sql_query)
        return result

    except Exception as e:
        return f"Database Error: {str(e)}"


@tool
def update_ticket_status(sql_query:str) ->str:
    """
    Update ticket status in database
    Do not update if ticket is already in the requested status
     When using this tool
    - Generate a valid SQLite  query.
    - Pass ONLY the SQL query to the tool.
    - Do not pass natural language.
    """   
    try:
        db=get_db()
        result = db.run(sql_query)
        return result

    except Exception as e:
        return f"Database Error: {str(e)}"
    

@tool
def add_ticket_comment(sql_query:str) ->str:
    """
    Add an internal comment or work note to a ticket
    """
    try:
        db=get_db()
        result = db.run(sql_query)
        return result

    except Exception as e:
        return f"Database Error: {str(e)}"
    
@tool
def save_conversation(file: json) -> str:
    """ Store user-agent interaction in 
    conversation_logs 
    """
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / "Coversation_summary.json"

    with open(output_file, "w") as f:
        json.dump(file, f, indent=4)
    
    return "Conversation saved successfully."
  

  
from memory import summary
@tool
def summarize_conversation(file: json) -> str:
    """
    Summarize recent conversation history 
    """
    output_dir = Path("outputs")
    output_file = output_dir / "Coversation_summary.json"

    with open(output_file, "r") as f:
        data = json.load(f)
        summary_result=summary(data)
        return summary_result