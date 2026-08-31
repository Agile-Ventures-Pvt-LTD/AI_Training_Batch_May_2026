from src.tools import validate_report_schema_tool
from src.schemas import ValidateReportSchemaOutput

def test_output_schema():
    result = validate_report_schema_tool()

    assert isinstance(result, ValidateReportSchemaOutput)

    assert result.content != "" or result.error != ""
