from servers.change_management_server import get_changes_for_service, get_change_details

def test_get_changes_for_payment_api():
    """Test get_changes_for_service returns recent changes for Payment API."""
    result = get_changes_for_service("Payment API")
    assert result["service_name"] == "Payment API"
    assert result["count"] > 0
    
    found_chg = False
    for change in result["changes"]:
        if change["change_id"] == "CHG-2001":
            found_chg = True
            assert "rollback_available" in change
    assert found_chg is True

def test_get_change_details_valid_change():
    """Test get_change_details returns correct data for a valid change."""
    result = get_change_details("CHG-2001")
    assert result["found"] is True
    change = result["change"]
    assert change["change_id"] == "CHG-2001"
    assert change["service_name"] == "Payment API"
    assert "risk" in change
    assert "implemented_at" in change
