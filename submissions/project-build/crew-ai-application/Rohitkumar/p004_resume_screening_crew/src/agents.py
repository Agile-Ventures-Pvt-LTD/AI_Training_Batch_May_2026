from crewai import Agent
from langchain_groq import ChatGroq
from src.config import GROQ_API_KEY, GROQ_MODEL


def get_llm():
    return ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0.1
    )


def create_jd_analyst_agent():
    return Agent(
        role="Job Description Analyst",
        goal="Analyze the job description and extract structured requirements including skills, responsibilities, and evaluation criteria.",
        backstory="You are an expert at parsing job descriptions and identifying key requirements. You extract structured data that can be used for candidate matching.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_resume_extraction_agent():
    return Agent(
        role="Resume Extraction Specialist",
        goal="Extract structured candidate information from resume text including skills, experience, projects, education, and certifications.",
        backstory="You are a resume parsing expert who can extract detailed structured information from any resume format. You ensure no relevant detail is missed.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_skill_matching_agent():
    return Agent(
        role="Skill and Experience Matcher",
        goal="Compare job description requirements with candidate profile to identify matched skills, partial matches, missing skills, and calculate fitment scores.",
        backstory="You are a recruitment analyst who compares candidate profiles against job requirements. You use structured scoring to determine candidate fit.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_interview_planning_agent():
    return Agent(
        role="Interview Planning Agent",
        goal="Generate candidate-specific interview questions based on job requirements, candidate profile, and identified gaps.",
        backstory="You are an interview coach who designs structured interview questions tailored to each candidate's profile and the role requirements.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_final_recommendation_agent():
    return Agent(
        role="Final Recommendation Agent",
        goal="Produce a comprehensive final screening report that consolidates all findings into a structured JSON output.",
        backstory="You are a senior hiring coordinator who compiles screening results into clear, actionable reports for hiring managers.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_gap_analysis_agent():
    return Agent(
        role="Gap Analysis Agent",
        goal="Identify missing or weak areas in the candidate profile compared to job requirements and categorize them as critical or moderate gaps.",
        backstory="You are a skills gap analyst who identifies development areas and flags missing competencies that may affect job performance.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )


def create_report_review_agent():
    return Agent(
        role="Report Review Agent",
        goal="Review the final report for completeness, schema consistency, and evidence quality before delivery.",
        backstory="You are a quality assurance reviewer who ensures screening reports meet all required standards and contain no errors.",
        llm=get_llm(),
        verbose=True,
        allow_delegation=False
    )