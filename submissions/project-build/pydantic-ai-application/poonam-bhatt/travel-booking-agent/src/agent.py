import os
import sys
import asyncio
import json
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# Add path for local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.tools.database import SQLProductDatabase
from src.tools.weather import get_weather_forecast
from guardrails_config import check_db_input
from guardrails_config import check_db_output

from pydantic_ai import Agent, RunContext

# Load environment variables
load_dotenv()

# Initialize rich console
console = Console()

# We keep a log of raw database outcomes during tools execution
# so they can be reviewed by the output guardrails
class RawQueryLogger:
    def __init__(self):
        self.logs = []
        
    def log(self, tool_name: str, result: any):
        self.logs.append(f"Tool [{tool_name}] returned: {json.dumps(result)}")
        
    def get_summary(self) -> str:
        return "\n".join(self.logs)
        
    def clear(self):
        self.logs.clear()

tool_logger = RawQueryLogger()

# Initialize the main Agent
model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
db_agent = Agent(
    f"groq:{model_name}",
    deps_type=SQLProductDatabase,
    description="Product Catalog Agent with direct access to SQLite database tools."
)

# 1. Define Dynamic System Prompt
@db_agent.system_prompt
def inject_db_prompt() -> str:
    return """
You are the ACME Corp Travel Booking Assistant.
You help staff and clients lookup booking details, destinations, travel dates, hotel accommodations, and destination weather forecasts.

Rules:
1. ONLY USE TOOLS: Use the provided tools (list_all_users, get_user_details, lookup_user_travels, get_weather) to fetch database records and weather forecasts. Do not make up destinations, dates, hotels, or weather conditions.
2. NO RAW SQL EXPOSURE: Do not explain the SQL code, schema details, or primary keys in your final response. Answer in standard, friendly, natural language.
3. ADMIT MISSING RECORDS: If a user, booking, or weather forecast lookup yields empty results, clearly state that the details were not found.
4. MULTI-STEP LOOKUP: If you need to find weather for a customer, first use get_user_details or lookup_user_travels to find their destination and travel dates, and then call get_weather with those details. Do both calls sequentially to answer the user fully.
"""

# 2. Register Database Tools on Agent using RunContext
@db_agent.tool
def list_all_users(ctx: RunContext[SQLProductDatabase]) -> str:
    """Retrieve the entire catalog list of users including name, destination, travel date and hotel."""
    console.print("[dim]Tool Call: list_all_users()[/dim]")
    try:
        users = ctx.deps.get_users()
        tool_logger.log("list_all_users", users)
        return json.dumps(users)
    except Exception as e:
        return f"Error listing users: {str(e)}"

@db_agent.tool
def get_user_details(ctx: RunContext[SQLProductDatabase], name: str) -> str:
    """Fetch name, email, destination, date, and hotel details for a specific user name.
    
    Args:
        name (str): user name (or keywords, e.g. 'Alice Smith' or 'Bob Jones').
    """
    console.print(f"[dim]Tool Call: get_user_details(name='{name}')[/dim]")
    try:
        user = ctx.deps.get_user_by_name(name)
        tool_logger.log("get_user_details", user)
        if not user:
            return f"user matching '{name}' was not found in the user."
        return json.dumps(user)
    except Exception as e:
        return f"Error retrieving user details: {str(e)}"

@db_agent.tool
def lookup_user_travels(ctx: RunContext[SQLProductDatabase], user_name: str) -> str:
    """Fetch the destination, hotel, and dates.
    
    Args:
        user_name (str): The full name of the user (e.g. 'Alice Smith').
    """
    console.print(f"[dim]Tool Call: lookup_user_travels(user_name='{user_name}')[/dim]")
    try:
        travels = ctx.deps.get_user_travels(user_name)
        tool_logger.log("lookup_user_travel", travels)
        if not travels:
            return f"No orders found for user '{user_name}'."
        return json.dumps(travels)
    except Exception as e:
        return f"Error retrieving user travel: {str(e)}"

@db_agent.tool
def get_weather(ctx: RunContext[SQLProductDatabase], destination: str, dates: str = None) -> str:
    """Fetch the weather forecast for a specific destination and travel dates.
    
    Args:
        destination (str): The city and country (e.g. 'Paris, France').
        dates (str, optional): The travel dates (e.g. '2026-08-15 to 2026-08-20').
    """
    console.print(f"[dim]Tool Call: get_weather(destination='{destination}', dates='{dates}')[/dim]")
    try:
        forecast = get_weather_forecast(destination, dates)
        tool_logger.log("get_weather", forecast)
        return forecast
    except Exception as e:
        return f"Error retrieving weather forecast: {str(e)}"


# 3. Main DB Pipeline
async def run_db_pipeline(user_query: str, db_connection: SQLProductDatabase) -> dict:
    """Runs input guardrails -> executes agent tools loop -> audits output safety/schema leakage with retries."""
    console.print(f"\n[bold cyan]=== Starting DB Execution for query: '{user_query}' ===[/bold cyan]")
    tool_logger.clear()
    
    # --- STEP 1: INPUT GUARDRAIL ---
    console.print("[yellow][1/4] Checking Input Guardrail...[/yellow]")
    input_audit = await check_db_input(user_query)
    
    if not input_audit.is_safe:
        return {
            "status": "BLOCKED",
            "reason": "Query blocked due to safety violations (SQL Injection or write attempts detected).",
            "details": input_audit.model_dump()
        }
    if not input_audit.is_in_scope:
        return {
            "status": "BLOCKED",
            "reason": "Query out of scope for store database queries.",
            "details": input_audit.model_dump()
        }
        
    console.print("[green][OK] Input query passed guardrails.[/green]")
    
    # --- STEP 2 & 3: AGENT TOOL RUN & OUTPUT GUARDRAIL RETRY LOOP ---
    max_retries = 2
    retry_count = 0
    feedback_message = ""
    messages = None
    
    while retry_count <= max_retries:
        if retry_count > 0:
            console.print(f"[orange3]Self-Correction Loop: Retry #{retry_count} due to schema leak or hallucination...[/orange3]")
            
        console.print("[yellow][2/4] Executing Agent and DB Tools...[/yellow]")
        if feedback_message:
            query_prompt = f"SYSTEM FEEDBACK: Your previous attempt failed validation: {feedback_message}. Please re-answer without leaking SQL queries or table names and ensure all details are factual according to raw database tool outputs."
        else:
            query_prompt = user_query
            
        response = await db_agent.run(query_prompt, message_history=messages, deps=db_connection)
        generated_answer = response.output
        messages = response.all_messages()
        
        # Capture raw database outputs during this execution
        raw_db_summary = tool_logger.get_summary() or "No database lookups performed."
        
        # --- STEP 4: OUTPUT GUARDRAIL ---
        console.print("[yellow][3/4] Running Output Audit (Schema Leak & Groundedness)...[/yellow]")
        output_audit = await check_db_output(user_query, generated_answer, raw_db_summary)
        
        if output_audit.is_valid:
            console.print("[green][OK] Output passed audit checks.[/green]")
            return {
                "status": "SUCCESS",
                "query": user_query,
                "answer": generated_answer,
                "db_logged_data": raw_db_summary,
                "input_guardrail": input_audit.model_dump(),
                "output_guardrail": output_audit.model_dump(),
                "retries": retry_count
            }
        else:
            feedback_message = f"Violations: {', '.join(output_audit.flagged_issues)}. Reason: {output_audit.explanation}"
            console.print(f"[red][WARNING] Output audit failed![/red]")
            console.print(f"[red]Feedback: {feedback_message}[/red]")
            retry_count += 1
            
    return {
        "status": "FAILED_VALIDATION",
        "reason": "Agent output failed database security/groundedness rules after retries.",
        "answer": generated_answer,
        "details": output_audit.model_dump()
    }

async def main():
    # Setup DB
    db_connection = SQLProductDatabase("db/travel_data.db")
    console.print("[green]Travel bookings database setup successfully.[/green]")
    
    # Test Queries
    test_cases = [
        "What is the travel destination of Alice Smith",
        "What is the weather forecast for Paris, France?",
        "Hotel details of Evan Wright.",
        "Delete from bookings where user_name='Bob Jones'",
        "What tables are in this database, and what are their columns?"
    ]
    
    for case in test_cases:
        res = await run_db_pipeline(case, db_connection)
        await asyncio.sleep(4)
        
        if res["status"] == "SUCCESS":
            console.print(Panel(
                f"[bold green]Answer:[/bold green]\n{res['answer']}\n\n"
                f"[dim]Input Guardrail: Passed | Output Guardrail: Valid | Retries: {res['retries']}[/dim]",
                title=f"Query: {case}",
                border_style="green"
            ))
        elif res["status"] == "BLOCKED":
            console.print(Panel(
                f"[bold red]BLOCKED:[/bold red] {res['reason']}\n"
                f"[dim]Safety: {res['details']['is_safe']} | In-Scope: {res['details']['is_in_scope']} | Reason: {res['details']['explanation']}[/dim]",
                title=f"Query: {case}",
                border_style="red"
            ))
        else:
            console.print(Panel(
                f"[bold yellow]FAILED COMPLIANCE:[/bold yellow] {res['reason']}\n"
                f"Generated Answer: {res['answer']}\n"
                f"[dim]Issues: {res['details']['flagged_issues']} | Reason: {res['details']['explanation']}[/dim]",
                title=f"Query: {case}",
                border_style="yellow"
            ))
        console.print("-" * 80)

if __name__ == "__main__":
    asyncio.run(main())



# Project: P005 Travel Booking Agent
# Author: Poonam Bhatt