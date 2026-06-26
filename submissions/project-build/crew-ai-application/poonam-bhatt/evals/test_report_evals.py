from tools import validate_report
def test_report_recommendation_matches_score_band():
 report = validate_report("outputs/CAND-001_screening_report.json")
 percentage = report["percentage"]
 recommendation = report["recommendation"]
 if percentage >= 80:
 assert recommendation == "STRONG_MATCH"
 elif percentage >= 60:
 assert recommendation == "MODERATE_MATCH"
 elif percentage >= 40:
 assert recommendation == "WEAK_MATCH"
 else:
 assert recommendation == "NEEDS_MANUAL_REVIEW