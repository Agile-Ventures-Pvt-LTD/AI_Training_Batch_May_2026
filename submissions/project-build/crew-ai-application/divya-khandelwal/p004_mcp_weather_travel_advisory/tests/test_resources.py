import src.resources as r

def test_required_resources_available():
    assert "Checklist" in r.get_resource("resource://travel/checklist")
    assert "Advisory" in r.get_resource("resource://travel/advisory-rules")
    assert "current_weather" in r.get_resource("resource://weather/normalized-forecast-schema")
