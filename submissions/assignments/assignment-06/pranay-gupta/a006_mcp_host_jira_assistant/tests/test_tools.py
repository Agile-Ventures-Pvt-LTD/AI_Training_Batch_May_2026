from unittest.mock import MagicMock, patch

from server.jira_mcp_server import (
    add_issue_comment,
    get_issue_comments,
    get_issues_details,
    list_projects,
    search_issues,
    update_issue_status,
)


@patch("server.jira_mcp_server.requests.get")
def test_list_projects(mock_get):
    response = MagicMock()

    response.raise_for_status.return_value = None

    response.json.return_value = [
        {
            "key": "TEST",
            "name": "Test Project",
        }
    ]

    mock_get.return_value = response

    result = list_projects()

    assert "TEST" in result

    assert "Test Project" in result


@patch("server.jira_mcp_server.requests.post")
def test_search_issues(mock_post):
    response = MagicMock()

    response.raise_for_status.return_value = None

    response.json.return_value = {
        "issues": [
            {
                "key": "TEST-1",
                "fields": {
                    "summary": "Bug",
                    "status": {
                        "name": "Open",
                    },
                    "priority": {
                        "name": "High",
                    },
                },
            }
        ]
    }

    mock_post.return_value = response

    result = search_issues("status=Open")

    assert "TEST-1" in result

    assert "Bug" in result

    assert "Open" in result


@patch("server.jira_mcp_server.requests.get")
def test_get_issue_details(mock_get):
    response = MagicMock()

    response.raise_for_status.return_value = None

    response.json.return_value = {
        "fields": {
            "summary": "Login Bug",
            "status": {
                "name": "Open",
            },
            "priority": {
                "name": "High",
            },
            "description": "Unable to login",
        }
    }

    mock_get.return_value = response

    result = get_issues_details("TEST-1")

    assert "Login Bug" in result

    assert "Open" in result

    assert "High" in result


@patch("server.jira_mcp_server.requests.get")
def test_get_issue_comments(mock_get):
    response = MagicMock()

    response.raise_for_status.return_value = None

    response.json.return_value = {
        "comments": [
            {
                "author": {
                    "displayName": "Pranay",
                },
                "body": "Looks good",
            }
        ]
    }

    mock_get.return_value = response

    result = get_issue_comments("TEST-1")

    assert "Pranay" in result

    assert "Looks good" in result


@patch("server.jira_mcp_server.requests.post")
def test_add_issue_comment(mock_post):
    response = MagicMock()

    response.raise_for_status.return_value = None

    response.status_code = 201

    mock_post.return_value = response

    result = add_issue_comment(
        "TEST-1",
        "New Comment",
    )

    assert "Success" in result


@patch("server.jira_mcp_server.requests.post")
def test_update_issue_status(mock_post):
    response = MagicMock()

    response.raise_for_status.return_value = None

    response.status_code = 204

    mock_post.return_value = response

    result = update_issue_status(
        "TEST-1",
        "31",
    )

    assert "Success" in result