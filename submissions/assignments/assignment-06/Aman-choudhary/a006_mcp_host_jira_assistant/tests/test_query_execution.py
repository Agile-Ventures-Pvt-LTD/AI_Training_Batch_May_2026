from unittest.mock import patch

from server.jira_mcp_server import search_issues


@patch("server.jira_mcp_server.jira")
def test_query_execution(mock_jira):

    issue = type("Issue", (), {})()

    issue.key = "AP-1"

    issue.fields = type("Fields", (), {})()

    issue.fields.summary = "Login Bug"

    issue.fields.issuetype = type("IssueType", (), {"name": "Bug"})()

    issue.fields.status = type("Status", (), {"name": "Open"})()

    issue.fields.priority = type("Priority", (), {"name": "High"})()

    mock_jira.search_issues.return_value = [issue]

    result = search_issues("project=AP")

    assert len(result) == 1

    assert result[0]["key"] == "AP-1"