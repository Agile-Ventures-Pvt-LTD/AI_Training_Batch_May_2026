import json
import os


def write_json_report(report_data, output_path, candidate_id):
    os.makedirs(output_path, exist_ok=True)

    file_path = os.path.join(
        output_path,
        f"{candidate_id}_screening_report.json"
    )

    with open(file_path, "w") as f:
        json.dump(report_data, f, indent=2)

    return file_path


def write_markdown_report(report_data, output_path, candidate_id):
    os.makedirs(output_path, exist_ok=True)

    md_path = os.path.join(
        output_path,
        f"{candidate_id}_screening_report.md"
    )

    content = f"""
# Candidate Report: {report_data.get("candidate_name")}

## Score
{report_data.get("overall_score")} / {report_data.get("max_score")}

## Recommendation
{report_data.get("recommendation")}

## Strengths
{', '.join(report_data.get("strengths", []))}

## Gaps
{', '.join(report_data.get("gaps", []))}
"""

    with open(md_path, "w") as f:
        f.write(content.strip())

    return md_path