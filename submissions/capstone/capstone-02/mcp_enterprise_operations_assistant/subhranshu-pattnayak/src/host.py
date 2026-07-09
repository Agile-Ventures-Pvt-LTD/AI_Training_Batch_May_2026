import os
import asyncio
from prompts import SYSTEM_PROMPT
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient
from config import SERVER_PATH
from langchain_core.callbacks import BaseCallbackHandler


class ToolCaptureCallback(BaseCallbackHandler):
    def __init__(self):
        self.tool_calls = []

    def on_tool_start(self, serialized, input_str, **kwargs):
        self.current = {
            "tool": serialized.get("name"),
            "input": input_str
        }

    def on_tool_end(self, output, **kwargs):
        self.current["output"] = output
        self.tool_calls.append(self.current)


async def main():

    # Initialize the MCP Client with the server using stdio transport
    
    config = MCPClient({
        "mcpServers": {
            "service-health": {
                "command": "uv",
                "args": [
                    "run",
                    "python",
                    os.path.join(SERVER_PATH, "service_health_server.py")
                ]
            },
            "support-ticket": {
                "command": "uv",
                "args": [
                    "run",
                    "python",
                    os.path.join(SERVER_PATH, "support_ticket_server.py")
                ]
            },
            "change-management": {
                "command": "uv",
                "args": [
                    "run",
                    "python",
                    os.path.join(SERVER_PATH, "change_management_server.py")
                ]
            }
        }
    })

    callback = ToolCaptureCallback()

    
    # Initialize the LLM
    llm = ChatGroq(model="openai/gpt-oss-120b")


    # Intialize the MCP Agent
        
    agent = MCPAgent(
        system_prompt=SYSTEM_PROMPT,
        llm=llm,
        client=config,
        max_steps=30,
        use_server_manager=True,
        callbacks=[callback]
    )
    
    query = input("Enter your query: ").strip().lower()
    if query in ["quit", "exit", "bye", "q"]:
        return False
    else:
        result = await agent.run(query)
        print(f"\nResult: {result}")
        print(callback.tool_calls)

if __name__ == '__main__':
    while True:
        should_continue = asyncio.run(main())
        if should_continue is False:
            print("Exiting gracefully...")
            break