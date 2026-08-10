from typing import Any
from config import OUTPUT_DIR
from utils.file_loader import write_json
from crewai.tools import tool

@tool("Save Report")
def save_report(candidate_id: str, report: dict[str, Any]) -> dict[str, Any]:
    """Saves the final report to the outputs/ folder.

    Args:
        candidate_id (str): Candidate ID
        report (dict[str, Any]): Candidate Report

    Returns:
        dict[str, Any]: Success Message or Error Message.
    """
    try:
        output_path = OUTPUT_DIR / f"{candidate_id}_screening_report.json"

        write_json(output_path, report)

        return {
            "success": True,
            "output_file": str(output_path)
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }