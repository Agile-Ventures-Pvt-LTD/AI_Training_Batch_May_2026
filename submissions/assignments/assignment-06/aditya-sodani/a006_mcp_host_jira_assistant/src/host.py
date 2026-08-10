import asyncio
import os

from dotenv import load_dotenv
from mcp_use import MCPAgent
from mcp_use.client import MCPClient
from src.prompts import SYSTEM_PROMPT
from output_logger import (
    log_query,
    clear_tools,
    get_tools_used,
)

from src.llm import get_llm

load_dotenv()


CONFIG = {
    "mcpServers": {
        "jira": {
            "command": "python",
            "args": [
                "-m",
                "server.jira_mcp_server"
                ],
        }
    }
}

async def initialize():

    print("=" * 60)
    print("Initializing Groq LLM...")
    print("=" * 60)

    llm = get_llm()

    print("✓ Groq initialized.\n")

    print("=" * 60)
    print("Starting MCP Client...")
    print("=" * 60)

    client = MCPClient.from_dict(CONFIG)

    await client.create_all_sessions()

    print("Connected to Jira MCP Server.\n")

    print("=" * 60)
    print("Discovering Tools...")
    print("=" * 60)

    discovered = await client.search_tools("")

    tool_names = [tool["name"] for tool in discovered["results"]]

    print()

    for tool in tool_names:
        print(f"• {tool}")

    print("\nTool discovery successful.\n")

    print("=" * 60)
    print("Creating MCP Agent...")
    print("=" * 60)

    agent = MCPAgent(
        llm=llm,
        client=client,
        system_prompt=SYSTEM_PROMPT,
        max_steps=10,
    )

    print("Agent Ready.\n")

    return client, agent


async def chat():

    client, agent = await initialize()

    print("=" * 60)
    print("JIRA AI ASSISTANT")
    print("=" * 60)
    print("Type 'exit' to quit.\n")

    while True:

        query = input("You : ")

        if query.lower() in ["exit", "quit"]:
            break

        try:
            clear_tools()

            response = await agent.run(query)

            tools = get_tools_used()

            log_query(
                user_query=query,
                tools_used=tools,
                final_answer=response,
                write_action_performed=any(
                    tool in ["add_issue_comment", "update_issue_status"]
                    for tool in tools
                ),
            )

            print("\nAssistant:\n")
            print(response)
            print()

        except Exception as e:

            print("\nError:\n")
            print(e)
            print()

    await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(chat())