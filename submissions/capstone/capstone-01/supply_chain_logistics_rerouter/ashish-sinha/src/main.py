import json
import logging
import sys

from config import SAMPLE_INCIDENTS_PATH,GROQ_API_KEY,GROQ_MODEL
from langchain_groq import ChatGroq
from nodes import llm
from rag import RAG_Retrieve
from graph import build_graph
from state import create_initial_state

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_incidents() -> list[dict]:
    with open(SAMPLE_INCIDENTS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def display_incidents(incidents: list[dict]) -> None:
    print("\nAvailable Incidents:")
    for idx, incident in enumerate(incidents, 1):
        print(f"  {idx}. {incident['incident_id']}")
    print(f"  {len(incidents) + 1}. Run all incidents")
    print()


def get_user_choice(incidents: list[dict]) -> int:
    while True:
        try:
            choice = int(input("Select incident: "))
            if 1 <= choice <= len(incidents) + 1:
                return choice
            print(f"Please enter a number between 1 and {len(incidents) + 1}")
        except ValueError:
            print("Please enter a valid number")
        except EOFError:
            return 1


def run_incident(incident: dict, app) -> dict:
    incident_id = incident["incident_id"]
    logger.info("Running incident %s", incident_id)

    initial_state = create_initial_state(
        incident_id=incident_id,
        manifest_text=incident["manifest_text"],
        disrupted_port_id=incident["disrupted_port_id"],
    )

    final_state = app.invoke(initial_state)
    report = final_state.get("final_report", {})

    print(f"\n{'=' * 60}")
    print(f"Incident: {incident_id}")
    print(f"{'=' * 60}")
    print(f"Decision: {report.get('graph_routing_metadata', {}).get('final_decision_state', 'UNKNOWN')}")
    print(f"Routes Checked: {len(report.get('routes_evaluated', []))}")
    print(f"Loops Executed: {report.get('graph_routing_metadata', {}).get('loops_executed', 0)}")
    print(f"Impact Score: {report.get('graph_routing_metadata', {}).get('reroute_impact_score', 0)}")
    print(f"\nOperations Brief:\n{report.get('final_operations_brief', '')}")
    print(f"\nReport saved to: outputs/{incident_id}_reroute_advisory_report.json")
    print()

    return final_state


def main():
    incidents = load_incidents()
    display_incidents(incidents)
    choice = get_user_choice(incidents)
    llm = ChatGroq(model=GROQ_MODEL,api_key=GROQ_API_KEY,temperature=0)
    rag=RAG_Retrieve

    logger.info("Building LangGraph workflow...")
    app = build_graph(llm,rag)
    logger.info("Workflow ready.")

    if choice == len(incidents) + 1:
        for incident in incidents:
            run_incident(incident, app)
    else:
        incident = incidents[choice - 1]
        run_incident(incident, app)


if __name__ == "__main__":
    main()