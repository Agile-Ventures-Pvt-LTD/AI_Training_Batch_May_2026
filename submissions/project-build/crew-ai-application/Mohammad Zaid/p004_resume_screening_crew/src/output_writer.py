# output_writer.py

from crewai.tools import tool
import json
from pathlib import Path

@tool("save_report_tool")
def save_report_tool(candidate_id: str, report_data: dict, save_markdown: bool = True) -> str: 
    """Saves the final report to the outputs/ folder as JSON, and optionally as Markdown."""
    print("---calling save_report_tool()---\n")
    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    json_path = output_dir / f"{candidate_id}_screening_report.json"
    with open(json_path, mode="w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)
        
    if save_markdown:
        md_path = output_dir / f"{candidate_id}_screening_report.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(f"# Screening Report: {candidate_id}\n\n```json\n{json.dumps(report_data, indent=2)}\n```")
            
    return f"Successfully saved report for {candidate_id} to {output_dir}/"