import os
import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp=FastMCP("Jira assistant")

BASE_URL = os.getenv("JIRA_BASE_URL").rstrip("/")
EMAIL = os.getenv("JIRA_EMAIL")
TOKEN = os.getenv("JIRA_API_TOKEN")

AUTH = (EMAIL, TOKEN)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

@mcp.tool
def list_projects():
    """List all jira projects"""

    url=f"{BASE_URL}/rest/api/3/project"
    response=requests.get(
        url,
   headers=HEADERS,
   auth=AUTH
)
    response.raise_for_status()
    projects = response.json()
    return [
            {
                "key": p["key"],
                "name": p["name"]
            }
            for p in projects
        ]

@mcp.tool
def search_issues(jql):
    """Search jira issues using JQL"""
    if not jql or not jql.strip():
        jql = "issuekey != null"
    url=f"{BASE_URL}/rest/api/3/search/jql"
    body={
        "jql": jql,
        "maxResults": 5,
        "fields": ["summary", "status"]
    }
    response = requests.post(
            url,
            json=body,
            headers=HEADERS,
            auth=AUTH
        )
    response.raise_for_status()
    issues = response.json().get("issues", [])
    if not issues:
        return "No issues found matching the query."
    return [
            {
                "key": issue["key"],
                "summary": issue["fields"]["summary"],
                "status": issue["fields"]["status"]["name"]
            }
            for issue in issues
        ]

@mcp.tool
def get_issue_details(issue_key):
    """Get details of jira issue"""
    url=f"{BASE_URL}/rest/api/3/issue/{issue_key}"
    response=requests.get(
        url,
        headers=HEADERS,
        auth=AUTH
    )
    response.raise_for_status()
    issue = response.json()
    return {
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "status": issue["fields"]["status"]["name"],
            "description": issue["fields"].get("description")
        }

@mcp.tool
def get_issue_comments(issue_key):
    """Get comments of a jira issue"""
    url=f"{BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    response=requests.get(
        url,
        headers=HEADERS,
        auth=AUTH
    )
    response.raise_for_status()
    comments = response.json().get("comments", [])
    if not comments:
        return "No comments found."
    return [comment["body"] for comment in comments]

@mcp.tool
def add_issue_comment(issue_key,text):
    """Add a comment to a jira issue"""
    url=f"{BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    body = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": text
                        }
                    ]
                }
            ]
        }
    }
    response = requests.post(
            url,
            json=body,
            headers=HEADERS,
            auth=AUTH
        )
    response.raise_for_status()
    return f"Comment added to {issue_key}"

@mcp.tool
def update_issue_status(issue_key, transition_id):
    """Update the status of a jira issue.
    transition_id can be a numeric ID or a transition/status name ('In Progress', 'In Review', 'Done').
    """
    transitions_url = f"{BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    response = requests.get(
        transitions_url,
        headers=HEADERS,
        auth=AUTH
    )
    response.raise_for_status()
    transitions = response.json().get("transitions", [])

    matched_id = None
    for t in transitions:
        if str(t.get("id")) == str(transition_id):
            matched_id = t["id"]
            break
        if t.get("name", "").strip().lower() == str(transition_id).strip().lower():
            matched_id = t["id"]
            break
        if t.get("to", {}).get("name", "").strip().lower() == str(transition_id).strip().lower():
            matched_id = t["id"]
            break

    body = {
        "transition": {
            "id": matched_id
        }
    }
    response = requests.post(
            transitions_url,
            json=body,
            headers=HEADERS,
            auth=AUTH
        )
    response.raise_for_status()
    return f"Updated {issue_key} successfully"

if __name__ == "__main__":
    mcp.run()