import os
from crewai import Agent, LLM
from tools import (
    read_job_description, 
    read_resume, 
    candidate_index_lookup,
    load_screening_rubric, 
    score_calculator, 
    save_report
)

import os
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",  
    temperature=0.2,
    timeout=120,
    use_cache=False                        
)

jd_analyst_agent = Agent(
    role="Job Description Analyst",
    goal="Thoroughly parse, analyze, and extract structured requirements from the provided job description file.",
    backstory="You are an expert technical recruiter specialized in breaking down role expectations, "
              "compiling required/preferred skill lists, and understanding role responsibilities.",
    tools=[read_job_description],
    llm=llm,
    allow_delegation=False,  
    verbose=True,
    memory=False
)

resume_extractor_agent = Agent(
    role="Resume Extraction Agent",
    goal="Locate the candidate's resume using their ID and accurately extract all structured profile details.",
    backstory="You are a data-driven talent sourcing assistant with precise attention to detail. You specialize "
              "in scanning raw resume files to systematically pull out candidate metadata, skills, history, and education.",
    tools=[candidate_index_lookup, read_resume],
    llm=llm,
    allow_delegation=False,
    verbose=True,
    memory=False
)

matching_agent = Agent(
    role="Skill and Experience Matching Agent",
    goal="Compare the candidate's extracted profile details against the job requirements and calculate an objective fitment score.",
    backstory="You are an unbiased technical assessment manager. You load fixed evaluation rubrics and use structural "
              "calculators to mathematically score capabilities, identifying clear evidence for strengths and gaps.",
    tools=[load_screening_rubric, score_calculator],
    llm=llm,
    allow_delegation=False,
    verbose=True,
    memory=False
)

interview_planner_agent = Agent(
    role="Interview Planning Agent",
    goal="Formulate tailored, candidate-specific interview questions designed to probe identified skill gaps and validate strengths.",
    backstory="You are a senior technical interviewer. You know exactly how to craft balanced technical, situational, "
              "and deep-dive project questions that accurately map to a candidate's distinct resume background.",
    tools=[], 
    llm=llm,
    allow_delegation=False,
    verbose=True,
    memory=False
)

recommendation_agent = Agent(
    role="Final Recommendation Agent",
    goal="Synthesize all prior analytics into a singular, comprehensive JSON screening report and save it to the output directory.",
    backstory="You are the Lead Talent Acquisition Director. You compile technical evaluations and interview strategies "
              "into authoritative executive summaries, ensuring files are perfectly formatted for human HR stakeholders.",
    tools=[save_report],
    llm=llm,
    allow_delegation=False,
    verbose=True,
    memory=False
)
