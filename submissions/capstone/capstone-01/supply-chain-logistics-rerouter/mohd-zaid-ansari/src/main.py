import argparse
import json
from pathlib import Path

from src.graph import compiled_graph


def load_sample_incident() -> dict:
    base_dir = Path(__file__).resolve().parent.parent
    sample_path = base_dir / "data" / "sample_incidents.json"
    with open(sample_path, "r", encoding="utf-8") as f:
        sample = json.load(f)

    if isinstance(sample, list):
        return sample[0] if sample else {}
    return sample if isinstance(sample, dict) else {}


def load_incident_from_file(incident_path: Path) -> dict:
    with open(incident_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    if isinstance(loaded, list):
        return loaded[0] if loaded else {}
    return loaded if isinstance(loaded, dict) else {}


def build_initial_state(incident: dict, *, incident_id_override: str | None = None) -> dict:
    incident_id = incident_id_override or incident.get("incident_id", "sample")

    return {
        "messages": [],
        "incident_id": incident_id,
        "final_report": {},
    }


def main():
    incident = load_sample_incident()
    state = build_initial_state(incident)
    final_state = compiled_graph.invoke(state)
    report = final_state.get("final_report")
    print(json.dumps(report, indent=2, default=str))


if __name__ == "__main__":
    main()

