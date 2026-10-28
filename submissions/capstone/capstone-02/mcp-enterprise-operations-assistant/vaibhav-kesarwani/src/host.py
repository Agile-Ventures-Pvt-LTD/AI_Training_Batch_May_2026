import os
import json
import asyncio
from mcp_use import MCPClient, MCPAgent
from config import llm
from prompts import agent_system_prompt, JSON_SCHEMA_PROMPT
from output_writer import output_writer

async def main():
    try:
        config = MCPClient(os.path.join(os.path.dirname(__file__), "mcp.json"))

    except Exception as e:
        print(f"Not able to load the mcp.json file")

    try:
        agent = MCPAgent(
            llm=llm,
            client=config,
            max_steps=10,
            use_server_manager=False,
            system_prompt=agent_system_prompt + "\n" + JSON_SCHEMA_PROMPT
        )
    except Exception as e:
        print(f"Error connecting with the agent : {e}")   


    try: 
        with open("./src/mcp.json", "r") as f:
            data = json.load(f)

        servers = list(data["mcpServers"].keys())

    except Exception as e:
        print(f"Error loading the mcp.json")


    print("Enterprise Operations Assistant\n\n")
    print("Connected MCP Servers:")
    for server in servers:
        print(f"- {server}")
        

    print("\n\nEnter your question: ")
    query = input("> ").strip().lower()
    print("\n\nProcessing...")

    if query in ["q", "quit", "exit"]:
        return False
    
    try:
        result = await agent.run(query)

        try:
            response = json.loads(result)
        except json.JSONDecodeError:
            print("Agent did not return valid JSON. Raw output:")
            print(result)
            return True

        output_writer(response, "mandatory_query.json")
    except Exception as e:
        print(f"Error processing query: {e}")


if __name__ == "__main__":
    while True:
        run = asyncio.run(main())

        if run is False:
            print("Bye....")
            break