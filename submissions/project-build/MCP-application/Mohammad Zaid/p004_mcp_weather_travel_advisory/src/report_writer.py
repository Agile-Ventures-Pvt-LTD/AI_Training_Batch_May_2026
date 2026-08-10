# src/report_writer.py
import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / os.getenv("OUTPUT_PATH", "outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def save_advisory_report(report_data: dict) -> str:
    file_path = OUTPUT_DIR / "travel_advisory_report.json"
    with open(file_path, "w") as f:
        json.dump(report_data, f, indent=2)
    return str(file_path)