from crewai import Task

from agents import (
    gap_analyst,
    interview_planner,
    jd_analyst,
    recommendation_agent,
    report_reviewer,
    resume_extractor,
    skill_matcher,
)

from schemas import (
    CandidateScreeningReport,
    GapAnalysis,
    InterviewPlan,
    JDAnalysis,
    MatchScore,
    ReportReview,
    ResumeProfile,
)

jd_analysis_task = Task(
    description="""
Read the job description from:

{jd_path}

Extract:

- role title
- required skills
- preferred skills
- responsibilities
- experience expectation
- evaluation criteria
""",
    expected_output="Structured job description.",
    agent=jd_analyst,
    output_pydantic=JDAnalysis,
)

resume_extraction_task = Task(
    description="""
Candidate ID:

{candidate_id}

Resume:

{resume_file}

Extract the candidate profile.
""",
    expected_output="Structured resume profile.",
    agent=resume_extractor,
    context=[
        jd_analysis_task,
    ],
    output_pydantic=ResumeProfile,
)

skill_matching_task = Task(
    description="""
Compare the resume against the job description.

Generate:

- matched skills
- partial matches
- missing skills
- category scores
- overall score
- recommendation
""",
    expected_output="Candidate score.",
    agent=skill_matcher,
    context=[
        jd_analysis_task,
        resume_extraction_task,
    ],
    output_pydantic=MatchScore,
)

gap_analysis_task = Task(
    description="""
Identify the candidate gaps.
""",
    expected_output="Gap analysis.",
    agent=gap_analyst,
    context=[
        skill_matching_task,
    ],
    output_pydantic=GapAnalysis,
)

interview_planning_task = Task(
    description="""
Generate interview questions.
""",
    expected_output="Interview plan.",
    agent=interview_planner,
    context=[
        resume_extraction_task,
        gap_analysis_task,
    ],
    output_pydantic=InterviewPlan,
)

recommendation_task = Task(
    description="""
Generate the final screening report.
""",
    expected_output="Final report.",
    agent=recommendation_agent,
    context=[
        jd_analysis_task,
        resume_extraction_task,
        skill_matching_task,
        gap_analysis_task,
        interview_planning_task,
    ],
    output_pydantic=CandidateScreeningReport,
)

report_review_task = Task(
    description="""
Validate the final report.
""",
    expected_output="Review result.",
    agent=report_reviewer,
    context=[
        recommendation_task,
    ],
    output_pydantic=ReportReview,
)