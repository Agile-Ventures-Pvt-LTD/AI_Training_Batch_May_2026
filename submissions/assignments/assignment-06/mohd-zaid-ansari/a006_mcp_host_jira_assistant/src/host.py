import asyncio
import json
from pathlib import Path

from dotenv import load_dotenv
from mcp_use import MCPAgent

from llm import get_llm
from mcp_client import mcp_client
from prompts import SYSTEM_PROMPT

load_dotenv()

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)
output_file=OUTPUT_DIR/ "sample_output.json"


async def main():

    llm = get_llm()
    client = mcp_client()

    agent = MCPAgent(
        llm=llm,
        client=client,
        system_prompt=SYSTEM_PROMPT,
    )

    while True:

        query = input("\nAsk Jira Assistant: ")

        if query.lower() == "exit":
            break

        response = await agent.run(query)
        print(agent.tools_used_names)

        print("\nAssistant:\n")
        print(response)

        output = {
            "user_query": query,
            "tools_used": agent.tools_used_names,        # Can improve later
            "final_answer": str(response),
            "write_action_performed": False,
        }

        if output_file.exists():
            with open(output_file, "r", encoding="utf-8") as file:
                data=json.load(file)
        else:
            data=[]

        data.append(output)

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4,ensure_ascii=file)

if __name__ == "__main__":
    asyncio.run(main())