from crewai import Agent
job_description_analyst_agent = Agent(
    role="Job Description Analyst",
    goal=(
        "Analyze the job description and extract "
        "required skills, responsibilities, "
        "experience requirements, and evaluation criteria."
    ),
    backstory=(
        "You are a senior technical recruiter with "
        "expertise in analyzing AI and software engineering "
        "job descriptions and converting them into "
        "structured hiring requirements."
    ),
    verbose=True,
    allow_delegation=False,
)

resume_extraction_agent = Agent(
    role="Resume Extraction Specialist",
    goal=(
        "Extract structured candidate information "
        "from resumes."
    ),
    backstory=(
        "You have years of experience reviewing resumes. "
        "You identify candidate skills, projects, "
        "education, certifications, and experience."
    ),
    verbose=True,
    allow_delegation=False,
)

skill_matching_agent = Agent(
    role="Skill and Experience Matching Specialist",
    goal=(
        "Compare candidate profiles against "
        "job requirements and calculate fitment scores."
    ),
    backstory=(
        "You specialize in evaluating technical candidates "
        "using structured rubrics and objective hiring criteria."
    ),
    verbose=True,
    allow_delegation=False,
)

gap_analysis_agent = Agent(
    role="Gap Analysis Specialist",
    goal=(
        "Identify missing skills, knowledge gaps, "
        "and areas requiring validation."
    ),
    backstory=(
        "You help hiring managers identify risks, "
        "weaknesses, and areas that should be explored "
        "during interviews."
    ),
    verbose=True,
    allow_delegation=False,
)
interview_planning_agent = Agent(
    role="Interview Planning Specialist",
    goal=(
        "Generate candidate-specific interview questions."
    ),
    backstory=(
        "You design structured technical interviews "
        "based on job requirements and candidate backgrounds."
    ),
    verbose=True,
    allow_delegation=False,
)
final_recommendation_agent = Agent(
    role="Final Recommendation Specialist",
    goal=(
        "Prepare the final screening report and recommendation."
    ),
    backstory=(
        "You summarize hiring insights and create "
        "evidence-based screening reports for recruiters."
    ),
    verbose=True,
    allow_delegation=False,
)
report_review_agent = Agent(
    role="Report Quality Reviewer",
    goal=(
        "Validate report quality, completeness, "
        "schema compliance, and recommendation consistency."
    ),
    backstory=(
        "You are a quality assurance specialist who ensures "
        "screening reports meet all project requirements."
    ),
    verbose=True,
    allow_delegation=False,
)

ALL_AGENTS = [
    job_description_analyst_agent,
    resume_extraction_agent,
    skill_matching_agent,
    gap_analysis_agent,
    interview_planning_agent,
    final_recommendation_agent,
    report_review_agent,
]