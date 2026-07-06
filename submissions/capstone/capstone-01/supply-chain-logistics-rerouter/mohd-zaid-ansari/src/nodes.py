import os
import json
from pathlib import Path
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from src.rag import retrive_data, get_embedding_model, create_vector_store
from src.tools import get_alternative_routes_tool, query_warehouse_inventory_tool
from src.state import LogisticsIncidentState
from src.prompts import system_prompt, human_message
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_PATH = BASE_DIR / "data" / "sample_incidents.json"

tools = [query_warehouse_inventory_tool, get_alternative_routes_tool]

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("GROQ_MODEL")

llm = ChatGroq(model=MODEL, groq_api_key=GROQ_API_KEY)
llm_with_tools = llm.bind_tools(tools, tool_choice="auto")

def agent_node(state: LogisticsIncidentState) -> dict:

    """Invokes the LLM with the current message history."""
    print("---LLM NODE---")
    messages = state['messages']
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def parse_incident(state: LogisticsIncidentState) -> dict:
    """Extract/compute incident information.

    Current implementation is a deterministic loader for `manifest_text`.
    It also initializes `extracted_metadata` with the loaded manifest text.
    """
    try:
        with open(SAMPLE_PATH, mode="r", encoding="utf-8") as file:
            sample = json.load(file)

        if isinstance(sample, list):
            sample = sample[0] if sample else {}
        if not isinstance(sample, dict):
            sample = {}

        manifest_text = sample.get("manifest_text", "")
        extracted_metadata = {"manifest_text": manifest_text}
        return {
            "manifest_text": manifest_text,
            "extracted_metadata": extracted_metadata,
        }
    except Exception as e:
        return {
            "manifest_text": "",
            "extracted_metadata": {},
            "error": "Failed to load manifest_text",
            "details": str(e),
        }

#=============================================================================================================================

def policy_rag_lookup(state: LogisticsIncidentState) -> dict:
    """Retrieve logistics rules relevant to the current incident."""
    embedding = get_embedding_model()
    vector_store = create_vector_store(embedding)

    # `retrive_data()` expects a text query, but `state` is a dict.
    query_text = state.get("manifest_text") or ""
    if not query_text:
        extracted = state.get("extracted_metadata") or {}
        query_text = extracted.get("manifest_text") or ""

    retriver = retrive_data(query=query_text, vector_store=vector_store)


    routing_rag_context = "\n\n".join([c.get("content", "") for c in retriver if isinstance(c, dict)])

    return{"routing_rag_context": routing_rag_context}

#============================================================================================================================

def load_alternative_routes(state: LogisticsIncidentState) -> dict:
    """Load alternate routes for `disrupted_port_id` using the tool."""
    disrupted_port_id = state.get("disrupted_port_id")
    if not disrupted_port_id:
        return {"available_routes": []}

    result = get_alternative_routes_tool.invoke(disrupted_port_id)

    if isinstance(result, dict) and "error" in result:
        return {"available_routes": []}

    routes = []
    if isinstance(result, dict):
        routes = result.get(disrupted_port_id, []) or []

    return {"available_routes": routes}

#=============================================================================================================================

def select_route(state: LogisticsIncidentState) -> dict:
    """Select route by current_route_index and store it in selected_route."""
    available_routes = state.get("available_routes") or []
    idx = state.get("current_route_index", 0)

    if not available_routes:
        return {"selected_route": {}}
    if not isinstance(idx, int):
        idx = 0
    if idx < 0:
        idx = 0
    if idx >= len(available_routes):
        idx = len(available_routes) - 1

    return {"selected_route": available_routes[idx]}

#=============================================================================================================================

def check_warehouse(state:LogisticsIncidentState) -> dict:
    """Get the warhouse_id from the selected_route. """
    selected_route=state.get("selected_route") or []
    warehouse_id=selected_route.get("warehouse_id")
    
    if not warehouse_id:
        return {"warehouse_db_context": []}
    
    result=query_warehouse_inventory_tool.invoke(warehouse_id)

    if isinstance(result, dict):
        return{"warehouse_db_context":{}, "warehouse_id":{}}
    
    if isinstance(result, dict):
        warehouse_db_context=result.get(warehouse_id, {})
    else:
        return {"warehouse_db_context": warehouse_db_context, "warehouse_id":warehouse_id}

#=========================================================================================================================

def analyze_route(state:LogisticsIncidentState) -> dict:
    """Evaluate selected route and analysis using extracted metadata."""

    extracted=state.get("extracted_metadata")
    selected_route=state.get("selected_route")
    warehouse_db_context=state.get("warehouse_db_context")
    retrived_context=state.get("routing_rag_context")
    added_delay_hours = float(selected_route.get("added_delay_hours") or 0)

    critical_delay = added_delay_hours > 120
    reroute_impact_score = int(added_delay_hours)

    routing_decision = "OK"
    if critical_delay:
        routing_decision = "CRITICAL_DELAY"

    return {
        "routing_decision": routing_decision,
        "reroute_impact_score": reroute_impact_score,
    }


#=========================================================================================================================

def route_clarification(state:LogisticsIncidentState) -> dict:
    """Reject the current node and check next available route"""

    available_routes=state.get("available_routes")
    max_attempts=state.get(int("max_clarification_attempts", 2))
    clarification_attempts=state.get(int("clarification_attempts",0))+1
    current_route_index=state.get(int("current_route_index",0))+1

    if clarification_attempts > max_attempts or current_route_index >= len(available_routes):
        return {
            "clarification_attempts": clarification_attempts,
            "current_route_index": current_route_index,
            "routing_decision": "CRITICAL_DELAY",
            "logs": (state.get("logs") or [])
            + [f"route_clarification: exhausted retries (attempts={clarification_attempts})"],
        }

    return {
        "clarification_attempts": clarification_attempts,
        "current_route_index": current_route_index,
        "routing_decision": "CLARIFICATION_REQUIRED",
        "logs": (state.get("logs") or [])
        + [f"route_clarification: trying next route (index={current_route_index})"],
    }
#=========================================================================================================================

def finalize_route(state:LogisticsIncidentState) -> dict:
    """Finlizes the accepted route and keep selected route in the graph state."""
    return{
        "selected_route":state.get("selected_route") or {},
        "routing_decision":state.get("routing_decision")
    }


#=========================================================================================================================

def escalate_incident(state:LogisticsIncidentState) -> dict:
    """Mark the incident for escalation.
Escalation should occur when: 
No acceptable route is available.
A critical delay condition exists.
The maximum route retry limit is reached."""

    routing_decision=state.get("routing_decision")
    return{
        "routing_decision":"ESCALATE",
        "final_report":{
            "status":"ESCALATE",
            "route_decision":routing_decision
        }
    }

#==============================================================================================================================

def generate_report(state:LogisticsIncidentState) -> dict:
    """Generate the final result.Use LangChain and the Groq LLM to create a short final_operations_brief.
    
    Save the output in JSON
    """
    extracted_metadata=state.get("extracted_metadata")
    routing_rag_context=state.get("routing_rag_context")
    available_routes=state.get("available_routes")
    selected_route=state.get("selected_route")
    warehouse_db_context=state.get("warehouse_db_context")

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", human_message)
    ])
                                                

    chain=prompt | llm
    response=chain.invoke({
            "extracted_metadata": extracted_metadata,
            "routing_rag_context": routing_rag_context,
            "selected_route": selected_route,
            "warehouse_db_context": warehouse_db_context,
            "reroute_impact_score": state.get("reroute_impact_score"),
            "routing_decision": state.get("routing_decision"),
    })

    final_response=getattr(response, "content", str(response)).strip()
    return {"final_report": json.loads(json.dumps(final_response, default=str))}