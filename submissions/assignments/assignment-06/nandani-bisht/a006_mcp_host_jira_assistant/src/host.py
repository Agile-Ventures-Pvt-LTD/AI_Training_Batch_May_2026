import asyncio
import json
import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm import GroqAgent
from mcp_client import JiraMCPClient
from prompts import build_messages

MAX_TOOL_ITERATIONS = 6
WRITE_TOOLS = frozenset({"add_issue_comment", "update_issue_status"})

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS_DIR = os.path.join(PROJECT_ROOT, "outputs")
HISTORY_FILE = os.path.join(OUTPUTS_DIR, "query_history.json")

console = Console()


class QueryResult(BaseModel):
    user_query: str
    tools_used: list[str] = Field(default_factory=list)
    final_answer: str
    write_action_performed: bool = False


class ToolLoopExceededError(Exception):
    pass


async def run_query(user_query, mcp_client, llm_agent, max_iterations=MAX_TOOL_ITERATIONS):
    messages = build_messages(user_query)
    tools = await mcp_client.list_tools_for_groq()
    tools_used = []

    for _ in range(max_iterations):
        assistant_message = llm_agent.next_step(messages, tools)

        if not assistant_message.tool_calls:
            final_answer = assistant_message.content or "No answer returned."
            return QueryResult(
                user_query=user_query,
                tools_used=tools_used,
                final_answer=final_answer,
                write_action_performed=any(t in WRITE_TOOLS for t in tools_used),
            )

        messages.append(assistant_message.model_dump(exclude_none=True))

        for tool_call in assistant_message.tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments or "{}")
            except json.JSONDecodeError:
                arguments = {}

            tool_result = await mcp_client.call_tool(tool_name, arguments)
            tools_used.append(tool_name)

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result,
                }
            )

    raise ToolLoopExceededError(
        f"Stopped after {max_iterations} iterations without a final answer: {user_query!r}"
    )


def save_result_to_outputs(result):
    os.makedirs(OUTPUTS_DIR, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    result_path = os.path.join(OUTPUTS_DIR, f"query_result_{timestamp}.json")
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2)

    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
        except (json.JSONDecodeError, OSError):
            history = []

    history.append({"timestamp": timestamp, **result.model_dump()})
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    return result_path


async def _interactive_loop():
    load_dotenv()
    server_script = os.environ.get(
        "MCP_SERVER_SCRIPT", os.path.join(PROJECT_ROOT, "server", "jira_mcp_server.py")
    )
    llm_agent = GroqAgent()

    console.print(
        Panel.fit(
            "Jira Issue Assistant\nType a question, or 'exit' to quit.",
            title="MCP Host",
        )
    )

    async with JiraMCPClient(server_script) as mcp_client:
        while True:
            try:
                user_query = console.input("[bold cyan]you>[/bold cyan] ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            if not user_query:
                continue
            if user_query.lower() in {"exit", "quit"}:
                break

            try:
                result = await run_query(user_query, mcp_client, llm_agent)
            except ToolLoopExceededError as exc:
                console.print(f"[red]error:[/red] {exc}")
                continue

            console.print_json(data=result.model_dump())
            saved_path = save_result_to_outputs(result)
            console.print(f"[dim]saved to {saved_path}[/dim]")


def main():
    asyncio.run(_interactive_loop())


if __name__ == "__main__":
    main()
