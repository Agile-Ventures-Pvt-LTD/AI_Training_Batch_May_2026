from crew import screening_crew
from crewai import LLM, Agent, Task, Crew, Process
from crewai.tools import tool
import json
import os

REQUIRED_NOTE = (
    "This will evaluate the candidate and then evaluate either it can fit for the role or not"
)

@tool("save_report_tool")
def save_report_tool(candidate_id: str, report_data: dict, markdown_content: str = None) -> dict:
    """save the report of the candidate."""
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    cid = str(candidate_id).strip()
    
    report_data["human_review_note"] = REQUIRED_NOTE
    
    json_path = os.path.join(output_dir, f"{cid}_screening_report.json")
    md_path = os.path.join(output_dir, f"{cid}_screening_report.md")
    saved_files = []
    
    try:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=4, ensure_ascii=False)
        saved_files.append(json_path)
        
        if markdown_content:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown_content.strip())
            saved_files.append(md_path)
            
        return {"success": True, "message": f"Saved report for {cid}.", "saved_files": saved_files}
    except Exception as e:
        return {"success": False, "message": str(e), "saved_files": saved_files}