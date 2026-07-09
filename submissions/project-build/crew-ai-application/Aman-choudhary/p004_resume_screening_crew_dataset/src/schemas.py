from typing import Dict, List
from pydantic import BaseModel, Field
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
class ReportReview(BaseModel):
    report_complete: bool
    missing_sections: List[str]
    schema_valid: bool
    review_notes: List[str]
class ScreeningReport(BaseModel):
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
    interview_questions: Dict
    evidence: List[str]
    human_review_note: str = Field(
        default=(
            "This is an AI-assisted screening report based on "
            "the provided resume and job description. "
            "A human reviewer should validate the recommendation "
            "before making any recruitment decision."))

def validate_report(report_data: Dict) -> ScreeningReport:
    """
    Validate final report schema.
    """
    return ScreeningReport(**report_data)