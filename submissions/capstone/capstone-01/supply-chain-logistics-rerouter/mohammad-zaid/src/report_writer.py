from pathlib import Path
import json

def save_report(report: dict, incident_id: str):

    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / f"{incident_id}_reroute_advisory_report.json"

    with open(output_file, "w") as f:
        json.dump(report, f, indent=4)

    return output_file