import os
from langchain_groq import ChatGroq
from src.state import LogisticsIncidentState
from src.schemas import ShipmentMetadata
from src.tools import get_alternative_routes_tool, query_warehouse_inventory_tool
from src.rag1 import LogisticsRAGPipeline

llm = ChatGroq(temperature=0.0,model_name=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),groq_api_key=os.getenv("GROQ_API_KEY"))

rag_pipeline = LogisticsRAGPipeline()

def parse_incident(state: LogisticsIncidentState) -> dict:
    structured_llm = llm.with_structured_output(ShipmentMetadata)
    prompt= f"Analyse the incident manifest text and extract the required parameter strictly: \n {state['manifest_text']}"
    extracted = structured_llm.invoke(prompt)
    return {"extracted_metadata": extracted.model_dump(),}

def policy_rag_lookup(state: LogisticsIncidentState) -> dict:
    context = rag_pipeline.retrieve_rules(state["manifest_text"])
    return {"routing_rag_context": context}

def load_alternative_routes(state: LogisticsIncidentState) -> dict:
    routes = get_alternative_routes_tool(state["disrupted_port_id"])
    return {"available_routes": routes,"current_route_index": 0,"clarification_attempts": 0,"max_clarification_attempts": 2,}

def select_route(state: LogisticsIncidentState) -> dict:
    i = state["current_route_index"]
    routes = state["available_routes"]
    if i < len(routes):
        return {"selected_route": routes[i]}
    return {"selected_route": None,"routing_decision": "CRITICAL_DELAY"}

def check_warehouse(state: LogisticsIncidentState) -> dict:
    if not state["selected_route"]:
        return {}
    warehouse_id = state["selected_route"]["warehouse_id"]
    metrics = query_warehouse_inventory_tool(warehouse_id)
    return {"warehouse_db_context": metrics}

def analyze_route(state: LogisticsIncidentState) -> dict:
    route = state["selected_route"]
    warehouse_context = state["warehouse_db_context"]
    metadata = state["extracted_metadata"]
    
    if not route:
        return {"routing_decision": "CRITICAL_DELAY"}
        
    if not warehouse_context or "error" in warehouse_context:
        return {"routing_decision": "ROUTE_CLARIFICATION","reroute_impact_score": 100}
        
    util = warehouse_context.get("current_utilization_pct", 0)
    status = warehouse_context.get("operational_status", "ACTIVE")
    risk = warehouse_context.get("risk_tier", "NORMAL")
    delay = route.get("added_delay_hours", 0)
    max_tolerate = metadata.get("maximum_tolerable_delay_hours")
    
    decision = "OPTIMAL_PATH_FOUND"
    score = 0
    
    if util > 85:
        decision = "ROUTE_CLARIFICATION"
        score += 30
    if risk == "ELEVATED":
        decision = "ROUTE_CLARIFICATION"
        score += 25
    if status != "ACTIVE":
        decision = "ROUTE_CLARIFICATION"
        score += 30
    if max_tolerate is not None and delay > max_tolerate:
        decision = "ROUTE_CLARIFICATION"
        score += 25
    if delay > 120:
        decision = "CRITICAL_DELAY"
        score += 50
        
    score = min(score, 100)
    
    return {"routing_decision": decision,"reroute_impact_score": score}

def route_clarification(state: LogisticsIncidentState) -> dict:
    attempts = state["clarification_attempts"] + 1
    j = state["current_route_index"] + 1
    
    if attempts > state["max_clarification_attempts"] or j >= len(state["available_routes"]):
        return {"routing_decision": "CRITICAL_DELAY","clarification_attempts": attempts,"current_route_index": j}
        
    return {"routing_decision": "ROUTE_CLARIFICATION","clarification_attempts": attempts,"current_route_index": j}

def finalize_route(state: LogisticsIncidentState) -> dict:
    return {"logs": state["logs"] }

def escalate_incident(state: LogisticsIncidentState) -> dict:
    return {"selected_route": {}}

