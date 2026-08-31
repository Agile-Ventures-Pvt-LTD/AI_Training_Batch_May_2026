import os
from crewai import Agent
from config import llm
from tools import (
    read_job_description_tool, 
    read_resume_tool, 
    load_screening_rubric_tool, 
    validate_report_schema_tool
)

class ResumeScreeningAgents:
    def __init__(self):
        # Initialize Groq LLM using enterprise-tier specifications
        self.llm = llm

    def jd_analyst(self) -> Agent:
        return Agent(
            role="Job Description Analyst",
            goal="Thoroughly parse and analyze target position requirements to extract core criteria.",
            backstory="Expert Technical Recruiter specialized in breakdown analysis and requirement extraction.",
            tools=[read_job_description_tool],
            llm=self.llm,
            verbose=True
        )

    def resume_extractor(self) -> Agent:
        return Agent(
            role="Resume Extraction Specialist",
            goal="Extract structured candidate details and technical facts directly from incoming text data.",
            backstory="Data parsing expert optimizing application profiles for alignment matching pipelines.",
            tools=[read_resume_tool],
            llm=self.llm,
            verbose=True
        )

    def skill_matcher(self) -> Agent:
        return Agent(
            role="Skill and Experience Matcher",
            goal="Compare profile skills to structural job requirements using the 8-category grading rubric.",
            backstory="Precise screening analyst skilled at structural alignment parsing metrics and compliance scoring.",
            tools=[load_screening_rubric_tool],
            llm=self.llm,
            verbose=True
        )

    def gap_analyst(self) -> Agent:
        return Agent(
            role="Gap Analysis Expert",
            goal="Identify explicit or latent skill, experience, and domain timeline discrepancies separately.",
            backstory="Deep-dive auditor searching for talent qualifications variance and technical risk factors.",
            tools=[],
            llm=self.llm,
            verbose=True
        )

    def interview_planner(self) -> Agent:
        return Agent(
            role="Interview Planning Architect",
            goal="Synthesize targeted technical, situational, and gap validation questions.",
            backstory="Senior Interview Panel Chairman designing rigorous loop architectures to validate candidate skills.",
            tools=[],
            llm=self.llm,
            verbose=True
        )

    def recommendation_specialist(self) -> Agent:
        return Agent(
            role="Final Recommendation Specialist",
            goal="Compile final decisions into an elegant screening summary structure matching organizational standards.",
            backstory="Talent Acquisition Director establishing strategic score alignment and final pipeline sorting.",
            tools=[],
            llm=self.llm,
            verbose=True
        )

    def quality_controller(self) -> Agent:
        return Agent(
            role="Report Quality Controller",
            goal="Validate system output schema compliance and verify evidence standards.",
            backstory="Rigorous QA Engineer ensuring zero documentation degradation and complete Pydantic structural compliance.",
            tools=[validate_report_schema_tool],
            llm=self.llm,
            verbose=True
        )
