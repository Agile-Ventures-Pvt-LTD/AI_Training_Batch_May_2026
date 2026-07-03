import asyncio
from pydantic_ai import Agent, RunContext
from tools.database import deps, db, toolset
from database_pydantic_ai import SQLiteDatabase, SQLDatabaseDeps, SQLITE_SYSTEM_PROMPT
from tools.weather import WeatherReport,get_weather

from guardrails_config import validate_input, validate_output
from dotenv import load_dotenv
from typing import Annotated
from pydantic import Field

load_dotenv()

agent_2 = Agent(
    model="groq:openai/gpt-oss-120b", 
    # result_type=WeatherReport,
    deps_type=None,
    system_prompt="You are a weather agent, take city name only as the query" \
    "You must use get_weather_tool tool to get weather conditions for the city and give proper advice on the current weather condition as well"
)    

@agent_2.tool
async def get_weather_tool(
    ctx: RunContext[None],
    city: Annotated[str, Field(description="The city to get weather for")]
) -> str:
    """Get the current weather for a specified city."""
    data = await get_weather(ctx, city)
    return str(data)

async def run_agent(query):
    if not validate_input(query):
        return "Your query is unsafe and therefore blocked"
    try:
        async with SQLiteDatabase("db/travel_data.db") as db_conn:
            run_deps = SQLDatabaseDeps(database=db_conn, read_only=True)
            agent_1 = Agent(
                'groq:openai/gpt-oss-120b',
                deps_type=SQLDatabaseDeps,
                toolsets=[toolset],
                system_prompt=SQLITE_SYSTEM_PROMPT,
                instructions="Check the bookings table with the user query"
            )
            result = await agent_1.run(query, deps=run_deps)
        result_2 = await agent_2.run(f"Give weather information for the city in the query: {result.output}", deps=None)
        response = result_2.output
    except Exception as e:
        print(f"This error:{e}")
        raise e
    safe_response = validate_output(response)
    return safe_response

async def main():
    print("Project build 05_case study 02")
    
    while True:
        try:
            user_query = input("Query: ")
            if user_query.strip().lower() == "exit":
                break
            if not user_query.strip():
                continue
                
            ans = await run_agent(user_query)
            print(f"Response: {ans}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"That Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())



