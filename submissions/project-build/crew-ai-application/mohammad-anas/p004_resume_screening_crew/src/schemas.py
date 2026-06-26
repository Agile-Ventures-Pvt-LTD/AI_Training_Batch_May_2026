from pydantic import BaseModel


class JDAnalysis(BaseModel):
    role_title: str
    required_skills: list[str]
    preferred_skills: list[str]
    responsibilities: list[str]
    experience_expectation: str
    evaluation_criteria: list[str]


class ResumeProfile(BaseModel):
    candidate_id: str
    candidate_name: str
    current_role: str
    years_experience: str
    skills: list[str]
    projects: list[str]
    experience_summary: str
    education: list[str]
    certifications: list[str]


class MatchScore(BaseModel):
    matched_skills: list[str]
    partial_matches: list[str]
    missing_skills: list[str]
    category_scores: dict[str, int]
    overall_score: int
    max_score: int
    percentage: float
    recommendation: str


class GapAnalysis(BaseModel):
    critical_gaps: list[str]
    moderate_gaps: list[str]
    areas_to_probe: list[str]


class InterviewPlan(BaseModel):
    interview_focus_areas: list[str]
    technical_questions: list[str]
    project_deep_dive_questions: list[str]
    scenario_questions: list[str]
    gap_validation_questions: list[str]


class CandidateScreeningReport(BaseModel):
    candidate_id: str
    candidate_name: str
    role_title: str
    overall_score: int
    max_score: int
    percentage: float
    recommendation: str
    executive_summary: str
    strengths: list[str]
    gaps: list[str]
    interview_focus_areas: list[str]
    interview_questions: InterviewPlan
    evidence: list[str]
    human_review_note: str


class ReportReview(BaseModel):
    report_complete: bool
    schema_valid: bool
    missing_sections: list[str]
    review_notes: list[str]