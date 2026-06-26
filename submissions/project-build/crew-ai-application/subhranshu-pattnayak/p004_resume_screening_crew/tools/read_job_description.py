from pathlib import Path
from utils.file_loader import read_markdown
from typing import Any
from crewai.tools import tool

@tool("Read Job Description")

def read_job_description(jd_path: Path) -> dict[str, Any]:
    """Reads the job description file.

    Args:
        jd_path (Path): job description file path of type .md 

    Returns:
        dict[str, Any]: Returns success status. Along with content and source file name on successful execution. Or Error message on failure.
    """
    try:
        jd_content = read_markdown(jd_path)
        return {
            "success": True,
            "content": jd_content,
            "source_file": jd_path.name
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }