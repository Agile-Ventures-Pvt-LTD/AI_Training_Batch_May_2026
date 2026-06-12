from src.agents.modern_agent import create_agent

def test_agent():
    agent = create_agent()
    response = agent.invoke({"input": "Show all customers"})
    assert "customers" in response["output"].lower()