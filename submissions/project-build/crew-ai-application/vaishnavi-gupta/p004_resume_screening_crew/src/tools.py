from crewai_tools import tools
  

@tool("Reads the job description file")
def read_job_description(jd_ai_enginerr: str):

    with open(jd_ai_enginerr, "r", encoding="utf-8") as f:
        return f.read(
                "success": True,
                "content": "",
                "source_file": "jd_ai_engineer.md")


@tool("Reads a candidate resume file")
def read_resume(candidate_001_rohan_mehta : str):

    with open(candidate_001_rohan_mehta, "r", encoding="utf-8") as f:
        return f.read(
            "success": True,
            "content": "",
            "source_file": "candidate_001_rohan_mehta.md"
        )


@tool("Finds the resume file for a candidate ID.")
def candidate_index_lookup(
    Input:{
        candidate_id: "CAND-001"
}
):
    with open(candidate_index, "r", encoding="utf-8") as f:
        return f.read(
            "found": true,
            "candidate_id": "CAND-001",
            "candidate_name": "Rohan Mehta",
            "resume_file": "candidate_001_rohan_mehta.md"
        )
        if not valid:
            {
                 "found": false,
                 "message": "Candidate ID not found."
            }

@tool("Loads the scoring rubric from")
def load_screening_rubric(screening_rubric : str):
    with open(screening_rubric, "r", encoding="utf-8") as f:
        return f.read(
            {
                "categories": [
                "python_programming",
                "sql_database_skills",
                "api_integration",
                "llm_application_development",
                "agent_frameworks",
                "rag_understanding",
                "testing_and_quality",
                "communication"
 ],
 "score_range": "0 to 5",
 "max_score": 40
            }
        )


@tool("Calculates total score, percentage, and recommendation band.")
def score_calculator({

    "category_scores": {
    "python_programming": 4,
    "sql_database_skills": 3,
    "api_integration": 4,
    "llm_application_development": 4,
    "agent_frameworks": 3,
    "rag_understanding": 3,
    "testing_and_quality": 3,
    "communication": 4}):
    """
    Expected calculation:
    overall_score = sum(category_scores)
    max_score = 40
    percentage = overall_score / 40 * 100
    Recommendation bands:
    Percentage Recommendation
    80–100 STRONG_MATCH
    60–79 MODERATE_MATCH
    Percentage Recommendation
    40–59 WEAK_MATCH
    Below 40 NEEDS_MANUAL_REVIEW
    """
    with open(screening_rubric, "r", encoding="utf-8") as f:
        return f.read(
            {
                "overall_score": 28,
                "max_score": 40,
                "percentage": 70,
                "recommendation_band": "MODERATE_MATCH"

            }
        )

@tool("Saves the final report to the outputs/ folder")
def save_report():
with open(candidate_001_rohan_mehta, "w", encoding="utf-8") as f:
        return f.read(
            "success": True,
            "content": "",
            "source_file": "candidate_001_rohan_mehta.md"
        )
  
TOOLS = [
    read_job_description,
    read_resume,
    candidate_screening_lookup,
    load_screening_rubric,
    score_calculator,
    save_report_tool
]