# agents.py

from crewai import Agent, LLM

from config import GROQ_API_KEY

from tools import (
    read_job_description_tool,
    candidate_index_lookup_tool,
    read_resume_tool,
    load_screening_rubric_tool, 
    load_skill_synonyms_tool, 
    score_calculator_tool,
    )

from output_writer import save_report_tool

import os
from crewai import LLM


llm = LLM(
    model="llama-3.3-70b-versatile", 
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1" 
)



Job_Description_Analyst_Agent = Agent(
    role='AI Job Description Analyst Expert',
    goal='Accurately analyze the AI Job description and output a strict JSON object with keys: role_title, required_skills, preferred_skills, responsibilities, experience_expectation, and evaluation_criteria.',
    backstory=(
        "You are an expert at reading and structuring job descriptions. "
        "Your task is to extract the exact details required by the hiring team into a clean JSON format."
        "Use the read_job_description_tool"
    ),
    verbose=True,
    allow_delegation=False,
    tools=[read_job_description_tool], 
    llm=llm
)

Resume_Extraction_Agent = Agent(
    role='Expert in Resume Parser',
    goal='Extract structured candidate information from the resume and output a strict JSON object with keys: candidate_id, candidate_name, current_role, years_experience, skills, projects, experience_summary, education, and certifications.',
    backstory=(
        "You are an Expert resume analyst. "
        "You use the candidate_index_lookup_tool to find the file, and the read_resume_tool to read it. "
        "You extract every relevant detail into the required JSON structure without making up any information from your own."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[candidate_index_lookup_tool, read_resume_tool], 
    llm=llm
)

Skill_Experience_Matching_Agent = Agent(
    role='Skill & Experience Matching Specialist',
    goal='Compare JD requirements with the candidate profile and output a strict JSON object containing: matched_skills, partial_matches, missing_skills, category_scores (0-5 for 8 specific categories), overall_score, max_score (40), percentage, and recommendation_band.',
    backstory=(
        "You are a technical recruiter AI. You receive the JD analysis and Resume profile. "
        "First, use the load_screening_rubric_tool to understand the 8 scoring categories. "
        "Then, use the load_skill_synonyms_tool to understand how resume keywords map to those categories. "
        "Then Carefully score the candidate 0-5 in each category based on this mapping, use the score_calculator_tool for this task, and return the complete match_score JSON."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[load_screening_rubric_tool, load_skill_synonyms_tool, score_calculator_tool], 
    llm=llm
)

Interview_Planning_Agent = Agent(
    role='Technical Interview Planner',
    goal='Generate candidate-specific interview questions and output a strict JSON object with keys: interview_focus_areas, technical_questions (min 3), project_deep_dive_questions (min 2), scenario_questions (min 2), and gap_validation_questions (min 2).',
    backstory=(
        "You are a senior technical interviewer. Based on the candidate profile and match scores, "
        "you generate tailored interview questions focusing on their specific projects and any skill gaps identified in the matching phase."
    ),
    verbose=True,
    allow_delegation=False,
    tools=[],
    llm=llm
)

Final_Recommendation_Agent = Agent(
    role='Final Screening Report Generator',
    goal='Produce the final screening report as a strict JSON object containing: candidate_id, candidate_name, role_title, overall_score,nax_score, percentage, recommendation eg. ("STRONG_MATCH | MODERATE_MATCH | WEAK_MATCH | NEEDS_MANUAL_REVIEW"), executive_summary, strengths, gaps, interview_focus_areas, interview_questions, evidence, and human_review_note.',
    backstory=(
        "You are the final decision-making AI. You use the JD analysis, resume profile, match scores, and interview plan into one complete JSON report. "
        "Once the JSON is perfectly formatted, you MUST use the save_report_tool to save the report to the outputs folder both in .json and .md."
        "Add this line in the final output in the human_review_note key: Required human_review_note:This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision."
    ), 
    verbose=True,
    allow_delegation=False,
    tools=[save_report_tool], 
    llm=llm
)