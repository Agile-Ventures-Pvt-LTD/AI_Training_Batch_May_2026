import pytest
from src.utils import read_json
from src.config import REPORT_SCHEMA_TEMPLATE

@pytest.mark.integration
def test_output_schema():
    result = read_json("outputs/travel_advisory_report.json")

    assert isinstance(result, REPORT_SCHEMA_TEMPLATE)

    assert result.content != "" or result.error != ""
