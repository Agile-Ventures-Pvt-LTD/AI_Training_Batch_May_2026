import os
import csv
import json
from crewai import Crew, Process
from src.config import DATASET_PATH
from src.agents import (
    jd_analyst_agent,
    resume_extraction_agent,
    skill_matching_agent,
    gap_analysis_agent,
    interview_planning_agent,
    report_reviewer_agent,
    final_recommendation_agent
)
from src.tasks import (
    jd_analysis_task,
    resume_extraction_task,
    skill_matching_task,
    gap_analysis_task,
    interview_planning_task,
    report_review_task,
    final_recommendation_task
)

def lookup_for_candidate(candidate_id):
    """Helper to lookup candidate resume file and other details"""
    csv_path = os.path.join(DATASET_PATH, "metadata/candidate_index.csv")
            
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("candidate_id").strip() == candidate_id.strip():
                return row
    return None

def run_screening_for_candidate(candidate_id):

    cand_details = lookup_for_candidate(candidate_id)
    if not cand_details:
        raise ValueError(f"'{candidate_id}' not found")
        
    candidate_name = cand_details.get("candidate_name")
    resume_file = cand_details.get("resume_file")
    
    jd_path = "job_description/jd_ai_engineer.md"
    resume_path = f"resumes/{resume_file}"
    
    jd_analyst = jd_analyst_agent()
    resume_extractor = resume_extraction_agent()
    skill_matcher = skill_matching_agent()
    gap_analyst = gap_analysis_agent()
    interview_planner = interview_planning_agent()
    reviewer = report_reviewer_agent()
    final_recommender = final_recommendation_agent()
    
    jd_task = jd_analysis_task(jd_analyst, jd_path)
    resume_task = resume_extraction_task(resume_extractor, resume_path)
    match_task = skill_matching_task(skill_matcher, jd_task, resume_task)
    gap_task = gap_analysis_task(gap_analyst, jd_task, resume_task)
    
    interview_task = interview_planning_task(
        interview_planner, jd_task, resume_task, match_task, gap_task
    )
    
    review_task = report_review_task(
        reviewer, jd_task, resume_task, match_task, interview_task, gap_task
    )
    
    final_task = final_recommendation_task(
        final_recommender,
        candidate_id,
        jd_task,
        resume_task,
        match_task,
        interview_task,
        gap_task,
        review_task
    )
    
    crew = Crew(
        agents=[
            jd_analyst,
            resume_extractor,
            skill_matcher,
            gap_analyst,
            interview_planner,
            reviewer,
            final_recommender
        ],
        tasks=[
            jd_task,
            resume_task,
            match_task,
            gap_task,
            interview_task,
            review_task,
            final_task
        ],
        process=Process.sequential,
        verbose=True, 
        tracing=True
    )
    
    print(f"\nScreening resume of: {candidate_name} ({candidate_id})")
    
    inputs = {
        "jd_path": jd_path,
        "resume_path": resume_path,
        "candidate_id": candidate_id
    }
    
    result = crew.kickoff(inputs=inputs)
    
    output_dict = {}
    if hasattr(result, "json_dict") and result.json_dict:
        output_dict = result.json_dict
    elif hasattr(result, "raw") and result.raw:
        
        output_dict = json.loads(result.raw)
        
    else:
        try:
            output_dict = json.loads(str(result))
        except:
            pass
            
    return output_dict
