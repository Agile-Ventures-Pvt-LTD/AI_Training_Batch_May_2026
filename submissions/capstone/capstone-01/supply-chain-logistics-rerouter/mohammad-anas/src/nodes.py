import json
from typing import Any, Dict, List,Tuple
from langchain_groq import ChatGroq
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.schema import HumanMessage
from state import LogisticsIncidentState
from tools import get_alternative_routes_tool, query_warehouse_inventory_tool
from schemas import ShipmentMetadata
from report_writer import write_report
import os
from dotenv import load_dotenv
load_dotenv()
GROQ_MODEL=os.environ['GROQ_MODEL'] = os.getenv("GROQ_MODEL")
GROQ_API_KEY = os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")
from pathlib import Path
from rag import retrieve_rules


def get_llm():
    model = ChatGroq(
        model = GROQ_MODEL,
        api_key=GROQ_API_KEY,
        temperature=0,
        max_token=1024
    )
    return model

def parse_incident(state:LogisticsIncidentState)->LogisticsIncidentState:
    response_schemas = [
        ResponseSchema(name="shipment_id",description="Shipment identifier"),
        ResponseSchema(name="cargo_weight_tons",description="weight in tons"),
        ResponseSchema(name="cargo_type",description="Cargo description"),
        ResponseSchema(name="target_warehouse_id",description="Warehouse ID"),
        ResponseSchema(name="has_perishables",description="True/False"),
    ]
    parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = parser.get_format_instructions()
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You extract the shipment metadata. Return JSON following the Scehma. {format_instructions}"),
        ("human","{manifest}")
    ])
    
    llm = get_llm()
    chain = prompt|llm
    
    response = chain.invoke({"manifest": state["manifest_text"]})
    try:
        metadata = parser.parse(response.content)
        state["extracted_metadata"] = metadata
    except Exception as e:
        state["logs"] = state.get("logs",[]) + [f"Parse error: {e}"]
    return state

def policy_rag_lookup(state:LogisticsIncidentState)->LogisticsIncidentState:
    query = f"Rules for rerouting shipment from port {state['disrupted_port_id']}"
    rag_text = retrieve_rules(query)
    state["routing_rag_context"] = rag_text
    return state
def load_alternative_routes(state: LogisticsIncidentState)->LogisticsIncidentState:
    routes = get_alternative_routes_tool(state["disrupted_port_id"])
    state["available_routes"] = routes
    state["current_route_index"] = 0
    state["clarification_attempts"] = 0
    state["max_clarification_attempts"] = len(routes)
    return state

def select_route(state: LogisticsIncidentState)->LogisticsIncidentState:
    idx = state["current_route_index"]
    routes = state["available_routes"]
    if idx < len(routes):
        state["selected_route"]
    else:
        state["selected_route"] = {}
def check_warehouse(state:LogisticsIncidentState)->LogisticsIncidentState:
    wh_id = state["extracted_metadata"]["target_warehouse_id"]
    state["warehouse_db_context"] = query_warehouse_inventory_tool(wh_id)
    return state
def evaluate(state: LogisticsIncidentState) -> Tuple[str, int, List[str]]:
    wh = state["warehouse_db_context"]
    md = state["extracted_metadata"]
    route = state["selected_route"]

    utilization = wh.get("utilization_percent", 0)
    status = wh.get("operational_status", "")
    risk = wh.get("risk_tier", "")
    added_delay = route.get("added_delay_hours", 0)

    decision = "OPTIMAL_PATH_FOUND"
    score = 0
    reasons: List[str] = []

    # rule checks (order matters for decision precedence)
    if utilization > 85:
        decision = "ROUTE_CLARIFICATION"
        score += 30
        reasons.append("warehouse utilization > 85%")
    if status != "ACTIVE":
        decision = "ROUTE_CLARIFICATION"
        score += 30
        reasons.append(f"warehouse status {status} not ACTIVE")
    if risk == "ELEVATED":
        decision = "ROUTE_CLARIFICATION"
        score += 25
        reasons.append("warehouse risk tier ELEVATED")
    if added_delay > 120:
        decision = "CRITICAL_DELAY"
        score += 50
        reasons.append("added delay > 120h")
    elif md.get("maximum_tolerable_delay_hours") and added_delay > md["maximum_tolerable_delay_hours"]:
        decision = "ROUTE_CLARIFICATION"
        score += 25
        reasons.append("added delay exceeds shipment tolerable limit")

    # cap score
    score = min(score, 100)
    return decision, score, reasons


def analyze_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    decision, score, reasons = evaluate(state)
    state["routing_decision"] = decision
    state["reroute_impact_score"] = score
    state.setdefault("logs", []).append(
        f"Route {state.get('selected_route', {}).get('route_id','N/A')} → {decision} ({'; '.join(reasons)})"
    )
    return state


def route_clarification(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """If clarification required, move to next candidate route."""
    if state["routing_decision"] == "ROUTE_CLARIFICATION":
        state["clarification_attempts"] += 1
        state["current_route_index"] += 1
        if state["clarification_attempts"] >= state["max_clarification_attempts"]:
            state["routing_decision"] = "CRITICAL_DELAY"
    return state


def finalize_route(state: LogisticsIncidentState) -> LogisticsIncidentState:
    """Accept the current route when optimal."""
    return state


def escalate_incident(state: LogisticsIncidentState) -> LogisticsIncidentState:
    if (
        state["routing_decision"] in ("CRITICAL_DELAY", "ROUTE_CLARIFICATION")
        and state["clarification_attempts"] >= state["max_clarification_attempts"]
    ):
        state["routing_decision"] = "CRITICAL_DELAY"
        state.setdefault("logs", []).append("Escalation triggered due to no viable routes")
    return state


def generate_report(state: LogisticsIncidentState) -> LogisticsIncidentState:
    llm = get_llm()
    brief_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a logistics operations assistant. Summarize the reroute decision in 2-3 concise sentences."),
            ("human", "Incident ID: {incident_id}\nDecision: {routing_decision}\nImpact score: {reroute_impact_score}\nSelected route: {selected_route}\nWarehouse: {warehouse_db_context}"),
        ]
    )
    brief_chain = brief_prompt | llm
    brief_resp = brief_chain.ainvoke(
        {
            "incident_id": state["incident_id"],
            "routing_decision": state["routing_decision"],
            "reroute_impact_score": state["reroute_impact_score"],
            "selected_route": json.dumps(state.get("selected_route", {})),
            "warehouse_db_context": json.dumps(state.get("warehouse_db_context", {})),
        }
    )
    report = {
        "incident_id": state["incident_id"],
        "original_incident_summary": state["manifest_text"],
        "parsed_metadata": state["extracted_metadata"],
        "rag_validation_rules_applied": state["routing_rag_context"].splitlines()[:5],
        "routes_evaluated": [
            {
                "route_id": r.get("route_id"),
                "decision": "OPTIMAL_PATH_FOUND"
                if r.get("route_id") == state.get("selected_route", {}).get("route_id")
                else "REJECTED",
                "reason": "selected as optimal" if r.get("route_id") == state.get("selected_route", {}).get("route_id") else "did not meet constraints",
            }
            for r in state["available_routes"]
        ],
        "final_selected_route": state.get("selected_route", {}),
        "queried_warehouse_metrics": state.get("warehouse_db_context", {}),
        "graph_routing_metadata": {
            "loops_executed": state["clarification_attempts"],
            "final_decision_state": state["routing_decision"],
            "reroute_impact_score": state["reroute_impact_score"],
        },
        "final_operations_brief": brief_resp.content.strip(),
    }
    write_report(state["incident_id"], report)
    state["final_report"] = report
    return state