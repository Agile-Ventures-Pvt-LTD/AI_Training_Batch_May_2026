# agent.py
    
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from typing import Optional

from tools.database import get_user_bookings
from tools.weather import get_weather_forecast
from guardrails_config import validate_input, validate_output, input_msg
from dotenv import load_dotenv
load_dotenv()

class TravelDeps(BaseModel):
    session_id: Optional[str] = None


travel_agent = Agent(
    'groq:openai/gpt-oss-120b',
    deps_type=TravelDeps,
    instructions="""You are an intelligent Travel Guiding Assistant.

    Your job is to help customers with their travel inquiries by:
    1. Looking up their bookings in the database (by email or booking ID)
    2. Fetching weather forecasts for their destinations
    3. Giving helpful, personalized travel advice

    RULES:
    - When asked about weather or trip details, FIRST use get_user_bookings to find their trip
    - THEN use get_destination_weather to get weather for that destination
    - Combine both info into a helpful response
    - Give specific advice based on weather (Example: "pack an umbrella" if rain is expected)
    - Be friendly and concise
    """
)

travel_agent.tool(get_user_bookings, get_weather_forecast)

async def run_travel_agent(user_input: str, session_id: Optional[str] = None) -> str:
    
    is_valid, processed_input = validate_input(user_input)
    if not is_valid:
        return input_msg
    
    try:
        deps = TravelDeps(session_id=session_id)
        result = await travel_agent.run(processed_input, deps=deps)
        agent_response = result.data
    except Exception:
        agent_response = (
            "I'm sorry, I encountered an issue processing your request. "
        )
    
    is_valid_output, final_response = validate_output(agent_response)
    return final_response

if __name__ == "__main__":
    import asyncio
    
    async def main():
        user_query = str(input("Enter your query along with either your email or booking ID (e.g., TRV-101): "))
        response = await run_travel_agent(user_query)
        print(response)
    
    asyncio.run(main())