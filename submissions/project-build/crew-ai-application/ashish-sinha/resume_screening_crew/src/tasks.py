import os
from crewai import Task
from schemas import (
    JobDescriptionAnalysis, 
    CandidateProfile, 
    SkillMatchReport,
    GapAnalysisReport, 
    InterviewPlan, 
    FinalScreeningReport, 
    ReportReviewStatus
)

class ResumeScreeningTasks:
    def jd_analysis_task(self, agent, jd_path: str) -> Task:
        return Task(
            description=f"Analyze the job criteria inside file: {jd_path}. Extract mandatory vs preferred requirements.",
            expected_output="JSON metrics breakdown matching the JobDescriptionAnalysis schema.",
            agent=agent,
            output_json=JobDescriptionAnalysis
        )

    def resume_extraction_task(self, agent, resume_path: str, candidate_id: str) -> Task:
        return Task(
            description=f"Extract resume features cleanly for candidate {candidate_id} from path: {resume_path}.",
            expected_output="Structured personal experience profile matching the CandidateProfile schema.",
            agent=agent,
            output_json=CandidateProfile
        )

    def skill_matching_task(self, agent, context_tasks: list) -> Task:
        return Task(
            description="Score candidate competency across all 8 rubric categories using metrics tools. Ensure explicit calculation values mapping perfectly to 0-5 limitations.",
            expected_output="Comprehensive skill match classification report matching the SkillMatchReport schema.",
            agent=agent,
            context=context_tasks,
            output_json=SkillMatchReport
        )

    def gap_analysis_task(self, agent, context_tasks: list) -> Task:
        return Task(
            description="Isolate explicit technical gaps, missing structural skills, or timeline limitations separately.",
            expected_output="Categorized risk profile matrix matching the GapAnalysisReport schema.",
            agent=agent,
            context=context_tasks,
            output_json=GapAnalysisReport
        )

    def interview_planning_task(self, agent, context_tasks: list) -> Task:
        return Task(
            description="Generate candidate-specific interview plan framework. Requirements: At least 3 technical, 2 deep-dives, 2 scenarios, and 2 gap-validation questions.",
            expected_output="Structured behavioral and domain questionnaire matching the InterviewPlan schema.",
            agent=agent,
            context=context_tasks,
            output_json=InterviewPlan
        )

    def final_recommendation_task(self, agent, context_tasks: list) -> Task:
        return Task(
            description="Integrate complete data into a final recommendation block. Output MUST match FinalScreeningReport schema parameter fields explicitly.",
            expected_output="Consolidated master application evaluation dashboard data matching the FinalScreeningReport schema.",
            agent=agent,
            context=context_tasks,
            output_json=FinalScreeningReport
        )

    def quality_control_task(self, agent, context_tasks: list) -> Task:
        return Task(
            description="Perform structural validation checks over the final report. Ensure human_review_note parameter contains exact mandated legal framing wording.",
            expected_output="System QA sign-off confirming execution structural parameters match the ReportReviewStatus schema.",
            agent=agent,
            context=context_tasks,
            output_json=ReportReviewStatus
        )
