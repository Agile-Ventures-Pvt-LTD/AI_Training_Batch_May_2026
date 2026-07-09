import pytest
from servers.change_management_server import get_changes_for_service,get_change_details

def test_get_changes_for_payment_api():
    result = get_changes_for_service("Payment API")
    assert result["count"]>=1
    has_target =any(chg['change_id'] == 'CHG-2001' for chg in result["changes"] )
    assert has_target is True
    assert "rollback_available" in result["changes"][0]

def test_get_change_details_valid_change():
    result = get_change_details("CHG-2001")
    assert result["found"] is True
    assert result["change"]["change_id"] == "CHG-2001"
    assert result["change"]["service_name"] == "Payment API"
    assert "risk" in result["change"]
    assert "implemented_at" in result["change"]