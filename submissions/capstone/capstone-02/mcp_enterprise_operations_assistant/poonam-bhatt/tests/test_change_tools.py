import pytest
from src.tool_discovery import get_changes_for_service, get_change_details

def test_get_changes_for_payment_api():
    """Test 9 - Payment API Changes: Find recent changes for Payment API."""
    result = get_changes_for_service("Payment API")
    assert result["service_name"] == "Payment API"
    assert result["count"] >= 1
    assert "changes" in result
    
    change_ids = [c["change_id"] for c in result["changes"]]
    assert "CHG-2001" in change_ids
    
    for c in result["changes"]:
        assert "rollback_available" in c
        assert "change_id" in c

def test_get_change_details_valid_change():
    """Test 10 - Change Details: Get details for CHG-2001."""
    result = get_change_details("CHG-2001")
    assert result["found"] is True
    assert "change" in result
    change = result["change"]
    assert change["change_id"] == "CHG-2001"
    assert change["service_name"] == "Payment API"
    assert "risk" in change
    assert "implemented_at" in change
