from src.tools import calculate_score

def evaluate_candidate_scores(scores: dict) -> dict:
    """
    Evaluates and calculates candidate fitment score based on the 8 rubric categories.
    """
    return calculate_score(scores)

if __name__ == "__main__":
    test_scores = {
        "python_programming": 5,
        "sql_database_skills": 4,
        "api_integration": 4,
        "llm_application_development": 3,
        "agent_frameworks": 2,
        "rag_understanding": 3,
        "testing_and_quality": 3,
        "communication": 4
    }
    result = evaluate_candidate_scores(test_scores)
    print("Scoring evaluation test:", result)