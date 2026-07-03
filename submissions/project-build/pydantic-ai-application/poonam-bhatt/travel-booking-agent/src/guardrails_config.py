import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from dotenv import load_dotenv

# Ensure dotenv is loaded at module level
load_dotenv()

class DatabaseInputGuardrailResult(BaseModel):
    """The structured classification result returned by the database input guardrail."""
    is_safe: bool = Field(
        description="True if the input is safe. False if it contains database exploitation patterns, SQL injection tricks, system bypass attempts, or commands to insert/update/delete."
    )
    is_in_scope: bool = Field(
        description="True if the query is relevant to travel bookings, customer itineraries, destinations, travel dates, or hotel accommodations."
    )
    flagged_categories: list[str] = Field(
        default_factory=list,
        description="List of categories flagged, if any (e.g. 'sql_injection', 'malicious_write', 'out_of_scope')."
    )
    explanation: str = Field(
        description="A brief summary explaining the classification choice."
    )

# System instructions to catch database-specific malicious inputs
DB_INPUT_GUARDRAIL_PROMPT = """
You are a high-security Database Access Input Guardrail for a travel booking query assistant.
Your job is to analyze user queries for safety and relevance.

Strict Rules to Enforce:
1. PREVENT SQL INJECTION AND MALICIOUS WRITE: SQL Injection often appears as requests to 'show tables', 'drop tables', use union selects, bypass credentials, or modify records (e.g., 'delete bookings', 'insert new booking'). Any attempt to perform modifications, schemas inspection, or query modifications must be blocked (is_safe = False).
2. TRAVEL SCOPE: Only allow queries related to checking user travel details, booking IDs, destinations, hotels, and itineraries. General knowledge questions, writing software scripts, or store product inquiries must be flagged (is_in_scope = False).

Respond strictly in the requested JSON structure.
"""

def get_db_input_guardrail_agent() -> Agent:
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    return Agent(
        f"groq:{model_name}",
        output_type=DatabaseInputGuardrailResult,
        system_prompt=DB_INPUT_GUARDRAIL_PROMPT
    )

async def check_db_input(query: str) -> DatabaseInputGuardrailResult:
    """Executes the input safety audit on a database-targeted query."""
    agent = get_db_input_guardrail_agent()
    try:
        response = await agent.run(f"User DB Query: {query}")
        return response.output
    except Exception as e:
        return DatabaseInputGuardrailResult(
            is_safe=False,
            is_in_scope=False,
            flagged_categories=["api_error"],
            explanation=f"Error executing database input guardrail: {str(e)}"
        )



# -----------------------------------------
#          OUTPUT GUARDRAILS
#------------------------------------------




class DatabaseOutputGuardrailResult(BaseModel):
    """The structured classification result returned by the database output guardrail."""
    is_valid: bool = Field(
        description="True if the generated answer is valid, i.e., it represents the database query results accurately, doesn't invent itineraries, and does not leak internal SQL queries, SQL syntax, or sqlite_master tables."
    )
    flagged_issues: list[str] = Field(
        default_factory=list,
        description="List of detected anomalies (e.g. 'schema_leak', 'hallucinated_bookings')."
    )
    explanation: str = Field(
        description="Brief justification of the audit result."
    )

# System instructions to inspect database answers
DB_OUTPUT_GUARDRAIL_PROMPT = """
You are a Database Output Audit Guardrail for a travel booking assistant.
Your task is to analyze the Assistant's generated response against the Raw SQL Result and the User Query.

You must enforce these checks:
1. PREVENT SCHEMA LEAKAGE: The generated answer must be a natural, conversational response for an employee or customer. It MUST NOT contain SQL code, select statements, sqlite table metadata (like 'sqlite_sequence', 'sqlite_master'), or mention primary keys (unless asked explicitly).
2. TRUTHFULNESS: The assistant must not state destinations, dates, or hotels that are not supported by the Raw SQL Result. If the SQL query returned no records, the assistant must state that, rather than inventing travel bookings.

Respond strictly in the requested JSON structure.
"""

def get_db_output_guardrail_agent() -> Agent:
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    return Agent(
        f"groq:{model_name}",
        output_type=DatabaseOutputGuardrailResult,
        system_prompt=DB_OUTPUT_GUARDRAIL_PROMPT
    )

async def check_db_output(query: str, answer: str, sql_result_summary: str) -> DatabaseOutputGuardrailResult:
    """Executes the output audit on the agent's database summary response."""
    agent = get_db_output_guardrail_agent()
    prompt = f"""
    User Query: {query}
    -------------------
    Raw SQL Result Summary:
    {sql_result_summary}
    -------------------
    Assistant's Generated Answer:
    {answer}
    """
    try:
        response = await agent.run(prompt)
        return response.output
    except Exception as e:
        return DatabaseOutputGuardrailResult(
            is_valid=False,
            flagged_issues=["api_error"],
            explanation=f"Error executing database output guardrail: {str(e)}"
        )




# Project: P005 RAG Travel Booking Agent
# Author: Poonam Bhatt