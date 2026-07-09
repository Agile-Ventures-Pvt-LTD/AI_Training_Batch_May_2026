import pytest
from servers.support_ticket_server import search_tickets, get_high_priority_tickets, get_ticket_details

@pytest.mark.asyncio
async def test_search_open_payment_tickets():
    '''
    Testing Search Tickets tool
    '''
    result = await search_tickets(service_name='Payment API', status='OPEN')
    
    assert ('tickets' in result.keys()) and all([x['service_name'] == 'Payment API' for x in result['tickets']])
    
    assert ('tickets' in result.keys()) and all([x['status'] == 'OPEN' for x in result['tickets']])
    
    assert isinstance(result, dict)



@pytest.mark.asyncio
async def test_get_ticket_details_valid_ticket():
    '''
    Testing get_ticket_details tool for valid ticket
    '''
    result = await get_ticket_details(ticket_id='TKT-1001')
    
    assert 'found' in result.keys() and result['found']
    
    assert ('ticket' in result.keys()) and ('ticket_id' in result['ticket'].keys()) and (result['ticket']['ticket_id'] == 'TKT-1001')
    
    assert ('ticket' in result.keys()) and ('service_name' in result['ticket'].keys()) and (result['ticket']['service_name'] == 'Payment API')
    
    assert ('ticket' in result.keys()) and ('priority' in result['ticket'].keys()) and result['ticket']['priority']



@pytest.mark.asyncio
async def test_get_ticket_details_invalid_ticket():
    '''
    Testing get_ticket_details tool for invalid ticket
    '''
    result = await get_ticket_details(ticket_id='TKT-9999')
    
    assert True
    
    assert 'found' in result.keys() and not result['found']
    
    assert ('message' in result.keys()) and result['message']



@pytest.mark.asyncio
async def test_high_priority_tickets_only_returns_p1_p2():
    '''
    Testing get_high_priority_tickets tool for high priority tickets, i.e., P1 and P2
    '''
    result = await get_high_priority_tickets()
    
    assert all([(res['priority'] == 'P1') or (res['priority'] == 'P2') for res in result['tickets']])
    
    assert all([res['status'] == 'OPEN' for res in result['tickets']])