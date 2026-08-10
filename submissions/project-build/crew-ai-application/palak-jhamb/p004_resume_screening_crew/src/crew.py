from crewai import Crew,Process
from agents import job_review, resume_extraction,Skill_and_Experience_Matching_Agent,Interview_Planning_Agent,Final_Recommendation_Agent
from tasks import job_review_task, resume_review_task,matching_task,planner_task,final_task


crew = Crew(
  agents=[job_review, resume_extraction, Skill_and_Experience_Matching_Agent,Interview_Planning_Agent,Final_Recommendation_Agent],
  tasks=[job_review_task, resume_review_task,matching_task,planner_task,final_task],
  process=Process.sequential,  
  memory=True,  
  cache=False,  
  max_rpm=100,
  share_crew=True
)

# result=crew.kickoff({})
# print(result)