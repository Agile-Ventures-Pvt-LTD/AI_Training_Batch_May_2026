import json

from crewai.tools import tool

from output_writer import (
    save_json,
    save_markdown,
)
from schemas import CandidateScreeningReport


@tool("save_report_tool")
def save_report_tool(
    report: dict,
    candidate_id: str,
) -> str:
    """Save the final report."""

    save_json(report, candidate_id)
    save_markdown(report, candidate_id)

    return "Report saved."


@tool("validate_report_schema_tool")
def validate_report_schema_tool(
    report: dict,
) -> bool:
    """Validate report schema."""

    try:
        CandidateScreeningReport.model_validate(report)
        return True
    except Exception:
        return False