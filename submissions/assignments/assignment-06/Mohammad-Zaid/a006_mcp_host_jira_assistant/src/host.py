import os
import json
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from mcp_use import MCPAgent

from llm import llm
from mcp_client import client, available_tools
from prompts import SYSTEM_PROMPT

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent
output_file = ROOT_DIR / "outputs" / "jira_outputs.txt"
output_file.parent.mkdir(parents=True, exist_ok=True)

def save_output(query, output, filename=output_file):
    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write(f"User Query:\n{query}\n\n")
            f.write("Jira Agent Response:\n")
            f.write(str(output))
            f.write("\n\n")

        print(f"Output saved to {filename}")

    except Exception as e:
        print(f"Error saving output: {e}")
async def main():
    
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=30,
        system_prompt=SYSTEM_PROMPT,
        use_server_manager=False,
        tools_used_names=available_tools,
    )
    
    while True:
        query = input("\nEnter your query: ").strip()

        if query.lower() in {"exit", "quit", "q"}:
            print("Exiting jira MCP server...")
            break
        try:
            result = await agent.run(query)
            # just for debugging purpose
            print("\nResult:\n")
            print(result)

            save_output(query, result)
        except Exception as e:
            print(f"\nError: {e}")
        

if __name__ == "__main__":
    asyncio.run(main())