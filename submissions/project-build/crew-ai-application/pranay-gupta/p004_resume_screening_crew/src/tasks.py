from crewai import Task
from src.schemas import JDAnalysis, ResumeProfile, MatchScore, GapAnalysis, InterviewPlan, ScreeningReport, ReportReview
from src.agents import (
    jd_analyst_agent, resume_extraction_agent, skill_matching_agent,
    gap_analysis_agent, interview_planning_agent, final_recommendation_agent,
    report_review_agent
)

def create_jd_analysis_task():
    return Task(
        description="Read the JD and extract role_title, required_skills, preferred_skills, responsibilities, experience_expectation, and evaluation_criteria.",
        expected_output="JDAnalysis JSON",
        agent=jd_analyst_agent,
        output_pydantic=JDAnalysis
    )

def create_resume_extraction_task(candidate_id, resume_path):
    return Task(
        description=f"Read resume at {resume_path} for {candidate_id}. Extract candidate_id, name, role, experience, skills, projects, education, certifications. Do not invent info.",
        expected_output="ResumeProfile JSON",
        agent=resume_extraction_agent,
        output_pydantic=ResumeProfile
    )

def create_skill_matching_task():
    return Task(
        description="Use rubric and skill_matcher tools. Score 8 categories 0-5 based on evidence. Use score_calculator tool. Return MatchScore JSON.",
        expected_output="MatchScore JSON",
        agent=skill_matching_agent,
        output_pydantic=MatchScore
    )

def create_gap_analysis_task():
    return Task(
        description="Based on matched/missing skills, identify critical_gaps, moderate_gaps, and areas_to_probe.",
        expected_output="GapAnalysis JSON",
        agent=gap_analysis_agent,
        output_pydantic=GapAnalysis
    )

def create_interview_planning_task():
    return Task(
        description="Generate >=3 technical, >=2 project deep-dive, >=2 scenario, and >=2 gap-validation questions based on resume and gaps.",
        expected_output="InterviewPlan JSON",
        agent=interview_planning_agent,
        output_pydantic=InterviewPlan
    )

def create_final_report_task(candidate_id):
    return Task(
        description=f"Create final report for {candidate_id}. Include scores, strengths, gaps, questions, and evidence. Use save_report_tool to save. Use validate_report_schema_tool.",
        expected_output="ScreeningReport JSON",
        agent=final_recommendation_agent,
        output_pydantic=ScreeningReport
    )

def create_report_review_task():
    return Task(
        description="Review final report for schema_valid and missing_sections. Return ReportReview JSON.",
        expected_output="ReportReview JSON",
        agent=report_review_agent,
        output_pydantic=ReportReview
    )

def build_tasks(candidate_id, resume_path):
    t1 = create_jd_analysis_task()
    t2 = create_resume_extraction_task(candidate_id, resume_path)
    
    t3 = create_skill_matching_task()
    t3.context = [t1, t2]
    
    t4 = create_gap_analysis_task()
    t4.context = [t3]
    
    t5 = create_interview_planning_task()
    t5.context = [t1, t2, t3, t4]
    
    t6 = create_final_report_task(candidate_id)
    t6.context = [t1, t2, t3, t4, t5]
    
    t7 = create_report_review_task()
    t7.context = [t6]
    
    return [t1, t2, t3, t4, t5, t6, t7]