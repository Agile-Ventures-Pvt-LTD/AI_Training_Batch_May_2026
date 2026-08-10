from pydantic_ai import Agent, RunContext
# from database_pydantic_ai import SQLITE_SYSTEM_PROMPT
# from database_pydantic_ai import (SQLDatabaseDeps,create_database_toolset,)
import asyncio
# from database_tool import create_dependencies
from  database_tool import create_database
from src.tools.weather import get_weather
from src.tools.database import get_traveller_profile
from src.guardrails_config import input_guardrail, output_guardrail


import os
from dotenv import load_dotenv
load_dotenv()



MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "groq:llama-3.3-70b-versatile"
)


SYSTEM_PROMPT="""
You are a travel agent.
Agent must be equipped with exactly two tools built using Pydantic AI's @agent.tool

1. Database Connection Tool: * Accepts user identifiers (e.g., Email or Booking
ID) and retrieves upcoming travel plans, destination cities, travel dates, and hotel details from the
provided travel_data.db file. 

2. Weather Information Tool: * Accepts a location (city/coordinates)
and dates, reaching out to an external Weather API to fetch current or forecasted weather conditions

-The agent must interpret natural language prompts
-deduce that it must first call the Database Tool to find out where the user is going
-second call the Weather Tool for that specific destination.
-The agent must synthesize the outputs of both tools into a natural, helpful, and concise
conversational response.
 """


# database_toolset = create_database_toolset()


database_agent = Agent(

    model=MODEL_NAME,


    system_prompt=SYSTEM_PROMPT
)

@agent.tool
async def get_weather_tool(ctx: RunContext,
                              latitude: float,
                                longitude: float,
                                hourly: Optional[str],
                                forecast_days : int = 7,
                                start_date : str = date.today()
                                ):
   
   """Return today's weather for the given city using location and date."""
   return get_weather(
       latitude,
        longitude,
        hourly,
        forecast_days,
        start_date
   )


@agent.tool
async def get_database_tool(ctx: RunContext,
                                id=None,
                                booking_id=None,
                                user_name=None,
                                user_email=None
                                )
    

    return get_traveller_profile(
    
            id=None,
            booking_id=None,
            user_name=None,
            user_email=None
            )



async def chat():

    async with create_database() as database:

        deps = create_dependencies(database)

        print("=" * 60)
        print("Intelligent Travel Booking Assistant")
        print("Type 'exit' to quit.")
        print("=" * 60)

        while True:

            user_input = input("\nYou : ")

            if user_input.lower() in {"exit", "quit"}:
                print("\nGoodbye!")
                break
            
            try:

                safe_input = input_guardrail(user_input)

            except Exception as e:

                print(e)
                return

            result = await database_agent.run(
                safe_input,
                deps=deps,
                )
        
            response = result.output

            try:
                safe_output = output_guardrail(response)

            except Exception as e:

                print(e)
                return

            print("\nAssistant:\n")
            print(safe_output)




if __name__ == "__main__":
    asyncio.run(chat())



