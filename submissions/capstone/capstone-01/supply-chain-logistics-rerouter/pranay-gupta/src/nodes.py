from src.config import get_llm, MAX_CLARIFICATION_ATTEMPTS
from src.tools import get_alternative_routes_tool,query_warehouse_inventory_tool
from src.report_writer import build_report,save_report
from src.schemas import ShipmentMetadata
from src.state import LogisticsIncidentState
from src.routing_rules import evaluate_route
from src.rag import retrieve_logistics_rules
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import json
import logging

logger = logging.getLogger(__name__)
llm_instance = None
retriever_instance = None

def configure_dependencies(llm=None,retriever=None):
    global llm_instance ,retriever_instance
    if llm_instance is not None:
        llm_instance = llm
    if retriever_instance is not None:
        retriever_instance = retriever
    
def resolve_retriever():
    global retriever_instance
    if retriever_instance is None:
        from src.rag import get_retriever
        retriever_instance = get_retriever() 
    return retriever_instance

def resolve_llm():
    global llm_instance
    if llm_instance is None:
        llm_instance = get_llm()
    return llm_instance


def parse_incident(state: LogisticsIncidentState) -> dict:
    manifest = state["manifest_text"]
    llm = resolve_llm()
    structured_llm = llm.with_structured_output(ShipmentMetadata)

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a logistics data extraction assistant. Extract shipment "
            "information from the incident manifest text. Identify the shipment "
            "ID, cargo weight in tons, cargo type, target warehouse ID, whether "
            "the shipment contains perishables, and the maximum tolerable delay "
            "in hours if explicitly stated. If the maximum tolerable delay is "
            "not mentioned, leave it as null.",
        ),
        ("human", "{manifest}"),
    ])

    chain = prompt | structured_llm
    result = chain.invoke({"manifest": manifest})
    metadata = result.model_dump()

    return {
        "extracted_metadata": metadata,
        "logs": [
            f"parse_incident: Extracted metadata for shipment "
            f"{metadata.get('shipment_id', 'unknown')} - "
            f"weight={metadata.get('cargo_weight_tons')} tons, "
            f"cargo={metadata.get('cargo_type', 'unknown')}"
        ],
    }


def policy_rag_lookup(state: LogisticsIncidentState) -> dict:
    metadata = state.get("extracted_metadata", {})
    disrupted_port = state.get("disrupted_port_id", "")

    query = (
        f"Logistics rerouting rules for shipment "
        f"{metadata.get('shipment_id', '')} carrying "
        f"{metadata.get('cargo_weight_tons', '')} tons of "
        f"{metadata.get('cargo_type', '')} from disrupted port "
        f"{disrupted_port}. Warehouse capacity, risk tier, "
        f"operational status, delay limits, and escalation rules."
    )

    retriever = resolve_retriever()
    rag_context = retrieve_logistics_rules(query, retriever=retriever)

    return {
        "routing_rag_context": rag_context,
        "logs": [
            f"policy_rag_lookup: Retrieved logistics rules from knowledge base "
            f"for incident query"
        ],
    }


def load_alternative_routes(state: LogisticsIncidentState) -> dict:
    disrupted_port_id = state["disrupted_port_id"]
    routes = get_alternative_routes_tool(disrupted_port_id)

    return {
        "available_routes": routes,
        "current_route_index": 0,
        "clarification_attempts": 0,
        "max_clarification_attempts": MAX_CLARIFICATION_ATTEMPTS,
        "routes_evaluated": [],
        "logs": [
            f"load_alternative_routes: Found {len(routes)} alternative routes "
            f"for {disrupted_port_id}"
        ],
    }


def select_route(state: LogisticsIncidentState) -> dict:
    routes = state.get("available_routes", [])
    index = state.get("current_route_index", 0)

    if index >= len(routes):
        return {
            "routing_decision": "CRITICAL_DELAY",
            "selected_route": {},
            "logs": [
                f"select_route: No route available at index {index}, "
                f"marking for escalation"
            ],
        }

    selected = routes[index]
    return {
        "selected_route": selected,
        "logs": [
            f"select_route: Selected route {selected.get('route_id')} "
            f"at index {index}"
        ],
    }


def check_warehouse(state: LogisticsIncidentState) -> dict:
    selected_route = state.get("selected_route", {})
    warehouse_id = selected_route.get("warehouse_id", "")

    if not warehouse_id:
        return {
            "warehouse_db_context": {"error": "No warehouse ID in selected route"},
            "logs": ["check_warehouse: No warehouse ID found in selected route"],
        }

    warehouse_info = query_warehouse_inventory_tool(warehouse_id)

    return {
        "warehouse_db_context": warehouse_info,
        "logs": [
            f"check_warehouse: Queried warehouse {warehouse_id} - "
            f"utilization={warehouse_info.get('current_utilization_pct', 'N/A')}, "
            f"status={warehouse_info.get('operational_status', 'N/A')}, "
            f"risk={warehouse_info.get('risk_tier', 'N/A')}"
        ],
    }


def analyze_route(state: LogisticsIncidentState) -> dict:
    metadata = state.get("extracted_metadata", {})
    route = state.get("selected_route", {})
    warehouse = state.get("warehouse_db_context", {})

    decision, reason, score = evaluate_route(metadata, route, warehouse)

    route_evaluation = {
        "route_id": route.get("route_id", ""),
        "decision": decision,
        "reason": reason,
    }

    return {
        "reroute_impact_score": score,
        "routing_decision": decision,
        "routes_evaluated": [route_evaluation],
        "logs": [
            f"analyze_route: Route {route.get('route_id', 'unknown')} "
            f"evaluated -> {decision} (score={score}). Reason: {reason}"
        ],
    }


def route_clarification(state: LogisticsIncidentState) -> dict:
    current_attempts = state.get("clarification_attempts", 0)
    current_index = state.get("current_route_index", 0)
    max_attempts = state.get("max_clarification_attempts", MAX_CLARIFICATION_ATTEMPTS)
    routes = state.get("available_routes", [])

    new_attempts = current_attempts + 1
    new_index = current_index + 1

    updates = {
        "clarification_attempts": new_attempts,
        "current_route_index": new_index,
        "logs": [
            f"route_clarification: Rejected route at index {current_index}, "
            f"attempt {new_attempts} of {max_attempts}"
        ],
    }

    if new_attempts > max_attempts or new_index >= len(routes):
        updates["routing_decision"] = "CRITICAL_DELAY"
        updates["logs"].append(
            f"route_clarification: No more acceptable routes available, "
            f"escalating incident"
        )

    return updates


def finalize_route(state: LogisticsIncidentState) -> dict:
    selected = state.get("selected_route", {})
    return {
        "logs": [
            f"finalize_route: Route {selected.get('route_id', 'unknown')} "
            f"finalized as optimal path"
        ],
    }


def escalate_incident(state: LogisticsIncidentState) -> dict:
    return {
        "routing_decision": "CRITICAL_DELAY",
        "logs": [
            f"escalate_incident: Incident {state.get('incident_id', 'unknown')} "
            f"escalated due to {state.get('routing_decision', 'unknown condition')}"
        ],
    }


def generate_report(state: LogisticsIncidentState) -> dict:
    llm = resolve_llm()

    routing_decision = state.get("routing_decision", "")
    selected_route = state.get("selected_route", {})
    routes_evaluated = state.get("routes_evaluated", [])
    warehouse = state.get("warehouse_db_context", {})
    rag_context = state.get("routing_rag_context", "")
    metadata = state.get("extracted_metadata", {})
    manifest = state.get("manifest_text", "")
    incident_id = state.get("incident_id", "")

    brief_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a logistics operations assistant. Generate a concise "
            "operations brief based on the incident information provided. "
            "The brief must explain what happened, which route was selected "
            "or why the incident was escalated, and the major rule or "
            "warehouse condition that affected the decision. Keep the brief "
            "to 3-5 sentences. Do not fabricate information beyond what is "
            "provided in the context.",
        ),
        (
            "human",
            "Incident ID: {incident_id}\n"
            "Disruption Summary: {manifest}\n"
            "Parsed Shipment: shipment_id={shipment_id}, "
            "cargo_weight={cargo_weight} tons, cargo_type={cargo_type}, "
            "target_warehouse={target_warehouse}, "
            "has_perishables={has_perishables}, "
            "max_delay={max_delay}\n"
            "Routing Decision: {routing_decision}\n"
            "Selected Route: {selected_route}\n"
            "Routes Evaluated: {routes_evaluated}\n"
            "Warehouse Metrics: {warehouse}\n"
            "Applied Logistics Rules: {rag_context}\n\n"
            "Generate the operations brief:",
        ),
    ])

    brief_chain = brief_prompt | llm | StrOutputParser()

    brief = brief_chain.invoke({
        "incident_id": incident_id,
        "manifest": manifest,
        "shipment_id": metadata.get("shipment_id", "unknown"),
        "cargo_weight": metadata.get("cargo_weight_tons", "unknown"),
        "cargo_type": metadata.get("cargo_type", "unknown"),
        "target_warehouse": metadata.get("target_warehouse_id", "unknown"),
        "has_perishables": metadata.get("has_perishables", False),
        "max_delay": metadata.get("maximum_tolerable_delay_hours", "not specified"),
        "routing_decision": routing_decision,
        "selected_route": json.dumps(selected_route),
        "routes_evaluated": json.dumps(routes_evaluated),
        "warehouse": json.dumps(warehouse),
        "rag_context": rag_context,
    })

    report = build_report(state, brief)
    save_report(report, incident_id)

    return {
        "final_report": report,
        "logs": [
            f"generate_report: Final report generated for {incident_id} "
            f"with decision {routing_decision}"
        ],
    }


def route_decision_router(state: LogisticsIncidentState) -> str:
    decision = state.get("routing_decision", "")
    if decision == "OPTIMAL_PATH_FOUND":
        return "OPTIMAL_PATH_FOUND"
    elif decision == "CRITICAL_DELAY":
        return "CRITICAL_DELAY"
    return "ROUTE_CLARIFICATION"


def clarification_router(state: LogisticsIncidentState) -> str:
    attempts = state.get("clarification_attempts", 0)
    max_attempts = state.get("max_clarification_attempts", MAX_CLARIFICATION_ATTEMPTS)
    index = state.get("current_route_index", 0)
    routes = state.get("available_routes", [])

    if attempts > max_attempts or index >= len(routes):
        return "escalate"
    return "retry"


def select_route_router(state: LogisticsIncidentState) -> str:
    decision = state.get("routing_decision", "")
    if decision == "CRITICAL_DELAY":
        return "escalate"
    return "check_warehouse"