from src.report_writer import assemble_final_report

def test_final_report_schema_valid():
    normal = {}
    risk = {"weather_risk": "MEDIUM", "risk_factors": ["High temp"], "recommended_actions": ["Drink water"]}
    report = assemble_final_report(normal, risk)
    assert "destination" in report
    assert "travel_readiness_advisory" in report
    assert "tools_used" in report
