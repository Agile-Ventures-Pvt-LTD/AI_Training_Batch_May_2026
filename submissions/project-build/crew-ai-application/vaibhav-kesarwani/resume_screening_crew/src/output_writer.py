import os
from crewai.tools import tool
from src.schemas import SaveReportInput

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "outputs")

@tool("save_report_tool")
def save_report_tool(input_data: SaveReportInput) -> dict:
    """
    Saves the final screening report as a Markdown (.md) file in the outputs/ folder.
    """
    
    try:
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        md_filename = f"{input_data.candidate_id}_screening_report.md"
        md_path = os.path.join(OUTPUT_DIR, md_filename)

        with open(md_path, "w", encoding="utf-8") as f:
            f.write(input_data.markdown_content)

        return {
            "success": True,
            "message": f"Report saved for {input_data.candidate_id}",
            "saved_file": md_filename
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e),
            "saved_file": None
        }