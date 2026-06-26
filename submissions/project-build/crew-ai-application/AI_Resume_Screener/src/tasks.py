from crewai import Task
from agents import (
    jd_analyst,
    resume_extractor,
    skill_matcher,
    interview_planner,
    final_recommender,
)


jd_analysis_task = Task(
    description="""
    Read the job description file using the read_job_description_tool and extract
    all structured information from it for the AI Engineer role.

    Extract the following:
    - role_title: the exact job title
    - required_skills: all must-have technical skills listed
    - preferred_skills: nice-to-have or bonus skills listed
    - responsibilities: key duties and responsibilities of the role
    - experience_expectation: years and type of experience expected
    - evaluation_criteria: any explicitly stated criteria for evaluating candidates

    Do not infer or add anything not present in the job description text.
    """,
    expected_output="""
    A JSON object with the following structure:
    {
        "role_title": "",
        "required_skills": [],
        "preferred_skills": [],
        "responsibilities": [],
        "experience_expectation": "",
        "evaluation_criteria": []
    }
    """,
    agent=jd_analyst,
)


resume_extraction_task = Task(
    description="""
    You will be given a candidate_id as input (e.g. CAND-001).

    Step 1: Use candidate_index_lookup_tool with the candidate_id to get the resume file path.
    Step 2: Use read_resume_tool with that resume_path to get the resume content.
    Step 3: Extract all structured information from the resume content.

    Extract the following:
    - candidate_id: the candidate ID provided
    - candidate_name: full name from the resume
    - current_role: their current or most recent job title
    - years_experience: total years of professional experience
    - skills: all technical and soft skills explicitly mentioned
    - projects: list of projects with name and brief description
    - experience_summary: list of past roles and responsibilities
    - education: degrees, institutions, and graduation years
    - certifications: any certifications or courses listed

    Only extract what is explicitly stated. Do not infer or add anything not in the resume.
    """,
    expected_output="""
    A JSON object with the following structure:
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
    """,
    agent=resume_extractor,
    context=[jd_analysis_task],
)


skill_matching_task = Task(
    description="""
    Using the job description analysis and the candidate resume profile from prior tasks,
    evaluate the candidate against all 8 scoring rubric categories.

    Step 1: Use load_screening_rubric_tool to get the rubric and skill synonyms.
    Step 2: Use skill_matcher_tool with the JD required_skills and candidate skills lists
            to identify matched, partial, and missing skills.
    Step 3: Score the candidate from 0 to 5 in each of these 8 categories:
            - python_programming
            - sql_database_skills
            - api_integration
            - llm_application_development
            - agent_frameworks
            - rag_understanding
            - testing_and_quality
            - communication
    Step 4: Use score_calculator_tool with the category_scores dict to get
            overall_score, percentage, and recommendation_band.

    Base every score strictly on evidence from the resume. Do not inflate scores.
    Use the skill synonyms to normalize terminology before scoring.
    """,
    expected_output="""
    A JSON object with the following structure:
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
    """,
    agent=skill_matcher,
    context=[jd_analysis_task, resume_extraction_task],
)


interview_planning_task = Task(
    description="""
    Using the candidate profile and skill match results from prior tasks,
    design a structured, candidate-specific interview plan.

    Focus on:
    - The candidate's strongest areas (to validate depth of knowledge)
    - The candidate's identified gaps (to probe and validate claims)
    - Scenarios relevant to the AI Engineer role responsibilities

    Generate the following minimum number of questions:
    - 3 technical_questions: test specific technical knowledge from the JD
    - 2 project_deep_dive_questions: probe specific projects listed on the resume
    - 2 scenario_questions: present real-world situations relevant to the role
    - 2 gap_validation_questions: directly address missing or weak skills

    All questions must be specific to this candidate — no generic templates.
    Each question should reference something from the resume or JD explicitly.
    Also identify the top 3 interview_focus_areas for the hiring panel.
    """,
    expected_output="""
    A JSON object with the following structure:
    {
        "interview_focus_areas": [],
        "technical_questions": [],
        "project_deep_dive_questions": [],
        "scenario_questions": [],
        "gap_validation_questions": []
    }
    """,
    agent=interview_planner,
    context=[jd_analysis_task, resume_extraction_task, skill_matching_task],
)


final_report_task = Task(
    description="""
    Synthesize all outputs from the prior tasks into a complete final screening report
    for this candidate.

    Step 1: Compile all fields from the JD analysis, resume profile, skill match,
            and interview plan into the final report structure below.
    Step 2: Use validate_report_schema_tool to check the report has all required fields.
            Fix any missing fields before proceeding.
    Step 3: Use save_report_tool with the candidate_id and the complete report dict
            to save the report to the outputs folder.

    The report must include:
    - executive_summary: 2-3 sentence summary of the candidate's fit for the role
    - strengths: list of specific strengths backed by resume evidence
    - gaps: list of specific gaps or missing skills with reference to JD requirements
    - evidence: list of specific resume items that support the recommendation
    - recommendation: must match the recommendation_band from the skill match score exactly
    - human_review_note: must always be set to exactly:
      "This is an AI-assisted screening report based on the provided resume and job
       description. A human reviewer should validate the recommendation before making
       any recruitment decision."

    Do not change the recommendation to be more favorable than the calculated score band.
    """,
    expected_output="""
    A saved JSON file at outputs/<candidate_id>_screening_report.json with this structure:
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
    agent=final_recommender,
    context=[jd_analysis_task, resume_extraction_task, skill_matching_task, interview_planning_task],
)