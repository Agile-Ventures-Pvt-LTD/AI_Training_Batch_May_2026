from crewai import Task

from schemas import (
    JDAnalysisOutput,
    ResumeExtractionOutput,
    MatchingOutput,
    InterviewPlanOutput,
    FinalReportSchema
)

from agents import (
    jd_analyst_agent,
    resume_extractor_agent,
    matching_agent,
    interview_planner_agent,
    recommendation_agent
)

task_analyze_jd = Task(
    description=(
        "Use the read_job_description_tool to open and parse the job description at path: '{jd_path}'. "
        "Extract the official job title, isolate required technical core proficiencies from optional "
        "nice-to-have capabilities, and list out the fundamental day-to-day role responsibilities.\n\n"
        "CRITICAL FOR SYSTEM PARSING: You must output ONLY a valid json raw block data structure matching "
        "the requested keys exactly. Do NOT wrap your output in markdown codeblocks (do not use ```json). "
        "Do NOT include conversational introductory greetings or concluding signs. Output pure JSON format content data tokens only."
    ),
    expected_output="A structured Pydantic object containing the extracted role title, required skills, preferred skills, and core responsibilities.",
    output_json=JDAnalysisOutput,
    agent=jd_analyst_agent
)

task_extract_resume = Task(
    description=(
        "Using the candidate ID '{candidate_id}', call the candidate_index_lookup_tool to resolve the correct filename. "
        "Once the file is resolved, look inside the provided target folder path variable '{resumes_dir}' to locate the file. "
        "Execute the read_resume_tool on that combined absolute path location to extract the clean markdown resume text data content."
    ),
    expected_output="A structured candidate profile layout holding raw parsed information details.",
    output_json=ResumeExtractionOutput,
    agent=resume_extractor_agent
)

task_match_skills = Task(
    description=(
        "Execute the load_screening_rubric_tool to read the official 8 evaluation criteria categories. "
        "Systematically compare the candidate's extracted profile against the extracted job requirements. "
        "For each of the 8 categories, assign an objective score between 0 and 5 based on explicit historical evidence. "
        "Pass this dictionary of scores into the score_calculator_tool to safely compute the total score, percentage, "
        "and recommendation band. Explicitly compile text fragments as factual evidence for all strengths and gaps identified."
    ),
    expected_output="An evaluation breakdown matching the MatchingOutput layout, complete with calculator metrics, strengths, gaps, and categorical justification strings.",
    output_json=MatchingOutput,
    agent=matching_agent,
    context=[task_analyze_jd, task_extract_resume]
)

task_plan_interview = Task(
    description=(
        "Review the gaps, partial skill alignments, and weak-scoring categories discovered during the previous matching task. "
        "Formulate tailored technical and behavioral interview questions designed to challenge or verify those specific gaps. "
        "For every single question designed, explicitly state the structural 'intent' explaining what the interviewer is trying to uncover."
    ),
    expected_output="A targeted interview package outlining clear focal vectors paired with high-signal interview questions and core discovery intents.",
    output_json=InterviewPlanOutput,
    agent=interview_planner_agent,
    context=[task_match_skills]
)

task_generate_report = Task(
    description=(
        "Consolidate all calculated statistics, analysis parameters, interview maps, and textual evidence for candidate '{candidate_id}' "
        "into a single structured schema matching the final reporting requirements. Write a polished, professional executive summary "
        "evaluating the candidate's fitment. Generate a 'human_review_note' outlining nuanced edge cases or unique traits for HR review. "
        "Finally, call the save_report_tool to write this complete record as a JSON document into your designated outputs directory."
    ),
    expected_output="A complete FinalReportSchema instance successfully committed to disk via the file system save tool.",
    output_json=FinalReportSchema,
    agent=recommendation_agent,
    context=[task_analyze_jd, task_extract_resume, task_match_skills, task_plan_interview]
)
