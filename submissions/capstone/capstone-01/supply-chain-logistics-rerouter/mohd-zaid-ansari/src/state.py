import os
import json
from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langgraph.graph.message import add_messages
from src.rag import retrive_data, get_embedding_model, create_vector_store
from src.tools import get_alternative_routes_tool, query_warehouse_inventory_tool

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_PATH = BASE_DIR / "data" / "sample_incidents.json"

tools = [query_warehouse_inventory_tool, get_alternative_routes_tool]

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL")

llm = ChatGroq(model=MODEL, groq_api_key=GROQ_API_KEY)
llm_with_tools = llm.bind_tools(tools, tool_choice="auto")


class LogisticsIncidentState(TypedDict):
    messages: Annotated[list, add_messages]
    incident_id: str
    manifest_text: str
    disrupted_port_id: str
    warehouse_id:str
    extracted_metadata: dict
    routing_rag_context: str
    available_routes: list
    current_route_index: int
    selected_route: dict
    warehouse_db_context: dict
    reroute_impact_score: int
    routing_decision: str
    clarification_attempts: int
    max_clarification_attempts: int
    logs: list[str]
    final_report: dict


#================================================================================================================================   


    


