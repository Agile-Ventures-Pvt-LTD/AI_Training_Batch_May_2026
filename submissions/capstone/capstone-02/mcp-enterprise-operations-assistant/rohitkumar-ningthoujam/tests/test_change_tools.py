import pytest
from servers.change_management_server import list_recent_changes,get_change_details,get_changes_for_service
def test_list_recent_changes(): 
    result = list_recent_changes(limit=10) 
    assert result["count"] > 0 
    assert "changes" in result 
def test_get_changes_for_payment_api(): 
    result = get_changes_for_service("Payment API") 
    assert result["service_name"] == "Payment API" 
    assert result["count"] >= 1 
    assert any( change["change_id"] == "CHG-2001" 
               for change in result["changes"] ) 
    assert "rollback_available" in result["changes"][0] 
def test_get_change_details_valid_change(): 
    result = get_change_details("CHG-2001") 
    assert result["found"] is True 
    assert result["change"]["change_id"] == "CHG-2001" 
    assert result["change"]["service_name"] == "Payment API" 
    assert "risk" in result["change"] 
    assert "implemented_at" in result["change"] 
def test_get_change_details_invalid_change(): 
    result = get_change_details("CHG-9999") 
    assert result["found"] is False 
    assert "message" in result