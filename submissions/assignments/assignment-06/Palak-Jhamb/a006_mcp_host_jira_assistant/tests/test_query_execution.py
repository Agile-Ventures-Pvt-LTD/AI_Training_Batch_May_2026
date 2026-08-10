from server.jira_mcp_server import search_issues

def test_query_execution():
    result = search_issues("project = MCP0 AND priority = High")
    assert len(result) > 0
    assert "id" in result[0]
    assert "key" in result[0]
