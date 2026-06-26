from crewai import Task
from crewai.tools import tool
from src.tools import (
    read_job_description_tool as _read_job_description_tool,
    read_resume_tool as _read_resume_tool,
    skill_matcher as _skill_matcher,
    find_resume as _find_resume,
    calculate_score as _calculate_score,
    LoadScreeningRubric,
    validate_report as _validate_report,
    save_report_tool as _save_report_tool
)
from src.agents import (
    job_description_agent,
    Resume_Extraction_Agent,
    Skill_Experience_Matching_Agent,
    save_report_Agent,
    Interview_Planning_Agent,
    Final_Recommendation_Agent,
    Gap_Analysis_Agent,
    Report_Review_Agent
)

read_job_description_tool = tool("Read Job Description File")(_read_job_description_tool)
read_resume_tool = tool("Read Resume File")(_read_resume_tool)
skill_matcher = tool("Match Candidate Skills")(_skill_matcher)
find_resume = tool("Find Resume Path")(_find_resume)
validate_report = tool("Validate Screening Report")(_validate_report)
save_report_tool = tool("Save Screening Report")(_save_report_tool)

@tool("Calculate Candidate Score")
def calculate_score_tool(scores: dict) -> dict:
    return _calculate_score(scores)

job_description_task = Task(
    description=(
        "Analyze the job description at '{job_description_path}'. "
        "Extract the job title, role title, required skills, preferred skills, "
        "responsibilities, experience expectation, and evaluation criteria."
    ),
    expected_output='A structured report detailing all the key parameters and requirements of the job description.',
    tools=[read_job_description_tool],
    agent=job_description_agent
)

resume_extraction_task = Task(
    description=(
        "Analyze the candidate resume at '{resume_path}'. "
        "Extract the candidate ID, candidate name, current role, years of experience, "
        "skills, projects, experience summary, education, and certifications."
    ),
    expected_output='A structured profile of the candidate containing all extracted details.',
    tools=[read_resume_tool],
    agent=Resume_Extraction_Agent
)

skill_experience_matching_task = Task(
    description=(
        "Compare the job description requirements with the extracted candidate profile. "
        "Evaluate the candidate across the 8 categories of the screening rubric: "
        "1. python_programming\n"
        "2. sql_database_skills\n"
        "3. api_integration\n"
        "4. llm_application_development\n"
        "5. agent_frameworks\n"
        "6. rag_understanding\n"
        "7. testing_and_quality\n"
        "8. communication\n"
        "For each category, assign a score from 0 to 5 based on the candidate's skills and experience. "
        "Identify matched skills, partial matches, and missing skills."
    ),
    expected_output='A detailed matching report with category scores (0-5) and matching/missing skills lists.',
    tools=[skill_matcher],
    context=[job_description_task, resume_extraction_task],
    agent=Skill_Experience_Matching_Agent
)

interview_planning_task = Task(
    description=(
        "Based on the job description, candidate resume, and matching results, "
        "generate candidate-specific interview questions. "
        "Include technical questions, project deep dive questions, scenario questions, "
        "and gap validation questions."
    ),
    expected_output='A customized interview plan with specific questions in each category.',
    tools=[find_resume],
    context=[job_description_task, resume_extraction_task, skill_experience_matching_task],
    agent=Interview_Planning_Agent
)

gap_analysis_task = Task(
    description=(
        "Identify missing or weak areas in the candidate's profile relative to the job requirements. "
        "Categorize gaps into critical gaps, moderate gaps, and areas to probe."
    ),
    expected_output='A gap analysis report detailing weak or missing areas.',
    context=[job_description_task, resume_extraction_task, skill_experience_matching_task],
    agent=Gap_Analysis_Agent
)

recommendation_task = Task(
    description=(
        "Generate the final recommendations. Compute the overall score (sum of the 8 category scores) "
        "and the percentage. Determine the recommendation band: "
        "- STRONG_MATCH (80% - 100%, score 32-40)\n"
        "- MODERATE_MATCH (60% - 79%, score 24-31)\n"
        "- WEAK_MATCH (40% - 59%, score 16-23)\n"
        "- NEEDS_MANUAL_REVIEW (Below 40%, score 0-15)\n"
        "Provide an executive summary, list of strengths, gaps, interview focus areas, "
        "and draft the human review note."
    ),
    expected_output='A recommendation report specifying the score, percentage, band, and summary.',
    context=[job_description_task, resume_extraction_task, skill_experience_matching_task, interview_planning_task, gap_analysis_task],
    agent=Final_Recommendation_Agent
)

report_review_task = Task(
    description=(
        "Review the final report for completeness, schema consistency, and evidence quality. "
        "Ensure all fields are present and valid."
    ),
    expected_output='A review report confirming validation status.',
    tools=[validate_report],
    context=[recommendation_task],
    agent=Report_Review_Agent
)

save_report_task = Task(
    description=(
        "Save the final screening report to the outputs/ folder. "
        "Ensure the file name is '{candidate_id}_screening_report.json'."
    ),
    expected_output='The file path where the report was successfully saved.',
    tools=[save_report_tool],
    context=[recommendation_task, report_review_task],
    agent=save_report_Agent
)
