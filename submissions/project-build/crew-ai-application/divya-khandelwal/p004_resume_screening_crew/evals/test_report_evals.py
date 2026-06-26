import pytest
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import HallucinationMetric

def test_easy_hallucination_check():
    """
    Checks if the AI agent's summary contains lies 
    compared to the original resume text.
    """
    source_resume = """
    Rohan Mehta - AI Engineer
    Skills: Python, SQL, PyTorch, Building basic RAG systems.
    Experience: 2 years at TechCorp.
    """
    ai_agent_output = """
    Candidate Rohan Mehta is an expert AI Engineer with 2 years of experience.
    He is highly skilled in Python and PyTorch. He also claims to have 5 years 
    of experience managing AWS Cloud Infrastructure and Docker containers.
    """
    test_case = LLMTestCase(
        input="Summarize the candidate profile.",
        actual_output=ai_agent_output,
        context=[source_resume] 
    )

    metric = HallucinationMetric(threshold=0.5)

    assert_test(test_case, [metric])
