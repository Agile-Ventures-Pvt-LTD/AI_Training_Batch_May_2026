import pytest
from servers.change_management_server import get_change_details, get_changes_for_service



@pytest.mark.asyncio
async def test_get_changes_for_payment_api():
    """
    Testing get_changes_for_service tool for Payment API Changes.
    """
    result = await get_changes_for_service(service_name='Payment API')
    
    assert 'changes' in result.keys()
    
    assert all([res['service_name'] == 'Payment API' for res in result['changes']])
    
    assert result['count'] >= 1
    
    assert any([res['change_id'] == 'CHG-2001' for res in result['changes']])
    
    assert ([res ['rollback_available'] for res in result['changes']])





@pytest.mark.asyncio
async def test_get_change_details_valid_change():
    """
    Testing get_change_details tool for valid Changes.
    """
    result = await get_change_details('CHG-2001')
    
    assert 'found' in result.keys() and result['found']
    
    assert 'change' in result.keys() and result['change']['change_id'] == 'CHG-2001'
    
    assert 'change' in result.keys() and result['change']['service_name'] == 'Payment API'
    
    assert 'change' in result.keys() and 'risk' in result['change'].keys() and result['change']['risk']
    
    assert 'change' in result.keys() and 'implemented_at' in result['change'].keys() and result['change']['implemented_at']