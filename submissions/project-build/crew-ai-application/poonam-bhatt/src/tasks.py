from crewai import Task
from tools import read_job_description_tool,read_resume_tool,skill_matcher, find_resume,calculate_score,LoadScreeningRubric,validate_report,save_report_tool
from agents import (job_description_agent,Resume_Extraction_Agent,Skill_Experience_Matching_Agent,save_report_Agent,
Interview_Planning_Agent, Final_Recommendation_Agent, Gap_Analysis_Agent, Report_Review_Agent)

## Research Task
job_description_task = Task(
  description=(
    "Identify the jd {job_description}."
    "Get detailed information about the video from the job description."
  ),
  expected_output='A consise 2 paragraphs report based on the {job_description} of jd.',
  tools=[read_job_description_tool],
  agent=job_description_agent,
  async_execution=True
)


resume_extraction_task = Task(
  description=(
    "Extract the detail from  {resume}."
    "Get detailed information about the candidate from the resume."
  ),
  expected_output='A consise 2 paragraphs report based on the {resume} of candidate.',
  tools=[read_resume_tool],
  agent=Resume_Extraction_Agent,
  async_execution=True
)




skill_experience_matching_task = Task(
  description=(
    "compare the detail from  {job_description} and {resume}."
    "find the matching skills and experience of candidate with jd ."
  ),
  expected_output='create a report based on the {job_description} and {resume} of candidate.',
  tools=[skill_matcher],
  agent=Skill_Experience_Matching_Agent,
  async_execution=True
)



interview_planning_task = Task(
  description=(
    "you need to create the interview question based on the candidate {candidate}"
    "find the matching skills and experience of candidate with jd ."
  ),
  expected_output='create a report based on the question created for candidate.',
  tools=[find_resume],
  agent=Interview_Planning_Agent,
  async_execution=True
)



recommendation_task = Task(
  description=(
    "compare the detail from  {job_description} and {resume}."
    "find the matching skills and experience of candidate with jd ."
  ),
  expected_output='create a report based on the {job_description} and {resume} of candidate.',
  tools=[calculate_score],
  agent=Final_Recommendation_Agent,
  async_execution=True
)




gap_analysis_task = Task(
  description=(
    "analyze the gap in the candidate ."
    "Find all the gaps that are in a particular candidate based on job description ."
  ),
  expected_output='create a report of a candidate with all the gaps found.',
  tools=[LoadScreeningRubric],
  agent=Gap_Analysis_Agent,
  async_execution=True
)


report_review_task = Task(
  description=(
    "review the given report and find the missing pointers"
    "give the score to the report along with missing area mention."
  ),
  expected_output='create a report based on the {report}.',
  tools=[validate_report],
  agent=Report_Review_Agent,
  async_execution=True
  
)




save_report_task = Task(
  description=(
    "save the report "
  ),
  expected_output='save the report using given tools and agents.',
  tools=[save_report_tool],
  agent=save_report_Agent,
  async_execution=True
  
)

