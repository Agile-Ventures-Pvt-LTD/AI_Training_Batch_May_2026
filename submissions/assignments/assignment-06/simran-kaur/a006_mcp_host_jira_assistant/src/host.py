
from mcp_use import MCPAgent
import asyncio
from src.utils import save_output
import json
from src.llm import model_llm
from src.mcp_client import config
from src.prompts import system_prompt


host_agent = MCPAgent(
    llm = model_llm,
    client = config,
    max_steps = 30,
    system_prompt = system_prompt

)


async def main():

    print("Jira MCP Assistant")

    while True:

        query = input("\nEnter your query: ").strip()

        if query.lower() in ["exit", "quit"]:
            print("Exiting...")
            break

        if not query:
            print("Please enter a query.")
            continue

        try:
            result = await host_agent.run(query)

            output = json.loads(result)

            print("\nOutput:")
            print(output)

            save_output(output)


        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())





