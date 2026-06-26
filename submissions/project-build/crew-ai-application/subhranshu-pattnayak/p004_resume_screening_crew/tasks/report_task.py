from crewai import Task
from schemas import FinalReport
from agents.report_writer import report_writer
from tools.save_report import save_report
from .jd_task import jd_task
from .resume_task import resume_task
from .matching_task import matching_task
from .interview_task import interview_task

report_task = Task(
    description="""
    
    Using the jd_task, resume_task, matching_task, interview_task as context generate the final candidate screening report.
    The screening report should include:
    Executive summary, Recommendation, Strengths, Gaps, Interview focus areas, Interview questions, Evidence, Human review note,
    Focus should remain on generation of a coherent, not confusing and holistic overview od the candidate for the job description.
    Do not invent any new information.
    Always mention:
    This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision.
    in human review note message.
    Return only structured information.
    Save the final report.
    """,

    expected_output="""
    A Final candidate screening report including:
    - candidate_id
    - candidate_name
    - role_title
    - overall_score
    - max_score
    - percentage
    - recommendation
    - executive_summary
    - strengths
    - gaps
    - interview_focus_areas
    - interview_questions
    - evidence
    - human_review_note
    """,

    agent=report_writer,
    context=[
        jd_task,
        resume_task,
        matching_task,
        interview_task
    ],
    tools=[
        save_report
    ],
    output_pydantic=FinalReport
)