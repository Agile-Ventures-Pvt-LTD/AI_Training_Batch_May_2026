import json

from crewai.tools import tool

import config


@tool("skill_matcher_tool")
def skill_matcher_tool(
    required_skills: list[str],
    candidate_skills: list[str],
) -> dict:
    """Match candidate skills."""

    try:
        synonym_path = (
            config.DATASET_PATH
            / "metadata"
            / "skill_synonyms.json"
        )

        with open(synonym_path, encoding="utf-8") as f:
            synonyms = json.load(f)

        required = {s.lower() for s in required_skills}
        candidate = {s.lower() for s in candidate_skills}

        matched = []
        partial = []
        missing = []

        for skill in required:
            if skill in candidate:
                matched.append(skill)
                continue

            found = False

            for synonym in synonyms.get(skill, []):
                if synonym.lower() in candidate:
                    partial.append(skill)
                    found = True
                    break

            if not found:
                missing.append(skill)

        return {
            "matched_skills": matched,
            "partial_matches": partial,
            "missing_skills": missing,
        }

    except Exception as e:
        return {"error": str(e)}