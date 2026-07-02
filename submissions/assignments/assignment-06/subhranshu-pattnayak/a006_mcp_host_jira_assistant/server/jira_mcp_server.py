"""Jira Mcp Server File Built Using FastMcp"""

try:
    from .jira_client import JiraClient
except ImportError:
    from jira_client import JiraClient
from typing import Any
from fastmcp import FastMCP

mcp = FastMCP("Jira MCP Server")

jira_client = JiraClient()

# Tools

@mcp.tool(name="list_projects", description="Get all Jira projects")
def list_projects() -> list[dict[str, Any]]:
    return jira_client.list_projects()


@mcp.tool(name="search_issues", description="Search Jira issues using JQL.")
def search_issues(jql_query: str, max_results: int = 10) -> list[dict[str, Any]]:
    return jira_client.search_issues(jql_query, max_results)


@mcp.tool(name="get_issue_details", description="Get details of a specific issue.")
def get_issue_details(issue_key: str) -> dict[str, Any]:
    return jira_client.get_issue_details(issue_key)


@mcp.tool(name="get_issue_comments", description="Get all comments for an issue.")
def get_issue_comments(issue_key: str) -> list[dict[str, Any]]:
    return jira_client.get_issue_comments(issue_key)


@mcp.tool(name="add_issue_comment", description="Post a comment to an issue.")
def add_issue_comment(issue_key: str, comment_text: str,) -> dict[str, Any]:
    return jira_client.add_issue_comment(issue_key, comment_text)

@mcp.tool(name="update_issue_status", description="Update an issue to another status.")
def update_issue_status(issue_key: str, target_status: str) -> dict[str, Any]:
    return jira_client.update_issue_status(issue_key, target_status)

# <==================================OK==================================>

if __name__ == "__main__":
    mcp.run(transport="stdio")

