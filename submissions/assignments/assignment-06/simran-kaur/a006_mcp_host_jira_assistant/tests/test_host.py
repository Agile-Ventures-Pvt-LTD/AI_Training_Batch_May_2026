from src.mcp_client import config
from src.host import host_agent
from src.llm import model_llm


def test_llm():
    assert model_llm is not None


def test_mcp_client():
    assert config is not None


def test_host_agent():
    assert host_agent is not None
