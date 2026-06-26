from pathlib import Path
from utils.file_loader import read_csv
from typing import Any
from config import METADATA_PATH
from crewai.tools import tool

@tool("Candidate Lookup")
def candidate_lookup(candidate_id: str) -> dict[str, Any]:
    """Finds the resume file for a candidate ID.

    Args:
        candidate_id (str): candidate id of the candidate

    Returns:
        dict[str, Any]: Returns found status. Along with candidate file on successful execution. And Invalid id message or error message on failure.
    """
    try:
        index_path = METADATA_PATH / "candidate_index.csv"
        index = read_csv(index_path)
        
        candidate = None
        for i in index:
            if i["candidate_id"] == candidate_id:
                candidate = i
                break
        
        if candidate:
            return {
                "found": True,
                "candidate_id": candidate["candidate_id"],
                "candidate_name": candidate["candidate_name"],
                "resume_file": candidate["resume_file"]
            }
        else:
            return {
                "found": False,
                "message": f"Candidate ID {candidate_id} not found."
            }
    except Exception as e:
        return {
            "found": False,
            "message": str(e)
        }