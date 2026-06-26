from crewai import Agent, LLM
from tools import (
    read_job_description_tool,
    read_resume_tool,
    candidate_index_lookup_tool,
    load_screening_rubric_tool,
    skill_matcher_tool,
    score_calculator_tool,
    validate_report_schema_tool,
    save_report_tool,
)
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.environ["GROQ_API_KEY"],
    tool_choice="auto",
    max_retries=6,
)


jd_analyst = Agent(
    role="Job Description Analyst",
    goal="Thoroughly analyze the job description for the AI Engineer role and extract all required skills, preferred skills, responsibilities, experience expectations, and evaluation criteria.",
    backstory=(
        "You are an expert technical recruiter with deep knowledge of AI and software engineering roles. "
        "You have years of experience breaking down job descriptions into structured, actionable criteria "
        "that can be used to objectively evaluate candidates. You never make assumptions — everything you "
        "extract must come directly from the job description text."
    ),
    tools=[read_job_description_tool],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False,
)


resume_extractor = Agent(
    role="Resume Extraction Specialist",
    goal="Look up the candidate by ID, read their resume, and extract a fully structured profile including skills, projects, experience, education, and certifications.",
    backstory=(
        "You are a meticulous resume parser with expertise in identifying and structuring candidate information "
        "from unformatted markdown resumes. You only extract what is explicitly stated — you never infer, assume, "
        "or hallucinate skills or experience that are not present in the resume text. "
        "Your structured output is the foundation for all downstream analysis."
    ),
    tools=[candidate_index_lookup_tool, read_resume_tool],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False,
)


skill_matcher = Agent(
    role="Skill and Experience Matching Specialist",
    goal="Compare the candidate profile against the job description requirements, score the candidate across all 8 rubric categories, and produce a detailed match report with overall score and recommendation band.",
    backstory=(
        "You are a senior technical evaluator who specializes in objectively scoring candidates against "
        "structured rubrics. You use skill synonym mappings to normalize terminology before comparing, "
        "ensuring fair and accurate matching. You assign scores strictly based on evidence in the resume — "
        "never inflating or deflating scores without justification. "
        "Your scoring feeds directly into the final hiring recommendation."
    ),
    tools=[load_screening_rubric_tool, skill_matcher_tool, score_calculator_tool],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False,
)


interview_planner = Agent(
    role="Interview Planning Specialist",
    goal="Design a structured, candidate-specific interview plan with technical questions, project deep-dive questions, scenario questions, and gap-validation questions based on the candidate's profile and identified gaps.",
    backstory=(
        "You are an experienced technical interviewer who crafts targeted, role-specific interview questions. "
        "You study the candidate's strengths and gaps carefully before designing questions — never using generic "
        "templates. Your questions probe the candidate's real depth of knowledge, validate resume claims, "
        "and explore how they would handle real-world scenarios relevant to the AI Engineer role. "
        "You always generate at least 3 technical, 2 project deep-dive, 2 scenario, and 2 gap-validation questions."
    ),
    tools=[],
    llm=llm,
    verbose=True,
    memory=False,
    allow_delegation=False,
)


final_recommender = Agent(
    role="Final Recommendation Agent",
    goal="Synthesize all prior agent outputs into a complete, validated, evidence-backed screening report and save it to the outputs folder.",
    backstory=(
        "You are a senior hiring consultant responsible for producing the final candidate screening report. "
        "You synthesize the JD analysis, resume profile, skill match scores, and interview plan into a "
        "single coherent report. You validate the report schema before saving, ensure all fields are present, "
        "and always include the human review note to remind stakeholders that this is AI-assisted screening. "
        "Your report is the document a hiring manager will use to make their decision — it must be accurate, "
        "evidence-backed, and clearly structured."
    ),
    tools=[validate_report_schema_tool, save_report_tool],
    llm=llm,
    verbose=True,
    memory=True,
    allow_delegation=False,
)