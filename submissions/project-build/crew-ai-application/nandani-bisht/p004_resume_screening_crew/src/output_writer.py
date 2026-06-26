import os
import json
from typing import Dict
from config import OUTPUT_PATH

REQUIRED_FIELDS = [
    "candidate_id", "candidate_name", "role_title", "overall_score",
    "max_score", "percentage", "recommendation", "executive_summary",
    "strengths", "gaps", "interview_focus_areas", "interview_questions",
    "evidence", "human_review_note"
]

def validate_schema(report_data: Dict) -> Dict:
    """Validates that the report contains all required fields."""
    if isinstance(report_data, str):
        try:
            report_data = json.loads(report_data)
        except json.JSONDecodeError:
            return {"schema_valid": False, "missing_fields": ["Invalid JSON format"]}
    
    missing = [f for f in REQUIRED_FIELDS if f not in report_data]
    return {"schema_valid": len(missing) == 0, "missing_fields": missing}

def save_report(candidate_id: str, report_data) -> Dict:
    """Persists the final JSON report to the outputs directory."""
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    filename = f"{candidate_id}_screening_report.json"
    filepath = os.path.join(OUTPUT_PATH, filename)
    
    try:
        data = json.loads(report_data) if isinstance(report_data, str) else report_data
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return {"success": True, "filepath": filepath}
    except Exception as e:
        return {"success": False, "error": str(e)}