import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))

from src.tools.database import get_details
from src.tools.weather import get_weather

from pydantic_ai import Agent
from dotenv import load_dotenv
from src.guardrails_config import profinity_guard, toxic_guard
load_dotenv()
from pydantic_ai import Agent, FunctionToolset

weather_toolset = FunctionToolset(tools=[get_details, get_weather])

agent = Agent(
  'groq:openai/gpt-oss-120b',
  instructions=(
      """you are an plan advisory agent . your task is to assist user in planning thier trips
      You have a tool to get user data that will help you to get user all information about travelling datesand all
      you also have a tool that is user to get weather.
      you first need to get user data and based on data you need to get weather of user's location using another tool
      now you have all the information , based on all information you get help the user to plan thier trip/tour
      
      Return the suggestions that help user in planning.
      """
  ),
  toolsets=weather_toolset
)


def run_pipeline(query:str)->dict:
  
  profinity_input=profinity_guard(query)
  if profinity_input["found"]==False:
    return {
      "error":"input is not valid"
    }
  toxic_input=toxic_guard(query)
  if toxic_input["found"]==False:
    return {
      "error":"input is not valid"
    }
  result=agent.run(query)
  
  profinity_out=profinity_guard(result)
  if profinity_out["found"]==False:
    return {
      "error":"output is not valid"
    }
  toxic_out=toxic_guard(result)
  if toxic_out["found"]==False:
    return {
      "error":"output is not valid"
    }
  
  return{
    "result":result
  }



