from unittest.mock import MagicMock, patch

import requests

from server.jira_mcp_server import (
    add_issue_comment,
    get_issue_comments,
    get_issues_details,
    list_projects,
    search_issues,
    update_issue_status,
)


@patch("server.jira_mcp_server.requests.get")
def test_list_projects_http_error(mock_get):
    response = MagicMock()
    response.status_code = 500
    response.text = "Internal Server Error"

    error = requests.exceptions.HTTPError(response=response)

    mock_get.return_value.raise_for_status.side_effect = error

    result = list_projects()

    assert "HTTP Error" in result


@patch("server.jira_mcp_server.requests.get")
def test_list_projects_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()

    result = list_projects()

    assert "timed out" in result.lower()


@patch("server.jira_mcp_server.requests.post")
def test_search_issues_exception(mock_post):
    mock_post.side_effect = Exception("Connection Failed")

    result = search_issues("project=TEST")

    assert "Connection Failed" in result


@patch("server.jira_mcp_server.requests.get")
def test_get_issue_details_not_found(mock_get):
    response = MagicMock()
    response.status_code = 404
    response.text = "Issue Not Found"

    error = requests.exceptions.HTTPError(response=response)

    mock_get.return_value.raise_for_status.side_effect = error

    result = get_issues_details("TEST-999")

    assert "does not exist" in result


@patch("server.jira_mcp_server.requests.get")
def test_get_issue_comments_timeout(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()

    result = get_issue_comments("TEST-1")

    assert "timed out" in result.lower()


@patch("server.jira_mcp_server.requests.post")
def test_add_issue_comment_not_found(mock_post):
    response = MagicMock()
    response.status_code = 404
    response.text = "Not Found"

    error = requests.exceptions.HTTPError(response=response)

    mock_post.return_value.raise_for_status.side_effect = error

    result = add_issue_comment(
        "TEST-999",
        "Hello",
    )

    assert "does not exist" in result


@patch("server.jira_mcp_server.requests.post")
def test_update_issue_status_invalid_transition(mock_post):
    response = MagicMock()
    response.status_code = 400
    response.text = "Bad Request"

    error = requests.exceptions.HTTPError(response=response)

    mock_post.return_value.raise_for_status.side_effect = error

    result = update_issue_status(
        "TEST-1",
        "999",
    )

    assert "invalid" in result.lower()


@patch("server.jira_mcp_server.requests.post")
def test_update_issue_status_not_found(mock_post):
    response = MagicMock()
    response.status_code = 404
    response.text = "Not Found"

    error = requests.exceptions.HTTPError(response=response)

    mock_post.return_value.raise_for_status.side_effect = error

    result = update_issue_status(
        "TEST-999",
        "31",
    )

    assert "does not exist" in result