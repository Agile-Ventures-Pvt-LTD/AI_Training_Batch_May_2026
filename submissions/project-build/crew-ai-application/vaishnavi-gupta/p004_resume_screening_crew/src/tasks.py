from crewai import Task

def descripton_analyst_task(agent, project_name):
    return Task(
        input = "job_description/jd_ai_enginerr.md",
        description=f"""
        Analyze the following Task:

        {project_name}

        Understand:
        1. Job desription
        2. Required skills
        3. Required experience
        4. Required qualification

        """,
        expected_output_file = "jd_analysis.json",
        expected_output={
            "role_title": "",
            "required_skills": [],
            "preferred_skills": [],
            "responsibilities": [],
            "experience_expectation": "",
            "evaluation_criteria": []
        },
        agent=agent
    )


def extraction_task(agent, project_name):
    return Task(
        input = "resumes",
        description=f"""
        Extract structured candidate information from the resume:

        {project_name}

        Include:
        1. Skills
        2. Education
        3. Personal details
        4. Certifications

        """,
        expected_output_file = "resume_profile.json",
        expected_output={
            "candidate_id": "",
            "candidate_name": "",
            "current_role": "",
            "years_experience": "",
            "skills": [],
            "projects": [],
            "experience_summary": [],
            "education": [],
            "certifications": []
        },
        agent=agent
    )

def skill_experience_matching_task(agent, project_name):
    return Task(
        input ={"jd_analysis.json",
                "resume_profile.json",
                "screening_rubric.json",
                "skill_synonyms.json"
        },
        description=f"""
        Compare JD requirements with the candidate profile.:

        {project_name}

        Compare:
        1. Skills
        2. Work experience.
        3. Technical as well as non-technical skills.
        """,

        expected_output_file = "match_score.json",
        expected_output={
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
        },
        agent=agent
    )

def interview_planning_task(agent, project_name):
    return Task(
        input ={ "jd_analysis.json",
                "resume_profile.json",
                "resume_profile.json",
                "match_score.json"},

        description=f"""
        Generate candidate-specific interview questions.

        {project_name}

        Generate:
        - 3 technical questions
        - 2 project deep-dive questions
        - 2 scenario questions
        - 2 gap-validation questions
        """,
        expected_output_file="interview_plan.json",
        expected_output = {
            "interview_focus_areas": [],
            "technical_questions": [],
            "project_deep_dive_questions": [],
            "scenario_questions": [],
            "gap_validation_questions": []
        },
        agent=agent
  )

def recommendation_task(agent, project_name):
    return Task(
        input = {
            "jd_analysis.json",
            "resume_profile.json",
            "match_score.json",
            "interview_plan.json"
        },
        description=f"""
        Produce the final screening report:

        {project_name}

        Create:
        1. Proper documents.
        2. Well designed report.
        3. Include all details (fucntional as well as non-functional)
        """,

        expected_output_file="candidate_screening_report.json",
        expected_output = {
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
             "interview_questions":{
                 "technical_questions": [],
                 "project_deep_dive_questions": [],
                 "scenario_questions": [],
                 "gap_validation_questions": []
             },
             "evidence": [],
             "human_review_note": ""
        },
        agent=agent

    )
def gap_analysis_task(agent, project_name):
    return Task(
        input = "candidate_screening_report.json",
        
        description = f"""
        Identify missing or weak areas separately.
        
        {project_name}
         
        Identify:
        1. Missing skills and knowledge.
        2. Weak areas to work on.
        """,
        expected_output_file = "gap_analysis.json" ,
        expected_output = {
            "critical_gaps": [],
            "moderate_gaps": [],
            "areas_to_probe": []

    },
    agent = agent
    )       

def report_review_task(agent, project_name):
    return Task(
        input = {
            "candidate_screening_report.json",
            "gap_analysis.json",
            "interview_plan.json"
            "match_score.json"

        },
        
        description = f"""
        Review final report for completeness, schema consistency, and 
        evidence quality.
        
        {project_name}
         
        Identify:
        1. Missing skills and knowledge.
        2. Weak areas to work on.
        """,
        expected_output_file = "gap_analysis.json" ,
        expected_output = {
            "report_complete": true,
            "missing_sections": [],
            "schema_valid": true,
            "review_notes": []
        },
        agent = agent
    )       
