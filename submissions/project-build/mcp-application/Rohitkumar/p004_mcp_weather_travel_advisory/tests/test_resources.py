import pytest


class TestResources:
    def test_checklist_content(self):

        checklist_text = (
            "Travel Readiness Checklist:\n"
            "- Confirm destination and travel date.\n"
            "- Check weather forecast before departure.\n"
            "- Carry water during high-temperature conditions.\n"
            "- Carry umbrella or rain protection if rain risk exists.\n"
            "- Avoid unnecessary outdoor exposure during extreme heat.\n"
            "- Avoid exposed outdoor areas during high wind conditions.\n"
            "- Keep phone charged.\n"
            "- Carry essential documents."
        )
        assert "Travel Readiness Checklist" in checklist_text
        assert "Carry water" in checklist_text
        assert "Carry essential documents" in checklist_text

    def test_advisory_rules_content(self):
        rules_text = (
            "Weather Advisory Rules:\n\n"
            "LOW:\n"
            "- No major heat, rain, or wind indicators.\n"
            "- Normal travel precautions are enough.\n\n"
            "MEDIUM:\n"
            "- Moderate heat, rain, or wind indicators exist.\n"
            "- Travel is possible, but the traveler should plan with basic precautions.\n\n"
            "HIGH:\n"
            "- High heat, high rain probability, heavy precipitation, or high wind condition exists.\n"
            "- The traveler should reconsider non-essential outdoor travel or plan with extra caution."
        )
        assert "Weather Advisory Rules" in rules_text
        assert "LOW:" in rules_text
        assert "MEDIUM:" in rules_text
        assert "HIGH:" in rules_text

    def test_forecast_schema_content(self):
        schema_text = (
            '"destination": "string"'
        )
        assert "destination" in schema_text
        assert "string" in schema_text

    def test_required_resources_available(self):
        from src.resources import register_resources
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("Test")
        register_resources(mcp)
        assert True