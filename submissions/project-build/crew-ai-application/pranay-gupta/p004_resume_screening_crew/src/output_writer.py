import json
from pathlib import Path
from datetime import datetime
from src.config import OUTPUT_PATH, get_output_report_path, get_output_md_path

def save_json_report(candidate_id: str, report: dict) -> Path:
    output_file = get_output_report_path(candidate_id)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    return output_file

def save_markdown_report(candidate_id: str, report: dict) -> Path:
    md_file = get_output_md_path(candidate_id)
    lines = [f"# Screening Report: {report.get('candidate_name', candidate_id)}"]
    md_file.write_text("\n".join(lines), encoding="utf-8")
    return md_file

def append_execution_log(message: str):
    log_file = OUTPUT_PATH / "execution_log.txt"
    log_file.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def load_report(candidate_id: str) -> dict:
    report_path = get_output_report_path(candidate_id)
    if not report_path.exists():
        raise FileNotFoundError(f"Report not found: {report_path}")
    return json.loads(report_path.read_text(encoding="utf-8"))