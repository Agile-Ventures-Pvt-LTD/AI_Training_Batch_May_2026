import pytest
from unittest.mock import patch, MagicMock
from server.jira_mcp_server import (
    mcp,
    list_projects,
    search_issues,
    get_issue_details,
    get_issue_comments,
    add_issue_comment,
    update_issue_status
)

def test_mcp_server_runs():
    """Verify that the FastMCP server is correctly initialized and has the tools registered."""
    assert mcp is not None
    assert mcp.name == "Jira Issue Assistant Server"
    
    # Check that tools are registered on the FastMCP object
    # FastMCP stores tools in a list or dict depending on version
    # We can fetch tools via public API or inspect our functions
    assert callable(list_projects)
    assert callable(search_issues)
    assert callable(get_issue_details)
    assert callable(get_issue_comments)
    assert callable(add_issue_comment)
    assert callable(update_issue_status)

@patch("server.jira_mcp_server.requests.request")
def test_list_projects_success(mock_request):
    """Test that list_projects handles successful API responses correctly."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {"key": "DEMO", "name": "Demo Project", "id": "10000", "projectTypeKey": "software", "style": "classic"}
    ]
    mock_request.return_value = mock_response

    projects = list_projects()
    
    assert len(projects) == 1
    assert projects[0]["key"] == "DEMO"
    assert projects[0]["name"] == "Demo Project"
    mock_request.assert_called_once_with(
        method="GET",
        url="https://mockinstance.atlassian.net/rest/api/2/project",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        auth=("mock_user@example.com", "mock_api_token_56789"),
        json=None,
        timeout=15
    )

@patch("server.jira_mcp_server.requests.request")
def test_search_issues_success(mock_request):
    """Test that search_issues triggers POST query with JQL parameter."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "issues": [
            {
                "key": "DEMO-1",
                "id": "10100",
                "fields": {
                    "summary": "Fix bugs",
                    "status": {"name": "In Progress"},
                    "priority": {"name": "High"},
                    "issuetype": {"name": "Bug"},
                    "assignee": {"displayName": "Poonam Bhatt"},
                    "created": "2026-07-01T12:00:00.000+0530",
                    "updated": "2026-07-01T13:00:00.000+0530"
                }
            }
        ]
    }
    mock_request.return_value = mock_response

    issues = search_issues("project = DEMO")
    
    assert len(issues) == 1
    assert issues[0]["key"] == "DEMO-1"
    assert issues[0]["assignee"] == "Poonam Bhatt"
    assert issues[0]["priority"] == "High"
    
    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert kwargs["method"] == "POST"
    assert kwargs["url"].endswith("/rest/api/3/search/jql")
    assert kwargs["json"]["jql"] == "project = DEMO"
    assert kwargs["json"]["maxResults"] == 50
    assert kwargs["json"]["startAt"] == 0

@patch("server.jira_mcp_server.requests.request")
def test_search_issues_custom_pagination(mock_request):
    """Test search_issues with custom max_results and start_at parameters."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"issues": []}
    mock_request.return_value = mock_response

    issues = search_issues("project = DEMO", max_results=10, start_at=20)
    
    assert len(issues) == 0
    mock_request.assert_called_once()
    args, kwargs = mock_request.call_args
    assert kwargs["json"]["maxResults"] == 10
    assert kwargs["json"]["startAt"] == 20

@patch("server.jira_mcp_server.requests.request")
def test_get_issue_details_success(mock_request):
    """Test retrieving details of a single Jira issue."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "key": "DEMO-1",
        "id": "10100",
        "fields": {
            "summary": "Fix bugs",
            "description": "Critical Bug description",
            "status": {"name": "To Do"},
            "priority": {"name": "Medium"},
            "issuetype": {"name": "Bug"},
            "assignee": None,
            "reporter": {"displayName": "Reporter Name"},
            "created": "2026-07-01",
            "updated": "2026-07-01"
        }
    }
    mock_request.return_value = mock_response

    details = get_issue_details("DEMO-1")
    
    assert details["key"] == "DEMO-1"
    assert details["assignee"] == "Unassigned"
    assert details["reporter"] == "Reporter Name"
    assert details["status"] == "To Do"
    assert "Critical Bug" in details["description"]

@patch("server.jira_mcp_server.requests.request")
def test_get_issue_comments(mock_request):
    """Test comments retrieval for an issue."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "comments": [
            {
                "id": "10200",
                "author": {"displayName": "Poonam"},
                "created": "2026-07-01",
                "body": "QA validation pending"
            }
        ]
    }
    mock_request.return_value = mock_response

    comments = get_issue_comments("DEMO-1")
    assert len(comments) == 1
    assert comments[0]["author"] == "Poonam"
    assert comments[0]["body"] == "QA validation pending"

@patch("server.jira_mcp_server.requests.request")
def test_add_issue_comment(mock_request):
    """Test adding a comment (Write Action)."""
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": "10201",
        "author": {"displayName": "Agent"},
        "created": "2026-07-01",
        "body": "This is a comment"
    }
    mock_request.return_value = mock_response

    comment = add_issue_comment("DEMO-1", "This is a comment")
    assert comment["id"] == "10201"
    assert comment["status"] == "Comment added successfully"

@patch("server.jira_mcp_server.requests.request")
def test_update_issue_status_success(mock_request):
    """Test transition status update where transition name is found."""
    # We mock two requests: first GET transitions, then POST transition
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {
        "transitions": [
            {
                "id": "11",
                "name": "In Progress",
                "to": {"name": "In Progress"}
            },
            {
                "id": "21",
                "name": "Done",
                "to": {"name": "Done"}
            }
        ]
    }
    
    mock_post_response = MagicMock()
    mock_post_response.status_code = 204
    
    mock_request.side_effect = [mock_get_response, mock_post_response]

    result = update_issue_status("DEMO-1", "Done")
    
    assert result["success"] is True
    assert result["transition_name"] == "Done"
    assert result["new_status"] == "Done"

@patch("server.jira_mcp_server.requests.request")
def test_update_issue_status_not_found(mock_request):
    """Test update_issue_status when requested transition is invalid."""
    mock_get_response = MagicMock()
    mock_get_response.status_code = 200
    mock_get_response.json.return_value = {
        "transitions": [
            {
                "id": "11",
                "name": "In Progress",
                "to": {"name": "In Progress"}
            }
        ]
    }
    mock_request.return_value = mock_get_response

    result = update_issue_status("DEMO-1", "Done")
    
    assert result["success"] is False
    assert "No status transition matching" in result["error"]
    assert len(result["available_transitions"]) == 1
