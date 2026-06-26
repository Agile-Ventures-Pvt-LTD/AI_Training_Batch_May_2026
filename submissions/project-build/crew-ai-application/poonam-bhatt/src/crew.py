from crewai import Crew,Process
from agents import (
    job_description_agent,
    Resume_Extraction_Agent,
    Skill_Experience_Matching_Agent,
    Interview_Planning_Agent,
    Final_Recommendation_Agent,
    Gap_Analysis_Agent,
    Report_Review_Agent
)
from tasks import (
   job_description_task,
   resume_extraction_task,
   skill_experience_matching_task,
   interview_planning_task,
   recommendation_task,
   gap_analysis_task,
   report_review_task
)


# Forming the tech-focused crew with some enhanced configurations
crew = Crew(
  agents=[job_description_agent,Resume_Extraction_Agent,Skill_Experience_Matching_Agent,Interview_Planning_Agent,Final_Recommendation_Agent,Gap_Analysis_Agent,Report_Review_Agent],
  tasks=[job_description_task,resume_extraction_task,skill_experience_matching_task,interview_planning_task,recommendation_task,gap_analysis_task,report_review_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=False,  # Disabled: memory requires OpenAI embeddings by default
  cache=False,   # Disabled: cache requires OpenAI embeddings by default
  max_rpm=100,
  share_crew=True
)

## start the task execution process with enhanced feedback
result=crew.kickoff(inputs={"candidate_id": "CAND-001"})
print(result)