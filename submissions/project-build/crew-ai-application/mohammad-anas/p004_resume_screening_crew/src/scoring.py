CATEGORY_WEIGHTS = {
    "required_skills": 40,
    "preferred_skills": 15,
    "experience": 20,
    "projects": 15,
    "education": 10,
}


def calculate_score(category_scores: dict[str, int]) -> dict:
    overall = sum(category_scores.values())
    maximum = sum(CATEGORY_WEIGHTS.values())

    percentage = round((overall / maximum) * 100, 2)

    if percentage >= 85:
        recommendation = "Strong Hire"
    elif percentage >= 70:
        recommendation = "Hire"
    elif percentage >= 50:
        recommendation = "Borderline"
    else:
        recommendation = "Reject"

    return {
        "overall_score": overall,
        "max_score": maximum,
        "percentage": percentage,
        "recommendation": recommendation,
    }