# call_crew.py

from crewai import LLM, Crew, Process

from config import GROQ_API_KEY

from agents import llm

from agents import(
    Job_Description_Analyst_Agent,
    Resume_Extraction_Agent,
    Skill_Experience_Matching_Agent,
    Interview_Planning_Agent,
    Final_Recommendation_Agent
)

from tasks import(
    Job_Description_task,
    Resume_Extraction_task,
    Skill_Matching_task,
    Interview_Planning_task,
    Final_Report_task
)


def run_screening_crew(candidate_id: str) -> Crew:
    
    screening_crew = Crew(
        agents=[
            Job_Description_Analyst_Agent,
            Resume_Extraction_Agent,
            Skill_Experience_Matching_Agent,
            Interview_Planning_Agent,
            Final_Recommendation_Agent
        ],
        tasks=[
            Job_Description_task,
            Resume_Extraction_task,
            Skill_Matching_task,
            Interview_Planning_task,
            Final_Report_task
        ],
        process=Process.sequential, 
        verbose=True,
        # llm=llm,
    )
    
    return screening_crew