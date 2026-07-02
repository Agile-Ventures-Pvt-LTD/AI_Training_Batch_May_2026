from jira import JIRA
from fastmcp import FastMCP

from config import (
    JIRA_BASE_URL,
    JIRA_EMAIL,
    JIRA_API_TOKEN,
    validate_env,
)


validate_env()


jira = JIRA(
    server=JIRA_BASE_URL,
    basic_auth=(
        JIRA_EMAIL,
        JIRA_API_TOKEN,
    ),
)


mcp = FastMCP("Jira MCP Server")



@mcp.tool()
def list_projects():
    """
    List all Jira projects.
    """

    projects = jira.projects()

    return [
        {
            "key": project.key,
            "name": project.name,
        }
        for project in projects
    ]



@mcp.tool()
def search_issues(jql: str, max_results: int = 10):
    """
    Search Jira issues using JQL.
    """

    issues = jira.search_issues(
        jql_str=jql,
        maxResults=max_results,
    )

    results = []

    for issue in issues:
        results.append(
            {
                "key": issue.key,
                "summary": issue.fields.summary,
                "status": issue.fields.status.name,
                "priority": (
                    issue.fields.priority.name
                    if issue.fields.priority
                    else None
                ),
                "assignee": (
                    issue.fields.assignee.displayName
                    if issue.fields.assignee
                    else "Unassigned"
                ),
            }
        )

    return results



@mcp.tool()
def get_issue_details(issue_key: str):
    """
    Get detailed information about an issue.
    """

    issue = jira.issue(issue_key)

    return {
        "key": issue.key,
        "summary": issue.fields.summary,
        "description": issue.fields.description,
        "status": issue.fields.status.name,
        "priority": (
            issue.fields.priority.name
            if issue.fields.priority
            else None
        ),
        "reporter": (
            issue.fields.reporter.displayName
            if issue.fields.reporter
            else None
        ),
        "assignee": (
            issue.fields.assignee.displayName
            if issue.fields.assignee
            else "Unassigned"
        ),
        "created": str(issue.fields.created),
        "updated": str(issue.fields.updated),
    }



@mcp.tool()
def get_issue_comments(issue_key: str):
    """
    Retrieve comments of an issue.
    """

    issue = jira.issue(issue_key)

    comments = []

    for comment in issue.fields.comment.comments:
        comments.append(
            {
                "author": comment.author.displayName,
                "created": str(comment.created),
                "body": comment.body,
            }
        )

    return comments


@mcp.tool()
def add_issue_comment(issue_key: str, comment: str):
    """
    Add a comment to an issue.
    """

    jira.add_comment(
        issue_key,
        comment,
    )

    return {
        "success": True,
        "message": f"Comment added to {issue_key}"
    }



@mcp.tool()
def update_issue_status(issue_key: str, transition_name: str):
    """
    Change issue workflow status.
    """

    transitions = jira.transitions(issue_key)

    transition_id = None

    for transition in transitions:
        if transition["name"].lower() == transition_name.lower():
            transition_id = transition["id"]
            break

    if transition_id is None:
        return {
            "success": False,
            "message": "Transition not found.",
        }

    jira.transition_issue(
        issue_key,
        transition_id,
    )

    return {
        "success": True,
        "message": (
            f"{issue_key} moved to "
            f"{transition_name}"
        ),
    }


if __name__ == "__main__":
    mcp.run()