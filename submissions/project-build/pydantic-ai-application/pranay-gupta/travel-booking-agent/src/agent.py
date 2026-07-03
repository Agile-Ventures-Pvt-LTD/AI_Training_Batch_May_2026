from pydantic_ai import Agent, RunContext
from pydantic import BaseModel, Field
from dataclasses import dataclass
from config import MODEL_NAME
from tools.database import get_details
from tools.weather import get_weather_details
from guardrails_config import input_guardrails, output_guardrails

@dataclass
class SupportDependencies:
    booking_id: str
    start_date: str
    end_date:str
    latitude:float
    longitude:float

class SupportOutput(BaseModel):
    get_user_details: str = Field(description='Advice to return of user details through booking ID')
    weather_details: str = Field(description="return all current day weather details based on user travel_dates")

agent = Agent(  
  MODEL_NAME,  
  deps_type=SupportDependencies,
  output_type=SupportOutput,  
  instructions=(  
      'You are a travel Booking Assistant, You use both tools database connection & weather information for user details.'
  ),
)

@agent.tool
async def get_details(booking_id:str):
    return await get_details(booking_id)

@agent.tool
async def get_weather_details(start_date: str,end_date:str,latitude:float,longitude:float):
    return await get_weather_details(start_date,end_date,latitude,longitude)

def main():
    user_query = input("user query: ")
    input_valid = input_guardrails(user_query)
    if input_valid.validation_passed is False:
        print("Invalid Input")
    
    deps = SupportDependencies(booking_id='TRV-101',start_date="2026-08-15",end_date="2026-08-20",latitude=48.85,longitude=2.35)
    result = agent.run(user_query, deps=deps)
    res = result.output
    output_valid = output_guardrails(res)
    if output_valid.validation_passed is False:
        print("I can't give answer because its toxic")  
    print(res)


if __name__ == "__main__":
    main()