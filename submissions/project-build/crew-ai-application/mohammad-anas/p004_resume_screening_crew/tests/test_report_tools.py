from tools.report_tools import (
    validate_report_schema_tool,
)


def test_schema_validation():
    result = validate_report_schema_tool.run(
        report={}
    )

    assert result is False