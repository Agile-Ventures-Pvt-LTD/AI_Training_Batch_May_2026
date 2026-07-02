from unittest.mock import patch

from server.jira_mcp_server import add_issue_comment


@patch("server.jira_mcp_server.jira")
def test_write_operation(mock_jira):
    mock_jira.add_comment.return_value = None
    result = add_issue_comment(
        "AP-1",
        "QA validation pending",
    )
    assert result["success"] is True
    mock_jira.add_comment.assert_called_once()