from tools import score_calculator_tool


def default_category_scores(matched_skills, missing_skills):
    """
    Basic logic:
    - More matched skills → higher score
    - Missing skills → lower score
    """

    base_score = 3

    category_scores = {
        "python_programming": base_score,
        "sql_database_skills": base_score,
        "api_integration": base_score,
        "llm_application_development": base_score,
        "agent_frameworks": base_score,
        "rag_understanding": base_score,
        "testing_and_quality": base_score,
        "communication": base_score
    }

    # simple adjustment
    for skill in matched_skills:
        for key in category_scores:
            if key.split("_")[0] in skill.lower():
                category_scores[key] = min(5, category_scores[key] + 1)

    for skill in missing_skills:
        for key in category_scores:
            if key.split("_")[0] in skill.lower():
                category_scores[key] = max(0, category_scores[key] - 1)

    return category_scores


def calculate_final_score(category_scores):
    return score_calculator_tool(category_scores)