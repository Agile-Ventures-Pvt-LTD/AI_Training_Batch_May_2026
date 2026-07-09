from servers.change_management_server import list_recent_changes, get_change_details,get_changes_for_service


#Test 9 – Payment API Changes
def test_get_changes_for_payment_api():
    data=get_changes_for_service("Payment API")
    assert data["service_name"]=="Payment API"
    assert data["count"]>0
    assert data["changes"][0]["change_id"]=="CHG-2001"
    assert "rollback_available" in data["changes"][0]

#Test 10 – Change Details
def test_get_change_details_valid_change():
    data=get_change_details("CHG-2001")
    assert data["found"]==True
    assert data["change"]["service_name"]=="Payment API"
    assert data["change"]["change_id"]=="CHG-2001"
    assert "risk" in data["change"]
    assert "implemented_at" in data["change"]
