# tests/test_report_schema.py
from src.schemas import get_final_report_schema

def test_final_report_schema_valid():
    schema = get_final_report_schema()
    assert schema["destination"] == ""
    assert "tools_used" in schema
    assert "prompts_used" in schema
    assert "resources_used" in schema