import pytest
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from servers.change_management_server import list_recent_changes, get_change_details, get_changes_for_service


def test_list_recent_changes():
    res = list_recent_changes()
    assert "changes" in res
    assert res["count"] >= 0


def test_get_changes_for_payment_api():
    res = get_changes_for_service("Payment API")
    assert res["count"] > 0
    assert any(c["change_id"] == "CHG-2001" for c in res["changes"])
    assert "rollback_available" in res


def test_get_change_details_valid_change():
    res = get_change_details("CHG-2001")
    assert res["found"] is True
    assert res["change"]["change_id"] == "CHG-2001"
    assert "risk" in res["change"]