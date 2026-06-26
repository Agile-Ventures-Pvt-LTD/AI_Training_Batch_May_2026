from typing import Any
from config import METADATA_PATH
from utils.file_loader import read_json
from crewai.tools import tool

@tool("Skill Matcher")
def skill_matcher(jd_skills: list[str], resume_skills: list[str]) -> dict[str, Any]:
    """
    Compares JD skills with candidate resume skills.

    Args:
        jd_skills (list[str]): skills in job description.
        resume_skills (list[str]): skills in resume.

    Returns:
        dict[str, Any]: Returns matched kills, partial skills, missing skills, and match percentage. Returns error message on failure.
    """

    try:
        synonym_path = METADATA_PATH / "skill_synonyms.json"
        synonyms = read_json(synonym_path)
        
        jd_set = {jd.lower().strip() for jd in jd_skills}
        resume_set = {skill.lower().strip() for skill in resume_skills}
        
        matched = []
        partial = []
        missing = []
        
        for jd_skill in jd_set:
            
            if jd_skill in resume_set:
                matched.append(jd_skill)
                continue
            
            synonym_found = False
            
            for key, values in synonyms.items():
                
                possible_matches = {key.lower(), *[value.lower() for value in values]}
                
                if jd_skill in possible_matches:
                    if resume_set.intersection(possible_matches):
                        partial.append(jd_skill)
                        synonym_found = True
                        break
            
            if not synonym_found:
                missing.append(jd_skill)
        
        total = len(jd_set)
        
        match_percentage = round(((len(matched) + 0.5 * len(partial)) / total) * 100, 2) if total else 0
        
        return {
            "matched_skills": matched,
            "partial_matches": partial,
            "missing_skills": missing,
            "match_percentage": match_percentage
        }

    except Exception as e:
        return {
            "message": str(e)
        }