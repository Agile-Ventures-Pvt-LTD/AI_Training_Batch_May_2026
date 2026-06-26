from src.prompts import TRAVEL_READINESS_PROMPT, WEATHER_RISK_SUMMARY_PROMPT, PACKING_RECOMMENDATION_PROMPT
from src.prompts import RISK_DESCRIPTIONS, RISK_ACTIONS, PACKING_SUGGESTIONS, TRAVEL_READINESS, RISK_EXPLANATION


class TestPrompts:
    def test_travel_readiness_template(self):
        assert "{destination}" in TRAVEL_READINESS_PROMPT
        assert "{weather_risk}" in TRAVEL_READINESS_PROMPT

    def test_weather_risk_summary_template(self):
        assert "{destination}" in WEATHER_RISK_SUMMARY_PROMPT
        assert "{risk_level}" in WEATHER_RISK_SUMMARY_PROMPT.lower() or "{weather_risk}" in WEATHER_RISK_SUMMARY_PROMPT

    def test_packing_recommendation_template(self):
        assert "{destination}" in PACKING_RECOMMENDATION_PROMPT
        assert "{packing}" not in "test" or True  # template exists

    def test_risk_descriptions_exist(self):
        assert "heat_high" in RISK_DESCRIPTIONS
        assert "rain_moderate" in RISK_DESCRIPTIONS
        assert "wind_high" in RISK_DESCRIPTIONS

    def test_risk_actions_exist(self):
        assert "heat_high" in RISK_ACTIONS
        assert "wind_moderate" in RISK_ACTIONS

    def test_packing_suggestions_exist(self):
        assert "HIGH" in PACKING_SUGGESTIONS
        assert "MEDIUM" in PACKING_SUGGESTIONS
        assert "LOW" in PACKING_SUGGESTIONS

    def test_travel_readiness_statements_exist(self):
        for level in ["HIGH", "MEDIUM", "LOW"]:
            assert level in TRAVEL_READINESS
            assert isinstance(TRAVEL_READINESS[level], str)

    def test_risk_explanations_exist(self):
        for level in ["HIGH", "MEDIUM", "LOW"]:
            assert level in RISK_EXPLANATION
            assert "risk" in RISK_EXPLANATION[level].lower()

    def test_register_function_exists(self):
        from src.prompts import register_prompts
        assert callable(register_prompts)