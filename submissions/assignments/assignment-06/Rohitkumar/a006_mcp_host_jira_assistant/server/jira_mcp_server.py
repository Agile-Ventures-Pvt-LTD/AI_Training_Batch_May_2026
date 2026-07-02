import os
import requests
from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Jira MCP Server")

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL", "").rstrip("/")
JIRA_EMAIL = os.getenv("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN", "")

AUTH = (JIRA_EMAIL, JIRA_API_TOKEN)
HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


def _request(method: str, path: str, params: dict = None, json_data: dict = None) -> dict:
    """Make a Jira REST API request."""
    url = f"{JIRA_BASE_URL}/rest/api/3{path}"
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=HEADERS,
            auth=AUTH,
            params=params,
            json=json_data,
            timeout=30
        )
        response.raise_for_status()
        if response.content:
            return response.json()
        return {"success": True}
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        if response := getattr(e, "response", None):
            try:
                error_detail = response.json()
                error_msg = error_detail.get("errorMessages", [error_msg])[0]
            except (ValueError, KeyError):
                error_msg = response.text or error_msg
        return {"error": f"Jira API error: {error_msg}"}


@mcp.tool
def list_projects() -> dict:
    """
    List all Jira projects accessible to the authenticated user.
    """
    result = _request("GET", "/project")
    # Jira API returns a list for /project; wrap in dict for FastMCP compatibility
    if isinstance(result, list):
        return {"projects": result, "total": len(result)}
    return result


@mcp.tool
def search_issues(jql: str, max_results: int = 50) -> dict:
    """
    Search Jira issues using JQL (Jira Query Language).

    Args:
        jql: Jira Query Language string (e.g. 'project = TEST AND status = "In Progress"')
        max_results: Maximum number of results to return (default 50)
    """
    return _request("POST", "/search", json_data={
        "jql": jql,
        "maxResults": max_results,
        "fields": ["summary", "status", "priority", "assignee", "issuetype", "created", "updated"]
    })


@mcp.tool
def get_issue_details(issue_key: str) -> dict:
    """
    Get full details of a Jira issue by its key.

    Args:
        issue_key: The issue key (e.g. 'ABC-12', 'TEST-1')
    """
    return _request("GET", f"/issue/{issue_key}")


@mcp.tool
def get_issue_comments(issue_key: str) -> dict:
    """
    Get all comments on a Jira issue.

    Args:
        issue_key: The issue key (e.g. 'ABC-12', 'TEST-1')
    """
    return _request("GET", f"/issue/{issue_key}/comment")


@mcp.tool
def add_issue_comment(issue_key: str, comment: str) -> dict:
    """
    Add a comment to a Jira issue.

    Args:
        issue_key: The issue key (e.g. 'ABC-12', 'TEST-1')
        comment: The comment text to add
    """
    return _request("POST", f"/issue/{issue_key}/comment", json_data={
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment
                        }
                    ]
                }
            ]
        }
    })


@mcp.tool
def update_issue_status(issue_key: str, transition_id: str) -> dict:
    """
    Update the status of a Jira issue using a transition.

    Args:
        issue_key: The issue key (e.g. 'ABC-12', 'TEST-1')
        transition_id: The transition ID for the target status (e.g. '11' for In Progress, '21' for Done)
                       Use search_issues with jql='project = <KEY>' to discover available transitions.
    """
    return _request("POST", f"/issue/{issue_key}/transitions", json_data={
        "transition": {
            "id": transition_id
        }
    })





if __name__ == "__main__":
    mcp.run(transport="stdio")