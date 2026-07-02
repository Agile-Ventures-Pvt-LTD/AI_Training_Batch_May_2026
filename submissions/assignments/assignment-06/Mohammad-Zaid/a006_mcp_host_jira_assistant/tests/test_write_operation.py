from src.mcp_client import available_tools

def test_write_operation():

    assert "add_issue_comment" in available_tools
    assert "update_issue_status" in available_tools