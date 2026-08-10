from src.mcp_client import available_tools

def test_multi_tool_flow():

    assert "search_issues" in available_tools
    assert "get_issue_details" in available_tools