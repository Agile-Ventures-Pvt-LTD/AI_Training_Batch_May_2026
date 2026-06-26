from crewai import Task
from agents import (job_description_analyst_agent,resume_extraction_agent,skill_matching_agent,gap_analysis_agent,interview_planning_agent,final_recommendation_agent,report_review_agent,)
jd_analysis_task = Task(description="""
Analyze the AI Engineer job description.
Extract:
1 role_title
2 required_skills
3 preferred_skills
4 responsibilities
5 experience_expectation
6 evaluation_criteria
Return output as structured JSON.
""",
    expected_output="""
{
    "role_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": [],
    "experience_expectation": "",
    "evaluation_criteria": []
}
""",agent=job_description_analyst_agent,)
resume_extraction_task = Task(description="""
Read and analyze candidate resume.
Extract:
1 candidate_id
2 candidate_name
3 current_role
4 years_experience
5 skills
6 projects
7 experience_summary
8 education
9 certifications
Return structured candidate profile.
""",
    expected_output="""
{
    "candidate_id": "",
    "candidate_name": "",
    "current_role": "",
    "years_experience": "",
    "skills": [],
    "projects": [],
    "experience_summary": [],
    "education": [],
    "certifications": []
}
""",agent=resume_extraction_agent,)
skill_matching_task = Task(description="""
Compare candidate profile with job requirements.
Tasks:
1. Identify matched skills.
2. Identify partial matches.
3. Identify missing skills.
4. Score all 8 rubric categories.
5. Calculate total score.
6. Calculate recommendation band.
Recommendation Bands:
80-100  = STRONG_MATCH
60-79   = MODERATE_MATCH
40-59   = WEAK_MATCH
Below40 = NEEDS_MANUAL_REVIEW
""",
    expected_output="""
{
    "matched_skills": [],
    "partial_matches": [],
    "missing_skills": [],
    "category_scores": {
        "python_programming": 0,
        "sql_database_skills": 0,
        "api_integration": 0,
        "llm_application_development": 0,
        "agent_frameworks": 0,
        "rag_understanding": 0,
        "testing_and_quality": 0,
        "communication": 0
    },
    "overall_score": 0,
    "max_score": 40,
    "percentage": 0,
    "recommendation_band": ""
}
""",agent=skill_matching_agent,)

gap_analysis_task = Task(description="""
Identify candidate gaps.
Find:
- critical_gaps
- moderate_gaps
- areas_to_probe
Use evidence from resume and scoring results.
""",
    expected_output="""
{
    "critical_gaps": [],
    "moderate_gaps": [],
    "areas_to_probe": []
}
""",agent=gap_analysis_agent,)
interview_planning_task = Task(description="""
Generate candidate-specific interview questions.
Requirements:
Minimum:
- 3 technical questions
- 2 project deep dive questions
- 2 scenario questions
- 2 gap validation questions
Questions must align with:
- Job Description
- Candidate Resume
- Skill Gaps
""",
    expected_output="""
{
    "interview_focus_areas": [],
    "technical_questions": [],
    "project_deep_dive_questions": [],
    "scenario_questions": [],
    "gap_validation_questions": []
}
""",agent=interview_planning_agent,)
final_recommendation_task = Task(description="""
Generate final candidate screening report.
Must include:
- Executive summary
- Strengths
- Gaps
- Evidence
- Recommendation
Recommendation can only be:
STRONG_MATCH
MODERATE_MATCH
WEAK_MATCH
NEEDS_MANUAL_REVIEW
Report must be valid JSON.
""",
    expected_output="""
{
    "candidate_id": "",
    "candidate_name": "",
    "role_title": "",
    "overall_score": 0,
    "max_score": 40,
    "percentage": 0,
    "recommendation": "",
    "executive_summary": "",
    "strengths": [],
    "gaps": [],
    "interview_focus_areas": [],
    "interview_questions": {
        "technical_questions": [],
        "project_deep_dive_questions": [],
        "scenario_questions": [],
        "gap_validation_questions": []
    },
    "evidence": [],
    "human_review_note": ""
}
""",
    agent=final_recommendation_agent,
)
report_review_task = Task(description="""
Review final report.
Validate:
1. Schema completeness.
2. Recommendation consistency.
3. Evidence availability.
4. Missing sections.
5. Output quality.

Return review summary.
""",
    expected_output="""
{
    "report_complete": true,
    "missing_sections": [],
    "schema_valid": true,
    "review_notes": []
}
""",agent=report_review_agent,)

ALL_TASKS = [
    jd_analysis_task,
    resume_extraction_task,
    skill_matching_task,
    gap_analysis_task,
    interview_planning_task,
    final_recommendation_task,
    report_review_task,
]