from crewai import Task
from src.schema import (
    JDanalysis,
    Resumeprofile,
    Matchscore,
    Interviewplan,
    Gapanalysis,
    Reportreview,
    Finalreport
)

def jd_analysis_task(agent,jd_path):
    return Task (
        description=f"""
        Analyze the job description file at '{jd_path}'
        use the 'read_job_description_tool' to read the content of file
        extract the below details:
        - Role title
        - Required skills
        - Preferred skills
        - Key responsibilities
        - Experience expectation
        - Evaluation criteria
        """,
        expected_output="json output containing role_title, required_skills, preferred_skills, responsibilities, experience_expectation, and evaluation_criteria",
        agent=agent,
        output_json=JDanalysis
        )

def resume_extraction_task(agent, resume_path):
    return Task(
        description=f"""
        Analyze the resume file at '{resume_path}'
        use 'read_resume_tool' to read the content of the file
        extract the following structured details:
        - Candidate ID (e.g. CAND-001)
        - Candidate name
        - Current role
        - Years of experience
        - Skills list
        - Projects list
        - Experience summary
        - Education
        - Certifications
        """,
    expected_output=" JSON with the candidate's resume profile containing candidate_id, candidate_name, current_role, years_experience, skills, projects, experience_summary, education, and certifications.",
    agent=agent,
    output_json=Resumeprofile
    )

def skill_matching_task(agent, jd_analysis,resume_extraction):
    return Task(
        description=f"""
    analyze the match between job description and resume
    1. use the 'skill_matcher_tool' to compare jd and candidate skills
    2. use 'load_screening_rubric_tool' to load the screening rubric
    3. score the candidate from 0 to 5 in 8 given categories: - python_programming, sql_database_skills, api_integration, llm_application_development, agent_frameworks, rag_understanding, testing_and_quality, communication
    4. pass these category scores to 'score_calculator_tool' to calculate the overall score, max score, percentage, and recommendation band. Do NOT calculate these values manually.

    the candidate should be evaulated only based on their resume

""",
expected_output="json containing matched_skills, partial_matches, missing_skills, category_scores, overall_score, max_score, percentage, and recommendation_band.",
        agent=agent,
        context=[jd_analysis, resume_extraction],
        output_json=Matchscore
    )

def gap_analysis_task(agent, jd_analysis, resume_extraction):
    return Task(
        description=f"""
    Do a gap analysis between job description and candidate's resume
    Identify:
        - Critical gaps: essential requirements from the JD that the candidate lacks
        - Moderate gaps: preferred requirements or minor skills that are missing
        - Areas to probe: specific areas where the candidate's experience is unclear or needs validation
        """,
        expected_output="json containing critical_gaps, moderate_gaps and areas_to_probe",
        agent=agent,
        context=[jd_analysis, resume_extraction],
        output_json=Gapanalysis
    )

def interview_planning_task(agent, jd_analysis, resume_extraction, match_score, gap_analysis):
    return Task(
        description=f"""
    develop a candidate specific interview plan
    based on the candidate's strengths and the gaps identified, generate:
        - Interview focus areas
        - At least 3 technical questions
        - At least 2 project deep-dive questions for their projects
        - At least 2 scenario-based questions relevant to the AI Engineer role
        - At least 2 gap-validation questions targeting their critical gaps
        
        Do not use generic questions. 
        """,
        expected_output="json containing interview_focus_areas, technical_questions, project_deep_dive_questions, scenario_questions and gap_validation_questions.",
        agent=agent,
        context=[jd_analysis, resume_extraction, match_score, gap_analysis],
        output_json=Interviewplan
    )

def report_review_task(agent, jd_analysis, resume_extraction, match_score, interview_plan, gap_analysis):
    return Task(
        description=f"""
        Do a quality assurance check on the generated reports.
        1. Check if the scores align with the recommendation band.
        2. Verify that the interview plan has the minimum number of questions.
        3. Validate that the report details are fully backed by evidence in the resume.
        """,
        expected_output="json with report_complete, missing_sections, schema_valid, and review_notes.",
        agent=agent,
        context=[jd_analysis, resume_extraction, match_score, interview_plan, gap_analysis],
        output_json=Reportreview
    )

def final_recommendation_task(agent, candidate_id, jd_analysis, resume_extraction, match_score, interview_plan, gap_analysis, report_review):
    return Task(
        description=f"""
        1.Compile all previous analyses into the final report for candidate '{candidate_id}'
        
        The final output MUST include:
        - candidate_id
        - candidate_name
        - role_title
        - overall_score
        - max_score
        - percentage
        - recommendation
        - executive_summary
        - strengths
        - gaps
        - interview_focus_areas
        - interview_questions: technical_questions, project_deep_dive_questions, scenario_questions and gap_validation_questions
        - evidence
        - human_review_note

        2.validate the report structure using 'validate_report_schema_tool'
        3. finally save the JSON report to the outputs directory using the 'save_report_tool'
        """,
        expected_output="The final candidate report in JSON format",
        agent=agent,
        context=[
            jd_analysis, 
            resume_extraction, 
            match_score, 
            interview_plan, 
            gap_analysis, 
            report_review
        ],
        output_json=Finalreport
    )
