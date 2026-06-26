import pytest

@pytest.mark.integration
def test_single_candidate_run_creates_json_report():
    from src.tools import read_job_description_tool, candidate_index_lookup_tool, read_resume_tool
    from src.scoring import score_candidate
    from src.output_writer import make_report
    from src.tools import save_report_tool

    jd = read_job_description_tool()
    assert jd["success"] is True

    lookup = candidate_index_lookup_tool("CAND-001")
    assert lookup["found"] is True

    resume = read_resume_tool(lookup["resume_file"])
    assert resume["success"] is True

    scores = score_candidate(resume["content"])
    assert scores["overall_score"] > 0

    jd_data = {"role_title": "AI Engineer"}
    profile = {
        "candidate_id": lookup["candidate_id"],
        "candidate_name": lookup["candidate_name"],
        "current_role": lookup["current_role"],
        "years_experience": lookup["years_experience"],
        "skills": []
    }
    interview = {
        "interview_focus_areas": ["Test"],
        "technical_questions": ["Q1", "Q2", "Q3"],
        "project_deep_dive_questions": ["Q4", "Q5"],
        "scenario_questions": ["Q6", "Q7"],
        "gap_validation_questions": ["Q8", "Q9"]
    }

    report = make_report(jd_data, profile, scores, interview)
    save_result = save_report_tool("CAND-001", report)
    assert save_result["success"] is True

    import os
    assert os.path.exists(save_result["file_path"])


@pytest.mark.integration
def test_invalid_candidate_id_returns_error():
    from src.tools import candidate_index_lookup_tool
    result = candidate_index_lookup_tool("INVALID-ID")
    assert result["found"] is False


@pytest.mark.integration
def test_tool_failure_handling():
    from src.tools import read_resume_tool
    result = read_resume_tool("nonexistent_file.md")
    assert result["success"] is False
    assert "not found" in result.get("error", "").lower() or "not found" in str(result)


@pytest.mark.integration
def test_full_pipeline_execution():
    from src.tools import read_job_description_tool, candidate_index_lookup_tool, read_resume_tool
    from src.scoring import score_candidate
    from src.tools import save_report_tool, validate_report_schema_tool
    from src.output_writer import make_report

    jd = read_job_description_tool()
    lookup = candidate_index_lookup_tool("CAND-002")
    resume = read_resume_tool(lookup["resume_file"])
    scores = score_candidate(resume["content"])

    profile = {
        "candidate_id": lookup["candidate_id"],
        "candidate_name": lookup["candidate_name"],
        "current_role": lookup["current_role"],
        "years_experience": lookup["years_experience"],
        "skills": []
    }
    jd_data = {"role_title": "AI Engineer"}
    interview = {
        "interview_focus_areas": ["Focus"],
        "technical_questions": ["Q1", "Q2", "Q3"],
        "project_deep_dive_questions": ["Q4", "Q5"],
        "scenario_questions": ["Q6", "Q7"],
        "gap_validation_questions": ["Q8", "Q9"]
    }

    report = make_report(jd_data, profile, scores, interview)
    validation = validate_report_schema_tool(report)
    assert validation["schema_valid"] is True

    save = save_report_tool("CAND-002", report)
    assert save["success"] is True