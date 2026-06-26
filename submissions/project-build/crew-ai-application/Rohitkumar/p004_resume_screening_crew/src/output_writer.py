import json
from src.config import OUTPUT_PATH


def save_report(candidate_id, report_data):
    json_path = OUTPUT_PATH / f"{candidate_id}_screening_report.json"
    with open(json_path, "w") as f:
        json.dump(report_data, f, indent=2)
    return str(json_path)


def make_report(jd_info, profile, match_data, interview):
    report = {
        "candidate_id": profile.get("candidate_id", ""),
        "candidate_name": profile.get("candidate_name", ""),
        "role_title": jd_info.get("role_title", "AI Engineer"),
        "overall_score": match_data.get("overall_score", 0),
        "max_score": 40,
        "percentage": match_data.get("percentage", 0.0),
        "recommendation": match_data.get("recommendation_band", ""),
        "executive_summary": f"{profile.get('candidate_name', 'Candidate')} is a {profile.get('current_role', 'N/A')} with {profile.get('years_experience', 'N/A')} years of experience. Score: {match_data.get('percentage', 0)}% - {match_data.get('recommendation_band', 'N/A')}.",
        "strengths": match_data.get("matched_skills", []),
        "gaps": match_data.get("missing_skills", []),
        "interview_focus_areas": interview.get("interview_focus_areas", []),
        "interview_questions": {
            "technical_questions": interview.get("technical_questions", []),
            "project_deep_dive_questions": interview.get("project_deep_dive_questions", []),
            "scenario_questions": interview.get("scenario_questions", []),
            "gap_validation_questions": interview.get("gap_validation_questions", [])
        },
        "evidence": build_evidence(profile, match_data),
        "human_review_note": "This is an AI-assisted screening report based on the provided resume and job description. A human reviewer should validate the recommendation before making any recruitment decision."
    }
    return report


def build_evidence(profile, match_data):
    evidence = []
    skills = profile.get("skills", [])
    if skills:
        evidence.append(f"Resume lists skills: {', '.join(skills[:5])}")
    matched = match_data.get("matched_skills", [])
    if matched:
        evidence.append(f"Matched {len(matched)} skills against job requirements.")
    missing = match_data.get("missing_skills", [])
    if missing:
        evidence.append(f"Missing skills: {', '.join(missing)}")
    return evidence


def save_markdown(candidate_id, report_data):
    md_path = OUTPUT_PATH / f"{candidate_id}_screening_report.md"
    lines = []
    lines.append(f"# Screening Report: {report_data.get('candidate_name', 'Unknown')}")
    lines.append(f"**Candidate ID:** {report_data.get('candidate_id', '')}")
    lines.append(f"**Role:** {report_data.get('role_title', '')}")
    lines.append(f"**Score:** {report_data.get('overall_score', 0)}/{report_data.get('max_score', 40)} ({report_data.get('percentage', 0)}%)")
    lines.append(f"**Recommendation:** {report_data.get('recommendation', '')}")
    lines.append("")
    lines.append("## Summary")
    lines.append(report_data.get("executive_summary", ""))
    lines.append("")
    lines.append("## Strengths")
    for s in report_data.get("strengths", []):
        lines.append(f"- {s}")
    lines.append("")
    lines.append("## Gaps")
    for g in report_data.get("gaps", []):
        lines.append(f"- {g}")
    lines.append("")
    lines.append("## Interview Focus Areas")
    for fa in report_data.get("interview_focus_areas", []):
        lines.append(f"- {fa}")
    lines.append("")
    lines.append("## Interview Questions")
    iq = report_data.get("interview_questions", {})
    if iq.get("technical_questions"):
        lines.append("### Technical")
        for q in iq["technical_questions"]:
            lines.append(f"- {q}")
    if iq.get("project_deep_dive_questions"):
        lines.append("### Project Deep Dive")
        for q in iq["project_deep_dive_questions"]:
            lines.append(f"- {q}")
    if iq.get("scenario_questions"):
        lines.append("### Scenario")
        for q in iq["scenario_questions"]:
            lines.append(f"- {q}")
    if iq.get("gap_validation_questions"):
        lines.append("### Gap Validation")
        for q in iq["gap_validation_questions"]:
            lines.append(f"- {q}")
    lines.append("")
    lines.append("## Evidence")
    for e in report_data.get("evidence", []):
        lines.append(f"- {e}")
    lines.append("")
    lines.append(f"**Note:** {report_data.get('human_review_note', '')}")

    with open(md_path, "w") as f:
        f.write("\n".join(lines))
    return str(md_path)