from pydantic import BaseModel
from typing import List, Dict


class JDAnalysis(BaseModel):
    role_title: str
    required_skills: List[str]
    preferred_skills: List[str]
    responsibilities: List[str]
    experience_expectation: str
    evaluation_criteria: List[str]


class ResumeProfile(BaseModel):
    candidate_id: str
    candidate_name: str
    current_role: str
    years_experience: str
    skills: List[str]
    projects: List[str]
    experience_summary: List[str]
    education: List[str]
    certifications: List[str]


class MatchScore(BaseModel):
    matched_skills: List[str]
    partial_matches: List[str]
    missing_skills: List[str]
    category_scores: Dict[str, int]
    overall_score: int
    max_score: int
    percentage: float
    recommendation_band: str


class InterviewQuestions(BaseModel):
    technical_questions: List[str]
    project_deep_dive_questions: List[str]
    scenario_questions: List[str]
    gap_validation_questions: List[str]


class InterviewPlan(BaseModel):
    interview_focus_areas: List[str]
    technical_questions: List[str]
    project_deep_dive_questions: List[str]
    scenario_questions: List[str]
    gap_validation_questions: List[str]


class FinalReport(BaseModel):
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
