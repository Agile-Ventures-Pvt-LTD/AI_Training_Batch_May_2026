import pytest

from servers.change_management_server import list_recent_changes, get_change_details, get_changes_for_service

@pytest.mark.asyncio
async def test_get_changes_for_payment_api():
    result=await get_changes_for_service()

    assert result["service_name"]== "Payment API"
    assert result["count"] > 1
    assert result["changes"] == "CHG-2001"

#==================================================================================================================

@pytest.mark.asyncio
async def test_get_change_details_valid_change():
    result= await get_change_details()

    assert result["found"] == True
    assert result["charge_id"] =="CHG-2001"
    assert result["service_name"] == "Payment API"
    assert result["message"] is "risk exist"


