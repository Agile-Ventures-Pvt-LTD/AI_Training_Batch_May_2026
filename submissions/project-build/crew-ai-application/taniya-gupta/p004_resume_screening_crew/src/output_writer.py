import os
import json

def write_json_report(candidate_id: str, report_data: dict, output_dir: str) -> str:
    clean_id = candidate_id.strip()
    filename = f"{clean_id}_screening_report.json"
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    return file_path

# def write_markdown_report(candidate_id, report_data, output_dir):
#     clean_id = candidate_id.strip()
#     filename = f"{clean_id}_screening_report.md"
#     file_path = os.path.join(output_dir, filename)
    
#     md_content = f"# Resume Screening Report for {report_data.get('candidate_name')} ({clean_id})\n"
#     md_content += f"Role Applied For:{report_data.get('role_title')}\n"
#     md_content += f"Recommendation: {report_data.get('recommendation')}\n"
#     md_content += f"Overall Score: {report_data.get('overall_score')} / {report_data.get('max_score', 40)} ({report_data.get('percentage')}%)\n\n"
    
#     md_content += f"## Executive Summary\n"
#     md_content += f"{report_data.get('executive_summary')}\n"
    
#     md_content += "## Candidate Key Strengths\n"
#     strengths = report_data.get('strengths')
    
#     md_content += "## Candidate Profile Gaps\n"
#     gaps = report_data.get('gaps')
    
        
    
#     md_content += f"**Note:** {report_data.get('human_review_note')}\n"
    
#     with open(file_path, "w", encoding="utf-8") as md_f:
#         md_f.write(md_content)
        
#     return file_path
