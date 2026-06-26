from pydantic import BaseModel
from typing import List, Dict


class InterviewQuestions(BaseModel):
    technical_questions: List[str]
    project_deep_dive_questions: List[str]
    scenario_questions: List[str]
    gap_validation_questions: List[str]


class CandidateReport(BaseModel):
    candidate_id: str
    candidate_name: str
    role_title: str

    overall_score: int
    max_score: int
    percentage: float
    recommendation: str

    executive_summary: str
    strengths: List[str]
    gaps: List[str]

    interview_focus_areas: List[str]
    interview_questions: InterviewQuestions

    evidence: List[str]
    human_review_note: str