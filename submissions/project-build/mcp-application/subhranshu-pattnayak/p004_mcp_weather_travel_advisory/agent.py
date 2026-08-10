import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
import os
from config import ROOT_DIR

SERVER_PATH = os.path.join(ROOT_DIR, "src", "server.py")


async def main():
    config = {
        "mcpServers": {
            "weather_server": {
                "command": "python",
                "args": [SERVER_PATH]
            }
        }
    }

    client = MCPClient(config=config)

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0
    )

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        system_prompt="""
            1. Validate the city.
            2. Fetch weather data.
            3. Normalize the weather data.
            4. Calculate the weather risk.
            5. Use the three prompts to generate:
            - Travel readiness advisory
            - Weather risk explanation
            - Packing suggestions
            6. Combine all outputs into the required report format.
            7. Call save_travel_advisory_tool with the complete report.
            8. Inform the user that the report has been saved.
        """
    )

    print("=" * 60)
    print("Weather Travel Advisory Assistant")
    print("=" * 60)

    while True:
        query = input("\nEnter your request (or 'exit'): ").strip()

        if query.lower() == "exit":
            break

        try:
            response = await agent.run(query)

            print("\nResponse\n")
            print(response)

        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())