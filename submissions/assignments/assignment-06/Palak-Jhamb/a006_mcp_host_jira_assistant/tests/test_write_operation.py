from server.jira_mcp_server import add_issue_comment

def test_write():
    result=add_issue_comment('MCP0-1','This is my first comment for this issue')
    assert result['id'] is not None
    assert result['message']== 'Comment added successfully to MCP0-1'