
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from src.prompts import travel_readiness_prompt
def test_required_resources_available():
    result = travel_readiness_prompt(
                                     "destination":"this is destination.",
                                     "weather_risk":"risks",
                                     'forecast_summary':"summary",
                                     "recommended_actions":"recommended_actions" )
    assert result is not None
    

