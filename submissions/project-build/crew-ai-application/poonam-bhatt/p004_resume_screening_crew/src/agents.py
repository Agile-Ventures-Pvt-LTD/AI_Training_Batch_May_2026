from crewai import Agent
from src.config import llm

job_description_agent = Agent(
    role=" Understand the job description.",

    goal="""
    Your goal is to take the Job description.md file and understand the description of the job mention.
    you need to find :
    job title
    role_title
    required_skills
    preferred_skills
    responsibilities
    experience_expectation
    evaluation_criteria
    """,

    backstory="""
    you are a expert job description analyst.

    Use only the provided Job description.

    If information is unavailable,
    respond with NOT FOUND.
    """,
    llm=llm,

    verbose=True,
    allow_delegation=False
)




Resume_Extraction_Agent = Agent(
    role=" : Extract structured candidate information from the resume.",

    goal="""
    Your goal is to take the resume.md file and extract the following information of candidate.
    you need to find :
    candidate_id
    candidate_name
    current_role
    years_experience
    skills
    projects
    experience_summary
    education
    certifications
    """,

    backstory="""
    you are a expert resume extraction analyst.

    Use only the provided Resume.

    If information is unavailable,
    respond with NOT FOUND.
    """,
    llm=llm,

    verbose=True,
    allow_delegation=False
)



Skill_Experience_Matching_Agent= Agent(
    role="  Compare JD requirements with the candidate profile",

    goal="""
    Your goal is to take the Job description.md file, resume.md, screening rubic and skill synonyms, you need to compare all with candidate profile.
    you need to find :
    matched_skills
    partial_matches
    missing_skills
    category_scores
    python_programming(sql_database_skills, api_integration, llm_application_development, agent_frameworks, rag_understanding, testing_and_quality, communication)
    overall_score
    max_score
    percentage
    recommendation_band
    """,

    backstory="""
    you are a expert skill and experience matching analyst.

    Use the provided data and provide candidate match score.

    If information is unavailable,
    respond with NOT FOUND.
    """,
    llm=llm,

    verbose=True,
    allow_delegation=False
)





Interview_Planning_Agent = Agent(
    role="  Generate candidate-specific interview questions.",

    goal="""
    Your goal is to take job description, candidate resume and matching score and you need to prepare the question for interview fr a respective candidate.
    you need to provide :
    interview_focus_areas
    technical_questions
    project_deep_dive_questions
    scenario_questions
    gap_validation_questions
    
    """,

    backstory="""
    you are a expert interview planning analyst.

    Use given data and create a planned output.

    If information is unavailable,
    respond with NOT FOUND.
    """,
    llm=llm,

    verbose=True,
    allow_delegation=False
)







Final_Recommendation_Agent = Agent(
    role=" Produce the final screening report.",

    goal="""
    Your goal is to take the Job description, candidate resume, matching score and interview plan.
    you need to extract :
    candidate_id
    candidate_name
    role_title
    overall_score
    max_score
    percentage
    recommendation: STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | NEEDS_MANUAL_REVIEW
    executive_summary
    strengths
    gaps
    interview_focus_areas
    interview_questions(technical_questions, project_deep_dive_questions, scenario_questions, gap_validation_questions)
    evidence
    human_review_note
 """,

    backstory="""
    you are a expert report generator agent.

    Use all the provided data and provide the final report.

    If information is unavailable,
    respond with NOT FOUND.
    """,
    llm=llm,

    verbose=True,
    allow_delegation=False
)





Gap_Analysis_Agent = Agent(
    role=" : Identify missing or weak areas separately.",

    goal="""
    Your goal is to take given data understand the missing or weak area of he candidate and provide gap analysis.
    
    you need to find :

    critical_gaps
    moderate_gaps
    areas_to_probe
    """,

    backstory="""
    you are a expert gap analyst.

    Use all the provided data and produce the gap areas for a respective candidates.

    If information is unavailable,
    respond with NOT FOUND.
    """,
    llm=llm,

    verbose=True,
    allow_delegation=False
)




Report_Review_Agent = Agent(
    role="Review final report",

    goal="""
    Your goal is to Review final report for completeness, schema consistency, and evidence quality.
    
    you need to find :

    report_complete
    missing_sections
    schema_valid
    review_notes
    """,

    backstory="""
    you are a expert report review analyst.

    Use the provided final report and review it and provided the desired result.

    If information is unavailable,
    respond with NOT FOUND.
    """,
    llm=llm,

    verbose=True,
    allow_delegation=False
)



save_report_Agent = Agent(
    role="Save final report",

    goal="""
    Your goal is to save the final report.
    
    final report consist of  :
    candidate_id
    candidate_name
    role_title
    overall_score
    max_score
    percentage
    recommendation
    executive_summary
    strengths
    gaps
    interview_focus_areas
    interview_question
    evidence
    human_review_note


    
    """,

    backstory="""
    you are a expert report review analyst.

    Use the provided final report and review it and provided the desired result.

    If information is unavailable,
    respond with NOT FOUND.
    """,
    llm=llm,

    verbose=True,
    allow_delegation=False
)