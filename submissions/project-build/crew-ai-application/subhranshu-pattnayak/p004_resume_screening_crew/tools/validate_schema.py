from typing import Any
from pydantic import ValidationError
from schemas import FinalReport
from crewai.tools import tool

@tool("Validate Report Schema")
def validate_schema(report: dict[str, Any]) -> dict[str, Any]:
    """Validates that the final report contains all required fields.

    Args:
        report (dict[str, Any]): Candidate Report

    Returns:
        dict[str, Any]: Valid Schema message or Validation error message.
    """
    try:
        FinalReport.model_validate(report)
        return {
            "schema_valid": True,
            "missing_fields": []
        }
    
    except ValidationError as e:
        
        missing_fields = []
        for error in e.errors():
            if error.get("loc"):
                missing_fields.append(".".join(map(str, error["loc"])))
        
        return {
            "schema_valid": False,
            "missing_fields": missing_fields
        }