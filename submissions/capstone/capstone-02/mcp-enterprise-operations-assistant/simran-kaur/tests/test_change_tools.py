from servers.change_management_server import (get_change_details,get_changes_for_service,list_recent_changes)
import pytest

def test_get_changes_for_payment_api():
    result = get_changes_for_service("Payment API")
    assert result["count"] >=1 
    changes=result["changes"]
    for change in changes:
        assert change["service_name"] == "Payment API"
        assert change["change_id"] == "CHG-2001"
        assert change["rollback_available"] is True


def test_get_change_details_valid_change():
    input="CHG-2001"
    result= get_change_details(input)
    assert result["found"] is True
    change= result["change"]
    assert change["change_id"] == "CHG-2001"
    assert change["service_name"]== "Payment API"
    assert change["risk"] is not None
    assert change["implemented_at"] is not None


def 