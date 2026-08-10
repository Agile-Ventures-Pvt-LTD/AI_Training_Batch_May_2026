from tools.scoring_tools import score_calculator_tool


def test_score():
    result = score_calculator_tool.run(
        category_scores={
            "required_skills": 35,
            "preferred_skills": 10,
            "experience": 15,
            "projects": 10,
            "education": 10,
        }
    )

    assert result["overall_score"] > 0