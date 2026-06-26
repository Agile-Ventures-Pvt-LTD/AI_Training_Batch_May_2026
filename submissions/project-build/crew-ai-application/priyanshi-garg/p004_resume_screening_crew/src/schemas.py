from pydantic import BaseModel, Field
from typing import List, Dict

class JDAnalysis(BaseModel):
    role_title: str = Field(..., description="The official job title")
    required_skills: List[str] = Field(..., description="List of mandatory technical skills")
    preferred_skills: List[str] = Field(..., description="List of optional/nice-to-have skills")
    responsibilities: List[str] = Field(..., description="Key duties of the role")
    experience_expectation: str = Field(..., description="Expected years or depth of experience")
    evaluation_criteria: List[str] = Field(..., description="Points used to grade candidates")

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

from pydantic import BaseModel, Field, field_validator
from typing import List, Dict

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
    interview_questions: Dict[str, List[str]]
    evidence: List[str]
    human_review_note: str

    @field_validator("human_review_note")
    @classmethod
    def validate_review_note(cls, value: str) -> str:
        required_text = "This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision."
        # Extra spaces ya case mismatches ko bypass karne ke liye generic clean checks
        if required_text.lower().replace(" ", "") not in value.lower().replace(" ", ""):
            raise ValueError(f"human_review_note must match the required disclaimer exactly.")
        return value

class ReviewReport(BaseModel):
    report_complete: bool
    missing_sections: List[str]
    schema_valid: bool
    review_notes: List[str]
