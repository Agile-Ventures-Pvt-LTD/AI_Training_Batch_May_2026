import os
import logging
from mcp_use import MCPClient, MCPAgent
from langchain_groq import ChatGroq

#
os.environ["MCP_USE_ANONYMIZED_TELEMETRY"] = "false"
logging.getLogger("mcp_use").setLevel(logging.WARNING)
logging.getLogger("mcp_use.telemetry").setLevel(logging.ERROR)


def get_mcp_config():
    """Return the MCP server configuration for the Jira server."""
    server_script = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "server", "jira_mcp_server.py"
    )
    return {
        "mcpServers": {
            "jira": {
                "command": "python",
                "args": [server_script]
            }
        }
    }


def create_mcp_client():
    """Create an MCPClient configured to connect to the Jira MCP server via stdio."""
    config = get_mcp_config()
    return MCPClient(config=config)


def create_mcp_agent(llm: ChatGroq = None, system_prompt: str = None):
    """Create an MCPAgent with the Jira MCP server and Groq LLM."""
    if llm is None:
        from src.llm import get_groq_llm
        llm = get_groq_llm()

    client = create_mcp_client()

    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=10,
        verbose=False,
        pretty_print=False,
        system_prompt=system_prompt
    )
    return agent