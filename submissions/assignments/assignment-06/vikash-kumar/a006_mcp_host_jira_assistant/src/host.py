import asyncio
import os
import json
from langgraph.func import task
from mcp_use import MCPAgent
from llm import get_llm
from mcp_client import get_client
from prompts import SYSTEM_PROMPT

async def run_query(agent, query):
    response = await agent.run(query)

    tools_used = list({(tool.get("name") if hasattr(tool, "get") else getattr(tool, "name", None))
        for msg in agent.get_conversation_history()
        for tool in getattr(msg, "tool_calls", [])} - {None})
    
    result = {"user_query": query,"tools_used": tools_used,"final_answer": response,"write_action_performed": any(t in {"add_issue_comment", "update_issue_status"} for t in tools_used)}
    
    print(f"{json.dumps(result, indent=2)}")
   
    filename = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs", "query_output.json")
    data = []
    if os.path.exists(filename):
        with open(filename, "r") as f:
            content = f.read().strip()
            if content:
                try:
                    parsed = json.loads(content)
                    if isinstance(parsed, list):
                        data = parsed
                    else:
                        data = [parsed]
                except json.JSONDecodeError:
                    data = []

    data.append(result)

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    print(f"The output is saved in {filename}")

async def main():
    client = get_client()
    agent = MCPAgent(llm=get_llm(), client=client, system_prompt=SYSTEM_PROMPT, max_steps=10)
    
    await client.create_all_sessions()
    
    try:
        tools_list = [task.name for task in await client.get_session("jira").list_tools()]
    except Exception:
        tools_list = ["list_projects", "search_issues", "get_issue_details", "get_issue_comments", "add_issue_comment", "update_issue_status"]
    
    print(f"{json.dumps({'available_tools': tools_list}, indent=2)}")
    
    os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs"), exist_ok=True)
    
    try:
        while True:
            try:
                query = input("Write your query: ").strip()
            except (KeyboardInterrupt, EOFError):
                break
            if not query:
                continue
            if query.lower() == "exit":
                break
            try:
                await run_query(agent, query)
                agent.clear_conversation_history()
            except Exception as e:
                print("The error is: ", e)
    finally:
        await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
