
import asyncio
from src.mcp_client import host_agent
from src.utils import save_output
import json


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





