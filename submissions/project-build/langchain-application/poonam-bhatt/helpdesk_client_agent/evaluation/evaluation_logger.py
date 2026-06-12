import json
import os
from datetime import datetime


class EvaluationLogger:
    """
    Collects full agent execution trace and saves it as JSON.
    """

    def __init__(self):
        self.data = {
            "user_request": "",
            "plan_summary": "",
            "tools_used": [],
            "tool_result_summary": "",
            "reflection_summary": "",
            "final_answer": "",
            "memory_used": False,
            "write_action_performed": False,
            "timestamp": str(datetime.now())
        }

    # ---------------- setters ----------------

    def set_user_request(self, text):
        self.data["user_request"] = text

    def set_plan(self, text):
        self.data["plan_summary"] = text

    def add_tool(self, tool_name):
        if tool_name not in self.data["tools_used"]:
            self.data["tools_used"].append(tool_name)

    def set_tool_summary(self, text):
        self.data["tool_result_summary"] = text

    def set_reflection(self, text):
        self.data["reflection_summary"] = text

    def set_final_answer(self, text):
        self.data["final_answer"] = text

    def set_memory_used(self, flag):
        self.data["memory_used"] = flag

    def set_write_action(self, flag):
        self.data["write_action_performed"] = flag

    # ---------------- save ----------------

    def save(self, path="outputs/evaluation_output.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)

        full_path = os.path.abspath(path)
        print("DEBUG: Saving evaluation file...")  # 👈 IMPORTANT
        print("DEBUG: Saving at:", full_path)  # 👈 IMPORTANT

        with open(full_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2)

        print("DEBUG: Save successful!")

        return full_path

# GLOBAL SINGLE INSTANCE
logger = EvaluationLogger()