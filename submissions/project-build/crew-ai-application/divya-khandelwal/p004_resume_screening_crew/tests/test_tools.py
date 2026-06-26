import pytest

# A simple mock function to simulate how your candidate lookup tool behaves
def simple_lookup_logic(candidate_id: str) -> dict:
    if candidate_id == "candidate_001":
        return {"found": True, "resume_file": "candidate_001_rohan_mehta.md"}
    return {"found": False, "resume_file": None}

def test_lookup_finds_valid_candidate():
    """Checks if the lookup returns the correct file for a valid ID."""
    result = simple_lookup_logic("candidate_001")
    assert result["found"] is True
    assert result["resume_file"] == "candidate_001_rohan_mehta.md"

def test_lookup_fails_for_invalid_candidate():
    """Checks if the lookup handles a missing candidate safely."""
    result = simple_lookup_logic("candidate_999")
    assert result["found"] is False
    assert result["resume_file"] is None
