import pytest
from src.crew import build_screening_crew

def test_crew_has_all_agents_and_tasks():
    """Verifies that your Crew object instantiates with all 5 elements."""
    crew_object = build_screening_crew()
    
    # Confirm exact count of components loaded into the pipeline
    assert len(crew_object.agents) == 5
    assert len(crew_object.tasks) == 5

def test_crew_is_running_sequentially():
    """Verifies that the tasks execute in a strict serial sequence order."""
    crew_object = build_screening_crew()
    
    # Check if the process property string matches "sequential"
    assert "sequential" in str(crew_object.process).lower()
