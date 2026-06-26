import json
from typing import Dict, List
from pathlib import Path
from crewai import Crew, Process
from src.agents import (
    create_jd_analyst_agent,
    create_resume_extraction_agent,
    create_skill_matching_agent,
    create_interview_planning_agent,
    create_final_recommendation_agent,
    create_gap_analysis_agent,
    create_report_review_agent
)
from src.tasks import (
    create_jd_analysis_task,
    create_resume_extraction_task,
    create_skill_matching_task,
    create_interview_planning_task,
    create_final_recommendation_task,
    create_gap_analysis_task,
    create_report_review_task
)
from src.tools import (
    read_job_description_tool,
    read_resume_tool,
    candidate_index_lookup_tool,
    save_report_tool
)


def screen_candidate(candidate_id: str) -> Dict:
    jd_result = read_job_description_tool()
    if not jd_result["success"]:
        return {"error": jd_result.get("error", "Failed to read job description")}

    lookup = candidate_index_lookup_tool(candidate_id)
    if not lookup["found"]:
        return {"error": lookup.get("message", "Candidate not found")}

    resume_result = read_resume_tool(lookup["resume_file"])
    if not resume_result["success"]:
        return {"error": resume_result.get("error", "Failed to read resume")}

    jd_text = jd_result["content"]
    resume_text = resume_result["content"]

    jd_analyst = create_jd_analyst_agent()
    resume_extractor = create_resume_extraction_agent()
    skill_matcher = create_skill_matching_agent()
    interview_planner = create_interview_planning_agent()
    final_recommender = create_final_recommendation_agent()
    gap_analyst = create_gap_analysis_agent()
    report_reviewer = create_report_review_agent()

    jd_task = create_jd_analysis_task(jd_analyst, jd_text)
    resume_task = create_resume_extraction_task(resume_extractor, resume_text, candidate_id, lookup["candidate_name"])
    skill_task = create_skill_matching_task(skill_matcher, "{{jd_task.output}}", "{{resume_task.output}}", "")
    interview_task = create_interview_planning_task(interview_planner, "{{jd_task.output}}", "{{resume_task.output}}", "{{skill_task.output}}")
    final_task = create_final_recommendation_task(final_recommender, "{{jd_task.output}}", "{{resume_task.output}}", "{{skill_task.output}}", "{{interview_task.output}}")
    gap_task = create_gap_analysis_task(gap_analyst, "{{jd_task.output}}", "{{resume_task.output}}", "{{skill_task.output}}")
    review_task = create_report_review_task(report_reviewer, "{{final_task.output}}")

    crew = Crew(
        agents=[jd_analyst, resume_extractor, skill_matcher, interview_planner, final_recommender, gap_analyst, report_reviewer],
        tasks=[jd_task, resume_task, skill_task, interview_task, final_task, gap_task, review_task],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()

    report_data = {"result": str(result)}
    try:
        if hasattr(result, "raw"):
            report_data = json.loads(result.raw)
    except (json.JSONDecodeError, TypeError):
        pass

    file_path = save_report_tool(candidate_id, report_data)
    return {
        "candidate_id": candidate_id,
        "report_json": file_path.get("file_path", ""),
        "status": "completed"
    }


def run_sample_screening() -> List[Dict]:
    results = []
    for cid in ["CAND-001", "CAND-002", "CAND-003"]:
        results.append(screen_candidate(cid))
    return results


def run_all_screening() -> List[Dict]:
    results = []
    for cid in ["CAND-001", "CAND-002", "CAND-003", "CAND-004", "CAND-005"]:
        results.append(screen_candidate(cid))
    return results