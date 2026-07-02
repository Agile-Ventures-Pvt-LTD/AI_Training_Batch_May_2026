import os
import sys
import json
import asyncio
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.mcp_client import MCPClientManager
from src.llm import GroqEngine
from src.prompts import System_Prompt

load_dotenv()

async def handle_user_query(query_str: str) -> dict:
    server_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../server/jira_mcp_server.py"))
    client = MCPClientManager(server_path)
    engine = GroqEngine()
    tools_used = []
    write_action_performed = False
    final_answer = ""
    await client.connect()
    groq_tools = engine.format_mcp_tools(client.tools)
    messages = [
        {"role": "system", "content": System_Prompt},
        {"role": "user", "content": query_str}
    ]
    try:
        for _ in range(5):
            response = engine.generate_chat_response(messages, tools=groq_tools)
            response_message = response.choices[0].message
            if response_message.tool_calls:
                messages.append(response_message) 
                for tool_call in response_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    tools_used.append(tool_name)
                    if tool_name in ["add_issue_comment", "update_issue_status"]:
                        write_action_performed = True                    
                    tool_output = await client.execute_tool(tool_name, tool_args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_name,
                        "content": tool_output
                    })
                continue
            else:
                final_answer = response_message.content
                break
        else:
            final_answer = "Error: Agent reached multi-step execution threshold limits without generating a completion answer."
    finally:
        await client.disconnect()
    return {
        "user_query": query_str,
        "tools_used": list(set(tools_used)),
        "final_answer": final_answer,
        "write_action_performed": write_action_performed
    }

def dump_output_to_file(output_data: dict):
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    output_dir = os.path.join(root_dir, "outputs")
    file_path = os.path.join(output_dir, "query_outputs.json")
    os.makedirs(output_dir, exist_ok=True)
    history = []
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = [history]
        except (json.JSONDecodeError, ValueError):
            history = []
    history.append(output_data)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

async def main():
    print("Jira Issue Assistant")
    print("Type your query and press Enter. Type 'exit' or 'quit' to terminate.\n")
    while True:
        try:
            query = input("Jira Assistant > ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit"]:
                print("Terminating session.")
                break
            print("\nProcessing query...")
            output = await handle_user_query(query)
            print("\nResult")
            print(json.dumps(output, indent=2))
            dump_output_to_file(output)  
        except KeyboardInterrupt:
            print("\nSession interrupted. Exiting.")
            break
        except Exception as e:
            print(f"\nAn error occurred while processing: {str(e)}\n")

if __name__ == "__main__":
    asyncio.run(main())
