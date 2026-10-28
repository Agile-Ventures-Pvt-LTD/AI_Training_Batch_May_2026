import pytest
from src.schemas import (
    JobDescriptionOutput, 
    ResumeOutput, 
    CandidateLookupOutput,
)
from src.tools import (
    read_job_description,
    read_resume_tool,
    candidate_index_lookup_tool,
)

def test_read_job_description():
    result = read_job_description()

    assert isinstance(result, JobDescriptionOutput)

    assert result.content != "" or result.error != ""


def test_read_resume_tool():
    BASE_DIR = "../data/p004_resume_screening_crew_dataset/resumes/candidate_001_rohan_mehta.md"

    result = read_resume_tool(BASE_DIR)

    assert isinstance(result, ResumeOutput)

    assert result.content != "" or result.error != ""


def test_candidate_index_lookup_tool():
    CAND_ID = "CAND-001"

    result = candidate_index_lookup_tool(CAND_ID)

    assert isinstance(result, CandidateLookupOutput)

    assert result.content != "" or result.error != ""




