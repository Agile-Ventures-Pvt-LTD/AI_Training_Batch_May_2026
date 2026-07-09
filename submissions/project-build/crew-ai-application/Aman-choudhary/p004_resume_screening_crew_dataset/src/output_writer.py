import json
import logging
from pathlib import Path
from typing import Dict, Any
from config import OUTPUT_PATH
logger = logging.getLogger(__name__)
OUTPUT_PATH.mkdir(parents=True,exist_ok=True)
def save_json_report(candidate_id: str,report: Dict[str, Any]) -> str:
    """
    Save candidate screening report.
    Example:
    outputs/CAND-001_screening_report.json
    """
    file_path = (OUTPUT_PATH /f"{candidate_id}_screening_report.json")
    with open(file_path,"w",encoding="utf-8") as file:
        json.dump(report,file,indent=4,ensure_ascii=False)
    logger.info("Report saved: %s",file_path)
    return str(file_path)
def load_json_report(file_path: str) -> Dict[str, Any]:
    """
    Load report file.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Report not found: {file_path}")
    with open(path,"r",encoding="utf-8") as file:
        return json.load(file)
def save_markdown_report(candidate_id: str,report_text: str) -> str:
    """
    Save markdown report.

    Example:
    outputs/CAND-001_screening_report.md
    """
    file_path = (OUTPUT_PATH /f"{candidate_id}_screening_report.md")
    with open(file_path,"w",encoding="utf-8") as file:
        file.write(report_text)
    logger.info("Markdown report saved: %s",file_path)
    return str(file_path)
def append_execution_log(message: str) -> None:
    """
    Append logs to:
    outputs/execution_log.txt
    """
    log_file = (OUTPUT_PATH /"execution_log.txt")
    with open(log_file,"a",encoding="utf-8") as file:
        file.write(f"{message}\n")
def write_report(candidate_id: str,report: Dict[str, Any]) -> Dict[str, str]:
    """
    Wrapper around report save operation.
    """
    try:
        file_path = save_json_report(candidate_id,report)
        return {"success": True,"file_path": file_path}
    except Exception as exc:
        logger.exception("Failed to save report.")
        return {"success": False,"error": str(exc)}
if __name__ == "__main__":
    sample_report = {
        "candidate_id": "CAND-001",
        "candidate_name": "Test Candidate",
        "overall_score": 32,
        "percentage": 80,
        "recommendation": "STRONG_MATCH"
    }
    result = write_report(
        candidate_id="CAND-001",
        report=sample_report
    )
    print(result)