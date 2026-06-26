from pydantic import BaseModel, Field
from typing import List, Dict

class JDanalysis(BaseModel):
    role_title:str = Field(description="The title of the job role")
    required_skills: List[str] = Field(description="list of required skills")
    preferred_skills: List[str] = Field(description="list of preferred skills")
    responsibilies: List[str] = Field(description="list of responsibilites")
    experience_expected: str = Field(description="Years of experience expected ")
    evaluation_criteria: List[str] = Field(description="criteria that will be used to evaluate")

class Resumeprofile(BaseModel):
    candidate_id: str = Field(description="Id of the candidate")
    candidate_name: str = Field(description="Name of the candidate")
    current_role: str = Field(description="current role of the candidate")
    years_experience: str = Field(description="Years of experience of candidate")
    skills: List[str]= Field(description="skills of the candidate")
    projects:List[str] = Field(description="projects of the candidate")
    experience_summary: List[str]= Field(description="summary of experience of candidate")
    education: List[str]= Field(description="educational qualifications of the candidate")
    certifications:List[str]= Field(description="certifications of the candidate")

class Matchscore(BaseModel):
    match_skills: List[str]= Field(description="skills that matched with jd")
    partial_match: List[str]= Field(description="Skills that partially matched with jd")
    missing_skills:List[str]= Field(description="required skills that were missing in resume")
    category_scores: Dict[str, int] = Field(description="Scores for the 8 rubric categories")
    overall_score: int = Field(description="Sum of all category scores")
    maximum_score: int = Field(default=40, description="max score that is 40")
    percentage: float = Field(description="calculated percentage")
    recommendation_band: str = Field(description="Assigned recommendation band like STRONG_MATCH and such")

class Interviewplan(BaseModel):
    focus_area: List[str] = Field(description="focus area for the candidate")
    technical_questions:List[str] = Field(description="atleast 3 technical questions")
    project_deep_questions:List[str]= Field(description=" atleast 2 deep dive questions for projects")
    scenario_questions:List[str] = Field(description="atleast 2 scenario questions")
    gap_validation:List[str] = Field(description="atleast 2 gap validations questions")

class Gapanalysis(BaseModel):
    critical_gaps:List[str]=Field(description="Missing critical skills")
    moderate_gaps:List[str]= Field(description="Missing preferred skills")
    areas_to_probe:List[str]= Field(description="certain areas to probe")

class Reportreview(BaseModel):
    report_complete: bool = Field(description="whether report is complete or not")
    missing_sections:List[str] = Field(description="missing sections in the report")
    schema_valid: bool = Field(description="if the schema is valid or not")
    review_notes: List[str] = Field(description="notes and feedback")

class Interviewquestions(BaseModel):
    technical_questions: List[str]
    project_deep_dive_questions: List[str]
    scenario_questions: List[str]
    gap_validation_questions: List[str]

class Finalreport(BaseModel):
    candidate_id: str = Field(description="Id of the candidate")
    candidate_name: str = Field(description="Full name of the candidate.")
    role_title: str = Field(description="job role title")
    overall_score: int = Field(description="overall score")
    max_score: int = Field(default=40, description="max score which is 40")
    percentage: float = Field(description="Calculated percentage")
    recommendation: str = Field(description="Recommendation which can be like STRONG_MATCH and such")
    executive_summary: str = Field(description="executive summary of candidate's fit")
    strengths: List[str] = Field(description="Key strengths of the candidate.")
    gaps: List[str] = Field(description="Key gaps in the candidate's profile.")
    interview_focus_areas: List[str] = Field(description="Key areas to focus on in the interview.")
    interview_questions: Interviewquestions = Field(description="Dictionary of interview questions.")
    evidence: List[str] = Field(description="Evidence from resume showing score and evaluation.")
    human_review_note: str = Field(
        default="This is AI screening report based on the given resume and job description.  It should not be treated as the final recruitment decision.",
        description="note for human reviewers."
    )

