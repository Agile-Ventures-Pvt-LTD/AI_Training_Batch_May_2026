from crewai import Crew, Process
from agent import (
    job_description_analyst_agent, 
    resume_extraction_agent, 
    skill_matching_agent, 
    interview_planning_agent, 
    final_response_agent
)
from tasks import (
    task_analyze_job_description,
    resume_extractor,
    skill_matcher,
    task_generate_interview_plan,
    task_generate_final_report
)

def run_batch_screening():
    """Loops through candidates by cleanly binding dynamic task paths per iteration."""
    candidates = ["CAND-001", "CAND-002", "CAND-003"]
    
    for candidate_id in candidates:
        print(f"Starting :{candidate_id}")
        resume_extractor.output_file = f"outputs/{candidate_id}_resume_profile.json"
        skill_matcher.output_file = f"outputs/{candidate_id}_match_score.json"
        task_generate_interview_plan.output_file = f"outputs/{candidate_id}_interview_plan.json"
        task_generate_final_report.output_file = f"outputs/{candidate_id}_screening_report.json"
        local_crew = Crew(
            agents=[
                job_description_analyst_agent,
                resume_extraction_agent,
                skill_matching_agent,
                interview_planning_agent,
                final_response_agent
            ],
            tasks=[
                task_analyze_job_description,
                resume_extractor,
                skill_matcher,
                task_generate_interview_plan,
                task_generate_final_report
            ],
            process=Process.sequential,
            verbose=True
        )
        local_crew.kickoff(inputs={"candidate_id": candidate_id})
        print(f"Finished processing {candidate_id}!")

if __name__ == "__main__":
    run_batch_screening()
