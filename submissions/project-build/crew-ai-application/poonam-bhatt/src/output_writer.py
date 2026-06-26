import os
from src.tools import save_report_tool

def write_final_report(report_content: str, report_name: str = "final_report") -> str:
    """
    Saves the final report content to the outputs/ folder.
    """
    return save_report_tool(report_content, report_name)
