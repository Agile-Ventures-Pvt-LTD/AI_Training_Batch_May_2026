import os 
from dotenv import load_dotenv
from fastmcp import FastMCP
import requests
from requests.auth import HTTPBasicAuth
from requests.exceptions import HTTPError, RequestException, Timeout

load_dotenv()
JIRA_BASE_URL = os.getenv('JIRA_BASE_URL')
JIRA_EMAIL = os.getenv('JIRA_EMAIL')
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

mcp = FastMCP("JIRA_MCP_Server")

def auth():
    return HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

def headers():
    return {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

@mcp.tool()
def list_projects() -> str:
    """List all Jira projects available in the connected instance."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/project"
        response = requests.get(url, auth=auth(), headers=headers(), timeout=10)
        response.raise_for_status()
        projects = response.json()
        result = []
        for p in projects:
            result.append(f"Key:{p.get('key')}, Name:{p.get('name')}")
        return "\n".join(result) if result else "No Project Found" 
    except HTTPError as h:
        return f"Jira API HTTP Error while fetching projects: {h.response.status_code} - {h.response.text}"
    except Timeout:
        return "Network request timed out while listing projects."

@mcp.tool()
def search_issues(jql: str) -> str:
    """Search Jira issues using JQL."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"
        payload = {"jql": jql,"maxResults": 50,"fields": ["summary","status","priority"]}
        response = requests.post(
            url,
            auth=auth(),
            headers=headers(),
            json=payload,
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        issues = data.get("issues", [])
        result = []
        for issue in issues:
            fields = issue.get("fields", {})
            result.append(
                f"[{issue.get('key')}] "
                f"{fields.get('summary')} "
                f"(Status: {fields.get('status', {}).get('name')}, "
                f"Priority: {fields.get('priority', {}).get('name', 'None')})"
            )
        return "\n".join(result) if result else "No issues found."

    except HTTPError as e:
        return f"{e.response.status_code}: {e.response.text}"
    except Exception as e:
        return str(e)
    
@mcp.tool()
def get_issues_details(issue_key: str) -> str:
    """Retrieve detailed properties including summary, description, and status of single Jira issue."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
        response = requests.get(url, auth=auth(), headers=headers(), timeout=10)
        response.raise_for_status()
        data = response.json()
        fields = data.get("fields", {})
        summary = fields.get("summary")
        status = fields.get("status", {}).get("name")
        priority = fields.get("priority", {}).get("name", "None")
        description = fields.get("description", "No description available.")
        
        return f"Issue: {issue_key}\nSummary: {summary}\nStatus: {status}\nPriority: {priority}\nDescription: {description}"
    except HTTPError as h:
        if h.response.status_code == 404:
            return f"Error: Issue with key '{issue_key}' does not exist."
        return f"Jira API Fetch Issue HTTP Error: {h.response.status_code} - {h.response.text}"
    except Timeout:
        return f"Network request timed out while fetching details for {issue_key}."

@mcp.tool()
def get_issue_comments(issue_key: str) -> str:
    """Get all user comments attached to a specific Jira issue key."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
        response = requests.get(url, auth=auth(), headers=headers(), timeout=10)
        response.raise_for_status()
        
        comments = response.json().get("comments", [])
        result = []
        for c in comments:
            author = c.get("author", {}).get("displayName", "Unknown")
            body_text = c.get("body", "")
            result.append(f"Author: {author}\nComment: {str(body_text)}\n")
        return "\n".join(result) if result else "No comments found on this issue."
    except Timeout:
        return f"Network request timed out while fetching comments for {issue_key}."
    except RequestException as re:
        return f"Network connectivity problem occurred: {str(re)}"
    except HTTPError as e:
        if e.response.status_code == 404:
          return f"Issue '{issue_key}' not found."
        return f"{e.response.status_code}: {e.response.text}"

@mcp.tool()
def add_issue_comment(issue_key: str, comment: str) -> str:
    """Add a new comment string to an existing Jira issue key."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": comment}]
                    }
                ]
            }
        }
        response = requests.post(url, json=payload, auth=auth(), headers=headers(), timeout=10)
        response.raise_for_status()
        
        if response.status_code in (200, 201):
           return f"Success: Comment added to issue {issue_key}."
        return f"Failed to add comment. Server returned status: {response.status_code}."
    except HTTPError as he:
        if he.response.status_code == 404:
            return f"Error: Issue with key '{issue_key}' does not exist to add a comment."
        return f"Jira API Add Comment HTTP Error: {he.response.status_code} - {he.response.text}"
    except Timeout:
        return f"Network request timed out while attempting to comment on {issue_key}."

@mcp.tool()
def update_issue_status(issue_key: str, transition_id: str) -> str:
    """Transition an issue status using a valid workflow transition ID."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
        payload = {"transition": {"id": transition_id}}
        response = requests.post(url, json=payload, auth=auth(), headers=headers(), timeout=10)
        response.raise_for_status()
        if response.status_code == 204:
            return f"Success: Status updated for issue {issue_key}."
        return f"Failed to update status. Server returned status: {response.status_code}."
        
    except HTTPError as he:
        if he.response.status_code == 400:
            return f"Error: Transition ID '{transition_id}' is invalid or illegal for the current status workflow of {issue_key}."
        if he.response.status_code == 404:
            return f"Error: Issue with key '{issue_key}' does not exist."
        return f"Jira API Status Update HTTP Error: {he.response.status_code} - {he.response.text}"
    except Timeout:
        return f"Network request timed out while updating status for {issue_key}."

if __name__ == "__main__":
    mcp.run()