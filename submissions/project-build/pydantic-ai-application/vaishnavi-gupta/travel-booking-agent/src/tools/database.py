import asyncio
from datetime import date
from pydantic_ai import Agent, RunContext
from fake_database import DatabaseConn  

database_agent = Agent(
  'llama-3.3-70b-versatile',
  deps_type=DatabaseService,
  instructions='Provide details to the users retrieving from the database as they ask.',
)


@database_agent.tool
def database(
  ctx: RunContext[DatabaseService], id: int, email_id: str
) -> str:
   return  travel_plans, destination_cities, travel_dates, hotel_details
  

