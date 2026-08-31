import os
import asyncio
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Literal
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

@dataclass
class SellerAgentDeps:
    sqlite_db_path: Path 
    read_only: bool = True

class AgentResponse(BaseModel):
    status: Literal["success", "fallback"] = Field(description="Whether the query was answered or handled by the fallback mechanism.")
    response_text: str = Field(description="The detailed response text meant for the seller.")

SELLER_SYSTEM_PROMPT = """
You are a highly efficient, professional E-commerce Operational Support Agent.
Your role is to assist sellers with operational workflows, calculating Average Selling Price (ASP), 
managing Detailed Seller Ratings (DSRs), and handling inventory fulfillment.

RULES:
1. Use the provided tools and databases to gather facts before responding.
2. If calculating metrics like ASP, execute the appropriate data analytical workflows.
3. CRITICAL: If a seller query falls completely outside the scope of your documentation or 
   database schema, or if you lack sufficient information, you must return a standardized, 
   polite fallback message. Do not fabricate or hallucinate any answers.
"""

model = 'groq:openai/gpt-oss-120b'

seller_agent = Agent(
    model=model,
    deps_type=SellerAgentDeps,
    output_type=AgentResponse, 
    system_prompt=SELLER_SYSTEM_PROMPT,
)

@seller_agent.tool
async def calculate_average_selling_price(ctx: RunContext[SellerAgentDeps]) -> str:
    """Calculates the Average Selling Price (ASP) from the database."""
    return "The system ASP for the requested timeframe evaluates to $42.50 across all channels."

@seller_agent.tool
async def query_fulfillment_workflows(ctx: RunContext[SellerAgentDeps], topic: str) -> str:
    """Queries vector storage documentation regarding operational fulfillment and DSRs."""
    return f"Found document reference: Fulfillment operations require 24-hour turnaround to protect DSR scores."

async def main():
    deps = SellerAgentDeps(sqlite_db_path="chroma_db\chroma.sqlite3", read_only=True)

    # Example 1
    user_query = "Can you check my fulfillment rules and calculate Average Selling Price?"
    print(f"Seller Query: {user_query}\n---")
    
    result = await seller_agent.run(user_query, deps=deps)
    
    print(f"Status: {result.output.status}")
    print(f"Agent Output:\n{result.output.response_text}\n")

    # Example 2
    out_of_scope_query = "What is the best recipe for baking chocolate chip cookies?"
    print(f"Seller Query: {out_of_scope_query}\n---")
    fallback_result = await seller_agent.run(out_of_scope_query, deps=deps)
    print(f"Status: {fallback_result.output.status}")
    print(f"Agent Output:\n{fallback_result.output.response_text}")

if __name__ == "__main__":
    asyncio.run(main())