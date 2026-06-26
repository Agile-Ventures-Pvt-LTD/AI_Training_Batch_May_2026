import pytest
from unittest.mock import MagicMock, patch
from crew import create_screening_crew

@patch("crewai.Crew.kickoff")
def test_crew_pipeline_execution(mock_kickoff):
    mock_kickoff.return_value = "Mocked Screening Report Completed Successfully"
    
    crew = create_screening_crew()
    inputs = {
        "jd_path": "data/mock_jd.md",
        "candidate_id": "CAND-001"
    }
    
    output = crew.kickoff(inputs=inputs)
    assert output == "Mocked Screening Report Completed Successfully"
    mock_kickoff.assert_called_once_with(inputs=inputs)
