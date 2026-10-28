import os
import asyncio
from mcp_use import MCPAgent, MCPClient
from config import llm


async def main():
    try:
        config = MCPClient(os.path.join(os.path.dirname(__file__), "mcp.json"))
    except Exception as e:
        print(e)


    agent = MCPAgent(
        llm = llm,
        client=config,
        max_steps=30,
        use_server_manager=False
    )

    query = input("Enter your query: ").strip().lower()
    
    if query in ["quit", "exit", "bye", "q"]:
            return False
    else:
            result = await agent.run(query)
            print(f"\nResult: {result}")


if __name__ == "__main__":
      while True:
        should_continue = asyncio.run(main())
        if should_continue is False:
            print("Bye Bye...")
            break