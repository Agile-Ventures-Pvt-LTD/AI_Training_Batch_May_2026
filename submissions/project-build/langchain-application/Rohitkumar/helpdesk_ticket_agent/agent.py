import uuid

from langchain_groq import ChatGroq
from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain_core.prompts import ChatPromptTemplate

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

from tools import TOOLS

from prompts import (
    SYSTEM_PROMPT,
    PLANNING_PROMPT,
    REFLECTION_PROMPT
)

from memory import (
    save_conversation,
    build_memory_context
)




llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name=GROQ_MODEL,
    temperature=0
)




agent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)




agent = create_tool_calling_agent(
    llm=llm,
    tools=TOOLS,
    prompt=agent_prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=TOOLS,
    verbose=True,
    return_intermediate_steps=True,
    handle_parsing_errors=True
)




def create_plan(user_input):

    try:

        chain = PLANNING_PROMPT | llm

        result = chain.invoke(
            {
                "user_input": user_input
            }
        )

        return result.content

    except Exception as e:

        return f"Planning Error: {str(e)}"


=

def reflect(
    user_input,
    tool_result,
    draft_answer
):

    try:

        chain = REFLECTION_PROMPT | llm

        result = chain.invoke(
            {
                "user_input": user_input,
                "tool_result": str(tool_result),
                "draft_answer": draft_answer
            }
        )

        return result.content

    except Exception as e:

        return f"Reflection Error: {str(e)}"




def run_agent(
    user_input,
    session_id=None
):

    if session_id is None:
        session_id = str(uuid.uuid4())

   

    memory_context = build_memory_context()

    enriched_input = f"""
User Request:
{user_input}

Known Preferences:
{memory_context}
"""

    

    plan = create_plan(user_input)

    

    result = agent_executor.invoke(
        {
            "input": enriched_input
        }
    )

    final_answer = result.get(
        "output",
        "No answer generated."
    )

    intermediate_steps = result.get(
        "intermediate_steps",
        []
    )

    tools_used = []

    for step in intermediate_steps:

        try:

            action = step[0]

            if hasattr(action, "tool"):

                tools_used.append(
                    action.tool
                )

        except Exception:
            pass

   

    reflection = reflect(
        user_input=user_input,
        tool_result=intermediate_steps,
        draft_answer=final_answer
    )

    
   

    try:

        save_conversation(
            session_id=session_id,
            user_message=user_input,
            agent_response=final_answer,
            tools_used=tools_used
        )

    except Exception as e:

        print(
            f"Conversation save failed: {e}"
        )

    

    tool_result_summary = []

    for step in intermediate_steps:

        try:

            tool_name = step[0].tool
            tool_output = step[1]

            tool_result_summary.append(
                {
                    "tool": tool_name,
                    "result": str(tool_output)[:500]
                }
            )

        except Exception:
            pass

    

    memory_tools = [
        "save_user_preference",
        "recall_user_preference",
        "recall_previous_conversation",
        "summarize_and_store_conversation"
    ]

    memory_used = any(
        tool in memory_tools
        for tool in tools_used
    )

   -

    write_tools = [
        "update_ticket_status",
        "add_ticket_comment",
        "save_user_preference",
        "summarize_and_store_conversation"
    ]

    write_action_performed = any(
        tool in write_tools
        for tool in tools_used
    )

  

    return {
        "user_request": user_input,
        "plan_summary": plan,
        "tools_used": tools_used,
        "tool_result_summary": tool_result_summary,
        "reflection_summary": reflection,
        "final_answer": final_answer,
        "memory_used": memory_used,
        "write_action_performed": write_action_performed
    }




def print_response(response):

    print("\n" + "=" * 80)

    print("\nUSER REQUEST")
    print(response["user_request"])

    print("\nPLAN SUMMARY")
    print(response["plan_summary"])

    print("\nTOOLS USED")
    print(response["tools_used"])

    print("\nTOOL RESULT SUMMARY")
    print(response["tool_result_summary"])

    print("\nREFLECTION SUMMARY")
    print(response["reflection_summary"])

    print("\nFINAL ANSWER")
    print(response["final_answer"])

    print("\nMEMORY USED")
    print(response["memory_used"])

    print("\nWRITE ACTION PERFORMED")
    print(response["write_action_performed"])

    print("\n" + "=" * 80)


# =====================================================
# LOCAL TEST
# =====================================================

if __name__ == "__main__":

    while True:

        query = input(
            "\nHelpdesk User > "
        ).strip()

        if query.lower() in [
            "exit",
            "quit"
        ]:
            break

        response = run_agent(query)

        print_response(response)