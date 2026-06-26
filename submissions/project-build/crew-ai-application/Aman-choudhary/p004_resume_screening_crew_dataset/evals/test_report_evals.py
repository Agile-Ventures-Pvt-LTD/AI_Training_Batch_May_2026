
import json
from pathlib import Path
REPORT_FILE = ("outputs/CAND-001_screening_report.json")
def load_report():
    path = Path(REPORT_FILE)
    assert path.exists()
    with open(path,"r",encoding="utf-8") as file:
        return json.load(file)

def test_report_relevance():
    report = load_report()
    assert report["role_title"]
    assert len(report["executive_summary"]) > 0
def test_groundedness():
    report = load_report()
    assert isinstance(report["evidence"],list)
    assert (len(report["evidence"]) >= 1)
def test_recommendation_consistency():
    report = load_report()
    percentage = report["percentage"]
    recommendation = report["recommendation"]
    if percentage >= 80:
        assert (recommendation == "STRONG_MATCH")
    elif percentage >= 60:
        assert (recommendation == "MODERATE_MATCH")
    elif percentage >= 40:
        assert (recommendation == "WEAK_MATCH")
    else:
        assert (recommendation=="NEEDS_MANUAL_REVIEW")
def test_interview_question_quality():
    report = load_report()
    questions = report["interview_questions"]
    assert ("technical_questions"in questions)
    assert ("scenario_questions"in questions)
    assert ("gap_validation_questions"in questions)