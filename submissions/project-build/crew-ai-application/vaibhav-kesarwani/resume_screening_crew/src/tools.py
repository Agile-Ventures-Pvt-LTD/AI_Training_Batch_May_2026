import csv
import json
import os
from crewai.tools import tool
import re
from src.schemas import (
    JobDescriptionOutput, 
    ResumeOutput, 
    ResumeInput,
    CandidateLookupInput, 
    CandidateLookupOutput,
    ScreeningRubricOutput,
    ScoreCalculatorInput, 
    ScoreCalculatorOutput,
    SaveReportInput,
    SkillMatcherOutput,
    ValidateReportSchemaInput, 
    ValidateReportSchemaOutput
)
from src.scoring import get_recommendation_band

BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "p004_resume_screening_crew_dataset", "job_description", "jd_ai_engineer.md")

@tool("read_job_description")
def read_job_description() -> JobDescriptionOutput:
    """
    Reads a job description markdown file from data/p004_resume_screening_crew_dataset/job_description/ and returns its content.
    """
    try:
        file_path = BASE_PATH

        if not os.path.exists(file_path):
            return JobDescriptionOutput(content="", error=f"Job Description not found.")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return JobDescriptionOutput(content=content)

    except Exception as e:
        return JobDescriptionOutput(content="", error=str(e))
    

RESUME_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "p004_resume_screening_crew_dataset", "resumes")

@tool("read_resume_tool")
def read_resume_tool(input_data: ResumeInput) -> ResumeOutput:
    """
    Reads a candidate resume markdown file and returns its content.
    """

    resume_file = os.path.join(RESUME_PATH, input_data.resume_path)

    try:
        if not os.path.exists(resume_file):
            return ResumeOutput(
                success=False,
                content="",
                source_file=None,
                error=f"File not found: {resume_file}"
            )


        with open(resume_file, "r", encoding="utf-8") as f:
            content = f.read()

        return ResumeOutput(
            success=True,
            content=content,
            source_file=os.path.basename(input_data.resume_path)
        )

    except Exception as e:
        return ResumeOutput(
            success=False,
            content="",
            source_file=os.path.basename(input_data.resume_path),
            error=str(e)
        )

INDEX_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "p004_resume_screening_crew_dataset", "metadata", "candidate_index.csv")

@tool("candidate_index_lookup_tool")
def candidate_index_lookup_tool(input_data: CandidateLookupInput) -> CandidateLookupOutput:
    """
    Finds candidate details from the CSV index based on candidate_id.
    """
    try:
        if not os.path.exists(INDEX_FILE):
            return CandidateLookupOutput(
                found=False,
                message="File not found."
            )

        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("candidate_id") == input_data.candidate_id:
                    return CandidateLookupOutput(
                        found=True,
                        candidate_id=row.get("candidate_id"),
                        candidate_name=row.get("candidate_name"),
                        resume_file=row.get("resume_file"),
                    )

        return CandidateLookupOutput(
            found=False,
            message="Candidate ID not found."
        )

    except Exception as e:
        return CandidateLookupOutput(
            found=False,
            message=str(e)
        )
    

RUBRIC_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "p004_resume_screening_crew_dataset", "metadata", "screening_rubric.json")

@tool("load_screening_rubric_tool")
def load_screening_rubric_tool() -> ScreeningRubricOutput:
    """
    Loads the screening rubric JSON file and returns its contents.
    """
    try:
        if not os.path.exists(RUBRIC_FILE):
            return ScreeningRubricOutput(
                categories=[],
                score_range="",
                max_score=0,
                message="File not found."
            )

        with open(RUBRIC_FILE, "r", encoding="utf-8") as f:
            rubric_data = json.load(f)

        if not all(k in rubric_data for k in ["categories", "score_range", "max_score"]):
            return ScreeningRubricOutput(
                categories=[],
                score_range="",
                max_score=0,
                message="Invalid rubric format"
            )

        return ScreeningRubricOutput(
            categories=rubric_data["categories"],
            score_range=rubric_data["score_range"],
            max_score=rubric_data["max_score"]
        )

    except Exception as e:
        return ScreeningRubricOutput(
            categories=[],
            score_range="",
            max_score=0,
            message=str(e)
        )
    

MAX_SCORE = 40  

@tool("score_calculator_tool")
def score_calculator_tool(input_data: ScoreCalculatorInput) -> ScoreCalculatorOutput:
    """
    Calculates total score, percentage, and recommendation band from category scores.
    """
    
    try:
        overall_score = sum(input_data.category_scores.values())
        percentage = round((overall_score / MAX_SCORE) * 100)

        return ScoreCalculatorOutput(
            overall_score=overall_score,
            max_score=MAX_SCORE,
            percentage=percentage,
            recommendation_band=get_recommendation_band(percentage)
        )

    except Exception as e:
        return ScoreCalculatorOutput(
            overall_score=0,
            max_score=MAX_SCORE,
            percentage=0,
            recommendation_band=f"ERROR: {str(e)}"
        )
    

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")

@tool("save_report_tool")
def save_report_tool(input_data: SaveReportInput) -> dict:
    """
    Saves the final screening report as a Markdown (.md) file in the outputs/ folder.
    """
    
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        md_filename = f"{input_data.candidate_id}_screening_report.md"
        md_path = os.path.join(OUTPUT_DIR, md_filename)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(input_data.markdown_content)

        return {
            "success": True,
            "message": f"Report saved for {input_data.candidate_id}",
            "saved_file": md_filename
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "saved_file": None
        }


@tool("skill_matcher_tool")
def skill_matcher_tool(jd_content: str, resume_content: str) -> SkillMatcherOutput:
    """
    Compares job description skills with candidate resume skills.
    Returns matched, partial, and missing skills with match percentage.
    """

    def extract_skills(text: str):
        tokens = re.split(r"[,\n;•\-]+", text)
        return [t.strip().lower() for t in tokens if t.strip()]

    jd_skills = set(extract_skills(jd_content))
    resume_skills = set(extract_skills(resume_content))

    matched = []
    partial = []
    missing = []

    for skill in jd_skills:
        if skill in resume_skills:
            matched.append(skill)
        else:
            if any(skill in rs or rs in skill for rs in resume_skills):
                partial.append(skill)
            else:
                missing.append(skill)

    match_percentage = round((len(matched) / len(jd_skills) * 100), 2) if jd_skills else 0

    return SkillMatcherOutput(
        matched_skills=sorted(matched),
        partial_matches=sorted(partial),
        missing_skills=sorted(missing),
        match_percentage=match_percentage
    )


@tool("validate_report_schema_tool")
def validate_report_schema_tool(input_data: ValidateReportSchemaInput, output_folder: str = "./output") -> ValidateReportSchemaOutput:
    """
    Validates that the candidate's screening report contains all required fields.
    """
    
    md_filename = f"{input_data.candidate_id}_screening_report.md"
    report_path = os.path.join(output_folder, md_filename)

    if not os.path.exists(report_path):
        return ValidateReportSchemaOutput(
            schema_valid=False,
            missing_fields=input_data.required_fields
        )

    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    missing = [field for field in input_data.required_fields if field not in content]

    return ValidateReportSchemaOutput(
        schema_valid=len(missing) == 0,
        missing_fields=missing
    )
