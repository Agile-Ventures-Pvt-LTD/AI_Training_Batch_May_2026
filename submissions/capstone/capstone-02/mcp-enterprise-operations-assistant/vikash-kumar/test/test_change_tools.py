import json
import pytest
from servers.change_management_server import list_recent_changes, get_change_details, get_changes_for_service

def test_list_recent_changes():
    result = json.loads(list_recent_changes(limit=2))
    assert "count" in result
    assert "changes" in result
    assert isinstance(result["changes"], list)

def test_get_change_details_valid():
    result = json.loads(get_change_details("CHG-2001"))
    assert "found" in result

def test_get_changes_for_service():
    result = json.loads(get_changes_for_service("payment-gateway"))
    assert "service_name" in result
    assert "changes" in result
