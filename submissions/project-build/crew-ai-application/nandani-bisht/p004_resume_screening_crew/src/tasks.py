from crewai import Task
from agents import (
    get_jd_analyst,
    get_resume_extractor,
    get_skill_matcher,
    get_gap_analyst,
    get_interview_planner,
    get_final_recommender,
    get_report_reviewer
)

def get_jd_task(jd_path: str):
    return Task(
        description=f"Read the job description at {jd_path} and extract structured data. Output strictly valid JSON matching the JDAnalysis schema.",
        expected_output="A JSON object containing role_title, required_skills, preferred_skills, responsibilities, experience_expectation, and evaluation_criteria.",
        agent=get_jd_analyst()
    )

def get_resume_task(candidate_id: str):
    return Task(
        description=f"Look up candidate {candidate_id}, read their resume, and extract their profile. Output strictly valid JSON matching the ResumeProfile schema. Do not invent skills.",
        expected_output="A JSON object containing candidate_id, candidate_name, current_role, years_experience, skills, projects, experience_summary, education, and certifications.",
        agent=get_resume_extractor()
    )

def get_matching_task():
    return Task(
        description="Use the JD analysis and Resume profile. Use the skill_matcher_tool and score_calculator_tool. Output strictly valid JSON matching the MatchScore schema.",
        expected_output="A JSON object with matched_skills, partial_matches, missing_skills, category_scores, overall_score, max_score, percentage, and recommendation_band.",
        agent=get_skill_matcher()
    )

def get_gap_task():
    return Task(
        description="Analyze the MatchScore and ResumeProfile to identify gaps. Output strictly valid JSON matching the GapAnalysis schema.",
        expected_output="A JSON object containing critical_gaps, moderate_gaps, and areas_to_probe.",
        agent=get_gap_analyst()
    )

def get_interview_task():
    return Task(
        description="Generate an interview plan based on the JD, Resume, MatchScore, and GapAnalysis. Output strictly valid JSON matching the InterviewPlan schema. Include exactly 3 technical, 2 project, 2 scenario, and 2 gap-validation questions.",
        expected_output="A JSON object containing interview_focus_areas, technical_questions, project_deep_dive_questions, scenario_questions, and gap_validation_questions.",
        agent=get_interview_planner()
    )

def get_recommendation_task(candidate_id: str):
    return Task(
        description=f"Synthesize all previous outputs into the final screening report for {candidate_id}. Use the save_report_tool to save it. Output strictly valid JSON matching the FinalReport schema. The human_review_note must be exactly: 'This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision.'",
        expected_output="A comprehensive JSON report saved to the outputs directory and returned as a JSON string.",
        agent=get_final_recommender()
    )

def get_review_task():
    return Task(
        description="Validate the final report JSON using the validate_report_schema_tool. Ensure all fields are present and the recommendation matches the score band. Output a brief validation summary.",
        expected_output="A validation summary confirming schema validity and data consistency.",
        agent=get_report_reviewer()
    )