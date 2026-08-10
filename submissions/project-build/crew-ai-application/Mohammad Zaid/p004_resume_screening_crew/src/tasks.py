# tasks.py

from crewai import Task
from agents import(
    Job_Description_Analyst_Agent,
    Resume_Extraction_Agent,
    Skill_Experience_Matching_Agent,
    Interview_Planning_Agent,
    Final_Recommendation_Agent
)

Job_Description_task = Task(
    description=(
        "Read the job description using your tool. "
        "Pull out the main role title, required skills, preferred skills, responsibilities, experience needed, and evaluation criteria."
    ),
    expected_output=(
        "A JSON object strictly looking like this: "
        '{"role_title": "", "required_skills": [], "preferred_skills": [], "responsibilities": [], "experience_expectation": "", "evaluation_criteria": []}'
    ),
    agent=Job_Description_Analyst_Agent 
)

Resume_Extraction_task = Task(
    description=(
        "Find the resume file for candidate ID {candidate_id} using your lookup tool. " # <--- FIX: Added {candidate_id} here
        "Then read the resume and pull out their name, current role, years of experience, skills, projects, work history, education, and certifications."
    ),
    expected_output=(
        "A JSON object strictly looking like this: "
        '{"candidate_id": "", "candidate_name": "", "current_role": "", "years_experience": "", "skills": [], "projects": [], "experience_summary": [], "education": [], "certifications": []}'
    ),
    agent=Resume_Extraction_Agent 
)

Skill_Matching_task = Task(
    description=(
        "Look at the job needs and the candidate's resume. "
        "First, get the rubric and the synonym list using your tools so you know what words match what categories. "
        "Figure out what skills match, what skills are missing, and give a score from 0 to 5 for each of the 8 categories. "
        "Finally, use your calculator tool to get the final total score and percentage."
    ),
    expected_output=(
        "A JSON object strictly looking like this: "
        '{"matched_skills": [], "partial_matches": [], "missing_skills": [], "category_scores": {"python_programming": 0, "sql_database_skills": 0, "api_integration": 0, "llm_application_development": 0, "agent_frameworks": 0, "rag_understanding": 0, "testing_and_quality": 0, "communication": 0}, "overall_score": 0, "max_score": 40, "percentage": 0, "recommendation_band": ""}'
    ),
    agent=Skill_Experience_Matching_Agent 
)

Interview_Planning_task = Task(
    description=(
        "Based on the candidate's resume and the score match, make an interview plan. "
        "You need to write at least 3 technical questions, 2 project deep-dive questions, 2 scenario questions, and 2 questions about the skills they are missing."
    ),
    expected_output=(
        "A JSON object strictly looking like this: "
        '{"interview_focus_areas": [], "technical_questions": [], "project_deep_dive_questions": [], "scenario_questions": [], "gap_validation_questions": []}'
    ),
    agent=Interview_Planning_Agent 
)

Final_Report_task = Task(
    description=(
        "Gather all the info from the previous steps (job info, resume info, scores, and interview questions). "
        "Write a short executive summary, list strengths and gaps, and put it all into one final report. "
        "Once the JSON is ready, use your save tool to save it to the outputs folder."
    ),
    expected_output=(
        "A saved JSON and Markdown file strictly matching this structure: "
        '{"candidate_id": "", "candidate_name": "", "role_title": "", "overall_score": 0, "max_score": 40, "percentage": 0, "recommendation": "STRONG_MATCH", "executive_summary": "", "strengths": [], "gaps": [], "interview_focus_areas": [], "interview_questions": {"technical_questions": [], "project_deep_dive_questions": [], "scenario_questions": [], "gap_validation_questions": []}, "evidence": [], "human_review_note": ""}'
    ),
    agent=Final_Recommendation_Agent 
)