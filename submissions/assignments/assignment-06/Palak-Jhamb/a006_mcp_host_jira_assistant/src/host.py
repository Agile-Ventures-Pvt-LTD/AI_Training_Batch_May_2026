import asyncio
from mcp_client import mcp_agent
import json
from pathlib import Path

OUTPUT_FILE = Path(__file__).resolve().parent.parent / "outputs" / "jira_output.json"


def save_output(output: dict):

    OUTPUT_FILE.parent.mkdir(exist_ok=True)

    if OUTPUT_FILE.exists():
        try:
            with open(OUTPUT_FILE, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    data.append(output)

    with open(OUTPUT_FILE, "w") as file:
        json.dump(data, file, indent=4)



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
            result = await mcp_agent.run(query)

            output = json.loads(result)

            print("\nOutput:")
            print(output)

            save_output(output)


        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())




