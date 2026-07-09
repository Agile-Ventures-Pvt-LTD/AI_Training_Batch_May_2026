## MCP Host — Enterprise Operations Assistant
## Connects Groq LLM to three local MCP servers over stdio.
## The LLM decides which tools to call — no hardcoded routing.

import os
import logging
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

logging.getLogger("mcp_use").setLevel(logging.WARNING)

load_dotenv()

model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

'''
Connect to all three local MCP servers (stdio) and load every tool they expose
'''
client = MCPClient.from_dict({
    "mcpServers": {
        "service-health": {
            "command": "uv",
            "args": ["run", "python", "servers/service_health_server.py"],
        },
        "support-ticket": {
            "command": "uv",
            "args": ["run", "python", "servers/support_ticket_server.py"],
        },
        "change-management": {
            "command": "uv",
            "args": ["run", "python", "servers/change_management_server.py"],
        },
    }
})

agent = MCPAgent(
    llm=ChatGroq(model=model, temperature=0),
    client=client,
    max_steps=10,
    system_prompt=(
        "You are an Enterprise Operations Assistant. "
        "Use the available MCP tools whenever the user asks about "
        "service health, incidents, tickets, or changes. "
        "Never invent values — always call a tool. "
        "Describe a change/incident timing match as a possible "
        "correlation only, never a confirmed root cause."
    ),
)


async def ask(question: str) -> str:
    return await agent.run(question)


async def main() -> None:
    print("Enterprise Operations Assistant")
    while True:
        question = input("Enter your question (or 'quit'): ").strip()
        if question.lower() in ("quit", "exit"):
            break
        if not question:
            continue
        print(await ask(question))
        print()


if __name__ == "__main__":
    asyncio.run(main())