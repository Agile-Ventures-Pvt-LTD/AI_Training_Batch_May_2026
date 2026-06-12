from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage
from langchain.agents import (AgentExecutor,create_tool_calling_agent)

from config import (GROQ_API_KEY,MODEL_NAME)

from prompts import (SYSTEM_PROMPT,PLANNING_PROMPT,REFLECTION_PROMPT)

from tools import (
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    get_open_tickets,
    get_overdue_tickets,
    update_ticket_status,
    add_ticket_comment,
    get_customer_history,
    save_memory,
    recall_memory,
    recall_conversation
)

from memory import (save_conversation_log,get_latest_summary)

model = ChatGroq(model=MODEL_NAME,api_key=GROQ_API_KEY,temperature=0)

TOOLS = [
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    get_open_tickets,
    get_overdue_tickets,
    update_ticket_status,
    add_ticket_comment,
    get_customer_history,
    save_memory,
    recall_memory,
    recall_conversation]


system_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ]
)

agent = create_tool_calling_agent(llm=model ,tools=TOOLS,prompt=system_prompt)


agent_executor = AgentExecutor(
    agent=agent,
    tools=TOOLS,
    verbose=True,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)


def create_plan(user_query: str):

    planning_input = f"""
{PLANNING_PROMPT}

User Request:
{user_query}
"""

    response = model.invoke(
        [HumanMessage(content=planning_input)]
    )

    return response.content


def reflect_response(user_query: str,answer: str):

    reflection_input = f"""
{REFLECTION_PROMPT}

User Request:
{user_query}

Generated Answer:
{answer}
"""

    response = model.invoke(
        [HumanMessage(content=reflection_input)]
    )

    return response.content


def build_context(session_id: str):

    summary = get_latest_summary(
        session_id
    )

    if not summary:
        return ""

    return summary.get(
        "summary",
        ""
    )


def run_agent(session_id: str,user_query: str):
    context = build_context(
        session_id
    )

    plan = create_plan(
        user_query
    )

    final_input = f"""
Conversation Context:
{context}

Execution Plan:
{plan}

User Query:
{user_query}
"""

    result = agent_executor.invoke(
        {
            "input": final_input
        }
    )

    answer = result["output"]

    reflection = reflect_response(
        user_query=user_query,
        answer=answer
    )

    save_conversation_log(
        session_id=session_id,
        user_message=user_query,
        agent_response=answer,
        tools_used="agent_executor"
    )

    return {
        "answer": answer,
        "plan": plan,
        "reflection": reflection,
        "intermediate_steps": result.get(
            "intermediate_steps",
            []
        )
    }


if __name__ == "__main__":

    response = run_agent(
        session_id="demo_session",
        user_query="Show me all critical open tickets"
    )

    print("\nPLAN")
    print(response["plan"])

    print("\nANSWER")
    print(response["answer"])

    print("\nREFLECTION")
    print(response["reflection"])