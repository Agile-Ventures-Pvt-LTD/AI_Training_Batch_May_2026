
import uuid  # to make unique identifier
import pprint

from langchain_groq import ChatGroq
from typing import List, Annotated, TypedDict, Literal

from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import StructuredTool

from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition, create_react_agent
from langgraph.graph.message import add_messages

from prompts import system_prompt

from tools import inspect_database_schema,get_customer_profile,get_card_details,search_transactions,get_customer_transactions,get_statement_summary,get_reward_summary,get_merchant_spend_summary
import os
# from PIL import Image

from config import groq_api_key

llm = ChatGroq(
    model="llama-3.3-70b-versatile",  # or your model
    groq_api_key=groq_api_key,
)


#----------------- testing is llm connected properly-------------

# print(llm.invoke("What is AI?").content)

def run_agent(user_query):
    agent = create_react_agent(
        model=llm,
        tools=[inspect_database_schema, get_customer_profile,get_card_details, search_transactions,get_customer_transactions,get_statement_summary,get_reward_summary,get_merchant_spend_summary],
        prompt=system_prompt
    )



    messages_input = [HumanMessage(content=user_query)]

    response = agent.invoke({"messages": messages_input})

    final_message = response["messages"][-1].content

    return {
        "user_question": user_query,
        "answer": final_message,
        "implementation_choice": "prebuilt_react_agent",
        "sensitive_data_masked": True,
        "limitations": []
    }