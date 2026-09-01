import os 
import sys
from dotenv import load_dotenv
from pydantic_ai import Agent
from groq import Groq
import asyncio


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import initialize,get_collection,retriever
from guardrails_config import validate_input, validate_output

load_dotenv()

# client=Groq( model_name="openai/gpt-oss-120b")

agent=Agent(
    'groq:openai/gpt-oss-120b',
    system_prompt=(
        "You are a ebay specialist for shopsphere marketplace, " \
        "You must answer seller queries instantly while maintaining absolute deterministic safety standards,"\
        "ensuring no toxic, profane, or hallucinated outputs"
        "Guidelines:" \
        "Use the tool retrieve_info , you must use it to search"\
        "Your answers must be from the context"\
        "If answer is not in the context mention that you are Unable to answer this query"
        )
)
@agent.tool_plain
def retrieve_info(query):
    return retriever(query,n=5)

async def run_agent(query):
    if not validate_input(query):
        return "Your query is unsafe and therefore blocked"

    try:
        result= await agent.run(query)
        response = result.output 
    except Exception as e:
        print(f"{e}")
        raise e
    safe_response = validate_output(response)
    return safe_response

async def main():
    print("Project build 05")
    
    initialize()
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
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())