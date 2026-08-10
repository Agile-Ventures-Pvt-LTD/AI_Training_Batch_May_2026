import asyncio
import json
from src.output_writer import save_output
from mcp_use import MCPAgent, MCPClient
from src.prompts import system_prompt
from src.config import config
import os
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
os.environ['GROQ_API_KEY']=os.getenv("GROQ_API_KEY")
os.environ['GROQ_MODEL']=os.getenv("GROQ_MODEL")


def get_llm():
    return ChatGroq(
        model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b"),
        api_key=os.getenv("GROQ_API_KEY")
    )

config_client = MCPClient(config)

mcp_agent = MCPAgent(
    llm = get_llm(),
    client = config_client,
    max_steps = 10,
    system_prompt = system_prompt

)

async def main():

    print("Operational Assistant")
    print("\nConnected MCP Servers:\n- service-health\n- support-ticket\n- change-management")

    while True:

        query = input("\nEnter your query: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        if not query:
            print("Please enter a query.")
            continue

        try:
            result = await mcp_agent.run(query)
            output = json.loads(result)

            print("\nOutput:")
            print(output)

            save_output(output)


        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())




