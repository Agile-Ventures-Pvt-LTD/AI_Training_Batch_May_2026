from agents import (
    jd_analyst,
    resume_extractor,
)


def test_agents():
    assert jd_analyst.role == "Job Description Analyst"
    assert resume_extractor.role == "Resume Extractor"