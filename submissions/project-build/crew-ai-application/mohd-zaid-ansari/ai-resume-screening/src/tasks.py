from crewai import LLM, Agent, Task, Crew, Process
from agent import job_description_analyst_agent, resume_extraction_agent, skill_matching_agent, interview_planning_agent, final_response_agent
from src.config import DATASET_PATH, OUTPUT_PATH

task_analyze_job_description = Task(
    description=f"Run the job description tool to read {DATASET_PATH}/job_description/jd_ai_engineer.md ."
        "Parse the text data carefully to find role information, core requirements, and preferred qualifications."
        "Arrange the extracted elements exactly into the requested JSON schema structure.",
    expected_output=
        "A JSON-formatted string matching this structure:"
        "{"
        '  "role_title": "...",'
        '  "required_skills": ["...", "..."],'
        '  "preferred_skills": ["...", "..."],'
        '  "responsibilities": ["...", "..."],'
        '  "experience_expectation": "...",'
        '  "evaluation_criteria": ["...", "..."]'
        "}",
    agent=job_description_analyst_agent,
    output_file=f"{OUTPUT_PATH}/jd_analysis.json"
    )

#==============================================================================================================================

resume_extractor=Task(
    description=
        f"Run the resume extraction tool to read {DATASET_PATH}/resumes/ using lookup results for {{candidate_id}}."
        "Carefully extract the candidate profile, all its skills, personal information, academic stats."
        "Arrange the extracted information exactly in the formatted JSON schema structure.",
    expected_output=
         "A JSON-formatted string matching this structure:"
        "{"
        '  "candidate_id": "...",'
        '  "candidate_name": "...",'
        '  "current_role": "...",'
        '  "years_experience": "...",'
        '  "skills": ["...", "..."],'
        '  "projects": ["...", "..."],'
        '  "experience_summary": ["...", "..."],'
        '  "education": ["...", "..."],'
        '  "certifications": ["...", "..."]'
        "}",
    output_file=f"{OUTPUT_PATH}/{{candidate_id}}_resume_profile.json",  
    agent=resume_extraction_agent
    )

#=================================================================================================================================

skill_matcher=Task(
    description=
        f"Ingest the data from 'outputs/jd_analysis.json' and 'outputs/resume_profile.json'"
        "Load {DATASET_PATH}/metadata/ to resolve acronym mappings."
        "Segment technical skills into explicit lists for fully matched, partially matched, and completely missing groups."
        "Assign a score from 0 to 5 for each of the 8 rubric categories based on candidate competency."
        "Execute the score calculator tool using those category metrics to extract the verified summary data.",
    expected_output=(
        "A JSON-formatted string matching this structure:"
        "{"
        '  "matched_skills": ["...", "..."],'
        '  "partial_matches": ["...", "..."],'
        '  "missing_skills": ["...", "..."],'
        '  "category_scores": {'
        '    "python_programming": 0,'
        '    "sql_database_skills": 0,'
        '    "api_integration": 0,'
        '    "llm_application_development": 0,'
        '    "agent_frameworks": 0,'
        '    "rag_understanding": 0,'
        '    "testing_and_quality": 0,'
        '    "communication": 0'
        '  },'
        '  "overall_score": 0,'
        '  "max_score": 40,'
        '  "percentage": 0,'
        '  "recommendation_band": "..."'
        "}"
    ),
    output_file=f"{OUTPUT_PATH}/{{candidate_id}}_match_score.json", 
    agent=skill_matching_agent
)

#===================================================================================================================================

task_generate_interview_plan = Task(
    description=
        "Identify core focus areas where the candidate needs evaluation based on identified missing or partial skills."
        "You task is to genrate interview questions from these areas:"
        "   - At least 3 deep technical questions"
        "   - At least 2 project deep-dive questions"
        "   - At least 2 situational scenario questions"
        "   - At least 2 gap-validation questions"
        "Format the generated contents into a clean JSON string matching the required structure."
    ),
expected_output=(
        "A JSON-formatted string matching this structure:"
        "{"
        '  "interview_focus_areas": ["...", "..."],'
        '  "technical_questions": ["Question 1", "Question 2", "Question 3"],'
        '  "project_deep_dive_questions": ["Question 1", "Question 2"],'
        '  "scenario_questions": ["Question 1", "Question 2"],'
        '  "gap_validation_questions": ["Question 1", "Question 2"]'
        "}"
    ),
output_file=f"{OUTPUT_PATH}/{{candidate_id}}_interview_plan.json", 
agent=interview_planning_agent

#==========================================================================================================================

task_generate_final_report = Task(
    description=(
        "Give a comprehensive summary describing the candidate alignments with the job description."
        "Construct a clear a human review for the HR and Technical team to easy the process."
        "Execute the save report tool to securely write 'candidate_screening_report.json' into the outputs folder."
    ),
    expected_output=(
        "A complete, valid nested JSON string matching this structure exactly:"
        "{"
        '  "candidate_id": "...",'
        '  "candidate_name": "...",'
        '  "role_title": "...",'
        '  "overall_score": 0,'
        '  "max_score": 40,'
        '  "percentage": 0,'
        '  "recommendation": "MODERATE_MATCH",'
        '  "executive_summary": "...",'
        '  "strengths": ["...", "..."],'
        '  "gaps": ["...", "..."],'
        '  "interview_focus_areas": ["...", "..."],'
        '  "interview_questions": {'
        '    "technical_questions": ["...", "..."],'
        '    "project_deep_dive_questions": ["...", "..."],'
        '    "scenario_questions": ["...", "..."],'
        '    "gap_validation_questions": ["...", "..."]'
        '  },'
        '  "evidence": ["...", "..."],'
        '  "human_review_note": "..."'
        "}"
    ),
    output_file=f"{OUTPUT_PATH}/{{candidate_id}}_screening_report.json", 
    agent=final_response_agent
)

