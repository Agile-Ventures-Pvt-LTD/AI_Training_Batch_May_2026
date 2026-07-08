import os
import sys
import asyncio

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.makedirs("outputs", exist_ok=True)
output_path = os.path.join("outputs", "mandatory_query_results.json")

os.makedirs("outputs", exist_ok=True)
output_path = os.path.join("outputs", "ample_run_outputs.md")

from pathlib import Path

from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from dotenv import load_dotenv

from src.prompts import System_Prompt
from src.config import GROQ_MODEL, GROQ_API_KEY

load_dotenv()


async def main():
    base_dir = Path(__file__).resolve().parent.parent
    service_health_path = str(base_dir / "servers" / "service_health_server.py")
    support_ticket_path = str(base_dir / "servers" / "support_ticket_server.py")
    change_management_path = str(base_dir / "servers" / "change_management_server.py")

    mcp_config = {
        "mcpServers": {
            "service-health": {
                "transport": "stdio",
                "command": "python",
                "args": ["-u", service_health_path],
            },
            "support_ticket": {
                "transport": "stdio",
                "command": "python",
                "args": ["-u", support_ticket_path],
            },
            "change_management": {
                "transport": "stdio",
                "command": "python",
                "args": ["-u", change_management_path],
            },
        }
    }

    client = MCPClient(mcp_config)

    llm = ChatGroq(model=GROQ_MODEL, temperature=0)

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        system_prompt=System_Prompt,
    )

    query = input("Enter your query: ").strip()
    query_lc = query.lower()
    if query_lc in ["quit", "exit", "bye", "q"]:
        return False
    else:
        result = await agent.run(query)
        print(f"\nResult: {result}")

    with open(output_path, "a", encoding="utf-8") as f:
        f.write(f"User Query: {query}\n")
        f.write(f"Agent Response:\n{result}\n")
        f.write("=" * 80 + "\n")

    print(f"\nOutput appended to: {output_path}")


if __name__ == "__main__":
    while True:
        should_continue = asyncio.run(main())
        if should_continue is False:
            print("Exiting gracefully...")
            break

