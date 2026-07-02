import os
from fastmcp import FastMCP
from dotenv import load_dotenv
import requests
load_dotenv()
from requests.auth import HTTPBasicAuth

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

mcp = FastMCP(name="JIRA", instructions="This server can information regarding jira.")




#Tool 1 for listing projects
@mcp.tool
def list_projects():
    """This is use to list all projects in the jira."""
    url=f"{JIRA_BASE_URL}/rest/api/3/project/search"
    headers = {
    "Accept": "application/json"
    }
    response = requests.request(
    "GET",
    url=url,
    headers=headers,
    timeout=10,
    auth=auth
    )
    data= response.json()
    projects = data.get("values", [])

    return [
        {
            "id": p.get("id"),
            "key": p.get("key"),
            "name": p.get("name"),
            "project_type": p.get("projectTypeKey")
        }
        for p in projects
    ]


#tool 2 to search any issue
@mcp.tool
def search_issues(jql: str, max_results: int = 10):
    """This tool is use to search about an issue.
    Input: query in jql format
    output: issue details"""
    url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    payload = {
        "jql": jql,
        "maxResults": max_results,
        "fields": ["summary", "status", "priority", "assignee"]
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers,
        auth=auth,
        timeout=10
    )
    response.raise_for_status()

    data = response.json()
    issues = data.get("issues", [])

    return [
        {
            "id": issue.get("id"),
            "key": issue.get("key"),
            "summary": issue.get("fields", {}).get("summary"),
            "status": issue.get("fields", {}).get("status", {}).get("name"),
            "priority": (
                issue.get("fields", {}).get("priority", {}).get("name")
                if issue.get("fields", {}).get("priority")
                else None
            ),
            "assignee": (
                issue.get("fields", {}).get("assignee", {}).get("displayName")
                if issue.get("fields", {}).get("assignee")
                else None
            )
        }
        for issue in issues
    ]


#tool 3 to get details about an issue
@mcp.tool
def get_issue_details(issueIdOrKey:str):
    """This tool is used to get details about particular issue.
        input: id 
        output: details about the issue.  """
    url=f"{JIRA_BASE_URL}/rest/api/3/issue/{issueIdOrKey}"

    headers = {
    "Accept": "application/json"
    }
    response = requests.request(
    "GET",
    url,
    headers=headers,
    auth=auth
    )
    data=response.json()
    fields = data.get("fields", {})

    return {
        "id": data.get("id"),
        "key": data.get("key"),
        "summary": fields.get("summary"),
        "description": fields.get("description"),
        "status": fields.get("status", {}).get("name") if fields.get("status") else None,
        "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
        "assignee": fields.get("assignee", {}).get("displayName") if fields.get("assignee") else None,
        "reporter": fields.get("reporter", {}).get("displayName") if fields.get("reporter") else None,
        "issue_type": fields.get("issuetype", {}).get("name") if fields.get("issuetype") else None,
        "project": fields.get("project", {}).get("key") if fields.get("project") else None,
        "due_date": fields.get("duedate"),
        "created": fields.get("created"),
        "updated": fields.get("updated")
    }



#tool 4 to get comments of an issue
@mcp.tool
def get_issue_comments(issueIdOrKey:str):
    """This tool is used to get comments from any issue
    input: issue id or key
    output: details about comment of an issue
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issueIdOrKey}/comment"

    headers = {
    "Accept": "application/json"
    }

    response = requests.request(
    "GET",
    url=url,
    headers=headers,
    auth=auth
    )
    data=response.json()
    return [
    {
        "id": comment.get("id"),
        "author": comment.get("author", {}).get("displayName") if comment.get("author") else None,
        "comment": (
            comment.get("body", {})
                   .get("content", [{}])[0]
                   .get("content", [{}])[0]
                   .get("text")
        ),
        "created": comment.get("created"),
        "updated": comment.get("updated")
    }
    for comment in data.get("comments", [])
]


# tool 5 to add comments to an issue
@mcp.tool
def add_issue_comment(issueIdOrKey: str, comment_text: str):
    """This tool is used to add comment in any issue
    input:
    arg1: issue id or key in string
    arg2: comment text in string
    output:id and a message for comment added
    """
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issueIdOrKey}/comment"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_text
                        }
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url,
        headers=headers,
        auth=auth,
        json=payload,
        timeout=10
    )

    response.raise_for_status()
    data = response.json()

    return {
        "id": data.get("id"),
        "message": f"Comment added successfully to {issueIdOrKey}"
    }


# Tool 6 to update status of an issue
@mcp.tool
def update_issue_status(issueIdOrKey: str, status_name: str):
    """
    this tool is used to update Jira issue status using transition name.
    Example:
        update_issue_status("MCP0-3", "Done")
    """
    transitions_url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issueIdOrKey}/transitions"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    transitions_response = requests.get(
        transitions_url,
        headers=headers,
        auth=auth,
        timeout=10
    )

    transitions_response.raise_for_status()
    transitions_data = transitions_response.json()

    transitions = transitions_data.get("transitions", [])

    transition_id = None
    available_statuses = []

    for transition in transitions:
        name = transition.get("name")
        if name:
            available_statuses.append(name)

        if name and name.lower() == status_name.lower():
            transition_id = transition.get("id")

    if not transition_id:
        return {
            "issue_key": issueIdOrKey,
            "updated": False,
            "requested_status": status_name,
            "available_transitions": available_statuses,
            "message": f"Status '{status_name}' is not a valid transition for {issueIdOrKey}"
        }

    update_url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issueIdOrKey}/transitions"

    payload = {
        "transition": {
            "id": transition_id
        }
    }

    update_response = requests.post(
        update_url,
        headers=headers,
        auth=auth,
        json=payload,
        timeout=10
    )

    update_response.raise_for_status()

    return {
        "issue_key": issueIdOrKey,
        "updated": True,
        "new_status": status_name,
        "message": f"{issueIdOrKey} moved to '{status_name}'"
    }

if __name__ == "__main__":
    mcp.run()