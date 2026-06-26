import os
import json
from typing import Dict, List, Tuple
from config import DATASET_PATH

def load_rubric() -> Dict:
    """Loads the screening rubric from the metadata folder."""
    rubric_path = os.path.join(DATASET_PATH, "metadata", "screening_rubric.json")
    if not os.path.exists(rubric_path):
        raise FileNotFoundError(f"Rubric file not found at {rubric_path}")
    with open(rubric_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_skill_synonyms() -> Dict[str, List[str]]:
    """Loads the skill synonym mapping."""
    synonyms_path = os.path.join(DATASET_PATH, "metadata", "skill_synonyms.json")
    if not os.path.exists(synonyms_path):
        return {}
    with open(synonyms_path, 'r', encoding='utf-8') as f:
        raw = json.load(f)
    return {k.strip(): v for k, v in raw.items()}

def match_skills(jd_skills: str, candidate_skills: str) -> Dict:
    """Compares JD skills with candidate skills using synonym mapping."""
    synonyms = load_skill_synonyms()
    jd_list = [s.strip().lower() for s in jd_skills.split(',') if s.strip()]
    cand_list = [s.strip().lower() for s in candidate_skills.split(',') if s.strip()]
    
    matched, partial, missing = [], [], []
    
    for jd_skill in jd_list:
        found = False
        alias_list = [jd_skill] + synonyms.get(jd_skill, [])
        for alias in alias_list:
            if alias in cand_list:
                matched.append(jd_skill)
                found = True
                break
        if not found:
            for c_skill in cand_list:
                if jd_skill in c_skill or c_skill in jd_skill:
                    partial.append(jd_skill)
                    found = True
                    break
        if not found:
            missing.append(jd_skill)
            
    match_pct = (len(matched) / len(jd_list) * 100) if jd_list else 0
    return {
        "matched_skills": matched,
        "partial_matches": partial,
        "missing_skills": missing,
        "match_percentage": round(match_pct, 2)
    }

def calculate_score(category_scores: Dict[str, int]) -> Dict:
    """Calculates overall score, percentage, and recommendation band."""
    overall_score = sum(category_scores.values())
    max_score = 40
    percentage = (overall_score / max_score) * 100
    
    if percentage >= 80: band = "STRONG_MATCH"
    elif percentage >= 60: band = "MODERATE_MATCH"
    elif percentage >= 40: band = "WEAK_MATCH"
    else: band = "NEEDS_MANUAL_REVIEW"
    
    return {
        "overall_score": overall_score,
        "max_score": max_score,
        "percentage": round(percentage, 2),
        "recommendation_band": band
    }