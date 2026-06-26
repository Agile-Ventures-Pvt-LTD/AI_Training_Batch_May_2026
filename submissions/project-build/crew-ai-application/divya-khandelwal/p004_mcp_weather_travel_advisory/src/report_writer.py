import os
import json
from typing import Dict

def save_travel_advisory_tool(report: dict) -> dict:
    """Persists the finished analytical compilation into a standard JSON file location."""
    output_dir = os.getenv("OUTPUT_PATH", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, "travel_advisory_report.json")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        return {
            "success": True,
            "saved_path": "outputs/travel_advisory_report.json"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to save report file: {str(e)}"
        }
