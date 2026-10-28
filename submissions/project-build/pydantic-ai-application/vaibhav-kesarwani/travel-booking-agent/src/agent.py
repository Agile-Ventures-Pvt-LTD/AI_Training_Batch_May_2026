import os
from pydantic_ai import Agent, RunContext
from dotenv import load_dotenv
from tools.database import query_travel_database
from tools.weather import get_latitude_longitude
from prompts import agent_system_prompt, agent_instructions
from schemas import TravelOutput

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["GROQ_MODEL"] = os.getenv("GROQ_MODEL")


def search_database_tool(query: RunContext[str]):
    """
    Use this tool to query the SQLite travel database. The database contains the booking table. Only use SELECT queries. Do not perform INSERT, UPDATE, DELETE, DROP, ALTER, or TRUNCATE operations.

    Args:
        query: User Query

    Return:
        return: The SQL query to search the database
    """

    return query_travel_database(query)


def search_weather_tool(country_name: RunContext[str]):
    """
    Use this tool to search the weather of any place

    Args:
        country_name: Name of the country from the user query

    Return:
        return: The hourly report of weather of the country
    """

    return get_latitude_longitude(country_name)


try:
    agent = Agent[None, TravelOutput](
        model=os.environ["GROQ_MODEL"],
        deps_type=None,
        output_type=TravelOutput,
        system_prompt=agent_system_prompt,
        instructions=agent_instructions,
        retries=2,
        tools=[search_database_tool, search_weather_tool]
    )

except Exception as e:
    print(f"Agent Error: {e}")
