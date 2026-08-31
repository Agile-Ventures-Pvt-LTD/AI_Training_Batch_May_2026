import os
import asyncio
from pydantic_ai import Agent,RunContext
from pydantic import BaseModel,Field,ConfigDict
from tools.database import BookingDetails,fetch_booking_from_db
from tools.weather import fetch_weather_forecast
from guardrails_config import ContentGuardrail
from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

class Agent_deps(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    db_file_path : str
    guardrail_handler: ContentGuardrail

travel_agent = Agent(
    model='groq:openai/gpt-oss-120b',
    deps_type=Agent_deps,
    system_prompt=('''You are experienced travel Assistant Agent. Your goal is to help users with thier trip.
    You must synthesize the outputs of both tools into a natural, helpful, and concise conversational response.
    Be aware about all the things,be context-aware.
    Mention the desitination city and specific travel details naturally.
    Also don't halluciante, don't give fabricated answers by your own.''')
)

@travel_agent.tool
async def customer_iternary_details(ctx:RunContext[Agent_deps],customer_token):
    """
    Extracts up-to-date travel documentation from database using Email or Booking ID.
    """
    
    booking = fetch_booking_from_db(ctx.deps.database_file_path, customer_token)
    if not booking:
        return f"Error: No valid travel bookings matching key '{customer_token}'"
    return f"Itinerary Data Found: {booking}"

@travel_agent.tool
async def get_destination_weather_conditions(ctx: RunContext[Agent_deps], target_city: str) -> str:
    """
    Fetches real-time weather outlook parameters for a given target city location.
    """
    weather = await fetch_weather_forecast(target_city)
    if not weather:
        return f"Error: '{target_city}' is currently unavailable."
    
    current = weather.get("current_weather", {})
    return (
        f"Weather report for {target_city}: Temp is {current.get('temperature')}°C, "
        f"Windspeed is {current.get('windspeed')} km/h."
    )

async def process_user_request(prompt: str, db_path: str) -> str:
    guard = ContentGuardrail()
    is_safe, evaluated_input = guard.validate_input(prompt)
    if not is_safe:
        return evaluated_input
    dependencies = Agent_deps(
        db_file_path=db_path,
        guardrail_handler=guard
    )

    try:
        runtime_payload = await travel_agent.run(evaluated_input, deps=dependencies)
        raw_output = runtime_payload.data
    except Exception as e:
        raw_output = {str(e)}
    return guard.validate_output(raw_output)
    
# if __name__ == "__main__":
#     asyncio.run(main())