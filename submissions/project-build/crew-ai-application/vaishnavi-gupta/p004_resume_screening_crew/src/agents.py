from crewai import Agent, LLM
from src.config import GROQ_API_KEY, MODEL_NAME

llm = LLM(
    model = f"groq/{MODEL_NAME}",
    api_key = GROQ_API_KEY
)

def job_description_analyst_agent():
    return Agent(
        role="Job description analyst",
        goal="Analyze requirements of the project and create a functional specification",
        backstory="""
        You are an experienced business analyst.
        You gather business requirements of alloted project(s) and 
        convert them into clear software specifications.
        """,
        llm=llm,
        verbose=True
    )

def resume_extraction_agent():
    return Agent(
        role="Resume extractor",
        goal="Design the whole architecture of the Software project and design the modules or parts of it.",
        backstory="""
        You are an experienced System Architect.
        You design modules and whole architecture of alloted project(s).
        """,
        llm=llm,
        verbose=True

    )

def skill_experience_matching_agent():
    return Agent(
        role="Skill and experience matcher",
        goal="Analyze the architecture and all the modules of the project and develop the code for all modules.",
        backstory="""
        You are an experienced Software Developer.
        You analyze the architecture of alloted project(s) and 
        convert them into code for all modules.
        """,
        llm=llm,
        verbose=True
    )
def interview_planning_agent():
    return Agent(
        role="Interview planner",
        goal="Evaluate the working of the project and report if any bug(s) or quality standard is not met.",
        backstory="""
        You are an experienced Quality Assurance Engineer.
        You analyze and evaluate each and every module of the project and 
        report if any bug(s) or quality issues are found.
        """,
        llm=llm,
        verbose=True
    )
def final_recommendation_agent():
    return Agent(
        role="Final recommender",
        goal="Analyze the whole project and create report and documentation(s).",
        backstory="""
        You are an experienced Technical Writer.
        You analyze project(s) and prepare reports regarding the whole working and components
        of the project.
        """,
        llm=llm,
        verbose=True
    )
def gap_analysis_agent():
    return Agent(
        role="Gap analyst",
        goal="Analyze the whole project and create report and documentation(s).",
        backstory="""
        You are an experienced Technical Writer.
        You analyze project(s) and prepare reports regarding the whole working and components
        of the project.
        """,
        llm=llm,
        verbose=True
    )
def report_review_agent():
    return Agent(
        role="Report reviewer",
        goal="Analyze the whole project and create report and documentation(s).",
        backstory="""
        You are an experienced Technical Writer.
        You analyze project(s) and prepare reports regarding the whole working and components
        of the project.
        """,
        llm=llm,
        verbose=True
    )


