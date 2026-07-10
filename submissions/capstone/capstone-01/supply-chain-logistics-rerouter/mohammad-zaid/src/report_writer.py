from pathlib import Path
import json

OUTPUT_DIR = Path("outputs")

def save_report(state: dict) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    report_path = (OUTPUT_DIR / f"{state['incident_id']}_reroute_advisory_report.json")

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(state["final_report"], f, indent=4, ensure_ascii=False,)

    return report_path