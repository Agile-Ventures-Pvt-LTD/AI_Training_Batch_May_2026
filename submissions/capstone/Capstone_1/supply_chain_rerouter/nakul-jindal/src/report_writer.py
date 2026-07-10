import json
import os

def build_report(state: dict, operations_brief: str) -> dict:
    metadata = state["extracted_metadata"]
    return {
        "incident_id": state["incident_id"],
        "original_incident_summary": state["manifest_text"][:200],
        "parsed_metadata": metadata,
        "rag_validation_rules_applied": state["routing_rag_context"],
        "routes_evaluated": state["evaluated_routes"],
        "final_selected_route": state["selected_route"],
        "queried_warehouse_metrics": state["warehouse_db_context"],
        "graph_routing_metadata": {
            "loops_executed": state["clarification_attempts"],
            "final_decision_state": state["routing_decision"],
            "reroute_impact_score": state["reroute_impact_score"],
        },
        "final_operations_brief": operations_brief,
    }

def save_report(report: dict, incident_id: str):
    os.makedirs("outputs", exist_ok=True)
    path = f"outputs/{incident_id}_reroute_advisory_report.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    return path
