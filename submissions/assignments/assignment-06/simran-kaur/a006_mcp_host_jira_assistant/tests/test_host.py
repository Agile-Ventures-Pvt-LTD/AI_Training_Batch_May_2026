from src.mcp_client import host_agent, config
from src.llm import model_llm


def test_llm():
    assert model_llm is not None


def test_mcp_client():
    assert config is not None


def test_host_agent():
    assert host_agent is not None
