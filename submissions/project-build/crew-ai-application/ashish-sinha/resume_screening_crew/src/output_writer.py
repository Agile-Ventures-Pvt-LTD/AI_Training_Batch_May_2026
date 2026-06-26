import os
import json
from typing import Dict, Any
from rich.console import Console

console = Console()

class OutputWriter:
    def __init__(self, output_dir: str = "outputs"):
        """Initializes the output directory path structure."""
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def write_json_report(self, candidate_id: str, report_data: Dict[str, Any]) -> str:
        """Saves the structured Pydantic-validated JSON data into the output directory."""
        filename = f"{candidate_id}_screening_report.json"
        filepath = os.path.join(self.output_dir, filename)
        
        report_data["human_review_note"] = (
            "This is an AI-assisted screening report based on the provided resume "
            "and job description. A human reviewer should validate the "
            "recommendation before making any recruitment decision."
        )
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(report_data, f, indent=2, ensure_ascii=False)
            console.print(f"JSON report saved successfully at: {filepath}[/bold green]")
            return filepath
        except Exception as e:
            console.print(f" Failed to write JSON report for {candidate_id}: {str(e)}[/bold red]")
            raise e
