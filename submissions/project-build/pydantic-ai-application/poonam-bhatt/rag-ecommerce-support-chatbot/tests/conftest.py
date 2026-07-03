import os
import sys
import pytest

# Add the project root to the python path so imports in tests work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set environment variables globally before any tests or modules are imported
os.environ["GROQ_API_KEY"] = "mock_groq_api_key_12345"
os.environ["GROQ_MODEL"] = "llama-3.3-70b-versatile"


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Ensure environment variables are populated for testing to avoid connection issues."""
    # Already set globally, but this fixture can remain as autouse
    pass
