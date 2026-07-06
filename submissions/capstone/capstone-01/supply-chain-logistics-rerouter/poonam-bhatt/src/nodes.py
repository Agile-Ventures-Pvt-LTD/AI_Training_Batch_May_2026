import os
import re
import json
from dotenv import load_dotenv
from typing import Literal
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from src.state import LogisticsIncidentState
from src.schemas import ShipmentMetadata
from src.tools import query_warehouse_inventory_tool, get_alternative_routes_tool
from src.rag import retrieve_logistics_rules
from src.report_writer import generate_operations_brief, save_reroute_advisory_report

load_dotenv()

def _parse_incident_fallback(manifest_text: str) -> dict:
    """Regex-based fallback parser for metadata extraction in case of LLM API issues."""
    shipment_id = "UNKNOWN"
    cargo_weight_tons = 100
    cargo_type = "general cargo"
    target_warehouse_id = "UNKNOWN"
    has_perishables = False
    maximum_tolerable_delay_hours = None

    # Extraction rules using regex
    # Shipment ID (e.g. SH-4002, SH-4105, SH-4208)
    sh_match = re.search(r"SH-\d{4}", manifest_text)
    if sh_match:
        shipment_id = sh_match.group(0)

    # Cargo Weight (e.g. 550 tons, 250 tons, 700 tons)
    weight_match = re.search(r"(\d+)\s*tons", manifest_text)
    if weight_match:
        cargo_weight_tons = int(weight_match.group(1))

    # Cargo Type (e.g. industrial electronics, consumer electronics, industrial machinery)
    type_match = re.search(r"carrying\s+\d+\s*tons\s+of\s+([^,.]+?)(\s+originally|\s+scheduled|\.|$)", manifest_text, re.IGNORECASE)
    if not type_match:
        type_match = re.search(r"contains\s+\d+\s*tons\s+of\s+([^,.]+?)(\.|$)", manifest_text, re.IGNORECASE)
    if type_match:
        cargo_type = type_match.group(1).strip()

    # Target Warehouse ID (e.g. WH-WEST-202, WH-SOUTH-303, WH-EAST-101)
    wh_match = re.search(r"WH-[A-Z]+-\d{3}", manifest_text)
    if wh_match:
        target_warehouse_id = wh_match.group(0)

    # Has Perishables
    if "perishable" in manifest_text.lower():
        has_perishables = True

    # Tolerable Delay (e.g. exceeding 72 hours)
    delay_match = re.search(r"exceeding\s+(\d+)\s*hours", manifest_text)
    if delay_match:
        maximum_tolerable_delay_hours = int(delay_match.group(1))

    return {
        "shipment_id": shipment_id,
        "cargo_weight_tons": cargo_weight_tons,
        "cargo_type": cargo_type,
        "target_warehouse_id": target_warehouse_id,
        "has_perishables": has_perishables,
        "maximum_tolerable_delay_hours": maximum_tolerable_delay_hours
    }

# Node-01: parse_incident
def parse_incident(state: LogisticsIncidentState) -> dict:
    print(f"\n--- Node: parse_incident ({state.get('incident_id')}) ---")
    manifest_text = state.get("manifest_text", "")
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    extracted = None
    if api_key:
        try:
            llm = ChatGroq(
                api_key=api_key,
                model_name=model_name,
                temperature=0.0
            )
            structured_llm = llm.with_structured_output(ShipmentMetadata)
            prompt = ChatPromptTemplate.from_messages([
                ("system", "Extract all key shipment information from the shipping manifest text."),
                ("user", "{manifest}")
            ])
            chain = prompt | structured_llm
            res = chain.invoke({"manifest": manifest_text})
            
            # Map object back to dictionary
            extracted = {
                "shipment_id": res.shipment_id,
                "cargo_weight_tons": res.cargo_weight_tons,
                "cargo_type": res.cargo_type,
                "target_warehouse_id": res.target_warehouse_id,
                "has_perishables": res.has_perishables,
                "maximum_tolerable_delay_hours": res.maximum_tolerable_delay_hours
            }
        except Exception as e:
            print(f"[Warning] LLM parsing failed, using fallback regex parser. Error: {e}")
            
    if not extracted:
        extracted = _parse_incident_fallback(manifest_text)
        
    print(f"Extracted Metadata: {json.dumps(extracted)}")
    return {
        "extracted_metadata": extracted,
        "logs": state.get("logs", []) + [f"Incident Parsed: shipment_id={extracted['shipment_id']}"]
    }

# Node-02: policy_rag_lookup
def policy_rag_lookup(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: policy_rag_lookup ---")
    manifest = state.get("manifest_text", "")
    metadata = state.get("extracted_metadata", {})
    
    # Query RAG with manifest and cargo type details
    query_str = f"Shipment details: {manifest}. Cargo: {metadata.get('cargo_type')} weight: {metadata.get('cargo_weight_tons')} tons."
    rules = retrieve_logistics_rules(query_str)
    
    print(f"Retrieved Logistics Rules:\n{rules}")
    return {
        "routing_rag_context": rules,
        "logs": state.get("logs", []) + ["Retrieved logistics rules using FAISS vector store."]
    }

# Node-03: load_alternative_routes
def load_alternative_routes(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: load_alternative_routes ---")
    port_id = state.get("disrupted_port_id", "")
    routes = get_alternative_routes_tool(port_id)
    
    print(f"Available alternative routes for {port_id}: {routes}")
    return {
        "available_routes": routes,
        "current_route_index": 0,
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": state.get("logs", []) + [f"Loaded {len(routes)} alternative routes."]
    }

# Node-04: select_route
def select_route(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: select_route ---")
    routes = state.get("available_routes", [])
    idx = state.get("current_route_index", 0)
    
    if idx < len(routes):
        selected = routes[idx]
        print(f"Selected route [{idx}]: {selected}")
    else:
        selected = {}
        print("No route available (index out of range)")
        
    return {
        "selected_route": selected,
        "logs": state.get("logs", []) + [f"Selected route: {selected.get('route_id', 'None')}"]
    }

# Node-05: check_warehouse
def check_warehouse(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: check_warehouse ---")
    selected = state.get("selected_route", {})
    warehouse_id = selected.get("warehouse_id", "")
    
    metrics = query_warehouse_inventory_tool(warehouse_id)
    print(f"Warehouse metrics for {warehouse_id}: {metrics}")
    
    return {
        "warehouse_db_context": metrics,
        "logs": state.get("logs", []) + [f"Checked warehouse status for: {warehouse_id}"]
    }

# Node-06: analyze_route
def analyze_route(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: analyze_route ---")
    metadata = state.get("extracted_metadata", {})
    route = state.get("selected_route", {})
    wh = state.get("warehouse_db_context", {})
    
    # Calculate score
    score = 0
    utilization = wh.get("current_utilization_pct", 0)
    risk = wh.get("risk_tier", "NORMAL")
    status = wh.get("operational_status", "ACTIVE")
    delay = route.get("added_delay_hours", 0)
    max_delay = metadata.get("maximum_tolerable_delay_hours")
    
    if "error" in wh:
        # Warehouse lookup failed
        status = "INACTIVE"
        utilization = 100
        score += 30
        reason = f"Warehouse lookup failed: {wh.get('error')}"
        decision = "ROUTE_CLARIFICATION"
    else:
        reasons = []
        decision = "OPTIMAL_PATH_FOUND"
        
        # Rule checks
        # 1. Warehouse utilization above 85%
        if utilization > 85:
            score += 30
            reasons.append("Warehouse utilization exceeds 85%")
            decision = "ROUTE_CLARIFICATION"
            
        # 2. Risk tier ELEVATED
        if risk == "ELEVATED":
            score += 25
            reasons.append("Warehouse risk tier is ELEVATED")
            decision = "ROUTE_CLARIFICATION"
            
        # 3. Operational status not ACTIVE
        if status != "ACTIVE":
            score += 30
            reasons.append("Warehouse operational status is not ACTIVE")
            decision = "ROUTE_CLARIFICATION"
            
        # 4. Added delay exceeds maximum tolerable delay
        if max_delay is not None and delay > max_delay:
            score += 25
            reasons.append(f"Route delay ({delay}h) exceeds maximum limit ({max_delay}h)")
            decision = "ROUTE_CLARIFICATION"
            
        # 5. Added delay exceeds 120 hours
        if delay > 120:
            score += 50
            reasons.append("Route delay exceeds 120 hours limit")
            decision = "CRITICAL_DELAY"
            
        reason = "; ".join(reasons) if reasons else "Warehouse and route conditions are acceptable"
        
    # Cap score at 100
    score = min(score, 100)
    
    print(f"Reroute Impact Score: {score}, Decision: {decision}, Reason: {reason}")
    route_log = f"Route Checked: {route.get('route_id')}. Decision: {decision}. Reason: {reason}"
    
    return {
        "reroute_impact_score": score,
        "routing_decision": decision,
        "logs": state.get("logs", []) + [route_log]
    }

# Node-07: route_clarification
def route_clarification(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: route_clarification ---")
    attempts = state.get("clarification_attempts", 0) + 1
    idx = state.get("current_route_index", 0) + 1
    routes = state.get("available_routes", [])
    
    # Check if another route exists or limit reached
    if attempts >= state.get("max_clarification_attempts", 2) or idx >= len(routes):
        decision = "CRITICAL_DELAY"
        print(f"Max retries reached or no more routes. Escalating to CRITICAL_DELAY. Index: {idx}/{len(routes)}")
    else:
        decision = "ROUTE_CLARIFICATION"
        print(f"Checking next alternative route. Index: {idx}")
        
    return {
        "clarification_attempts": attempts,
        "current_route_index": idx,
        "routing_decision": decision,
        "logs": state.get("logs", []) + [f"Executed route retry. Attempt={attempts}, Next Index={idx}"]
    }

# Node-08: finalize_route
def finalize_route(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: finalize_route ---")
    route = state.get("selected_route", {})
    print(f"Finalized Route: {route.get('route_id')}")
    return {
        "routing_decision": "OPTIMAL_PATH_FOUND",
        "logs": state.get("logs", []) + [f"Finalized route selection: {route.get('route_id')}"]
    }

# Node-09: escalate_incident
def escalate_incident(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: escalate_incident ---")
    print("Incident escalated to regional coordinator.")
    return {
        "routing_decision": "CRITICAL_DELAY",
        "selected_route": {}, # Clean selected route for escalation
        "logs": state.get("logs", []) + ["Incident escalated due to critical delay or route exhaustion."]
    }

# Node-10: generate_report
def generate_report(state: LogisticsIncidentState) -> dict:
    print("\n--- Node: generate_report ---")
    brief = generate_operations_brief(state)
    print(f"LLM Operations Brief:\n{brief}")
    
    # Temporarily store brief in report
    state_copy = {**state, "final_report": {"final_operations_brief": brief}}
    
    # Save the report JSON
    incident_id = state.get("incident_id", "UNKNOWN")
    save_reroute_advisory_report(state_copy, f"{incident_id}_reroute_advisory_report.json")
    
    return {
        "final_report": {"final_operations_brief": brief},
        "logs": state.get("logs", []) + ["Final operations briefing report generated and saved."]
    }




### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026