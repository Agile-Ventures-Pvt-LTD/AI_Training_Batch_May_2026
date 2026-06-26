from tools import score_calculator_tool

def evaluation(user_input) -> float:
    max_score = 40
    score = sum(user_input)
    percentage = score / max_score * 100
    return {"overall_score": score,
"max_score": max_score,
"percentage": percentage,
"recommendation_band": "MODERATE_MATCH"}