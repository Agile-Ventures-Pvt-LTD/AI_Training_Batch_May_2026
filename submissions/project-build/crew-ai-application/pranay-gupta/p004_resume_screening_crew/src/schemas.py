from pydantic import BaseModel, field_validator
from typing import List, Dict, Literal
from src.config import MAX_SCORE, RUBRIC_CATEGORIES, HUMAN_REVIEW_NOTE

RecommendationBand = Literal["STRONG_MATCH", "MODERATE_MATCH", "WEAK_MATCH", "NEEDS_MANUAL_REVIEW"]

class JDAnalysis(BaseModel):
    role_title: str
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    responsibilities: List[str] = []
    experience_expectation: str = ""
    evaluation_criteria: List[str] = []

class Project(BaseModel):
    name: str
    description: str = ""
    technologies: List[str] = []

class ExperienceEntry(BaseModel):
    role: str
    company: str = ""
    duration: str = ""
    summary: str = ""

class EducationEntry(BaseModel):
    degree: str
    institution: str = ""
    year: str = ""

class ResumeProfile(BaseModel):
    candidate_id: str
    candidate_name: str
    current_role: str = ""
    years_experience: str = ""
    skills: List[str] = []
    projects: List[Project] = []
    experience_summary: List[ExperienceEntry] = []
    education: List[EducationEntry] = []
    certifications: List[str] = []

class MatchScore(BaseModel):
    matched_skills: List[str] = []
    partial_matches: List[str] = []
    missing_skills: List[str] = []
    category_scores: Dict[str, int]
    overall_score: int
    max_score: int = MAX_SCORE
    percentage: float
    recommendation_band: RecommendationBand

    @field_validator("category_scores")
    def check_categories(cls, v):
        if set(v.keys()) != set(RUBRIC_CATEGORIES):
            raise ValueError("Invalid categories")
        for score in v.values():
            if not (0 <= score <= 5):
                raise ValueError("Scores must be 0-5")
        return v

class GapAnalysis(BaseModel):
    critical_gaps: List[str] = []
    moderate_gaps: List[str] = []
    areas_to_probe: List[str] = []

class InterviewPlan(BaseModel):
    interview_focus_areas: List[str] = []
    technical_questions: List[str] = []
    project_deep_dive_questions: List[str] = []
    scenario_questions: List[str] = []
    gap_validation_questions: List[str] = []

class InterviewQuestions(BaseModel):
    technical_questions: List[str] = []
    project_deep_dive_questions: List[str] = []
    scenario_questions: List[str] = []
    gap_validation_questions: List[str] = []

class ScreeningReport(BaseModel):
    candidate_id: str
    candidate_name: str
    role_title: str
    overall_score: int
    max_score: int = MAX_SCORE
    percentage: float
    recommendation: RecommendationBand
    executive_summary: str
    strengths: List[str] = []
    gaps: List[str] = []
    interview_focus_areas: List[str] = []
    interview_questions: InterviewQuestions
    evidence: List[str] = []
    human_review_note: str = HUMAN_REVIEW_NOTE

class ReportReview(BaseModel):
    report_complete: bool
    missing_sections: List[str] = []
    schema_valid: bool
    review_notes: List[str] = []