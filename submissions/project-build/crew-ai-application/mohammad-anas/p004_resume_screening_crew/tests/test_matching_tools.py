from tools.matching_tools import skill_matcher_tool


def test_skill_match():
    result = skill_matcher_tool.run(
        required_skills=[
            "Python",
            "SQL",
        ],
        candidate_skills=[
            "Python",
            "Machine Learning",
            "SQL",
        ],
    )

    assert "python" in result["matched_skills"]