from src.host import mcp_agent

# Test 11
def test_host_payment_api_change_query():
    data=mcp_agent.run("Why is the Payment API unhealthy and is there any recent change that may be related?")
    assert data is not None