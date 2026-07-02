from unittest.mock import patch

from server.jira_mcp_server import (
    get_issue_comments,
    get_issue_details,
)


@patch("server.jira_mcp_server.jira")
def test_multi_tool_flow(mock_jira):

    issue = type("Issue", (), {})()

    issue.key = "AP-2"

    issue.fields = type("Fields", (), {})()

    issue.fields.summary = "Payment Failure"

    issue.fields.description = "Failure"

    issue.fields.status = type("Status", (), {"name": "Open"})()

    issue.fields.priority = type("Priority", (), {"name": "Highest"})()

    issue.fields.assignee = type(
        "Assignee",
        (),
        {"displayName": "Aditya"},
    )()

    issue.fields.reporter = type(
        "Reporter",
        (),
        {"displayName": "Manager"},
    )()

    comment = type("Comment", (), {})()

    comment.author = type(
        "Author",
        (),
        {"displayName": "QA"},
    )()

    comment.body = "Looks good"

    comment.created = "2026"

    issue.fields.comment = type(
        "Comments",
        (),
        {"comments": [comment]},
    )()

    mock_jira.issue.return_value = issue

    details = get_issue_details("AP-2")

    comments = get_issue_comments("AP-2")

    assert details["key"] == "AP-2"

    assert len(comments) == 1

    assert comments[0]["author"] == "QA"