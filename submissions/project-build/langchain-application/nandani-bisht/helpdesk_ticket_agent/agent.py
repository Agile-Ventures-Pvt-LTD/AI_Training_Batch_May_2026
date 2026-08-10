from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain_core.prompts import (
    ChatPromptTemplate
)

from langchain_groq import (
    ChatGroq
)

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

from prompts import (
    SYSTEM_PROMPT
)

from tools import (
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment
)

from memory import (
    memory
)


llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model=GROQ_MODEL,
    temperature=0
)


TOOLS = [
    search_tickets,
    get_ticket_details,
    get_ticket_comments,
    calculate_sla_status,
    prioritize_tickets,
    update_ticket_status,
    add_ticket_comment,
]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            SYSTEM_PROMPT
        ),

        (
            "human",
            "{input}"
        ),

        (
            "placeholder",
            "{agent_scratchpad}"
        )
    ]
)


agent = create_tool_calling_agent(
    llm=llm,
    tools=TOOLS,
    prompt=prompt
)


executor = AgentExecutor(
    agent=agent,
    tools=TOOLS,
    verbose=True,
    return_intermediate_steps=True
)


def run_agent(
    user_input,
    session_id="default"
):

    result = executor.invoke(
        {
            "input":
            user_input
        }
    )

    output = result["output"]

    tool_calls = []

    for step in result.get(
        "intermediate_steps",
        []
    ):

        try:

            tool_calls.append(
                step[0].tool
            )

        except Exception:
            pass

    memory.save_conversation(
        session_id=session_id,
        user_message=user_input,
        agent_response=output,
        tools_used=",".join(
            tool_calls
        )
    )

    return {

        "response":
        output,

        "tools":
        tool_calls
    }
    