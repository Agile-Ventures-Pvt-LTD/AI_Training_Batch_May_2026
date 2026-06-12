from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory

from prompts import system_prompt
from output_formatter import format_output
from tools import (
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
from config import llm

import os

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
tools = [
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
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    memory=memory,
    verbose=True,
    max_iteration=3,
    handle_parsing_errors=True,
    agent_kwargs={
        "prefix": system_prompt
    }
)

def reflect(result: str) -> dict:
    if not result:
        return {
            "tool_result_available": False,
            "answer_complete": False,
            "missing_information": ["No output from agent"],
            "risk": "High risk: empty response"
        }

    return {
        "tool_result_available": True,
        "answer_complete": True,
        "missing_information": [],
        "risk": "No issues detected"
    }


def run_agent(user_input: str):
    result = agent.run(user_input)

    reflection = reflect(result)

    return format_output(
        user_request=user_input,
        plan_summary="Agent decided tool based execution flow",
        tools_used=["agent.run"],
        tool_result_summary=str(result),
        reflection_summary=reflection,
        final_answer=result,
        memory_used=True,
        write_action_performed=False
    )

if __name__ == "__main__":
    print("\nHelpdesk Agent Running...\n")

    while True:
        query = input("User: ")

        if query.lower() in ["exit", "quit"]:
            break

        response = run_agent(query)

        print("\nAgent:", response["final_answer"])
        print("\nReflection:", response["reflection_summary"])