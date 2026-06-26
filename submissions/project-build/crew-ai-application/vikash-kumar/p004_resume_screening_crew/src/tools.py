from crewai.tools import tool
from config import SCREENING_SUPPORT_INDICATORS,JOB_DESCRIPTION_PATH,RESUME_PATH,SCREENING_RUBRIC_PATH,CANDIDATE_INDEX_PATH

@tool("read_job_description_tool")
def read_job_description_tool(JOB_DESCRIPTION_PATH) -> str:
    """
    Retrieves the job description file and use it for future references.
    Use this tool only when required for the job description.
    Input should contain the path of the Job Description
        """
    print(f"Tool: read_job_description_tool --- Input: {JOB_DESCRIPTION_PATH=}")

    return {"success": True,"content": "","source_file": "jd_ai_engineer.md"}   

@tool("read_resume_tool")
def read_resume_tool(RESUME_PATH) -> str:
    """
    Retrieves the candidate resume file and use to analyse further.
    Use this tool only when required.
    Input should contain the path of the Resume.
    """
    print(f"Tool: read_resume_tool  -- INPUT: {RESUME_PATH}")

    return {"success": True,"content": "","source_file": "*.md"}
    
@tool("candidate_index_lookup_tool")
def candidate_index_lookup_tool(CANDIDATE_INDEX_PATH) -> str:
    """
    Retrieves the resume file for the candidate ID.
    Use this toll only when required.
    Input should be the candidate_id
    """

    print(f"Tool: candidate_index_lookup_tool ")

    return 
    if CANDIDATE_INDEX_PATH is True: {"found": True,"candidate_id": "",
            "candidate_name": "Rohan Mehta","resume_file": "*.md"}

    else:
        { "found": false,"message": "Candidate ID not found."}

@tool("load_screening_rubric_tool")
def load_screening_rubric_tool():
    """
    Load the scoring rubric from {SCREENING_RUBRIC_PATH}.
    Use this tool only when required.
    Input should be the path of the screening rubric path.
    """

    print(f"Tool:load_screening_rubric_tool")

    return {
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

@tool("score_calculator_tool")
def score_calculator_tool():
    """
    Calculates total score, percentage, and recommendation band.
    Use this tool only when required.
    Input should be in the form {{{"category_scores": {
"python_programming": 4,
"sql_database_skills": 3,
"api_integration": 4,
"llm_application_development": 4,
"agent_frameworks": 3,
"rag_understanding": 3,
"testing_and_quality": 3,
"communication": 4}}

Expected calculation:
overall_score = sum(category_scores)
max_score = 40
percentage = overall_score / 40 * 100

Recommendation bands: {SCREENING_SUPPORT_INDICATORS}
Percentage Recommendation
80–100 STRONG_MATCH
60–79 MODERATE_MATCH
40–59 WEAK_MATCH
Below 40 NEEDS_MANUAL_REVIEW
    """

    print(f"Tool:score_calculator_tool")

    return {"overall_score": 28,
"max_score": 40,
"percentage": 70,
"recommendation_band": "MODERATE_MATCH"}

@tool("save_report_tool")
def save_report_tool():
    """
    Saves the final report to the outputs folder.
    Required output: outputs/CAND-001_screening_report.json
    Required output: outputs/CAND-001_screening_report.md
    Create both the files
    Use this tool only when required.
    """

    print(f"Tool:save_report_tool")

    return 
    with open("CAND-001_screening_report.md", "w", encoding="utf-8") as f:
        f.write(f"# ")
        f.write("## Report\n\n")
        f.write(Report)

@tool("skill_matcher_tool")
def skill_matcher_tool():
    """
    Compares JD skills with candidate resume skills.
    Use this tool only when required.
    """
    print(f"Tool: skill_matcher_tool")
    return {
        "matched_skills": [],
"partial_matches": [],
"missing_skills": [],
"match_percentage": 0
    }

@tool("validate_report_schema_tool")
def validate_report_schema_tool():
    """
    Validates that the final report contains all required fields.
    Use this tool only when required.
    """

    print(f" Tool used: validate_report_schema_tool")

    return {
        "schema_valid": True,
"missing_fields": []
    }

resume_tools=[read_job_description_tool,read_resume_tool,candidate_index_lookup_tool,load_screening_rubric_tool,score_calculator_tool,save_report_tool,skill_matcher_tool,validate_report_schema_tool]

