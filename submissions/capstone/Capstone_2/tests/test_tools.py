import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "servers"))

import service_health_server as shs
import support_ticket_server as sts
import change_management_server as cms


def test_service_health_payment_api():
    """Service Health: valid lookup returns correct status and an unknown
    service returns found=False instead of crashing."""
    result = shs.get_service_health("Payment API")
    assert result["found"] is True
    assert result["service"]["status"] == "UNHEALTHY"

    missing = shs.get_service_health("Nonexistent Service")
    assert missing["found"] is False


def test_support_ticket_high_priority_only_open():
    """Support Tickets: high-priority tool only returns open P1/P2 tickets."""
    result = sts.get_high_priority_tickets()
    assert result["count"] > 0
    for ticket in result["tickets"]:
        assert ticket["priority"] in ("P1", "P2")
        assert ticket["status"] == "OPEN"


def test_change_management_payment_api_change():
    """Change Management: known change lookup succeeds and returns the
    expected change_id; unknown change_id returns found=False."""
    result = cms.get_changes_for_service("Payment API")
    assert result["count"] >= 1
    assert any(c["change_id"] == "CHG-2001" for c in result["changes"])

    missing = cms.get_change_details("CHG-9999")
    assert missing["found"] is False
