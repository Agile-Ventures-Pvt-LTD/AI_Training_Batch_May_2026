import json
from typing import Dict, List
from src.config import SCREENING_RUBRIC_PATH, SKILL_SYNONYMS_PATH


def load_rubric() -> Dict:
    with open(SCREENING_RUBRIC_PATH, "r") as f:
        return json.load(f)


def load_skill_synonyms() -> Dict[str, List[str]]:
    with open(SKILL_SYNONYMS_PATH, "r") as f:
        return json.load(f)


def get_recommendation_band(percentage: float) -> str:
    if percentage >= 80:
        return "STRONG_MATCH"
    elif percentage >= 60:
        return "MODERATE_MATCH"
    elif percentage >= 40:
        return "WEAK_MATCH"
    else:
        return "NEEDS_MANUAL_REVIEW"


def match_skills(jd_skills: List[str], resume_text: str) -> Dict:
    synonyms = load_skill_synonyms()
    resume_lower = resume_text.lower()
    matched = []
    missing = []

    for skill in jd_skills:
        skill_lower = skill.lower()
        found = False
        if skill_lower in resume_lower:
            found = True
        else:
            for category, aliases in synonyms.items():
                if skill_lower in category.replace("_", " ") or skill_lower in category:
                    if any(alias.lower() in resume_lower for alias in aliases):
                        found = True
                        break
        if found:
            matched.append(skill)
        else:
            missing.append(skill)

    total = len(jd_skills) if jd_skills else 1
    match_pct = round((len(matched) / total) * 100, 1)

    return {
        "matched_skills": matched,
        "partial_matches": [],
        "missing_skills": missing,
        "match_percentage": match_pct
    }


def score_candidate(resume_text: str) -> Dict:
    rubric = load_rubric()
    synonyms = load_skill_synonyms()
    categories = rubric["categories"]
    resume_lower = resume_text.lower()

    category_scores = {}
    for cat_key in categories:
        score = 0
        if cat_key in synonyms:
            for alias in synonyms[cat_key]:
                if alias.lower() in resume_lower:
                    score += 1
        score = min(score, 5)
        category_scores[cat_key] = score

    overall_score = sum(category_scores.values())
    max_score = rubric["max_score"]
    percentage = round((overall_score / max_score) * 100, 1)
    recommendation_band = get_recommendation_band(percentage)

    return {
        "category_scores": category_scores,
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": percentage,
        "recommendation_band": recommendation_band
    }


def calculate_scores_direct(category_scores: Dict[str, int]) -> Dict:
    rubric = load_rubric()
    overall_score = sum(category_scores.values())
    max_score = rubric["max_score"]
    percentage = round((overall_score / max_score) * 100, 1)
    recommendation_band = get_recommendation_band(percentage)

    return {
        "category_scores": category_scores,
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": percentage,
        "recommendation_band": recommendation_band
    }