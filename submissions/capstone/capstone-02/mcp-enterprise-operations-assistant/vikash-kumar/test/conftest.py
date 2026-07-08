import os
import pytest

@pytest.fixture(autouse=True)
def mock_env_vars():
    os.environ["GROQ_API_KEY"] = "gsk_mock_test_key_string"
