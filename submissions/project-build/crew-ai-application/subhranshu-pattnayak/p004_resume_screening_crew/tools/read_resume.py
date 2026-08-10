from pathlib import Path
from utils.file_loader import read_markdown
from typing import Any
from crewai.tools import tool
from config import DATASET_PATH

@tool("Read Resume")
def read_resume(resume_path: Path) -> dict[str, Any]:
    """Reads a candidate resume file.

    Args:
        resume_path (Path): Resume file path of type .md for a candidate

    Returns:
        dict[str, Any]: Returns success status. Along with content and source file name on successful execution. Or Error message on failure.
    """
    try:
        res = DATASET_PATH / "resumes" / resume_path
        resume_content = read_markdown(res)
        return {
            "success": True,
            "content": resume_content,
            "source_file": resume_path.name
        }
    except Exception as e:
        return {
            "success": False,
            "message": str(e),
        }