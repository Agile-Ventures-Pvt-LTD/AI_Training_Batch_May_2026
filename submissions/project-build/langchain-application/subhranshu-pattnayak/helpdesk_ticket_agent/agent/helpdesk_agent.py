from langchain.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from langchain_core.prompts import ChatPromptTemplate

from agent.prompt import SYSTEM_PROMPT

def build_agent(llm, tools):

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ]
    )

    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )