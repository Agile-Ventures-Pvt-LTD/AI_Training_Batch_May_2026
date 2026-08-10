from src.tools.database import get_travel_plan
from src.tools.weather import weather_information
from src.agent import Agent

query="TRV-101"
result=get_travel_plan(query)
print(result)

result=weather_information("Chicago")
print(result)

result=Agent.run_sync("All information about booking_id TRV-101")
print(result)
