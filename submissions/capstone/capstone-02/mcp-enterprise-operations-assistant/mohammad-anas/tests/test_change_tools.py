import pytest
from servers.change_management_server import get_change_details

def test_get_change_details_valid_change():
    result = get_change_details("CHG-2001")
    assert result["found"] is True
    assert result["change"]["change_id"] == "CHG-2001"
    assert result["change"]["service_name"] == "Payment API"
    assert "risk" in result["change"]
    assert "implemented_at" in result["change"]