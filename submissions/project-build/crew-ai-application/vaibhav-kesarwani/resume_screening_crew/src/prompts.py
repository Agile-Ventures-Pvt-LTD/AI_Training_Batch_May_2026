manager_ds = """
You are very good at undertanding the user Query so understand this user query {user_query}
and call the different agent.
"""

manager_eo = """
The expected output is simple you are responsible to call the right agent to do that task.
"""


job_description_ds = """
Understand the job description using the given tool and read the whole content of the file.
"""

job_description_eo = """
The expected ouput structure is in the JSON form which looks like this 

{
    "role_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "responsibilities": [],
    "experience_expectation": "",
    "evaluation_criteria": []
}
"""


resume_extraction_ds = """
Extract the structured candidate resume using the tools which are provided from the resume folder.
"""

resume_extraction_eo = """
The expected ouput structure is in the JSON form which looks like this 

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
"""


experience_matching_ds = """
Compare the job description and the candidate profile use the provided tools to complete the task.
"""

experience_matching_eo = """
The expected ouput structure is in the JSON form which looks like this 

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
"""


interview_planning_ds = """
Generate the candidate specific interview questions uses the tool to get the job description, resume profile and match score.

Minimum required questions:
3 technical questions
2 project deep-dive questions
2 scenario questions
2 gap-validation questions
"""

interview_planning_eo = """
The expected ouput structure is in the JSON form which looks like this 

{
    "interview_focus_areas": [],
    "technical_questions": [],
    "project_deep_dive_questions": [],
    "scenario_questions": [],
    "gap_validation_questions": []
}
"""


final_recommendation_ds = """
Produce the final recommendation using the job description, resume profile, match score and interview plan and to get these answeres use the tools which are provided to you.
"""

final_recommendation_eo = """
The expected ouput structure is in the JSON form which looks like this 

{
    "candidate_id": "",
    "candidate_name": "",
    "role_title": "",
    "overall_score": 0,
    "max_score": 40,
    "percentage": 0,
    "recommendation": "STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | 
    NEEDS_MANUAL_REVIEW",
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
    "human_review_note": "This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision."  # Do not change this field.
}
"""


gap_analysis_ds = """
Identify the gaps in the resume of the candidate to so they improv themseleves on there weak areas and missing information.
"""

gap_analysis_eo = """
The expected ouput structure is in the JSON form which looks like this 

{
    "critical_gaps": [],
    "moderate_gaps": [],
    "areas_to_probe": []
}
"""


report_review_ds = """
Analyse the Report inside the output folder for the completness, schema consistency and evidence quality you use the provided tools to do that.
"""

report_review_eo = """
{
    "report_complete": true, 
    "missing_sections": [],
    "schema_valid": true,
    "review_notes": []
}
"""