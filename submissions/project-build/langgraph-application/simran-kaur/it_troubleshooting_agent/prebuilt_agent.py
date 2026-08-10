
import uuid  # to make unique identifier
import pprint
import os
from config import GROQ_MODEL
from config import GROQ_API_KEY
from langchain_groq import ChatGroq
from typing import List, Annotated, TypedDict, Literal

from pydantic import BaseModel, Field

from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import StructuredTool

from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition, create_react_agent
from langgraph.graph.message import add_messages

from prompts import system_prompt

from tools import inspect_database_schema,get_user_profile,get_device_status,check_known_incidents,run_diagnostic_check,classify_issue_type
# from PIL import Image

from config import groq_api_key

llm = ChatGroq(
    model=GROQ_MODEL,  
    groq_api_key=os.getenv("GROQ_API_KEY")
)


#----------------- testing is llm connected properly-------------

# print(llm.invoke("What is AI?").content)

def run_agent(user_query):
    agent = create_react_agent(
        model=llm,
        tools= [inspect_database_schema,get_user_profile,get_device_status,check_known_incidents,run_diagnostic_check,classify_issue_type],
        prompt=system_prompt
    )



    messages_input = [HumanMessage(content=user_query)]

    response = agent.invoke({"messages": messages_input})

    final_message = response["messages"][-1].content

    return final_message

