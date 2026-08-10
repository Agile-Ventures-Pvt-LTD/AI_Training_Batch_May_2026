import os
import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv
load_dotenv()
import os
import requests

WTTR_PRIMARY_URL = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
WTTR_FALLBACK_URL = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")

def get_weather_from_wttr(normalized_city_name: str) -> dict:
    urls = [
    f"{WTTR_PRIMARY_URL}/{normalized_city_name}?format=j1",
    f"{WTTR_FALLBACK_URL}/{normalized_city_name}?format=j1"
        ]
        
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return {
                "success": True,
                "url_used": url,
                "raw_weather_data": response.json()
                        }
        except Exception as error:
                last_error = str(error)
                
    return {
        "success": False,
        "message": f"Unable to fetch weather data. Last error:{last_error}"
        }

async def main():

    # Initialize the MCP Client with Server  
    config = MCPClient(os.path.join(os.path.dirname(__file__), "mcp.json"))
    
    # Initialize the LLM
    llm = ChatGroq(model="openai/gpt-oss-120b")

    #Initialize the MCP Agent
    agent = MCPAgent(llm=llm,
                    client=config,
                    max_steps=30,
                    use_server_manager=False)



    query = input("Enter the city: ").strip().lower()

    if query in ["quit", "exit", "bye", "q"]:
        return False
    else:
        result = await agent.run(query)
        print(f"\nResult: {result}")


if __name__ == "__main__":
    while True:
        should_continue = asyncio.run(main())
        if should_continue is False:
            print("Exiting gracefully...")
            break



