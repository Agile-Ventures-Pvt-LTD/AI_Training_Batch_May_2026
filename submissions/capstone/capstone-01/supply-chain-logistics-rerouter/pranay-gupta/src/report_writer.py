from src.config import OUTPUT_DIR, ensure_output_dir
from src.state import LogisticsIncidentState
from pathlib import Path

import json

def build_report(state: LogisticsIncidentState,operations_brief: str) -> dict:
    metadata = state.get("extracted_metadata",{})
    routes_evaluated = state.get("routes_evaluated",[])
    selected_route = state.get("selected_route",{})
    routing_decision = state.get("routing_decision","")
    warehouse = state.get("warehouse_db_context",{})
    impact_score = state.get("reroute_impact_score",0)
    manifest = state.get("manifest_text","")

    if routing_decision == "OPTIMAL_PATH_FOUND":
        final_route = selected_route
    else:
        final_route = {}

    loops_executed = max(0,len(routes_evaluated) - 1) if routes_evaluated else 0
     
    report = {
        "incident_id": state.get("incident_id",""),
        "original_incident_summary": manifest,
        "parsed_metadata": {
            "shipment_id": metadata.get("shipment_id",""),
            "target_warehouse_id": metadata.get("target_warehouse_id",""),
            "cargo_weight_tons": metadata.get("cargo_weight_tons",0),
            "cargo_type": metadata.get("cargo_type",""),
            "has_perishables": metadata.get("has_perishables", False),
            "maximum_tolerable_delay_hours": metadata.get("maximum_tolerable_delay_hours"),
        },
        "rag_validation_rules_applied": state.get("routing_rag_context","").split("\n\n"),
        "routes_evaluated": routes_evaluated,
        "final_selected_route": final_route,
        "queried_warehouse_metrics": warehouse,
        "graph_routing_metadata": {
            "loops_executed": loops_executed,
            "final_decision_state": routing_decision,
            "reroute_impact_score": impact_score
        },
        "final_operations_brief": operations_brief
    }

    return report

def save_report(report:dict,incident_id:str)->str:
    ensure_output_dir()
    incident_filename = f"{incident_id}_reroute_advisory_report.json"
    output_path = Path(OUTPUT_DIR)
    incident_filepath = output_path / incident_filename

    with open(incident_filepath,"w",encoding="utf-8")as handle:
        json.dump(report,handle,indent=2,ensure_ascii=False)

    general_filepath = output_path / "reroute_advisory_report.json"
    with open(general_filepath,"w",encoding="utf-8") as data:
        json.dump(report,data,indent=2,ensure_ascii=False)

    return str(incident_filepath)
