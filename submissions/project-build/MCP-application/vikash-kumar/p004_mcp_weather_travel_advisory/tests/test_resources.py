from src.resources import RESOURCES

def test_required_resources_available():
    assert "resource://travel/checklist" in RESOURCES
    assert "resource://travel/advisory-rules" in RESOURCES
    assert "resource://weather/normalized-forecast-schema" in RESOURCES
