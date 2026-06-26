from typing import List, Dict
from pydantic import BaseModel, Field

class JDAnalysisOutput(BaseModel):
    role_title: str = Field(..., description="The official title of the job role.")
    required_skills: List[str] = Field(..., description="List of essential hard/technical skills required.")
    preferred_skills: List[str] = Field(..., description="List of optional or nice-to-have skills.")
    core_responsibilities: List[str] = Field(..., description="Main duties and operational expectations of the role.")

class ResumeExtractionOutput(BaseModel):
    candidate_id: str = Field(..., description="The unique identifier for the candidate.")
    candidate_name: str = Field(..., description="Full name of the applicant.")
    extracted_skills: List[str] = Field(..., description="Complete list of skills explicitly mentioned in the resume.")
    experience_summary: str = Field(..., description="A high-level summary of the candidate's work history.")

class MatchingOutput(BaseModel):
    category_scores: Dict[str, int] = Field(..., description="Scores (0-5) assigned to each of the 8 screening rubric categories.")
    overall_score: int = Field(..., description="Sum total of all category scores.")
    max_score: int = Field(..., description="Maximum possible score (40).")
    percentage: int = Field(..., description="Calculated percentage score.")
    recommendation_band: str = Field(..., description="The mapped status band (e.g., STRONG_MATCH, MODERATE_MATCH, etc.).")
    strengths: List[str] = Field(..., description="Key technical highlights where the candidate meets or exceeds requirements.")
    gaps: List[str] = Field(..., description="Areas where the candidate is lacking skills or experiences.")
    evidence: Dict[str, str] = Field(..., description="Direct text justifications from the resume proving why each score was assigned.")

class InterviewPlanOutput(BaseModel):
    interview_focus_areas: List[str] = Field(..., description="Target topics that need verification based on gaps.")
    interview_questions: List[Dict[str, str]] = Field(..., description="List of dictionaries containing 'question' and 'intent'.")

class FinalReportSchema(BaseModel):
    candidate_id: str = Field(..., description="The unique identifier for the candidate.")
    candidate_name: str = Field(..., description="Full name of the applicant.")
    role_title: str = Field(..., description="The official title of the job role.")
    overall_score: int = Field(..., description="Sum total of all category scores.")
    max_score: int = Field(..., description="Maximum possible score (40).")
    percentage: int = Field(..., description="Calculated percentage score.")
    recommendation: str = Field(..., description="The final recommendation band determined by the calculator.")
    executive_summary: str = Field(..., description="Comprehensive written summary evaluating overall fitment.")
    strengths: List[str] = Field(..., description="Validated key proficiencies matching the job criteria.")
    gaps: List[str] = Field(..., description="Core skills missing or lacking in-depth experience.")
    interview_focus_areas: List[str] = Field(..., description="Identified areas requiring deep verification during interviewing.")
    interview_questions: List[Dict[str, str]] = Field(..., description="Tailored candidate questions containing 'question' and 'intent'.")
    evidence: Dict[str, str] = Field(..., description="Structural mappings showing text fragments used as proof of evaluation.")
    human_review_note: str = Field(..., description="A custom note flagging any borderline criteria or nuanced observations.")
