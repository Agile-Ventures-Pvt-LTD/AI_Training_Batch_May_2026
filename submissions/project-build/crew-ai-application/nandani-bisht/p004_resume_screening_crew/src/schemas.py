from pydantic import BaseModel, Field
from typing import List

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

class CategoryScores(BaseModel):
    python_programming: int = Field(ge=0, le=5)
    sql_database_skills: int = Field(ge=0, le=5)
    api_integration: int = Field(ge=0, le=5)
    llm_application_development: int = Field(ge=0, le=5)
    agent_frameworks: int = Field(ge=0, le=5)
    rag_understanding: int = Field(ge=0, le=5)
    testing_and_quality: int = Field(ge=0, le=5)
    communication: int = Field(ge=0, le=5)

class MatchScore(BaseModel):
    matched_skills: List[str]
    partial_matches: List[str]
    missing_skills: List[str]
    category_scores: CategoryScores
    overall_score: int
    max_score: int = 40
    percentage: float
    recommendation_band: str

class GapAnalysis(BaseModel):
    critical_gaps: List[str]
    moderate_gaps: List[str]
    areas_to_probe: List[str]

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
    max_score: int = 40
    percentage: float
    recommendation: str
    executive_summary: str
    strengths: List[str]
    gaps: List[str]
    interview_focus_areas: List[str]
    interview_questions: InterviewPlan
    evidence: List[str]
    human_review_note: str