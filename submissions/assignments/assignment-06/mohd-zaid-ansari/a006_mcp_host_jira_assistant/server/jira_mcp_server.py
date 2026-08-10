import os
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
load_dotenv()

from typing import Any, Dict
from pathlib import Path
from fastmcp import FastMCP

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

JIRA_BASE_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_USERNAME")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
}

mcp = FastMCP("Jira mcp server")

#====================================================================================================================================

@mcp.tool()
def list_projects() -> list[Dict]:
    """Fetches and list all the Jira Projects."""
    url=f"{JIRA_BASE_URL}/rest/api/3/project"

    response=requests.get(url=url,headers=headers,auth=auth)
    response.raise_for_status()
    projects=response.json()

    return[{
        "id":project["id"],
        "key":project["key"],
        "name":project["name"],
        "project_type":project["projectTypeKey"],
    }
    for project in projects
    ]

#========================================================================================================================================

@mcp.tool()
def search_issues(jql:str) -> list[Dict]:
    """Search jira issues using a JQL query."""
    url=f"{JIRA_BASE_URL}/rest/api/3/search/jql"
    params={"jql":jql, "maxResults":10,"fields": "summary,status,priority,assignee,issuetype"}
    response=requests.get(url=url,headers=headers,auth=auth,params=params)
    response.raise_for_status()
    data=response.json()
    issues=response.json().get("issues", [])
    return [
        {
            "key": issue["key"],
            "summary": issue["fields"]["summary"],
            "status": issue["fields"]["status"]["name"],
            "priority": (
                issue["fields"]["priority"]["name"]
                if issue["fields"]["priority"]
                else None
            ),
            "assignee": (
                issue["fields"]["assignee"]["displayName"]
                if issue["fields"]["assignee"]
                else "Unassigned"
            ),
        }
        for issue in issues
    ]

#================================================================================================================================

@mcp.tool()
def get_issue_details(issue_key: str) -> str:
    """Retrieve details of a specific Jira issue."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"
        response = requests.get(url=url,headers=headers,auth=auth,timeout=10)
        response.raise_for_status()
        issue = response.json()
        fields = issue.get("fields", {})
        summary = fields.get("summary", "No Summary")
        status = fields.get("status", {}).get("name", "Unknown")
        assignee = (
            fields.get("assignee", {}).get("displayName", "Unassigned")
            if fields.get("assignee")
            else "Unassigned"
        )
        description = fields.get("description", "No description available.")
        return (
            f"Issue Key : {issue_key}"
            f"Summary   : {summary}"
            f"Status    : {status}"
            f"Assignee  : {assignee}"
            f"Description:{description}"
        )
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Issue '{issue_key}' not found."
        return f"Jira API Error ({e.response.status_code}): {e.response.text}"
    except Exception as e:
        return f"Unexpected Error: {e}"
    
#===============================================================================================================================

@mcp.tool()
def get_issue_comments(issue_key: str) -> str:
    """Retrieve all comments for a specific Jira issue."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"
        response = requests.get(
            url=url,
            headers=headers,
            auth=auth,
            timeout=10,
        )
        response.raise_for_status()
        comments = response.json().get("comments", [])
        if not comments:
            return f"No comments found for issue '{issue_key}'."
        output = [f"Comments for {issue_key}:\n"]
        for index, comment in enumerate(comments, start=1):
            author = comment.get("author", {}).get("displayName","Unknown User")
            body = comment.get("body")
            comment_text = ""
            if isinstance(body, dict):
                try:
                    for block in body.get("content", []):
                        for item in block.get("content", []):
                            if item.get("type") == "text":
                                comment_text += item.get("text", "")
                except Exception:
                    comment_text = "[Unable to parse comment]"
            else:
                    comment_text = body or "No comment"
            output.append(
                f"{index}. {author}\n"
                f"{comment_text}\n"
            )
        return "\n".join(output)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return f"Issue '{issue_key}' not found."
        return (
            f"Jira API Error ({e.response.status_code}): "
            f"{e.response.text}"
        )
    except Exception as e:
        return f"Unexpected Error: {e}"
    
#================================================================================================================================

@mcp.tool()
def add_issue_comment(issue_key: str, comment_text: str):
    """Adds a plain text comment to a Jira issue using the v2 API."""
    try:
        url = f"{JIRA_BASE_URL}/rest/api/2/issue/{issue_key}/comment"
        payload = {"body": comment_text}
        response = requests.post(url=url, json=payload, headers=headers, auth=auth)
        response.raise_for_status()
        return f"Successfully added comment to {issue_key}."
    except Exception as e:
        return f"Error adding comment: {str(e)}"

#================================================================================================================================

@mcp.tool()
def update_issue_status(issue_key: str, status_name: str):
    """
    Updates the status of a Jira issue (e.g., 'Done', 'In Progress').
    """
    try:
        url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
        res = requests.get(url=url, auth=auth, headers=headers)
        res.raise_for_status()
        transitions = res.json().get("transitions", [])
        transition_id = next((t["id"] for t in transitions if t["name"].lower() == status_name.lower()), None)
        if not transition_id:
            valid_statuses = ", ".join([t["name"] for t in transitions])
            return f"Error: Status '{status_name}' not found. Available: {valid_statuses}"
        payload = {"transition": {"id": transition_id}}
        post_res = requests.post(url=url, json=payload, auth=auth, headers=headers)
        post_res.raise_for_status()
        return f"Successfully moved {issue_key} to '{status_name}'."
    except Exception as e:
        return f"Failed to update status: {str(e)}"

#================================================================================================================================
if __name__ == "__main__":
    mcp.run()

