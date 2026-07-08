from servers.change_management_server import get_changes_for_service, get_change_details

def test_get_changes_for_payment_api(service_name: str = "Payment API"):
    data = get_changes_for_service(service_name=service_name)

    change_id = data["changes"][0]["change_id"]
    rollback = data["changes"][0]["rollback_available"]

    assert change_id == "CHG-2001"
    assert rollback == True


def test_get_change_details_valid_change(change_id: str = "CHG-2001"):
    data = get_change_details(change_id=change_id)

    found = data["found"]
    change = data["change"]
    data_change_id = change["change_id"]
    service_name = change["service_name"]
    risk = change["risk"]
    implemented_at = change["implemented_at"]

    assert found == True
    assert data_change_id == change_id
    assert service_name == "Payment API"
    assert risk
    assert implemented_at