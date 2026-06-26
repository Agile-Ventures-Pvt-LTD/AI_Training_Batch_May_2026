import json

from crewai.tools import tool

import config
from scoring import calculate_score


@tool("load_screening_rubric_tool")
def load_screening_rubric_tool() -> dict:
    """Load the screening rubric."""

    try:
        rubric_path = (
            config.DATASET_PATH
            / "metadata"
            / "screening_rubric.json"
        )

        with open(rubric_path, encoding="utf-8") as f:
            return json.load(f)

    except Exception as e:
        return {"error": str(e)}


@tool("score_calculator_tool")
def score_calculator_tool(
    category_scores: dict,
) -> dict:
    """Calculate the candidate score."""

    return calculate_score(category_scores)