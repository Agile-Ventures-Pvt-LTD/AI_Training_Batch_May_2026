import pytest
from src.crew import resume_screening_crew

result = resume_screening_crew.kickoff()
assert isinstance(result)