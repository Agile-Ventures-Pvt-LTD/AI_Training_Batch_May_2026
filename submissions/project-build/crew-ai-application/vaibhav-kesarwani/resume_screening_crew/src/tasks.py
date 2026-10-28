from crewai import Task
from src.agents import (
    manager,
    job_description,
    resume_extraction,
    experience_matching,
    interview_planning,
    final_recommendation,
    gap_analysis,
    report_review
)
from src.prompts import (
    manager_ds,
    manager_eo,
    job_description_ds,
    job_description_eo,
    resume_extraction_ds,
    resume_extraction_eo,
    experience_matching_ds,
    experience_matching_eo,
    interview_planning_ds,
    interview_planning_eo,
    final_recommendation_ds,
    final_recommendation_eo,
    gap_analysis_ds,
    gap_analysis_eo,
    report_review_ds,
    report_review_eo
)

manager_task = Task(
    description=manager_ds,
    expected_output=manager_eo,
    agent=manager,
    output_file="task_reasoning/manager_task.md"
)


job_description_task = Task(
    description=job_description_ds,
    expected_output=job_description_eo,
    agent=job_description,
    output_file="task_reasoning/job_description_task.md"
)


resume_extraction_task = Task(
    description=resume_extraction_ds,
    expected_output=resume_extraction_eo,
    agent=resume_extraction,
    output_file="task_reasoning/resume_extraction_task.md"
)


experience_matching_task = Task(
    description=experience_matching_ds,
    expected_output=experience_matching_eo,
    agent=experience_matching,
    output_file="task_reasoning/experience_matching_task.md"
)


interview_planning_task = Task(
    description=interview_planning_ds,
    expected_output=interview_planning_eo,
    agent=interview_planning,
    output_file="task_reasoning/interview_planning_task.md"
)


final_recommendation_task = Task(
    description=final_recommendation_ds,
    expected_output=final_recommendation_eo,
    agent=final_recommendation,
    output_file="task_reasoning/final_recommendation_task.md"
)


gap_analysis_task = Task(
    description=gap_analysis_ds,
    expected_output=gap_analysis_eo,
    agent=gap_analysis,
    output_file="task_reasoning/gap_analysis_task.md"
)


report_review_task = Task(
    description=report_review_ds,
    expected_output=report_review_eo,
    agent=report_review,
    output_file="task_reasoning/report_review_task.md"
)