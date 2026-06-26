# client.py
import os
import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv
load_dotenv()

async def main():
    config = MCPClient(os.path.join(os.path.dirname(__file__), "mcp.json"))
    llm = ChatGroq(model="openai/gpt-oss-120b")

    agent = MCPAgent(llm=llm,
                    client=config,
                    max_steps=30,
                    use_server_manager=False)

    query = input("Enter your query: ").strip().lower()
    if query in ["quit", "exit", "q"]:
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