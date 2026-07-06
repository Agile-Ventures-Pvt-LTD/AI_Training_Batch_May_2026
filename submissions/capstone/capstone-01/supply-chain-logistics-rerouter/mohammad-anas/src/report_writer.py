import json
from pathlib import Path
from typing import Any, Dict


def write_report(incident_id: str, report: Dict[str, Any]) -> None:
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    file_path = output_dir / f"{incident_id}_reroute_advisory_report.json"

    try:
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
    except Exception as exc:
        raise RuntimeError(f"Failed to write report to {file_path}: {exc}")