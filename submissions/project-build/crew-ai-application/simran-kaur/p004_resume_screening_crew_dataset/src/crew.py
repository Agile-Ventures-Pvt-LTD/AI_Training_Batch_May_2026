from crewai import Crew, Process
from agents import job_description_analyst,resume_extraction_agent,skill_and_experience_matching_agent,interview_planning_agent,recommendation_agent
from tasks import job_description_task,resume_extraction_task,skill_matching_task,interview_planning_task,interview_planning_task,recommendation_task



# Forming the tech-focused crew with some enhanced configurations
run_crew = Crew(
  agents=[job_description_analyst, resume_extraction_agent, skill_and_experience_matching_agent,interview_planning_agent,recommendation_agent],
  tasks=[job_description_task,resume_extraction_task,skill_matching_task,interview_planning_task,recommendation_task],
  process=Process.sequential,  # Optional: Sequential task execution is default
  memory=False,  # Disabled: memory requires OpenAI embeddings by default
  cache=False,   # Disabled: cache requires OpenAI embeddings by default
  max_rpm=10,
  share_crew=True
)


# start the task execution process with enhanced feedback

# result = crew.kickoff(inputs={'topic': 'Python for AI - Full Beginner Course'})
# print(result)