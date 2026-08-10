from pydantic import BaseModel, Field
from typing import List, Optional


class JDRequirement(BaseModel):
    role_title: str = ""
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    responsibilities: List[str] = []
    experience_expectation: str = ""
    evaluation_criteria: List[str] = []


class ResumeProfile(BaseModel):
    candidate_id: str = ""
    candidate_name: str = ""
    current_role: str = ""
    years_experience: str = ""
    skills: List[str] = []
    projects: List[str] = []
    experience_summary: List[str] = []
    education: List[str] = []
    certifications: List[str] = []


class CategoryScores(BaseModel):
    python_programming: int = 0
    sql_database_skills: int = 0
    api_integration: int = 0
    llm_application_development: int = 0
    agent_frameworks: int = 0
    rag_understanding: int = 0
    testing_and_quality: int = 0
    communication: int = 0


class MatchScore(BaseModel):
    matched_skills: List[str] = []
    partial_matches: List[str] = []
    missing_skills: List[str] = []
    category_scores: CategoryScores = Field(default_factory=CategoryScores)
    overall_score: int = 0
    max_score: int = 40
    percentage: float = 0.0
    recommendation_band: str = ""


class InterviewQuestions(BaseModel):
    technical_questions: List[str] = []
    project_deep_dive_questions: List[str] = []
    scenario_questions: List[str] = []
    gap_validation_questions: List[str] = []


class InterviewPlan(BaseModel):
    interview_focus_areas: List[str] = []
    technical_questions: List[str] = []
    project_deep_dive_questions: List[str] = []
    scenario_questions: List[str] = []
    gap_validation_questions: List[str] = []


class FinalReport(BaseModel):
    candidate_id: str = ""
    candidate_name: str = ""
    role_title: str = ""
    overall_score: int = 0
    max_score: int = 40
    percentage: float = 0.0
    recommendation: str = ""
    executive_summary: str = ""
    strengths: List[str] = []
    gaps: List[str] = []
    interview_focus_areas: List[str] = []
    interview_questions: InterviewQuestions = Field(default_factory=InterviewQuestions)
    evidence: List[str] = []
    human_review_note: str = ""


class GapAnalysis(BaseModel):
    critical_gaps: List[str] = []
    moderate_gaps: List[str] = []
    areas_to_probe: List[str] = []


class ReportReview(BaseModel):
    report_complete: bool = False
    missing_sections: List[str] = []
    schema_valid: bool = False
    review_notes: List[str] = []