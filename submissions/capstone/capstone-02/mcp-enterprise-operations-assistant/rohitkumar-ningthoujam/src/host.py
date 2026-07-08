import asyncio
import json
import sys
from pathlib import Path
from langchain_groq import ChatGroq
from mcp_use import MCPClient, MCPAgent
from src.config import GROQ_API_KEY, GROQ_MODEL, MCP_SERVER_CONFIG
from src.prompts import SYSTEM_PROMPTS

OUTPUTS_DIR = Path(__file__).resolve().parents[1] / "outputs"

async def run_query(agent, query: str):
    result = await agent.run(query)
    return result

async def main():
    if not GROQ_API_KEY:
        print("Error: GROQ_API_KEY not set in .env file")
        sys.exit(1)

    llm = ChatGroq(model=GROQ_MODEL, temperature=0, api_key=GROQ_API_KEY)
    client = MCPClient(MCP_SERVER_CONFIG)
    agent = MCPAgent(llm=llm, client=client, max_steps=10, system_prompt=SYSTEM_PROMPTS)

    await agent.initialize()

    print("Enterprise Operations Assistant")
    print()

    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        print(f"Query: {query}")
        print("Processing...")
        result = await run_query(agent, query)
        print(result)
    else:
        print("Enter your question:")
        try:
            query = input("> ")
            print("Processing...")
            result = await run_query(agent, query)
            print(result)
        except (EOFError, KeyboardInterrupt):
            print()

    await agent.close()

if __name__ == "__main__":
    asyncio.run(main())