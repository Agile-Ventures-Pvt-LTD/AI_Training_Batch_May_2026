import os
import json

class ReportWriter:
    @staticmethod
    def write_json_report(filepath: str, data: dict) -> dict:
        """Safely saves a completed advisory dictionary asset structurally to disk."""
        try:
            directory = os.path.dirname(filepath)
            if directory:
                os.makedirs(directory, exist_ok=True)
                
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
                
            return {
                "success": True,
                "saved_path": filepath
            }
        except IOError as e:
            return {
                "success": False,
                "message": f"FileSystem write permission operation failed: {str(e)}"
            }
