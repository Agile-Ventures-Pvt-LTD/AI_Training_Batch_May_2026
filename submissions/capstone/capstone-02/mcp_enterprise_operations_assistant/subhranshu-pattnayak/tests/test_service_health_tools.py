import pytest
from servers.service_health_server import list_services, get_service_health, get_active_incidents

@pytest.mark.asyncio
async def test_list_services_returns_services():
    """
    Testing list_services tool for:
    Result contains services
    Result count is greater than zero
    Each service contains service_name
    Each service contains status
    """
    result = await list_services()
    
    assert 'services' in result.keys()
    
    assert result['count'] > 0
    
    assert all([True if x['service_name'] != '' else False for x in result['services']])
    
    assert all([True if x['status'] != '' else False for x in result['services']])


@pytest.mark.asyncio
async def test_get_service_health_payment_api():
    result = await get_service_health('Payment API')
    
    assert result['found'] or result['found'] != None
    
    assert result['service']['service_name'] == 'Payment API'
    
    assert result['service']['status'] == 'UNHEALTHY'
    
    assert result['service']['error_rate_percent']
    
    assert result['service']['average_latency_ms']



@pytest.mark.asyncio
async def test_get_service_health_unknown_service():
    """Test invalid service using get_service_health"""
    result = await get_service_health(service_name='Unknown Service')
    
    assert True
    
    assert result['found'] == False
    
    assert 'message' in result.keys()


@pytest.mark.asyncio
async def test_get_active_incidents_payment_api():
    """Testing get_active_incidents tool"""
    result = await get_active_incidents('Payment API')
    
    assert result['count'] > 0
    
    assert ('incidents' in result.keys()) and any([res['status'] == 'ACTIVE' for res in result['incidents']])
    
    assert ('incidents' in result.keys()) and any([res['incident_id'] == 'INC-OPS-101' for res in result['incidents']])