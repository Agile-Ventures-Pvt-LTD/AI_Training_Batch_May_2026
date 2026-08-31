import pytest
from src.schemas import (
    ScreeningRubricOutput,
    ScoreCalculatorOutput,
)
from src.tools import (
    load_screening_rubric_tool,
    score_calculator_tool,
)


def test_load_screening_rubric_tool():
    result = load_screening_rubric_tool()

    assert isinstance(result, ScreeningRubricOutput)

    assert result.content != "" or result.error != ""


def test_score_calculator_tool():
    result = score_calculator_tool()

    assert isinstance(result, ScoreCalculatorOutput)

    assert result.content != "" or result.error != ""