from server.jira_mcp_server import mcp


def test_mcp_server_runs():
    assert mcp is not None