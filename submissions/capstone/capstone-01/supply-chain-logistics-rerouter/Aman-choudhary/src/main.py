import os 
import json
import logging
from pathlib import Path
from src.graph import build_graph
logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s",)
LOGGER = logging.getLogger(__name__)
DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")
def load_incidents() -> list:
    """
    Load trainer-provided incidents.
    """
    incident_file = DATA_DIR / "sample_incidents.json"
    with open(incident_file,"r",encoding="utf-8",) as file:
        return json.load(file)
def display_incidents(incidents: list[dict],) -> None:
    """
    Print incidents available for execution.
    """
    print("\nAvailable Incidents:\n")
    for index, incident in enumerate(incidents,start=1,):
        print(f"{index}. "f"{incident['incident_id']}")
    print()
def get_user_selection(incidents: list[dict],) -> dict:
    """
    Select incident from CLI.
    """
    while True:
        try:
            selected = int(input("Select incident: "))
            if 1 <= selected <= len(incidents):
                return incidents[selected - 1]
            print(f"Please choose between "f"1 and {len(incidents)}")
        except ValueError:
            print("Please enter a valid number.")
def save_report(incident_id: str,report: dict,)->str:
    """
    Save advisory report.
    """
    OUTPUT_DIR.mkdir(exist_ok=True,parents=True,)
    report_path = (OUTPUT_DIR/ f"{incident_id}_reroute_advisory_report.json")
    with open(report_path,"w",encoding="utf-8",) as file:
        json.dump(report,file,indent=4,ensure_ascii=False,)
    return str(report_path)
def build_initial_state(incident: dict,) -> dict:
    """
    Create initial LangGraph state.
    """
    return {"incident_id":incident["incident_id"],
        "manifest_text":incident["manifest_text"],
        "disrupted_port_id":incident["disrupted_port_id"],
        "extracted_metadata": {},
        "routing_rag_context": "",
        "available_routes": [],
        "current_route_index": 0,
        "selected_route": {},
        "warehouse_db_context": {},
        "reroute_impact_score": 0,
        "routing_decision": "",
        "clarification_attempts": 0,
        "max_clarification_attempts": 2,
        "logs": [],
        "evaluated_routes": [],
        "final_report": {},
        }
def run_workflow(incident: dict,)->dict:
    """
    Execute LangGraph workflow.
    """
    LOGGER.info("Starting incident %s",incident["incident_id"],)
    app = build_graph()
    initial_state = build_initial_state(incident)
    final_state = app.invoke(initial_state)
    LOGGER.info("Completed incident %s",incident["incident_id"],)
    return final_state
def print_summary(final_state: dict,) -> None:
    """
    Display concise execution summary.
    """
    report = final_state.get("final_report",{},)
    graph_metadata = report.get("graph_routing_metadata",{},)
    print("\n" + "=" * 60)
    print("summery")
    print("=" * 60)
    print(f"Incident ID: "f"{report.get('incident_id')}")
    print(f"Decision: "f"{graph_metadata.get('final_decision_state')}")
    print(f"Impact Score: "f"{graph_metadata.get('reroute_impact_score')}")
    print(f"Loops Executed: "f"{graph_metadata.get('loops_executed')}")
    print("\nOperations Brief:\n")
    print(report.get("final_operations_brief","No brief generated",))
    print("\n" + "=" * 60)
def main() -> None:
    """
    Application entry point.
    """
    try:
        incidents = load_incidents()
        display_incidents(incidents)
        selected_incident = (get_user_selection(incidents))
        final_state = run_workflow(selected_incident)
        report = final_state.get("final_report",{})
        report_path = save_report(selected_incident["incident_id"],report,)
        print_summary(final_state)
        print(f"\nReport saved to:\n"f"{report_path}")
    except Exception as exc:
        LOGGER.exception("Application failed")
        raise RuntimeError(f"Fatal application error: {exc}") from exc
if __name__ == "__main__":
    main()