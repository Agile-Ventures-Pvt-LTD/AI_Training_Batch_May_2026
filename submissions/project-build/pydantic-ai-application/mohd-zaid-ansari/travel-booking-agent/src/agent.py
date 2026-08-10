from pydantic_ai import Agent, RunContext, Tool
from src.tools.database import get_travel_plan
from src.tools.weather import weather_information
from src.guardrails import validation_check

system_prompt="""you are a Travel Booking Assistant Agent your task is to get the user details from database and weather information from weather api tool and give update of weather to the user where they are travelling and give suggestion what precautions or measures they can take before travelling.

Rule:
- You have to lookup to database for any user infomation.
- according to the city user is travelling get weather information for them.
- provide some essential measures they can take before travelling.
- Do not fetch weather from your own knowledge.
- Always check weather the user_input is validated or not.
"""

agent=Agent(
    'groq:llama-3.1-8b-instant',
    deps_type=str,
    tools=[get_travel_plan, weather_information],
    instructions=system_prompt
)


result=agent.run_sync("All information about booking_id TRV-101")
print(result)

try:
    validated_output = validation_check.validate(result)
    final_clean_object = validated_output.model_validate_json(validated_output.validation_output)
    final_clean_object
except Exception as e:
    {"status": "Rejected", "reason": "Database record content failed safety policies.", "error": str(e)}