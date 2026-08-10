from pathlib import Path 
import json 
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from src.schemas import ShipmentMetadata 
from src.tools import ( query_warehouse_inventory_tool, get_alternative_routes_tool, ) 
from src.rag import retrieve_logistics_rules 
BASE_DIR = Path(__file__).resolve().parent.parent 
OUTPUT_DIR = BASE_DIR / "outputs" 
OUTPUT_DIR.mkdir(exist_ok=True) 

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def get_llm(): 

    return ChatGroq( model="llama-3.3-70b-versatile", 
                    temperature=0 ) 

def parse_incident(state: dict) -> dict: 
    """Extract shipment details from manifest text using LangChain.""" 
    llm = get_llm().with_structured_output(ShipmentMetadata) 
    prompt = ChatPromptTemplate.from_messages([ ( "system", "Extract shipment information. " "If maximum delay is missing, return null. " "Do not invent values." ), ("human", "{manifest_text}") ]) 
    chain = prompt | llm 
    metadata = chain.invoke({"manifest_text": state["manifest_text"]}) 
    return { "extracted_metadata": metadata.model_dump(), "logs": ["Shipment metadata extracted."] } 

def policy_rag_lookup(state: dict) -> dict: 
    """Retrieve relevant logistics rules.""" 
    metadata = state["extracted_metadata"] ,
    query = ( f"Cargo weight {metadata.get('cargo_weight_tons')} tons. " f"Cargo type {metadata.get('cargo_type')}. " f"Maximum delay {metadata.get('maximum_tolerable_delay_hours')}. " "Find warehouse, delay, route and escalation rules." ) 
    rules = retrieve_logistics_rules(query) 
    return { "routing_rag_context": rules, "logs": state.get("logs", []) + ["Relevant logistics rules retrieved."] }
def load_alternative_routes(state: dict) -> dict: 
    """Load routes and initialize retry values.""" 
    routes = get_alternative_routes_tool(state["disrupted_port_id"]) 
    return { "available_routes": routes, "current_route_index": 0, 
            "clarification_attempts": 0, "max_clarification_attempts": 2, 
            "logs": state.get("logs", []) + [f"{len(routes)} routes loaded."] }

def select_route(state: dict) -> dict:
    """Select route using current route index.""" 
    index = state["current_route_index"] 
    routes = state["available_routes"] 
    if index >= len(routes):
        return { "selected_route": {},
                 "routing_decision": "CRITICAL_DELAY",
                   "logs": state.get("logs", []) + ["No more routes available."] }
    route = routes[index]
    return { "selected_route": route, "logs": state.get("logs", []) + [f"Selected {route['route_id']}."] } 


def check_warehouse(state: dict) -> dict:
    """Check selected route warehouse.""" 
    route = state["selected_route"] 
    if not route: 
        return { "warehouse_db_context": {}, 
                "logs": state.get("logs", []) + ["Warehouse check skipped."] } 
    warehouse = query_warehouse_inventory_tool(route["warehouse_id"]) 
    return { "warehouse_db_context": warehouse, "logs": state.get("logs", []) + ["Warehouse checked."] }
            
def evaluate_route(metadata: dict, route: dict, warehouse: dict) -> tuple: 
    """ Deterministic routing decision. Returns: decision, score, reason """ 
    if not route or not warehouse or not warehouse.get("success"): 
        return "CRITICAL_DELAY", 100, "Route or warehouse data is unavailable." 
    score = 0 
    reasons = [] 
    utilization = warehouse.get("current_utilization_pct", 0) 
    status = warehouse.get("operational_status", "") 
    risk = warehouse.get("risk_tier", "") 
    delay = route.get("added_delay_hours", 0) 
    max_delay = metadata.get("maximum_tolerable_delay_hours") 
    if utilization > 85: 
        score += 30 
        reasons.append("Warehouse utilization is above 85%.") 
    if risk == "ELEVATED": 
        score += 25 
        reasons.append("Warehouse risk tier is ELEVATED.") 
    if status != "ACTIVE": 
        score += 30

        reasons.append("Warehouse is not ACTIVE.") 
    if max_delay is not None and delay > max_delay: 
        score += 25 
        reasons.append("Route delay exceeds shipment delay limit.") 
    if delay > 120: 
        score += 50 
        reasons.append("Route delay exceeds 120 hours.") 
        return "CRITICAL_DELAY", min(score, 100), " ".join(reasons) 
    if utilization > 85 or risk == "ELEVATED" or status != "ACTIVE":
        return "ROUTE_CLARIFICATION", min(score, 100), " ".join(reasons) 
    if max_delay is not None and delay > max_delay: 
        return "ROUTE_CLARIFICATION", min(score, 100), " ".join(reasons) 
    return "OPTIMAL_PATH_FOUND", min(score, 100), "Warehouse and route conditions are acceptable." 


def analyze_route(state: dict) -> dict: 
    """Analyze the current route using deterministic rules.""" 
    decision, score, reason = evaluate_route( state["extracted_metadata"], 
                                             state["selected_route"], 
                                             state["warehouse_db_context"], ) 
    evaluated = state.get("routes_evaluated", []) 
    route = state["selected_route"] 
    if route: 
        evaluated.append({ "route_id": route.get("route_id"), "decision": decision, "reason": reason }) 
        return { "routing_decision": decision,
                 "reroute_impact_score": score, 
                 "routes_evaluated": evaluated, 
                 "logs": state.get("logs", []) + [f"Decision: {decision}"] } 
def route_clarification(state: dict) -> dict: 
    """Reject route and move to next available route.""" 
    attempts = state["clarification_attempts"] + 1 
    next_index = state["current_route_index"] + 1 
    if ( attempts >= state["max_clarification_attempts"] or next_index >= len(state["available_routes"]) ):
         return { "clarification_attempts": attempts, 
                 "current_route_index": next_index, 
                 "routing_decision": "CRITICAL_DELAY",
                "logs": state.get("logs", []) + ["Retry limit reached. Escalating incident."] } 
    return { "clarification_attempts": attempts,
             "current_route_index": next_index, 
             "logs": state.get("logs", []) + ["Trying next route."] } 
def finalize_route(state: dict) -> dict: 
    """Keep the selected route as final.""" 
    return { "logs": state.get("logs", []) + ["Route finalized."] }
def escalate_incident(state: dict) -> dict: 
    """Mark the incident as escalated.""" 
    return { "routing_decision": "CRITICAL_DELAY", "logs": state.get("logs", []) + ["Incident escalated."] } 

def generate_report(state: dict) -> dict:
     """Create and save the final JSON report.""" 
    llm = get_llm() 
    prompt = ChatPromptTemplate.from_messages([ ( "system", "Write a concise logistics operations brief in 2-3 sentences. " "Explain the disruption, route decision, and key reason." ), 
                                               ( "human", "Incident: {incident_id}\n" "Manifest: {manifest_text}\n" 
                                                "Decision: {decision}\n" "Route: {route}\n" "Warehouse: {warehouse}\n" 
                                                "Rules: {rules}" ) ]) 
    chain = prompt | llm 
    response = chain.invoke({ "incident_id": state["incident_id"], 
                                                  "manifest_text": state["manifest_text"], 
                                                  "decision": state["routing_decision"],
                                                    "route": state.get("selected_route", {}), 
                                                    "warehouse": state.get("warehouse_db_context", {}), 
                                                    "rules": state.get("routing_rag_context", ""), }) 
    report = { "incident_id": state["incident_id"], "original_incident_summary": state["manifest_text"][:200], 
          "parsed_metadata": state["extracted_metadata"], 
          "rag_validation_rules_applied": state["routing_rag_context"].split("\n\n"), 
          "routes_evaluated": state.get("routes_evaluated", []), 
          "final_selected_route": ( state["selected_route"] 
                                   if state["routing_decision"] == "OPTIMAL_PATH_FOUND" else {} ), 
                                   "queried_warehouse_metrics": state.get("warehouse_db_context", {}), 
                                   "graph_routing_metadata": { "loops_executed": state.get("clarification_attempts", 0), 
                                                              "final_decision_state": state["routing_decision"], 
                                                              "reroute_impact_score": state.get("reroute_impact_score", 0), }, 
                                                              "final_operations_brief": response.content, } 
    report_path = OUTPUT_DIR / f"{state['incident_id']}_reroute_advisory_report.json" 
    with open(report_path, "w", encoding="utf-8") as file: 
        json.dump(report, file, indent=4) 
    return { "final_report": report, 
            "logs": state.get("logs", []) + [f"Report saved: {report_path.name}"] }


d


