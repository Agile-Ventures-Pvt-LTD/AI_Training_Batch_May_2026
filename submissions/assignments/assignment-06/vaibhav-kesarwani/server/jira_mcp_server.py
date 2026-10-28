import os
from dotenv import load_dotenv
from jira import JIRA
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("jira-tools")


jira = JIRA(
    server=os.getenv("JIRA_BASE_URL"),
    basic_auth=(
        os.getenv("JIRA_EMAIL"),
        os.getenv("JIRA_API_TOKEN")
    )
)


@mcp.tool()
def list_projects():
    """List all the Jira projects / spaces in my jira account"""

    projects = jira.projects()

    return [
        {
            "key": p.key,
            "name": p.name
        }
        for p in projects
    ]


@mcp.tool()
def search_issues(jql: str):
    """Search Jira issues into the spaces"""

    issues = jira.search_issues(jql)

    return [
        {
            "key": i.key,
            "summary": i.fields.summary,
            "status": i.fields.status.name
        }
        for i in issues
    ]


@mcp.tool()
def get_issue_details(issue_key: str):
    """Get Jira issue details from the projects / spaces"""

    issue = jira.issue(issue_key)

    return {
        "key": issue.key,
        "summary": issue.fields.summary,
        "description": str(issue.fields.description),
        "status": issue.fields.status.name,
        "assignee": (
            issue.fields.assignee.displayName
            if issue.fields.assignee
            else None
        )
    }


@mcp.tool()
def get_issue_comments(issue_key: str):
    """Get comments for todos from the jira spaces / projects."""

    issue = jira.issue(issue_key)

    return [
        {
            "author": c.author.displayName,
            "comment": c.body
        }
        for c in issue.fields.comment.comments
    ]


@mcp.tool()
def add_issue_comment(issue_key: str, comment: str):
    """Add comment to the issue in the jira account"""

    jira.add_comment(issue_key, comment)

    return {
        "success": True
    }


@mcp.tool()
def update_issue_status(issue_key: str, transition_id: str):
    """Update issue status in the jira space / project"""

    jira.transition_issue(issue_key, transition_id)

    return {
        "success": True
    }


if __name__ == "__main__":
    mcp.run()