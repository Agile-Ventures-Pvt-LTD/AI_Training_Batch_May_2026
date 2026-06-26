from langchain_groq import ChatGroq

from langchain.agents import create_agent

from config import (
    GROQ_API_KEY,
    GROQ_MODEL
)

from prompts import SYSTEM_PROMPT

from tools import TOOLS



def get_llm():

    return ChatGroq(
        model=GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0
    )



def create_helpdesk_agent():

    llm = get_llm()


    agent = create_agent(

    model=llm,

    tools=TOOLS,

    system_prompt=SYSTEM_PROMPT,

)

    return agent



def create_plan(user_query):

    return {

        "user_goal": user_query,

        "steps": [

            "Understand request",

            "Select required tool",

            "Fetch data from SQLite",

            "Validate output",

            "Generate response"

        ]

    }



def reflection(result):

    return {

        "tool_result_available":
        bool(result),

        "answer_complete":
        bool(result)

    }



def run_agent(user_query):

    agent = create_helpdesk_agent()


    plan = create_plan(
        user_query
    )


    response = agent.invoke(
        user_query
    )


    final_answer = response["output"]


    return {

        "user_request":
        user_query,


        "plan_summary":
        plan,


        "reflection_summary":
        reflection(final_answer),


        "tools_used":
        "LangChain ReAct Agent",


        "final_answer":
        final_answer

    }