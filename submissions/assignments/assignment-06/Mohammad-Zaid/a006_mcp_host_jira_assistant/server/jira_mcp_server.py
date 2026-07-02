
from pathlib import Path
import sys

from fastmcp import FastMCP
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

load_dotenv()

mcp = FastMCP("Jira_MCP_Server")

# We have to run the server in STDIO mode only
from src.config import JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN


def jira_request(
    method: str,
    endpoint: str,
    params: dict | None = None,
    payload: dict | None = None,
):
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

    headers = {
    "Accept": "application/json"
    }
    
    url = f"{JIRA_BASE_URL}{endpoint}"

    response = requests.request(
        method=method,
        url=url,
        headers=headers,
        auth=auth,
        params=params,
        json=payload,
    )

    response.raise_for_status()

    if response.text:
        return response.json()
    else:
        return {"status_code": response.status_code, "data": None, "message": "Success (No Content)"}

@mcp.tool
def list_projects():
    """
    gets the list of all the projects in the jira account
    """
    
    projects = jira_request(
        "GET",
        "/rest/api/3/project",
    )
    return [
        {
            "key": project.get("key"),
            "id": project.get("id"),
            "name": project.get("name"),
            "type": project.get("projectTypeKey"),
        }
        for project in projects
    ]
    
@mcp.tool
def search_issues(jql: str):
    """
    Search Jira issues using a JQL query.

    Examples:
    - project = AA
    - status = "To Do"
    - priority = High
    - assignee = currentUser()
    - project = AA AND status = "In Progress"
    """

    response = jira_request(
        "POST",
        "/rest/api/3/search/jql",
        payload={
            "jql": jql,
            "maxResults": 10
        }
    )
    # return response
    import json

    print(json.dumps(response, indent=4))
    issues = response.get("issues", [])

    return response.get("issues", [])
    
    
@mcp.tool
def get_issue_details(issue_key: str):
    """
    returns issue info including - key, summary, description, status, priority and due date
    Args:
    Issue key (e.g: AA-1)
    """
    
    issue = jira_request(
        "GET",
        f"/rest/api/3/issue/{issue_key}",
    )
    fields = issue["fields"]
    
    return {
    "key": issue.get("key"),
    "summary": fields.get("summary"),
    "description": fields.get("description", {}).get("content", [{}])[0].get("content", [{}])[0].get("text") 
        if fields.get("description") else None,
    "status": fields.get("status", {}).get("name"),
    "priority": fields.get("priority", {}).get("name"),
    "assignee": fields.get("assignee", {}).get("displayName"),
    "reporter": fields.get("reporter", {}).get("displayName"),
    "due_date": fields.get("duedate")
}

    
    
@mcp.tool
def get_issue_comments(issue_key: str):
    """
    gets the comment of the issue with the id, author and the updated by info.
    """
    
    issue_comments = jira_request(
        "GET",
        f"/rest/api/3/issue/{issue_key}/comment",
    )
    comments = issue_comments.get("comments", [])

    if not comments:
        return []

    first_comment = comments[0]

    return {
        "id": first_comment.get("id"),
        "author": first_comment.get("author", {}).get("displayName"),
        "author_comment": (
            first_comment.get("body", {})
            .get("content", [{}])[0]
            .get("content", [{}])[0]
            .get("text")
        ),
        "updated_by": first_comment.get("updateAuthor", {}).get("displayName"),
    }

    
    
@mcp.tool
def add_issue_comment(issue_key: str, comment: str):
    """
    adds a comment to the issue with the given issue_key
    Args:
    issue_key: str - The key of the issue to which the comment will be added.
    comment: str - The text of the comment to be added."""
    response = jira_request(
        "POST",
        f"/rest/api/3/issue/{issue_key}/comment",
        payload={
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "type": "text",
                                "text": comment,
                            }
                        ],
                    }
                ],
            }
        },
    )

    # We will now extract the updated comment from Jira's ADF format
    body_text = None
    if response.get("body") and "content" in response["body"]:
        try:
            body_text = response["body"]["content"][0]["content"][0]["text"]
        except (IndexError):
            body_text = None

    return {
        "status": "Success" if response.get("id") else "Failed",
        "id": response.get("id"),
        "author": response.get("author", {}).get("displayName"),
        "comment_text": body_text,
        "updated_by": response.get("updateAuthor", {}).get("displayName"),
    }

    
@mcp.tool
def update_issue_status(issue_key: str, status: str):
    """
    Updates the status of a Jira issue to the specified status.
    Args:
        issue_key (str): The key of the Jira issue to update.
        status (str): Status to transition the issue to.
    """
    
    transitions = jira_request(
        "GET",
        f"/rest/api/3/issue/{issue_key}/transitions"
    )

    transition_id = None
    for transition in transitions.get("transitions", []):
        if transition.get("name", "").lower() == status.lower():
            transition_id = transition.get("id")
            break

    if not transition_id:
        return {"error": f"Status '{status}' not found for Issue id:{issue_key}."}

    try:
        jira_request(
            "POST",
            f"/rest/api/3/issue/{issue_key}/transitions",
            payload={"transition": {"id": transition_id}}
        )
        return {"status": "Success", "transition_id": transition_id}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}


    
if __name__ == "__main__":
    print("Starting Jira MCP Server...")
    mcp.run(transport="stdio")
    