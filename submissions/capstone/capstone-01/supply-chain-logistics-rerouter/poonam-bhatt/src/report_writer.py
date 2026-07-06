import os
import json
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def generate_operations_brief(state: dict) -> str:
    """Uses Groq LLM to generate a short final operations brief summarizing the incident and decision.
    
    Args:
        state: The current LangGraph state dictionary.
        
    Returns:
        A concise operations brief string.
    """
    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Fallback brief if API key is not configured or in case of error
    fallback_brief = (
        f"Incident {state.get('incident_id')} processed. "
        f"Decision State: {state.get('routing_decision')}. "
        f"Selected Route: {state.get('selected_route', {}).get('route_id', 'None')}. "
        f"Impact Score: {state.get('reroute_impact_score')}."
    )
    
    if not api_key:
        return fallback_brief + " (Groq API Key not configured)"
        
    try:
        llm = ChatGroq(
            api_key=api_key,
            model_name=model_name,
            temperature=0.1
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", (
                "You are an expert logistics coordinator. Your task is to write a short, professional "
                "final operations brief for the logistics team based on the incident report details. "
                "The brief must explain:\n"
                "1. What happened.\n"
                "2. Which alternative route was selected (or why the incident was escalated).\n"
                "3. The major rule or warehouse condition that affected the decision.\n"
                "Keep the brief concise (2-4 sentences)."
            )),
            ("user", (
                "Incident ID: {incident_id}\n"
                "Manifest Summary: {manifest_text}\n"
                "Metadata Extracted: {metadata}\n"
                "Retrieved Rules Applied: {rules}\n"
                "Evaluated Routes Log: {logs}\n"
                "Routing Decision: {decision}\n"
                "Final Route Details: {route}\n"
                "Warehouse Utilization and Metrics: {warehouse}\n"
                "Reroute Impact Score: {impact_score}\n"
            ))
        ])
        
        chain = prompt | llm | StrOutputParser()
        brief = chain.invoke({
            "incident_id": state.get("incident_id"),
            "manifest_text": state.get("manifest_text"),
            "metadata": json.dumps(state.get("extracted_metadata", {})),
            "rules": state.get("routing_rag_context"),
            "logs": "\n".join(state.get("logs", [])),
            "decision": state.get("routing_decision"),
            "route": json.dumps(state.get("selected_route", {})),
            "warehouse": json.dumps(state.get("warehouse_db_context", {})),
            "impact_score": state.get("reroute_impact_score")
        })
        return brief.strip()
    except Exception as e:
        return fallback_brief + f" (Error generating brief: {str(e)})"

def save_reroute_advisory_report(state: dict, output_filename: str = None):
    """Compiles the final report from the state and saves it as a JSON file."""
    # Split the rulebook context to list applied rules
    rules_applied = []
    rag_context = state.get("routing_rag_context", "")
    if rag_context:
        rules_applied = [rule.strip() for rule in rag_context.split("\n\n") if rule.strip()]
        
    # Build list of checked routes from state logs or history
    routes_evaluated = []
    logs = state.get("logs", [])
    
    # We parse the log entries to compile routes_evaluated
    for log in logs:
        if "Route Checked:" in log:
            # Format: "Route Checked: ROUTE_ID. Decision: DECISION. Reason: REASON"
            try:
                parts = log.split(". Decision: ")
                route_id = parts[0].replace("Route Checked: ", "").strip()
                subparts = parts[1].split(". Reason: ")
                decision = subparts[0].strip()
                reason = subparts[1].strip()
                routes_evaluated.append({
                    "route_id": route_id,
                    "decision": decision,
                    "reason": reason
                })
            except Exception:
                pass

    # Build the report JSON
    report = {
        "incident_id": state.get("incident_id"),
        "original_incident_summary": state.get("manifest_text"),
        "parsed_metadata": state.get("extracted_metadata"),
        "rag_validation_rules_applied": rules_applied,
        "routes_evaluated": routes_evaluated,
        "final_selected_route": state.get("selected_route") if state.get("routing_decision") == "OPTIMAL_PATH_FOUND" else {},
        "queried_warehouse_metrics": state.get("warehouse_db_context") if state.get("selected_route") else {},
        "graph_routing_metadata": {
            "loops_executed": state.get("current_route_index", 0),
            "final_decision_state": state.get("routing_decision"),
            "reroute_impact_score": state.get("reroute_impact_score", 0)
        },
        "final_operations_brief": state.get("final_report", {}).get("final_operations_brief", "")
    }

    # Ensure outputs directory exists
    os.makedirs("outputs", exist_ok=True)

    # Save to the main advisory report location
    advisory_path = "outputs/reroute_advisory_report.json"
    with open(advisory_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    # Save to incident-specific path if specified
    if output_filename:
        specific_path = f"outputs/{output_filename}"
        with open(specific_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

    return report





### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026