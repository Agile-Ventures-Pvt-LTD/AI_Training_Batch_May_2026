from crewai import Task
from pydantic import BaseModel, Field
from typing import List, Dict
from agents import job_description_analyst, resume_extraction_agent, skill_experience_matching_agent, interview_planning_agent, final_recommendation_agent, gap_analysis_agent, report_review_agent
from schemas import JDAnalysis, ResumeProfile, MatchScore, GapAnalysis, InterviewPlan, FinalReport, ReviewReport


analyze_jd_task = Task(
    description=(
        "Read and extract key details from the job description file located at '{jd_path}'. "
        "Identify the role title, core technical skills, nice-to-have capabilities, "
        "responsibilities, and target seniority levels."
    ),
    expected_output="A structured JSON object detailing the role requirements.",
    agent=job_description_analyst, # References your Job Description Analyst Agent
    output_json=JDAnalysis,
    output_file="outputs/jd_analysis.json"
)

extract_resume_task = Task(
    description=(
        "Locate the correct file for candidate ID '{candidate_id}'. "
        "Read the resume and extract structured profile data, covering metadata, "
        "skills, project history, and career timelines."
    ),
    expected_output="A structured profile JSON mapping the candidate's history.",
    agent=resume_extraction_agent, # References your Resume Extraction Agent
    output_json=ResumeProfile,
    output_file="outputs/resume_profile.json"
)

match_skills_task = Task(
    description=(
        "Compare the requirements from the extracted job description analysis with the "
        "extracted candidate profile. Use the screening rubric to compute category scores. "
        "Calculate the overall score, percentage, and recommendation band using the calculation tools."
    ),
    expected_output="A detailed score match card showing structural strengths and alignment math.",
    agent=skill_experience_matching_agent, # References your Skill and Experience Matching Agent
    output_json=MatchScore,
    output_file="outputs/match_score.json",
    context=[analyze_jd_task, extract_resume_task]
)

gap_analysis_task = Task(
    description=(
        "Review the matched skills results against the primary job requirements. "
        "Isolate missing capabilities, weak tech stacks, or domain experience flags. "
        "Categorize these entries cleanly into critical gaps, moderate gaps, and areas to probe."
    ),
    expected_output="A gap matrix organizing missing qualifications by severity tiers.",
    agent=gap_analysis_agent, # References your Gap Analysis Agent
    output_json=GapAnalysis,
    output_file="outputs/gap_analysis.json",
    context=[analyze_jd_task, extract_resume_task, match_skills_task]
)

# tasks.py ke andar plan_interview_task ko aise modify karein:
plan_interview_task = Task(
    description=(
        "Design a custom, target evaluation plan for the candidate based on the job requirements, "
        "resume profile, and calculated gap metrics. "
        "You must generate actual, detailed textual questions. Do not use generic placeholders like 'Q1' or 'Q2'.\n"
        "Strictly generate:\n"
        "- At least 3 detailed technical_questions probing deep software principles.\n"
        "- At least 2 project_deep_dive_questions focused on engineering trade-offs in their history.\n"
        "- At least 2 scenario_questions placing them in production-down or scaling situations.\n"
        "- At least 2 gap_validation_questions directly verifying the missing items found in gap analysis."
    ),
    expected_output="An interview blueprint script containing tailored real-world verification prompts.",
    agent=interview_planning_agent,
    output_json=InterviewPlan,
    output_file="outputs/interview_plan.json",
    context=[analyze_jd_task, extract_resume_task, match_skills_task, gap_analysis_task]
)


generate_report_task = Task(
    description=(
        "Synthesize all pipeline artifacts into a comprehensive master candidate screening report. "
        "Draft an insightful executive summary, highlight concrete textual evidence matching requirements, "
        "and package the interview questions. Save the verified report."
    ),
    expected_output="A master screening dossier structured for hiring manager evaluation.",
    agent=final_recommendation_agent, # References your Final Recommendation Agent
    output_json=FinalReport,
    output_file="outputs/candidate_screening_report.json",
    context=[analyze_jd_task, extract_resume_task, match_skills_task, gap_analysis_task, plan_interview_task]
)

review_report_task = Task(
    description=(
        "Audit the completed master screening report. Verify all schema fields are populated, "
        "crosscheck that calculations look accurate, and ensure textual evaluation evidence "
        "is specific and objective."
    ),
    expected_output="A quality assurance audit report clearing or flagging the final file.",
    agent=report_review_agent, # References your Report Review Agent
    output_json=ReviewReport,
    output_file="outputs/report_review.json",
    context=[generate_report_task]
)
