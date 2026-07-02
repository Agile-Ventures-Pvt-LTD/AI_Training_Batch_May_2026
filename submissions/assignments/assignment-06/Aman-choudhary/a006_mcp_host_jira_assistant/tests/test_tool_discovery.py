from server import jira_mcp_server
def test_tool_discovery():
    expected_tools = [
        "list_projects_tool",
        "search_issues_tool",
        "get_issue_details_tool",
        "get_issue_comments_tool",
        "add_issue_comment_tool",
        "update_issue_status_tool",
    ]
    for tool in expected_tools:
        assert hasattr(jira_mcp_server, tool)