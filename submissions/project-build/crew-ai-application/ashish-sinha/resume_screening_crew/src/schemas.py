from pydantic import BaseModel, Field
from typing import List, Dict

class JobDescriptionAnalysis(BaseModel):
    role_title: str = Field(description="Target role name.")
    required_skills: List[str] = Field(description="Mandatory core skill sets.")
    preferred_skills: List[str] = Field(description="Nice-to-have auxiliary skills.")
    responsibilities: List[str] = Field(description="Main tasks listed in the JD.")
    experience_expectation: str = Field(description="Expected years or depth of expertise.")
    evaluation_criteria: List[str] = Field(description="Rubric evaluation points derived.")

class CandidateProfile(BaseModel):
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
    python_programming: int
    sql_database_skills: int
    api_integration: int
    llm_application_development: int
    agent_frameworks: int
    rag_understanding: int
    testing_and_quality: int
    communication: int

class SkillMatchReport(BaseModel):
    matched_skills: List[str]
    partial_matches: List[str]
    missing_skills: List[str]
    category_scores: CategoryScores
    overall_score: int
    max_score: int = 40
    percentage: float
    recommendation_band: str

class GapAnalysisReport(BaseModel):
    critical_gaps: List[str]
    moderate_gaps: List[str]
    areas_to_probe: List[str]

class InterviewPlan(BaseModel):
    interview_focus_areas: List[str]
    technical_questions: List[str]
    project_deep_dive_questions: List[str]
    scenario_questions: List[str]
    gap_validation_questions: List[str]

class ReportReviewStatus(BaseModel):
    report_complete: bool
    missing_sections: List[str]
    schema_valid: bool
    review_notes: List[str]

class FinalScreeningReport(BaseModel):
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