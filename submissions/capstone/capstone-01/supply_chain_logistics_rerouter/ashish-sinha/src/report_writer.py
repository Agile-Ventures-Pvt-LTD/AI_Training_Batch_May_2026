import json
from pathlib import Path
from config import OUTPUT_DIR
from typing import Dict,Any,List

def build_report(incident_id: str,manifest_text: str,metadata: dict[str, Any],retrieved_rules: list[str],
    routes_evaluated: list[dict[str, Any]],selected_route: dict[str, Any],warehouse_metrics: dict[str, Any],
    loops_executed: int,final_decision: str,impact_score: int,original_summary: str,operations_brief: str,
) -> dict[str, Any]:
    parsed_metadata = {
        "shipment_id": metadata.get("shipment_id", ""),
        "target_warehouse_id": metadata.get("target_warehouse_id", ""),
        "cargo_weight_tons": metadata.get("cargo_weight_tons", 0),
        "cargo_type": metadata.get("cargo_type", ""),
        "has_perishables": metadata.get("has_perishables", False),
        "maximum_tolerable_delay_hours": metadata.get("maximum_tolerable_delay_hours"),
    }
    return {
        "incident_id": incident_id,
        "original_incident_summary": original_summary,
        "parsed_metadata": parsed_metadata,
        "rag_validation_rules_applied": retrieved_rules,
        "routes_evaluated": routes_evaluated,
        "final_selected_route": selected_route,
        "queried_warehouse_metrics": warehouse_metrics,
        "graph_routing_metadata": {
            "loops_executed": loops_executed,
            "final_decision_state": final_decision,
            "reroute_impact_score": impact_score,
        },
        "final_operations_brief": operations_brief,
    }

def save_report(report: dict[str, Any], incident_id: str) -> Path:
    filename = f"{incident_id}_reroute_advisory_report.json"
    filepath = OUTPUT_DIR / filename

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return filepath

def build_and_save_report(
    incident_id: str,
    manifest_text: str,
    metadata: dict[str, Any],
    retrieved_rules: list[str],
    routes_evaluated: list[dict[str, Any]],
    selected_route: dict[str, Any],
    warehouse_metrics: dict[str, Any],
    loops_executed: int,
    final_decision: str,
    impact_score: int,
    original_summary: str,
    operations_brief: str,
) -> dict[str, Any]:
    report = build_report(
        incident_id=incident_id,
        manifest_text=manifest_text,
        metadata=metadata,
        retrieved_rules=retrieved_rules,
        routes_evaluated=routes_evaluated,
        selected_route=selected_route,
        warehouse_metrics=warehouse_metrics,
        loops_executed=loops_executed,
        final_decision=final_decision,
        impact_score=impact_score,
        original_summary=original_summary,
        operations_brief=operations_brief,
    )
    save_report(report, incident_id)
    return report
