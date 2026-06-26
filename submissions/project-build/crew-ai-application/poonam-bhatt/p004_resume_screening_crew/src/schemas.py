from pydantic import BaseModel, Field
from typing import List

class InterviewQuestions(BaseModel):
    technical_questions: List[str] = Field(..., description="List of technical questions based on the candidate's experience and role requirements.")
    project_deep_dive_questions: List[str] = Field(..., description="List of project deep dive questions based on the projects in candidate's resume.")
    scenario_questions: List[str] = Field(..., description="List of scenario-based questions to evaluate soft skills and situational judgment.")
    gap_validation_questions: List[str] = Field(..., description="List of questions to validate gaps or weak areas identified in the screening.")

class ScreeningReport(BaseModel):
    candidate_id: str = Field(..., description="Candidate ID (e.g. CAND-001)")
    candidate_name: str = Field(..., description="Name of the candidate")
    role_title: str = Field(..., description="Role title (e.g. AI Engineer)")
    overall_score: int = Field(..., description="Overall fitment score (sum of the 8 category scores, 0-40)")
    max_score: int = Field(default=40, description="Maximum possible score (40)")
    percentage: float = Field(..., description="Overall fitment percentage (overall_score / 40 * 100)")
    recommendation: str = Field(..., description="Recommendation band: STRONG_MATCH (80-100), MODERATE_MATCH (60-79), WEAK_MATCH (40-59), NEEDS_MANUAL_REVIEW (0-39)")
    executive_summary: str = Field(..., description="A concise executive summary of the candidate's fit for the role.")
    strengths: List[str] = Field(..., description="Key strengths identified from the resume.")
    gaps: List[str] = Field(..., description="Identified gaps or missing skills based on the job description.")
    interview_focus_areas: List[str] = Field(..., description="Focus areas for the interview.")
    interview_questions: InterviewQuestions = Field(..., description="Categorized interview questions.")
    evidence: List[str] = Field(..., description="Detailed evidence justifying the category scores and evaluation results.")
    human_review_note: str = Field(..., description="Note for human review.")
