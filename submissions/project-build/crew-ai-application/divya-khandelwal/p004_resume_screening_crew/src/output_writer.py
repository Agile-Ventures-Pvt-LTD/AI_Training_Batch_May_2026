# output_writer.py
import os
import json
from typing import Dict, Any

def parse_and_save_report(candidate_id: str, raw_data: Dict[str, Any], output_path: str):
    """
    Extracts JSON data from the crew output and saves it to a file.
    """
    os.makedirs(output_path, exist_ok=True)
    file_name = os.path.join(output_path, f"{candidate_id}_screening_report.json")
    
    if raw_data.get("json_dict"):
        parsed_json = raw_data["json_dict"]
    else:
        text = raw_data.get("raw", "").strip()
        text = text.replace("```json", "").replace("```", "").strip()
        parsed_json = json.loads(text)

    parsed_json["candidate_id"] = candidate_id

    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(parsed_json, file, indent=4)
        
    print(f"Saved report: {file_name}")
