import sys
from typing import Any, Dict

from pydantic_ai import Agent
try:
    from pydantic_ai import tool  
except Exception:  
    def tool(func):  
        return func

from .guardrails_config import safe_input, safe_output
from .tools import database, weather

import os
from dotenv import load_dotenv
load_dotenv()
os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
from pydantic_ai import Agent
travel_agent = Agent(  
  'groq:openai/gpt-oss-120b',
  system_prompt=(
      """Retrieve upcoming booking for a user 
      Get weather forecast for *city* on *date* (YYYY‑MM‑DD)"""
  ),
)

@travel_agent.tool_plain
def fetch_booking(self, identifier: str) -> Dict[str, Any]:
    """Retrieve upcoming booking for a user."""
    booking = database.get_upcoming_booking(identifier)
    if not booking:
        raise ValueError("No upcoming booking found for the given identifier.")
    return booking.model_dump()

@travel_agent.tool_plain
def fetch_weather(self, city: str, date: str) -> Dict[str, Any]:
    """Get weather forecast for *city* on *date* (YYYY‑MM‑DD)."""
    return weather.get_forecast(city, date)

def _plan_and_execute(self, prompt: str) -> str:
    """
    Very lightweight planner:
    - If the prompt mentions “my upcoming trip” or “booking”, we first call
      fetch_booking using the e‑mail (extracted via a simple heuristic).
    - Then we call fetch_weather with the destination and travel_dates.
    - Finally we synthesize a response.
    """
        
    identifier = None
    if "@" in prompt:
        identifier = prompt.split()[prompt.split().index("@") - 1] + "@" + \
                     prompt.split()[prompt.split().index("@") + 1]
    else:
        for token in prompt.split():
            if token.upper().startswith("TRV-"):
                identifier = token.upper()
                break

    if not identifier:
        identifier = ""  

    try:
        booking_data = self.fetch_booking(identifier)
    except Exception as e:
        return safe_output(str(e))

    dest_city = booking_data["destination"].split(",")[0].strip()
    travel_date = booking_data["travel_dates"].split("to")[0].strip()


    try:
        weather_data = self.fetch_weather(dest_city, travel_date)
    except Exception as e:
        return safe_output(f"Could not obtain weather data: {e}")


    answer = (
        f"Hi {booking_data['user_name']}, your trip to {booking_data['destination']} "
        f"({booking_data['travel_dates']}) looks great! The forecast for {travel_date} "
        f"in {dest_city} is {weather_data['description']} with a high of "
        f"{weather_data['temp_max']}°C and a low of {weather_data['temp_min']}°C. "
        f"Enjoy your stay at {booking_data['hotel_details']}."
    )
    return safe_output(answer)

    
def run(self, user_prompt: str) -> str:
        
    safe_prompt = safe_input(user_prompt)
    return self._plan_and_execute(safe_prompt)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.agent \"<user prompt>\"")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    result = travel_agent.run_sync(user_prompt)
    print(result)