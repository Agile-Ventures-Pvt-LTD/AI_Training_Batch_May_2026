from utils.file_loader import read_json
from typing import Any
from config import METADATA_PATH
from crewai.tools import tool

@tool("Load Screening Rubric")
def load_rubric() -> dict[str, Any]:
    """Loads the scoring rubric

    Returns:
        dict[str, Any]: Returns categories, score range and max score. Returns Error Message on failed execution.
    """
    try:
        rubric_path = METADATA_PATH / "screening_rubric.json"
        rubric = read_json(rubric_path)
        if not isinstance(rubric, dict):
            return {
                "message": "Error: Rubric file is empty or invalid."
            }
        return {
            "categories": list(rubric.get("categories", {}).keys()),
            "score_range": rubric.get("score_range", {}).get("description"),
            "max_score": rubric.get("max_score", 40)
        }
    except Exception as e:
        return {
            "message": str(e)
        }