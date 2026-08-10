import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from jira import JIRA
from mcp.server.fastmcp import FastMCP
from output_logger import record_tool

load_dotenv()

JIRA_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

if not all([JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
    raise RuntimeError("Missing Jira environment variables.")

jira = JIRA(
    server=JIRA_URL,
    basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
)

mcp = FastMCP("Jira MCP Server")

# Business Functions

def list_projects() -> List[Dict[str, Any]]:
    projects = jira.projects()
    return [{"key": p.key, "name": p.name} for p in projects]


def search_issues(jql: str, max_results: int = 20):
    issues = jira.search_issues(jql, maxResults=max_results)
    return [
        {
            "key": i.key,
            "summary": i.fields.summary,
            "type": i.fields.issuetype.name,
            "status": i.fields.status.name,
            "priority": getattr(i.fields.priority, "name", None),
        }
        for i in issues
    ]


def get_issue_details(issue_key: str):
    issue = jira.issue(issue_key)
    return {
        "key": issue.key,
        "summary": issue.fields.summary,
        "description": getattr(issue.fields.description, "content", issue.fields.description),
        "status": issue.fields.status.name,
        "priority": getattr(issue.fields.priority, "name", None),
        "assignee": getattr(issue.fields.assignee, "displayName", None),
        "reporter": getattr(issue.fields.reporter, "displayName", None),
    }


def get_issue_comments(issue_key: str):
    issue = jira.issue(issue_key)
    return [
        {
            "author": c.author.displayName,
            "comment": getattr(c.body, "content", c.body),
            "created": c.created,
        }
        for c in issue.fields.comment.comments
    ]


def add_issue_comment(issue_key: str, comment: str):
    jira.add_comment(issue_key, comment)
    return {"success": True, "message": "Comment added."}


def update_issue_status(issue_key: str, status_name: str):
    transitions = jira.transitions(issue_key)
    transition_id = None

    for t in transitions:
        if t["name"].lower() == status_name.lower():
            transition_id = t["id"]
            break

    if transition_id is None:
        return {
            "success": False,
            "available_statuses": [t["name"] for t in transitions],
        }

    jira.transition_issue(issue_key, transition_id)
    return {
        "success": True,
        "message": f"Status updated to {status_name}"
    }


# MCP Tools

@mcp.tool(name="list_projects")
def list_projects_tool():
    """List all Jira projects available to the authenticated user."""
    record_tool("list_projects")
    return list_projects()


@mcp.tool(name="search_issues")
def search_issues_tool(jql: str, max_results: int = 20):
    """Search Jira issues using a JQL query.

    Args:
        jql: Valid Jira Query Language expression.
        max_results: Maximum issues to return.
    """
    record_tool("search_issues")
    return search_issues(jql, max_results)


@mcp.tool(name="get_issue_details")
def get_issue_details_tool(issue_key: str):
    """Retrieve complete details for a Jira issue.

    Args:
        issue_key: Jira issue key such as AP-1.
    """
    record_tool("get_issue_details")
    return get_issue_details(issue_key)


@mcp.tool(name="get_issue_comments")
def get_issue_comments_tool(issue_key: str):
    """Retrieve all comments associated with a Jira issue.

    Args:
        issue_key: Jira issue key such as AP-1.
    """
    record_tool("get_issue_comments")
    return get_issue_comments(issue_key)


@mcp.tool(name="add_issue_comment")
def add_issue_comment_tool(issue_key: str, comment: str):
    """Add a comment to a Jira issue.

    Args:
        issue_key: Jira issue key.
        comment: Comment text to add.
    """
    record_tool("add_issue_comment")
    return add_issue_comment(issue_key, comment)


@mcp.tool(name="update_issue_status")
def update_issue_status_tool(issue_key: str, status_name: str):
    """Transition a Jira issue to another workflow status.

    Args:
        issue_key: Jira issue key.
        status_name: Target workflow status (e.g. Open, In Progress, Done).
    """
    record_tool("update_issue_status")
    return update_issue_status(issue_key, status_name)


if __name__ == "__main__":
    mcp.run(transport="stdio")
