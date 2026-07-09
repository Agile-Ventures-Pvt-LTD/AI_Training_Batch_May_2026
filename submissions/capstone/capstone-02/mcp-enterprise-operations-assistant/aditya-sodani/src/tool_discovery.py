import asyncio
import json
import os
from mcp_use import MCPClient
from src.config import MCP_CONFIG

OUTPUT_FILE = "outputs/tool_discovery.json"

async def discover_tools():
   print("Starting MCP Tool Discovery...")
   os.makedirs("outputs",exist_ok=True)

   client = MCPClient(MCP_CONFIG)

   try:
       await client.create_all_sessions()
       discovery_result = {}

       for server_name, session in client.sessions.items():
           print(
               f"Discovering tools from {server_name}"
           )

           tools_response = await session.list_tools()

           tools = []

           for tool in tools_response:

               tools.append(
                   tool.name
               )

           discovery_result[
               server_name
           ] = tools


       with open(OUTPUT_FILE,"w") as f:

           json.dump(discovery_result,f,indent=4)

       print("\nTool Discovery Completed")

       print(
           json.dumps(discovery_result,indent=4)
       )

   finally:

       await client.close_all_sessions()



if __name__ == "__main__":

   asyncio.run(
       discover_tools()
   )