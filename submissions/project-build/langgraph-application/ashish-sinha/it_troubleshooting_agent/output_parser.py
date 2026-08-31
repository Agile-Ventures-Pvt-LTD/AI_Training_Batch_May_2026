import json
import re
from typing import Dict, Any

def clean_and_parse_json(raw_text: str) -> Dict[str, Any]:
    if not raw_text:
        return {}
    try:
        match = re.search(r"(\{.*\})", raw_text.strip(), re.DOTALL)
        json_str = match.group(1) if match else raw_text.strip()
        json_str = re.sub(r"^```(?:json)?\s*|\s*```$", "", json_str, flags=re.IGNORECASE)
        return json.loads(json_str.strip())
    except Exception:
        return {}

def parse_classification_output(raw_output: str) -> Dict[str, Any]:
    data = clean_and_parse_json(raw_output)
    return {
        "issue_type": str(data.get("issue_type", "UNKNOWN")).upper(),
        "confidence": str(data.get("confidence", "LOW")).upper(),
        "requires_clarification": bool(data.get("requires_clarification", True)),
        "reasoning_summary": str(data.get("reasoning_summary", "Parsing failed."))
    }

def parse_resolution_plan(raw_output: str) -> Dict[str, Any]:
    data = clean_and_parse_json(raw_output)
    return {
        "diagnosis_summary": str(data.get("diagnosis_summary", "System error processing data.")),
        "recommended_steps": list(data.get("recommended_steps", ["Please contact IT support directly."])),
        "escalation_required": bool(data.get("escalation_required", False)),
        "escalation_group": str(data.get("escalation_group", "Workplace IT")),
        "safety_notes": list(data.get("safety_notes", ["Unable to verify safety metrics."]))
    }

def parse_safety_review(raw_output: str) -> Dict[str, Any]:
    data = clean_and_parse_json(raw_output)
    return {
        "unsafe_content_detected": bool(data.get("unsafe_content_detected", True)),
        "violations_found": list(data.get("violations_found", ["Parsing failure during audit."])),
        "safe_alternative_plan": data.get("safe_alternative_plan", None)
    }
