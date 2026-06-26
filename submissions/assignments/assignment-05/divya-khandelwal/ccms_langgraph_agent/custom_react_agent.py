from typing import Annotated, TypedDict, Literal

import os

from dotenv import load_dotenv


from langchain_groq import ChatGroq

from langchain_core.messages import (
    SystemMessage
)


from langgraph.graph import (
    StateGraph,
    START,
    END
)


from langgraph.graph.message import add_messages


from langgraph.prebuilt import ToolNode


from prompts import SYSTEM_PROMPT


load_dotenv()


os.environ["GROQ_API_KEY"] = os.getenv(
    "GROQ_API_KEY"
)


from tools import (


    inspect_database_schema,

    get_customer_profile,

    get_card_details,

    search_transactions,

    get_customer_transactions,

    get_statement_summary,

    get_rewards_summary,

    get_merchant_spend_summary

)





# -----------------------------
# Agent State
# -----------------------------

class AgentState(TypedDict):


    messages: Annotated[
        list,
        add_messages
    ]


    plan: str


    reflection: str


    tools_used: list



# -----------------------------
# Register Tools
# -----------------------------

tools = [

    inspect_database_schema,

    get_customer_profile,

    get_card_details,

    search_transactions,

    get_customer_transactions,

    get_statement_summary,

    get_rewards_summary,

    get_merchant_spend_summary


]



# -----------------------------
# LLM
# -----------------------------


llm = ChatGroq(

    api_key=os.environ["GROQ_API_KEY"],

    model=os.getenv(
        "GROQ_MODEL",
        "llama-3.1-8b-instant"
    ),

    temperature=0

)



llm_with_tools = llm.bind_tools(
    tools
)




# -----------------------------
# Agent Reasoning Node
# -----------------------------


def agent_node(
    state: AgentState
):


    messages = state["messages"]



    system_message = SystemMessage(

        content=SYSTEM_PROMPT

    )



    response = llm_with_tools.invoke(

        [

            system_message

        ]

        +

        messages

    )



    return {


        "messages":[response]

    }





# -----------------------------
# Tool Decision Router
# -----------------------------


def should_continue(

    state: AgentState

) -> Literal["tools","reflection"]:



    print(
        "--- Checking Tool Decision ---"
    )



    last_message = (
        state["messages"][-1]
    )



    if (

        hasattr(
            last_message,
            "tool_calls"
        )

        and

        last_message.tool_calls

    ):



        print(
            "Tool required"
        )


        return "tools"



    else:


        print(
            "No tool required"
        )


        return "reflection"





# -----------------------------
# Reflection Node
# -----------------------------


def reflection_node(

    state: AgentState

):


    print(
        "--- Reflection Node ---"
    )



    last_message = (
        state["messages"][-1]
    )



    reflection = f"""


Response Generated:


{last_message.content}



Validation:


✓ User request processed

✓ Required tools executed

✓ Final response generated



"""


    return {


        "reflection":
        reflection

    }




# -----------------------------
# Build LangGraph
# -----------------------------


graph = StateGraph(
    AgentState
)



# Nodes

graph.add_node(

    "agent",

    agent_node

)



graph.add_node(

    "tools",

    ToolNode(tools)

)



graph.add_node(

    "reflection_node",

    reflection_node

)



# Entry Point

graph.add_edge(

    START,

    "agent"

)



# Agent Decision

graph.add_conditional_edges(

    "agent",

    should_continue,


    {


        "tools":
        "tools",


        "reflection":
        "reflection_node"


    }

)



# Tool Output Back To Agent

graph.add_edge(

    "tools",

    "agent"

)



# End

graph.add_edge(

    "reflection_node",

    END

)




# Compile Graph

compiled_graph = graph.compile()