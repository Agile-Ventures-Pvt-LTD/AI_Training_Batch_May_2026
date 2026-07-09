import os
import asyncio
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from src.config import (MCP_CONFIG,GROQ_MODEL,)
from src.prompts import SYSTEM_PROMPT
async def main() -> None:
    """
    MCP Host
    """
    llm = ChatGroq(model=GROQ_MODEL,temperature=0,)
    client = MCPClient(MCP_CONFIG)
    agent = MCPAgent(llm=llm,client=client,system_prompt=SYSTEM_PROMPT,max_steps=10,)
    try:
        await client.connect()
        print("Enterprise Operations Assistant")
        while True:
            query = input("Enter your question  ")
            if query.lower() == "exit":
                break
            response = await agent.run(query)
            print("Response")
            print(response)
    finally:
        await client.close()
if __name__ == "__main__":
    asyncio.run(main())