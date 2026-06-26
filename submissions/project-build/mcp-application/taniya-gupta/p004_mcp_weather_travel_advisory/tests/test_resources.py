import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.resources import TRAVEL_CHECKLIST, WEATHER_ADVISORY_RULES, NORMALIZED_FORECAST_SCHEMA

def test_resources_contain_key_words():
    assert "Checklist" in TRAVEL_CHECKLIST
    assert "LOW" in WEATHER_ADVISORY_RULES
    assert "destination" in NORMALIZED_FORECAST_SCHEMA
