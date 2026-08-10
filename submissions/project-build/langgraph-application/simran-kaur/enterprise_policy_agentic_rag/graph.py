import os
from langchain_groq import ChatGroq
from typing_extensions import TypedDict, Literal
from pydantic import BaseModel, Field
from mermaid import Mermaid
from prebuilt_agent import should_generate_answer,

from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import START, END, StateGraph

# from google.colab import userdata
from IPython.display import Image, display

workflow = StateGraph(State)

# Add the nodes
workflow.add_node("generate_outline", generate_outline)
workflow.add_node("validate_outline", validate_outline)
workflow.add_node("generate_document", generate_document)

# Add edges for the sequential flow
workflow.add_edge(START, 'generate_outline')
workflow.add_edge("generate_outline", "validate_outline")

# Add the conditional edge (the gate)
workflow.add_conditional_edges(
    "validate_outline",         # Source node
    should_generate_answer   # Function to decide the next step
)

# Add the final edge
workflow.add_edge("generate_document", END)