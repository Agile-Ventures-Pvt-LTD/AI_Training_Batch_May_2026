from src.nodes import parse_incident

def test_parse_incident_required_fields(mocker):
    mock_client = mocker.Mock()
    mock_response = mocker.Mock()
    mock_response.shipment_id =  "SH-4002"
    mock_response.cargo_weight_tons = 550
    mock_client.get.return_value = mock_response
    result = parse_incident(mock_client)
    assert result["shipment_id"]=="SH-4002"
    assert result["cargo_weight_tons"]==550
