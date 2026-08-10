import os
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.state import LogisticsIncidentState
from src.schemas import ShipmentMetadata
from src.tools import query_warehouse_inventory_tool, get_alternative_routes_tool
from src.rag import retrieve_relevant_rules

load_dotenv()
llm = ChatGroq(
    model=os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
    temperature=0
)

class IncidentParsingResult(BaseModel):
    metadata: ShipmentMetadata
    summary: str = Field(description="A short, one-sentence summary of the original disruption.")

structured_parser = llm.with_structured_output(IncidentParsingResult)

def parse_incident(state: LogisticsIncidentState) -> dict:
    """Extract the shipment metadata and incident summary from manifest text using LLM."""
    manifest_text = state.get("manifest_text", "")
    incident_id = state.get("incident_id", "")
    
    logs = state.get("logs", []).copy()
    logs.append(f"[{incident_id}] Node 'parse_incident': Extracting shipment details from manifest")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert logistics coordinator. Extract the shipment metadata and generate a short, one-sentence summary of the original disruption from the manifest text."),
        ("user", "Incident Manifest Text:\n{manifest_text}")
    ])
    
    chain = prompt | structured_parser
    result = chain.invoke({"manifest_text": manifest_text})
    
    logs.append(f"[{incident_id}] Node 'parse_incident': Extracted shipment {result.metadata.shipment_id}.")
    
    return {
        "extracted_metadata": result.metadata.model_dump(),
        "original_incident_summary": result.summary,
        "logs": logs
    }

def policy_rag_lookup(state: LogisticsIncidentState) -> dict:
    """Retrieve logistics rules relevant to current incident using RAG pipeline."""
    manifest_text = state.get("manifest_text", "")
    incident_id = state.get("incident_id", "")
    
    logs = state.get("logs", []).copy()
    logs.append(f"[{incident_id}] Node 'policy_rag_lookup': Retrieving relevant rules via RAG")
    
    rules = retrieve_relevant_rules(manifest_text)
    context = "\n\n".join(rules)
    
    logs.append(f"[{incident_id}] Node 'policy_rag_lookup': Retrieved {len(rules)} relevant rules.")
    
    return {
        "routing_rag_context": context,
        "rag_validation_rules_applied": rules,
        "logs": logs
    }

def load_alternative_routes(state: LogisticsIncidentState) -> dict:
    """Load alternative routes using the get_alternative_routes_tool."""
    disrupted_port_id = state.get("disrupted_port_id", "")
    incident_id = state.get("incident_id", "")
    
    logs = state.get("logs", []).copy()
    logs.append(f"[{incident_id}] Node 'load_alternative_routes': Querying alternative routes for port {disrupted_port_id}...")
    
    routes = get_alternative_routes_tool(disrupted_port_id)
    
    logs.append(f"[{incident_id}] Node 'load_alternative_routes': Found {len(routes)} alternative routes.")
    
    return {
        "available_routes": routes,
        "current_route_index": 0,
        "clarification_attempts": 0,
        "logs": logs
    }

def select_route(state: LogisticsIncidentState) -> dict:
    """Select the route at the current route index from available routes."""
    routes = state.get("available_routes", [])
    index = state.get("current_route_index", 0)
    incident_id = state.get("incident_id", "")
    
    logs = state.get("logs", []).copy()
    
    if not routes or index >= len(routes):
        logs.append(f"[{incident_id}] Node 'select_route': No routes available at index {index}.")
        return {
            "selected_route": {},
            "routing_decision": "CRITICAL_DELAY",
            "logs": logs
        }
        
    selected = routes[index]
    logs.append(f"[{incident_id}] Node 'select_route': Selected route {selected.get('route_id')} (Index {index}).")
    
    return {
        "selected_route": selected,
        "logs": logs
    }

def check_warehouse(state: LogisticsIncidentState) -> dict:
    """Query warehouse inventory for the warehouse of the selected route."""
    selected_route = state.get("selected_route", {})
    incident_id = state.get("incident_id", "")
    logs = state.get("logs", []).copy()
    
    if not selected_route:
        logs.append(f"[{incident_id}] Node 'check_warehouse': No route selected to check warehouse.")
        return {
            "warehouse_db_context": {},
            "logs": logs
        }
        
    wh_id = selected_route.get("warehouse_id", "")
    logs.append(f"[{incident_id}] Node 'check_warehouse': Querying inventory for warehouse {wh_id}...")
    
    wh_info = query_warehouse_inventory_tool(wh_id)
    
    logs.append(f"[{incident_id}] Node 'check_warehouse': Warehouse details retrieved.")
    
    return {
        "warehouse_db_context": wh_info,
        "logs": logs
    }

def calculate_reroute_impact_score(
    current_utilization_pct: int,
    risk_tier: str,
    operational_status: str,
    added_delay_hours: int,
    maximum_tolerable_delay_hours: Optional[int]
) -> int:
    """Calculate the reroute impact score using the given PRD rules."""
    score = 0
    if current_utilization_pct > 85:
        score += 30
    if risk_tier == "ELEVATED":
        score += 25
    if operational_status != "ACTIVE":
        score += 30
    if maximum_tolerable_delay_hours is not None and added_delay_hours > maximum_tolerable_delay_hours:
        score += 25
    if added_delay_hours > 120:
        score += 50
    return min(score, 100)

def analyze_route(state: LogisticsIncidentState) -> dict:
    """Evaluate selected route and warehouse details deterministically."""
    selected_route = state.get("selected_route", {})
    warehouse_db = state.get("warehouse_db_context", {})
    extracted_metadata = state.get("extracted_metadata", {})
    incident_id = state.get("incident_id", "")
    logs = state.get("logs", []).copy()
    routes_evaluated = state.get("routes_evaluated", []).copy()
    
    if not selected_route or "error" in warehouse_db:
        logs.append(f"[{incident_id}] Node 'analyze_route': Missing route or warehouse query failed.")
        return {
            "routing_decision": "ROUTE_CLARIFICATION",
            "logs": logs
        }
        
    route_id = selected_route.get("route_id", "")
    current_utilization_pct = warehouse_db.get("current_utilization_pct", 0)
    operational_status = warehouse_db.get("operational_status", "")
    risk_tier = warehouse_db.get("risk_tier", "")
    added_delay_hours = selected_route.get("added_delay_hours", 0)
    max_tolerable_delay = extracted_metadata.get("maximum_tolerable_delay_hours")
    
    rejection_reasons = []
    routing_decision = "OPTIMAL_PATH_FOUND"
    
    if current_utilization_pct > 85:
        routing_decision = "ROUTE_CLARIFICATION"
        rejection_reasons.append("Warehouse utilization is above 85 percent")
    if operational_status != "ACTIVE":
        routing_decision = "ROUTE_CLARIFICATION"
        rejection_reasons.append("Warehouse operational status is not ACTIVE")
    if risk_tier == "ELEVATED":
        routing_decision = "ROUTE_CLARIFICATION"
        rejection_reasons.append("Warehouse risk tier is ELEVATED")
    if added_delay_hours > 120:
        routing_decision = "CRITICAL_DELAY"
        rejection_reasons.append("Added route delay exceeds 120 hours")
    elif max_tolerable_delay is not None and added_delay_hours > max_tolerable_delay:
        if routing_decision != "CRITICAL_DELAY":
            routing_decision = "ROUTE_CLARIFICATION"
        rejection_reasons.append("Added route delay exceeds shipment delay limit")
        
    if routing_decision == "OPTIMAL_PATH_FOUND":
        reason = "Warehouse and route conditions are acceptable"
    else:
        reason = ", ".join(rejection_reasons)
        
    score = calculate_reroute_impact_score(
        current_utilization_pct=current_utilization_pct,
        risk_tier=risk_tier,
        operational_status=operational_status,
        added_delay_hours=added_delay_hours,
        maximum_tolerable_delay_hours=max_tolerable_delay
    )
    
    logs.append(f"[{incident_id}] Node 'analyze_route': Evaluated {route_id}. Decision: {routing_decision}, Score: {score}, Reason: {reason}")
    
    routes_evaluated.append({
        "route_id": route_id,
        "decision": routing_decision,
        "reason": reason
    })
    
    return {
        "routing_decision": routing_decision,
        "reroute_impact_score": score,
        "routes_evaluated": routes_evaluated,
        "logs": logs
    }

def route_clarification(state: LogisticsIncidentState) -> dict:
    """Process route rejection and check if another route is available."""
    incident_id = state.get("incident_id", "")
    clarification_attempts = state.get("clarification_attempts", 0) + 1
    current_route_index = state.get("current_route_index", 0) + 1
    routes = state.get("available_routes", [])
    max_attempts = state.get("max_clarification_attempts", 2)
    logs = state.get("logs", []).copy()
    
    another_route_exists = current_route_index < len(routes)
    attempts_remaining = clarification_attempts < max_attempts
    
    if another_route_exists and attempts_remaining:
        logs.append(f"[{incident_id}] Node 'route_clarification': Route rejected. Attempt {clarification_attempts}/{max_attempts}. Retrying with next route (Index {current_route_index}).")
        return {
            "clarification_attempts": clarification_attempts,
            "current_route_index": current_route_index,
            "routing_decision": "ROUTE_CLARIFICATION",
            "logs": logs
        }
    else:
        reason_msg = "No more routes available" if not another_route_exists else "Max clarification attempts reached"
        logs.append(f"[{incident_id}] Node 'route_clarification': Route rejected. {reason_msg}. Escalating incident.")
        return {
            "clarification_attempts": clarification_attempts,
            "current_route_index": current_route_index,
            "routing_decision": "CRITICAL_DELAY",
            "logs": logs
        }

def finalize_route(state: LogisticsIncidentState) -> dict:
    """Finalize the accepted route."""
    incident_id = state.get("incident_id", "")
    logs = state.get("logs", []).copy()
    logs.append(f"[{incident_id}] Node 'finalize_route': Route accepted. Saving decision.")
    return {
        "routing_decision": "OPTIMAL_PATH_FOUND",
        "logs": logs
    }

def escalate_incident(state: LogisticsIncidentState) -> dict:
    """Mark the incident as escalated."""
    incident_id = state.get("incident_id", "")
    logs = state.get("logs", []).copy()
    logs.append(f"[{incident_id}] Node 'escalate_incident': Escalating incident due to lack of viable routes.")
    return {
        "selected_route": {},
        "routing_decision": "CRITICAL_DELAY",
        "logs": logs
    }

def generate_report(state: LogisticsIncidentState) -> dict:
    """Generate final JSON report and save it to the output folder."""
    incident_id = state.get("incident_id", "")
    logs = state.get("logs", []).copy()
    logs.append(f"[{incident_id}] Node 'generate_report': Generating final advisory report...")
    

    brief_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a professional supply chain crisis management assistant. "
            "Write a short, concise operations brief for the logistics team summarizing the incident and the decision. "
            "Explain:\n"
            "1. What happened.\n"
            "2. Which alternative route was selected (or explain why the incident had to be escalated).\n"
            "3. The major rules or warehouse conditions (such as utilization, risk tier, status, or delay limits) that drove this decision.\n"
            "Keep the brief concise (1-3 sentences total) and highly professional. Do not refer to the internal state variables or python code directly."
        )),
        ("user", (
            "Incident ID: {incident_id}\n"
            "Original Incident Summary: {original_summary}\n"
            "Disrupted Port ID: {disrupted_port_id}\n"
            "Metadata Extracted: {extracted_metadata}\n"
            "Routes Evaluated: {routes_evaluated}\n"
            "Final Selected Route: {selected_route}\n"
            "Warehouse Checked: {warehouse_db_context}\n"
            "Routing Decision: {routing_decision}\n"
            "Reroute Impact Score: {reroute_impact_score}\n"
        ))
    ])
    
    brief_chain = brief_prompt | llm
    brief_response = brief_chain.invoke({
        "incident_id": incident_id,
        "original_summary": state.get("original_incident_summary", ""),
        "disrupted_port_id": state.get("disrupted_port_id", ""),
        "extracted_metadata": state.get("extracted_metadata", {}),
        "routes_evaluated": state.get("routes_evaluated", []),
        "selected_route": state.get("selected_route", {}),
        "warehouse_db_context": state.get("warehouse_db_context", {}),
        "routing_decision": state.get("routing_decision", ""),
        "reroute_impact_score": state.get("reroute_impact_score", 0)
    })
    
    operations_brief = brief_response.content.strip()
    logs.append(f"[{incident_id}] Node 'generate_report': Generated brief: {operations_brief}")
    

    report = {
        "incident_id": incident_id,
        "original_incident_summary": state.get("original_incident_summary", ""),
        "parsed_metadata": state.get("extracted_metadata", {}),
        "rag_validation_rules_applied": state.get("rag_validation_rules_applied", []),
        "routes_evaluated": state.get("routes_evaluated", []),
        "final_selected_route": state.get("selected_route", {}),
        "queried_warehouse_metrics": state.get("warehouse_db_context", {}),
        "graph_routing_metadata": {
            "loops_executed": state.get("clarification_attempts", 0),
            "final_decision_state": state.get("routing_decision", ""),
            "reroute_impact_score": state.get("reroute_impact_score", 0)
        },
        "final_operations_brief": operations_brief
    }
    
    outputs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    

    specific_report_path = os.path.join(outputs_dir, f"{incident_id}_reroute_advisory_report.json")
    with open(specific_report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    latest_report_path = os.path.join(outputs_dir, "reroute_advisory_report.json")
    with open(latest_report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    logs.append(f"[{incident_id}] Node 'generate_report': Advisory reports saved to outputs/.")
    
    return {
        "final_report": report,
        "logs": logs
    }
