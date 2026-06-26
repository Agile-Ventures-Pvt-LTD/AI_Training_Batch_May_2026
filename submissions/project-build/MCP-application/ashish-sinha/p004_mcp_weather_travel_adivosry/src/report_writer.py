import os
import json
from typing import Dict, Any

def save_travel_advisory_report(report_data: Dict[str, Any]) -> Dict[str, Any]:
    """Writes compiled telemetry reports to disk location cleanly."""
    output_dir = os.getenv("OUTPUT_PATH", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "travel_advisory_report.json")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        return {"success": True, "saved_path": file_path}
    except Exception as e:
        return {"success": False, "message": f"Failed writing report target: {str(e)}"}
