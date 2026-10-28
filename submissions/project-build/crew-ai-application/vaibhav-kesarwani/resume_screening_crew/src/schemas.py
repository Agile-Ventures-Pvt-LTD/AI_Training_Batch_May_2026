from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class JobDescriptionOutput(BaseModel):
    content: str = Field(description="Full text content of the job description file")


class ResumeInput(BaseModel):
    resume_path: str = Field(description="Full path to the candidate resume markdown file inside the dataset folder")


class ResumeOutput(BaseModel):
    success: bool = Field(description="Whether the resume was read successfully")
    content: str = Field(description="Full text content of the resume")
    source_file: Optional[str] = Field(description="Name of the resume file")
    error: Optional[str] = Field(description="Error message if reading failed")


class CandidateLookupInput(BaseModel):
    candidate_id: str = Field(description="Unique candidate ID, e.g., CAND-001")


class CandidateLookupOutput(BaseModel):
    found: bool = Field(description="Whether the candidate was found")
    candidate_id: Optional[str] = Field(description="Candidate ID")
    candidate_name: Optional[str] = Field(description="Full name of the candidate")
    resume_file: Optional[str] = Field(description="Resume filename")
    message: Optional[str] = Field(description="Error or status message")


class ScreeningRubricOutput(BaseModel):
    categories: List[str] = Field(description="List of scoring categories")
    score_range: str = Field(description="Allowed score range for each category")
    max_score: int = Field(description="Maximum total score possible")
    message: Optional[str] = Field(description="Error or status message")


class ScoreCalculatorInput(BaseModel):
    category_scores: Dict[str, int] = Field(description="Dictionary of category scores, each between 0 and 5")


class ScoreCalculatorOutput(BaseModel):
    overall_score: int = Field(description="Sum of all category scores")
    max_score: int = Field(description="Maximum possible score")
    percentage: int = Field(description="Percentage score (0 - 100)")
    recommendation_band: str = Field(description="Recommendation category")


class SaveReportInput(BaseModel):
    candidate_id: str = Field(description="Candidate ID, e.g., CAND-001")
    markdown_content: str = Field(description="Markdown content of the screening report")


class SkillMatcherOutput(BaseModel):
    matched_skills: List[str] = Field(description="Skills present in both JD and resume")
    partial_matches: List[str] = Field(description="Skills partially matched between JD and resume")
    missing_skills: List[str] = Field(description="Skills in JD but not in resume")
    match_percentage: float = Field(description="Percentage of JD skills matched in resume")


class ValidateReportSchemaInput(BaseModel):
    candidate_id: str = Field(description="Unique candidate ID for locating the report file")
    required_fields: List[str] = Field(description="List of required field names to validate in the report")


class ValidateReportSchemaOutput(BaseModel):
    schema_valid: bool = Field(description="Whether the report matches the required schema")
    missing_fields: List[str] = Field(description="List of missing or invalid fields")
