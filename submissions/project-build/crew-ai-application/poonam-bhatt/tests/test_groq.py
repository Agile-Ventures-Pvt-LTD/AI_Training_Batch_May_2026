import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config import llm

@pytest.mark.skipif(
    not os.getenv("GROQ_API_KEY") or os.getenv("GROQ_API_KEY") == "...",
    reason="Requires valid GROQ_API_KEY"
)
def test_groq_llm_setup():
    try:
        response = llm.call("What is 2+2?")
        assert response is not None
        assert len(response) > 0
    except Exception as e:
        pytest.fail(f"LLM call failed: {e}")