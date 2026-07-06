from state import LogisticsIncidentState, create_initial_state
from typing import TypedDict, Annotated, List, Any
from langchain_core.messages import ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph.message import add_messages
from tools import get_alternative_route_tool, query_warehouse_inventory_tool
from langchain_groq import ChatGroq
from config import GROQ_MODEL, GROQ_API_KEY, MAX_CLARIFICATION_ATTEMPTS
from rag import RAG_Retrieve
import json

llm = ChatGroq(model=GROQ_MODEL, api_key=GROQ_API_KEY, temperature=0)

def evaluate_route(route: dict[str, Any], warehouse: dict[str, Any], metadata: dict[str, Any]) -> tuple[str, str]:
    added_delay_hour = route.get("added_delay_hours", 0)
    max_tolerable = metadata.get("maximum_tolerable_delay_hours")
    if "error" in warehouse:
        return "ROUTE_CLARIFICATION", "Warehouse data error detected"
    utilization = warehouse.get("current_utilization_pct", 0)
    status = warehouse.get("operational_status", "UNKNOWN")
    risk_tier = warehouse.get("risk_tier", "UNKNOWN")
    if added_delay_hour > 120:
        return "CRITICAL_DELAY", "Critical delay threshold exceeded"
    if utilization > 85:
        return "ROUTE_CLARIFICATION", "Warehouse utilization limit reached"
    if status != "ACTIVE":
        return "ROUTE_CLARIFICATION", "Warehouse is currently inactive"
    if risk_tier == "ELEVATED":
        return "ROUTE_CLARIFICATION", "Warehouse risk tier is elevated"
    if max_tolerable is not None and added_delay_hour > max_tolerable:
        return "ROUTE_CLARIFICATION", "Delay exceeds max tolerable limit"
    return "OPTIMAL_PATH_FOUND", "Route within operational parameters"

def calculate_impact_score(route: dict[str, Any], warehouse: dict[str, Any], metadata: dict[str, Any]) -> int:
    score = 0
    added_delay = route.get("added_delay_hours", 0)
    max_tolerable = metadata.get("maximum_tolerable_delay_hours")
    if "error" in warehouse:
        return 0
    utilization = warehouse.get("current_utilization_pct", 0)
    status = warehouse.get("operational_status", "UNKNOWN")
    risk_tier = warehouse.get("risk_tier", "UNKNOWN")
    if utilization > 85:
        score += 30
    if risk_tier == "ELEVATED":
        score += 25
    if status != "ACTIVE":
        score += 30
    if max_tolerable is not None and added_delay > max_tolerable:
        score += 25
    if added_delay > 120:
        score += 50
    return min(score, 100)

class ShipmentMetadata(TypedDict):
    shipment_id: str
    cargo_weight_tons: float
    cargo_type: str
    target_warehouse_id: str
    has_perishables: bool
    maximum_tolerable_delay_hours: int

def parse_incident(state: LogisticsIncidentState) -> LogisticsIncidentState:
    manifest_text = state.get("manifest_text", "")
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a logistics metadata extraction assistant. Extract structural information matching ShipmentMetadata schemas from the manifest."),
        ("human", "{manifest_text}")
    ])
    try:
        structured_llm = llm.with_structured_output(ShipmentMetadata)
        chain = prompt | structured_llm
        result = chain.invoke({"manifest_text": manifest_text})
        metadata = result if isinstance(result, dict) else result.model_dump()
    except Exception:
        metadata = {
            'shipment_id': '',
            'cargo_weight_tons': 0,
            'cargo_type': "",
            'target_warehouse_id': "",
            'has_perishables': False,
            "maximum_tolerable_delay_hours": 0
        }
    state['extracted_metadata'] = metadata
    return state

def policy_rag_lookup(state: LogisticsIncidentState, rag: RAG_Retrieve) -> LogisticsIncidentState:
    manifest_text = state.get("manifest_text", "")
    query = manifest_text[:200]
    try:
        rules = rag.retrieve(query, k=5)
        context = "\n\n".join(rules)
    except Exception:
        rules = []
        context = ''
    state['routing_rag_context'] = context
    state['retrieval_rules'] = rules
    return state

def load_alternative_routes(state: LogisticsIncidentState) -> LogisticsIncidentState:
    disrupted_port_id = state.get("disrupted_port_id", "")
    routes = get_alternative_route_tool(disrupted_port_id)
    state['available_routes'] = routes if isinstance(routes, list) else []
    state['current_route_index'] = 0
    state['clarification_attempts'] = 0
    state['max_clarification_attempts'] = MAX_CLARIFICATION_ATTEMPTS
    state['routes_evaluated'] = []
    return state

def select_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    routes = state.get("available_routes", [])
    index = state.get("current_route_index", 0)
    if index < len(routes):
        state["selected_route"] = routes[index]
    else:
        state["selected_route"] = {}
    return state

def check_warehouse(state: LogisticsIncidentState) -> LogisticsIncidentState:
    selected_route = state.get("selected_route", {})
    warehouse_id = selected_route.get("warehouse_id", "")
    warehouse_data = query_warehouse_inventory_tool(warehouse_id)
    state['warehouse_db_context'] = warehouse_data if isinstance(warehouse_data, dict) else {"error": "Invalid response format"}
    return state

def analyze_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    route = state.get("selected_route", {})
    warehouse = state.get("warehouse_db_context", {})
    metadata = state.get("extracted_metadata", {})
    decision, reason = evaluate_route(route, warehouse, metadata)
    impact_score = calculate_impact_score(route, warehouse, metadata)
    state["routing_decision"] = decision
    state["reroute_impact_score"] = impact_score
    route_eval_entry = {
        "route_id": route.get("route_id", ""),
        "decision": decision,
        "reason": reason,
    }
    evaluated = state.get("routes_evaluated", [])
    if evaluated is None:
        evaluated = []
    evaluated.append(route_eval_entry)
    state["routes_evaluated"] = evaluated
    return state

def route_clarification(state: LogisticsIncidentState) -> LogisticsIncidentState:
    attempts = state.get("clarification_attempts", 0) + 1
    state["clarification_attempts"] = attempts
    new_index = state.get("current_route_index", 0) + 1
    state["current_route_index"] = new_index
    routes = state.get("available_routes", [])
    max_attempts = state.get("max_clarification_attempts", MAX_CLARIFICATION_ATTEMPTS)
    has_more_routes = new_index < len(routes)
    within_retry_limit = attempts <= max_attempts
    if has_more_routes and within_retry_limit:
        state["routing_decision"] = "ROUTE_CLARIFICATION"
    else:
        state["routing_decision"] = "CRITICAL_DELAY"
    return state

def finalize_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    return state

def escalate_incident(state: LogisticsIncidentState) -> LogisticsIncidentState:
    state["routing_decision"] = "CRITICAL_DELAY"
    return state

class OperationsBrief(TypedDict):
    incident_summary: str
    operations_brief: str
def generate_report(state: LogisticsIncidentState) -> LogisticsIncidentState:
    from report_writer import build_and_save_report
    incident_id = state.get("incident_id", "")
    manifest_text = state.get("manifest_text", "")
    decision = state.get("routing_decision", "")
    selected_route = state.get("selected_route", {})
    warehouse = state.get("warehouse_db_context", {})
    metadata = state.get("extracted_metadata", {})
    routes_evaluated = state.get("routes_evaluated", [])
    rag_context = state.get("routing_rag_context", "")
    retrieval_rules = state.get("retrieval_rules", [])
    impact_score = state.get("reroute_impact_score", 0)
    loops = state.get("clarification_attempts", 0)
    routes_summary = "; ".join(
        [f"{r.get('route_id', '')}: {r.get('decision', '')} ({r.get('reason', '')})" for r in routes_evaluated]
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a logistics operations assistant. Generate a concise incident summary and operations brief based on the provided shipment disruption information. The operations brief must only reference information provided in the context and must not fabricate any details."),
        ("human", "Incident ID: {incident_id}\nManifest: {manifest_text}\nRouting Decision: {decision}\nSelected Route: {selected_route}\nWarehouse Data: {warehouse}\nRoutes Evaluated: {routes_summary}\nRAG Rules Applied: {rag_context}\nImpact Score: {impact_score}\nLoops Executed: {loops}")
    ])
    try:
        structured_llm = llm.with_structured_output(OperationsBrief)
        chain = prompt | structured_llm
        report_data = chain.invoke({
            "incident_id": incident_id,
            "manifest_text": manifest_text,
            "decision": decision,
            "selected_route": json.dumps(selected_route),
            "warehouse": json.dumps(warehouse),
            "routes_summary": routes_summary,
            "rag_context": rag_context,
            "impact_score": impact_score,
            "loops": loops
        })
        brief_dict = report_data if isinstance(report_data, dict) else report_data.model_dump()
        original_summary = brief_dict.get("incident_summary", "")
        operations_brief = brief_dict.get("operations_brief", "")
    except Exception:
        original_summary = "Failed to compile automated LLM summary."
        operations_brief = "Operations manual intervention required."
        
    build_and_save_report(
        incident_id=incident_id,
        manifest_text=manifest_text,
        metadata=metadata,
        retrieved_rules=retrieval_rules,
        routes_evaluated=routes_evaluated,
        selected_route=selected_route,
        warehouse_metrics=warehouse,
        loops_executed=loops,
        final_decision=decision,
        impact_score=impact_score,
        original_summary=original_summary,
        operations_brief=operations_brief
    )
    return state
