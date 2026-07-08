import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from servers.change_management_server import get_change_details, get_changes_for_service

def test_get_changes_for_payment_api():
    result = get_changes_for_service("Payment API")
    assert result["service_name"] == "Payment API"
    assert result["count"] >= 1
    change_ids=[c["change_id"] for c in result["changes"]]
    assert "CHG-2001" in change_ids
    for c in result["changes"]:
        assert "rollback_available" in c

def test_get_change_details_valid_change():
    result=get_change_details("CHG-2001")
    assert result["found"] is True
    change=result["change"]
    assert change["change_id"]=="CHG-2001"
    assert change["service_name"]=="Payment API"
    assert "risk" in change
    assert "implemented_at" in change
