import json
import asyncio
import logging
from dotenv import load_dotenv
from src.llm import get_groq_llm
from src.prompts import SYSTEM_PROMPT
from src.mcp_client import create_mcp_agent

for name in ["mcp_use", "mcp_use.telemetry", "langgraph", "langchain", "langchain_core"]:
    logging.getLogger(name).setLevel(logging.WARNING)
    logging.getLogger(name).handlers = []
    logging.getLogger(name).propagate = False

load_dotenv()


async def process_query(agent, user_query: str) -> dict:
    """Process a user query using the MCP agent with Groq LLM."""
    tools_used = []
    write_action_performed = False
    write_tools = {"add_issue_comment", "update_issue_status"}
    final_answer = ""

   
    async for chunk in agent.stream(user_query):
       
        if isinstance(chunk, tuple):
            agent_action, step_output = chunk
            # agent_action contains tool info
            if hasattr(agent_action, "tool"):
                tool_name = agent_action.tool
                if tool_name not in tools_used:
                    tools_used.append(tool_name)
                    if tool_name in write_tools:
                        write_action_performed = True
            final_answer = step_output
        else:
            # Plain string output (final answer)
            final_answer = chunk

    return {
        "user_query": user_query,
        "tools_used": tools_used,
        "final_answer": final_answer,
        "write_action_performed": write_action_performed
    }


async def main():
    print("Initializing Jira Issue Assistant...")
    print("Connecting to Jira MCP Server via stdio...")

    llm = get_groq_llm()
    agent = create_mcp_agent(llm=llm, system_prompt=SYSTEM_PROMPT)

    print("Jira Issue Assistant is ready!")
    print("Type 'exit' to quit")
    print()

    while True:
        try:
            query = input("Enter your query: ")
            if query.lower() in ("exit", "quit"):
                break

            result = await process_query(agent, query)
            print()
            print(json.dumps(result, indent=2))
            print()

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())