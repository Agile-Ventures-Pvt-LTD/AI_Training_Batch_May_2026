from pathlib import Path

def test_mcp_server_exists():
    assert Path("server/jira_mcp_server.py").exists()