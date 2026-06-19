import re


def evaluate_answer(question: str, result: dict, context: list):
    answer = result.get("answer", {})

    if isinstance(answer, dict):
        answer_text = answer.get("answer", "")
        sources = answer.get("sources", [])
    else:
        answer_text = str(answer)
        sources = result.get("sources", [])

    score = 0
    breakdown = {}

  
    grounding = 0
    if context and len(context) > 0:
        grounding = 2
    elif "policy" in answer_text.lower():
        grounding = 1
    breakdown["grounding"] = grounding
    score += grounding

  
    citation_score = 0
    if sources and len(sources) > 0:
        citation_score = 2
    elif re.search(r"chunk|policy|source", answer_text.lower()):
        citation_score = 1
    breakdown["citations"] = citation_score
    score += citation_score


    policy_match = 1.5 if len(context) >= 1 else 0
    breakdown["policy_match"] = policy_match
    score += policy_match

  
    clarity = 2 if len(answer_text) > 50 else 1
    breakdown["clarity"] = clarity
    score += clarity

    
    hallucination_penalty = 0

    if len(context) == 0 and "must" in answer_text.lower():
        hallucination_penalty = -2
    elif "definitely approved" in answer_text.lower():
        hallucination_penalty = -1

    breakdown["hallucination_penalty"] = hallucination_penalty
    score += hallucination_penalty

   
    final_score = max(0, min(10, score))

  
    if final_score >= 8:
        feedback = "Excellent grounding and policy adherence"
    elif final_score >= 6:
        feedback = "Good but minor improvements needed"
    elif final_score >= 4:
        feedback = "Weak grounding or missing citations"
    else:
        feedback = "Poor response - likely hallucinated or unsupported"

    return {
        "score": round(final_score, 2),
        "breakdown": breakdown,
        "feedback": feedback
    }