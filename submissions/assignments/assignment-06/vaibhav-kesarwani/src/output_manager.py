import os
import json


class OutputManager:

    def __init__(self):
        self.output_dir = "outputs"

        os.makedirs(self.output_dir, exist_ok=True)

        self.file_path = os.path.join(self.output_dir, "responses.json")

        if not os.path.exists(self.file_path):
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def save(self, result: dict):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                existing = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):
            existing = []


        output = {
            "user_query": result.get("user_query", ""),
            "tools_used": result.get( "tools_used", []),
            "final_answer": result.get("final_answer", ""),
            "write_action_performed": result.get("write_action_performed", False)
        }

        existing.append(output)

        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(existing, f, indent=4, ensure_ascii=False)
