from crewai import LLM, Agent, Task, Crew, Process
from crewai import Agent, Task
from config import llm
from src.tools import read_job_description,read_resume_tool, load_screening_rubric_tool,score_calculator_tool, save_report_tool

job_description_analyst_agent = Agent(
    role='Job Description Analyst Agent',
    goal="""Analyze job descriptions to match the hiring criteria of the role and give description of Job.""",
    backstory=""""
        "You are a meticulous human resources tracking data analyst. "
        "Your sole task is to take raw markdown job descriptions, strip away conversational filler, "
        "and isolate the core role attributes. You map requirements cleanly into the requested structural schema "
        "without changing terminology or inventing preferred skills that are not explicitly written in the file." """
    ,
    verbose=True,
    allow_delegation=False,
    tools=[read_job_description],
    llm=llm,
    reasoning=True,
    max_reasoning_attempt=3
)

#====================================================================================================================

resume_extraction_agent=Agent(
    role='Resume Extraction Specialist',
    goal="""Your goal is to provide the structured candidate information from the resume.""",
    backstory="""You are a good resume extractor and have experince in parsing resume.'
    "You are very good in extracting information from the resumes to shortist profile."
    "You have access to tools to get the information from the resume use that tools."
    "Analyze the resume carefully using tools to get correct information from that." """
,
verbose=True,
allow_delegation=False,
tools=[read_resume_tool],
llm=llm,
reasoning=True,
max_reasoning_attempt=3
)

#===============================================================================================================================

skill_matching_agent=Agent(
    role='Skill and Experince Maching agent',
    goal="""Compare the skills of the candidate with the job description and match the skills required in job description.""",
    backstory="""you are a evalutor master in evaluation skills.'
    "your task is to match the skills of one candidate with the job profile."
    "You can map the skills of candidate with job profile using keyword matches."
    "you can also use metrices to get the precise match of the profile." """
,
verbose=True,
allow_delegation=False,
tools=[load_screening_rubric_tool,score_calculator_tool],
llm=llm,
reasoning=True,
max_reasoning_attempt=3
)
#===================================================================================================================================

interview_planning_agent=Agent(
    role='Interview Question Planner',
    goal="""Generate a good interview question based on the candidates profile and that can test candidates skill set.3 technical questions2 project deep-dive questions2 scenario questions2 gap-validation questions""",
    backstory="""you are a good technical interview and have good hiring experince."
    "your responsiblity is to evalute candidate profile based on there skill sets and gaps."
    "you can make a good interview roadmap from the skill set of the candidate."
    "you always delivered best interview question based on the job description and skill sets." """
,
verbose=True,
allow_delegation=False,
tools=[],
llm=llm,
reasoning=True,
max_reasoning_attempt=3
)
#======================================================================================================================================

final_response_agent=Agent(
    role='Final Recommendation Agent',
    goal="""Analyze all the result and make a final recommendation on the profile of the candidate generate score and rubrics.""",
    backstory="""Your are experience talent acquisition lead and can make final decision.'
    'As a talent acquisition lead your task is to get candidate profile and make decision according to job descripion.'
    'you can make evaluation metrics and rubrics from the final result.'
    'You can present the final human review if needed my the candidate profile.' """
,
verbose=True,
allow_delegation=False,
tools=[save_report_tool],
llm=llm,
reasoning=True,
max_reasoning_attempt=3
)


