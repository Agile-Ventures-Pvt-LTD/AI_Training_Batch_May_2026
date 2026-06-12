import os
import json
from pathlib import Path
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    ToolMessage
)

from prompts import SYSTEM_PROMPT,planning_prompt

from tools import search_tickets,get_ticket_details,add_ticket_comment, update_ticket_status, ticket_comment_tools, calculate_sla_status, prioritization, save_conversation



load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


available_tools = {
     "search_tickets": search_tickets,
     "get_ticket_details":get_ticket_details,
     "ticket_comment_tools":ticket_comment_tools,
     "calculate_sla_status":calculate_sla_status,
     "prioritization":prioritization,
     "update_ticket_status":update_ticket_status,
     "add_ticket_comment":add_ticket_comment,
     "save_conversation":save_conversation
}


agent = llm.bind_tools(
    list(available_tools.values()),
    tool_choice="auto",
    parallel_tool_calls=True
)


def invoke(user_query: str):
    """
    Main function to handle user queries, invoke tools, and generate final response.
    """

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=user_query)
    ]

    
    response = agent.invoke(messages)
    
    messages.append(response)

    plan=agent.invoke([
        SystemMessage(content=planning_prompt)
    ])
    print("Initial Agent Response:", plan.content)

    if not response.tool_calls:
        return response.content
   
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool = available_tools[tool_name]
        tool_result = tool.invoke(tool_call["args"])

        messages.append(
            ToolMessage(
                content=str(tool_result),
                tool_call_id=tool_call["id"]
            )
        )

  
    final_response = agent.invoke(messages)

    from prompts import Reflection_prompt, reflection_user

    raw_response = agent.invoke([
        SystemMessage(content=Reflection_prompt),
        HumanMessage(content=reflection_user.format(user_query=user_query, agent_response=final_response.content))
    ])
    print(raw_response.content)

    # output_dir = Path("outputs")
    # output_dir.mkdir(exist_ok=True)

    # output_file = output_dir / "reflection.json"

    # with open(output_file, "w") as f:
    #     json.dump(raw_response, f, indent=4)

    return final_response.content


