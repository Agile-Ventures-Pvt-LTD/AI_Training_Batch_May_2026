import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from servers.change_management_server import get_changes_for_service, get_change_details, list_recent_changes

def test_get_changes_for_payment_api():
    result = get_changes_for_service(service_name="Payment API")
    assert result["service_name"] == "Payment API"
    assert result["count"] > 0
    change_ids = [c["change_id"] for c in result["changes"]]
    assert "CHG-2001" in change_ids
    assert "rollback_available" in result["changes"][0]

def test_get_change_details_valid_change():
    result = get_change_details(change_id="CHG-2001")
    assert result["found"] is True
    assert result["change"]["change_id"] == "CHG-2001"
    assert result["change"]["service_name"] == "Payment API"
    assert "risk" in result["change"]
