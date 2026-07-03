import os
import json
from pydantic_ai import Agent
from pydantic import BaseModel
from typing import List
from tools.database import user_information
from tools.weather import get_weather_forcast
from guardrails_config import validattion_user_input, validate_output
from dotenv import load_dotenv
load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
from groq import Groq
client = Groq()

rag_prompt = """
Destination: {destination}
travel_dates : {travel_dates}
hotel_details: {hotel_details}

analyse the user input query: {input_query} and according to the user , expalain the travel 
retrieve destination :{destination} and travel_dates: {travel_dates} and according to the weather report retreive generated some recommendation action
here is one example of output
1. input_query: "What is the weather going to be like for
my upcoming trip
    answers: "I see you are flying to London next Tuesday; you should pack an umbrella as rain is
forecasted
"""


agent = Agent(
    "groq:openai/gpt-oss-120b",
    output_type=ResponseModel,
    system_prompt=(
        rag_prompt
    ),
    tools=[user_information,get_weather_forcast],
)

async def main():
    print("Agent support is active")
    print("Type 'exit' to quit")
    print()
    final_result=""
    while True:
        try:
            input_query = input("Enter your query: ")
            if input_query.lower() in ("exit", "quit"):
                break
            
            if validattion_user_input:
                result = await agent.run(input_query)
                result.all_messages()
                final_result = validattion_user_input(result)
                return final_result      
            else:
                return "validation fail " 
            print()
            print(json.dumps(final_result, indent=2))
            print()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())