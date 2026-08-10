from src.mcp_client import available_tools

def test_tool_discovery():

    expected = {
        "list_projects",
        "search_issues",
        "get_issue_details",
        "get_issue_comments",
        "add_issue_comment",
        "update_issue_status",
    }

    assert expected == set(available_tools)