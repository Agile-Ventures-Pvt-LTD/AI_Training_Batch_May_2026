from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, ToolMessage
from config import GROQ_API_KEY, GROQ_MODEL
from prompts import system_prompt
from memory import get_recent_logs
from langchain_experimental.utilities import PythonREPL

import json
from langchain import hub
from langchain.agents import create_react_agent, Tool, AgentExecutor
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_experimental.utilities import PythonREPL

from tools import (
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
    save_conversation,
    recall_conversation,
    save_archival_memory,
    recall_archival_memory,
    summarize_conversation
)

# ---------------- LLM ----------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0
)

# ---------------- TOOLS ----------------
tools = {
    'search_tickets':search_tickets,
    'get_ticket_details':get_ticket_details,
    'get_ticket_comments':get_ticket_comments,
    'calculate_sla_status':calculate_sla_status,
    'prioritize_tickets':prioritize_tickets,
    'update_ticket_status':update_ticket_status,
    'add_ticket_comment':add_ticket_comment,
    'save_conversation':save_conversation,
    'recall_conversation':recall_conversation,
    'save_archival_memory':save_archival_memory,
    'recall_archival_memory':recall_archival_memory,
    'summarize_conversation':summarize_conversation
    }

# ---------------- AGENT ----------------
agent = llm.bind_tools(list(tools.values()),
                       tool_choice="any",
                       parallel_tool_calls = True)


print(tools)

for tool in tools:
    print(tool)
    print(type(tool))

# query = "user_input"

# messages = [HumanMessage(query)]
# ---------------- PLAN ----------------


python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="A Python shell used to execute python commands. Input should be a valid python command.",
    func=python_repl.run,
)

react_agent = create_react_agent(
    llm=llm,
    tools=[repl_tool],
    prompt=react_prompt
)


def create_plan(user_input):
    return {
        "user_goal": user_input
    }

# ---------------- REFLECT ----------------
def reflect(result):
    return {
        "tool_result_available": True,
        "answer_complete": bool(result),
        "missing_information": [],
        "risk": "No ambiguity detected"
    }

# ---------------- RUN ----------------
def run_agent(user_input):

    plan = create_plan(user_input)

    response = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    })

    # safe extraction (IMPORTANT)
    final_answer = ""

    if "messages" in response:
        for msg in reversed(response["messages"]):
            if hasattr(msg, "type") and msg.type == "ai":
                final_answer = msg.content
                break

    if not final_answer:
        final_answer = response.get("output", "")

    return {
        "user_request": user_input,
        "plan_summary": plan,
        "tools_used": [],  # NOTE: this agent version doesn't expose tools reliably
        "tool_result_summary": "",
        "reflection_summary": reflect(final_answer),
        "final_answer": final_answer,
        "memory_used": (
            "remember" in user_input.lower()
            or "discuss earlier" in user_input.lower()
        ),
        "write_action_performed": (
            "update" in user_input.lower()
            or "comment" in user_input.lower()
        )
    }

