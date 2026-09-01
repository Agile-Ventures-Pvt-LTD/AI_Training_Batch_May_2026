from src.tools import (
    read_job_description_tool,
    read_resume_tool,
    skill_matcher_tool,
    validate_report_schema_tool
)

def test_read_job_description_tool_success():
    result = read_job_description_tool.func("job_description/jd_ai_engineer.md")
    assert result["success"] is True
    assert "AI Engineer" in result["content"]
    assert result["source_file"] == "jd_ai_engineer.md"

def test_read_resume_tool_success():
    result = read_resume_tool.func("resumes/candidate_001_rohan_mehta.md")
    assert result["success"] is True
    assert "Rohan Mehta" in result["content"]
    assert result["source_file"] == "candidate_001_rohan_mehta.md"

def test_skill_matcher_identifies_missing_skills():
    jd_skills = ["Python", "C++", "Rust", "SQL"]
    candidate_skills = ["Python", "SQL", "Java"]
    
    result = skill_matcher_tool.func(jd_skills, candidate_skills)
    assert "Python" in result["matched_skills"]
    assert "SQL" in result["matched_skills"]
    assert "C++" in result["missing_skills"]
    assert "Rust" in result["missing_skills"]
    assert result["match_percentage"] == 50.0

def test_validate_report_schema_tool_valid():
    valid_report = {
        "candidate_id": "CAND-001",
        "candidate_name": "Rohan Mehta",
        "role_title": "AI Engineer",
        "overall_score": 30,
        "max_score": 40,
        "percentage": 75.0,
        "recommendation": "MODERATE_MATCH",
        "executive_summary": "Rohan matches.",
        "strengths": ["Python"],
        "gaps": ["None"],
        "interview_focus_areas": ["RAG"],
        "interview_questions": {
            "technical_questions": ["Q1"],
            "project_deep_dive_questions": ["Q2"],
            "scenario_questions": ["Q3"],
            "gap_validation_questions": ["Q4"]
        }
    }
    result = validate_report_schema_tool.func(valid_report)
    assert result["schema_valid"] is True
    assert len(result["missing_fields"]) == 0

