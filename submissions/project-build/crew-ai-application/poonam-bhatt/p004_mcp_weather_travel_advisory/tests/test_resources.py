import sys
import os
import pytestn

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.resources import get_checklist, get_advisory_rules, get_forecast_schema
from src.server import mcp
def test_required_resources_available():
    
    checklist = get_checklist()
    assert "Travel Readiness Checklist:" in checklist
    assert "- Confirm destination and travel date." in checklist
    
    rules = get_advisory_rules()
    assert "Weather Advisory Rules:" in rules
    assert "LOW:" in rules
    assert "MEDIUM:" in rules
    assert "HIGH:" in rules
    
    schema = get_forecast_schema()
    assert "destination" in schema
    assert "current_weather" in schema
    assert "daily_forecast" in schema
    
    registered_uris = []
    
    if hasattr(mcp, "_resources"):
        registered_uris = list(mcp._resources.keys())
    elif hasattr(mcp, "resources"):
        registered_uris = [r.uri for r in mcp.resources]
        
    expected_uris = [
        "resource://travel/checklist",
        "resource://travel/advisory-rules",
        "resource://weather/normalized-forecast-schema"
    ]
    
    
    if registered_uris:
        for uri in expected_uris:
            assert uri in registered_uris
