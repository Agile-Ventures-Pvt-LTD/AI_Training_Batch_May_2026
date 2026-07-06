import os
import json
from langchain_core.prompts import ChatPromptTemplate
from src.state import LogisticsIncidentState
from src.nodes import llm

def generate_report(state: LogisticsIncidentState) -> dict:
    prompt_template = ChatPromptTemplate.from_template(
        "You are the expert opearational manager and write brief for cargo organisation \n"
        "Draft short and concise summary explaining the incident resoulution details based on: "
        "Raw Incident Text: {manifest} \n"
        "Final Decision: {decision} \n"
        "Governance RAG Parameters: {rag} \n"
        "Selected Alternative Route Profile: {route}\n"
        "Target Storage Facility Status: {warehouse_context} \n" )
    
    chain = prompt_template | llm
    brief_res = chain.invoke({"manifest": state["manifest_text"],"decision": state["routing_decision"],
        "rag": state["routing_rag_context"],"route": json.dumps(state["selected_route"]),"warehouse_context": json.dumps(state["warehouse_db_context"])})
    
    report_data = {"incident_id": state["incident_id"],"original_incident_summary": state["manifest_text"][:160] + "...",
        "parsed_metadata": state["extracted_metadata"],"rag_validation_rules_applied": [state["routing_rag_context"]],
        "routes_evaluated": state["logs"],"final_selected_route": state["selected_route"] if state["selected_route"] else {},
        "queried_warehouse_metrics": state["warehouse_db_context"] if state["warehouse_db_context"] else {},
        "graph_routing_metadata": {"loops_executed": state.get("clarification_attempts", 0),"final_decision_state": state["routing_decision"],"reroute_impact_score": state["reroute_impact_score"]},"final_operations_brief": brief_res.content.strip()}
    
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, "reroute_advisory_report.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    return {"final_report": report_data}
