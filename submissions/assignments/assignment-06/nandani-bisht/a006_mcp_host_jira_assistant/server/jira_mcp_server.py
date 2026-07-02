import os

import requests
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("jira-issue-assistant")

DEFAULT_MAX_RESULTS = int(os.environ.get("JIRA_DEFAULT_MAX_RESULTS", "25"))


class JiraAPIError(Exception):
    def __init__(self, message: str, status_code: int = None):
        super().__init__(message)
        self.status_code = status_code


_session = None
_base_url = None


def _get_session():
    global _session, _base_url

    if _session is None:
        base_url = os.environ.get("JIRA_BASE_URL", "")
        email = os.environ.get("JIRA_EMAIL", "")
        api_token = os.environ.get("JIRA_API_TOKEN", "")

        if not base_url or not email or not api_token:
            raise JiraAPIError(
                "Jira credentials not configured. Set JIRA_BASE_URL, JIRA_EMAIL and "
                "JIRA_API_TOKEN in your .env file."
            )

        session = requests.Session()
        session.auth = (email, api_token)
        session.headers.update({"Accept": "application/json", "Content-Type": "application/json"})

        _session = session
        _base_url = base_url.rstrip("/")

    return _session, _base_url


def _request(method, path, **kwargs):
    session, base_url = _get_session()
    url = f"{base_url}{path}"
    try:
        response = session.request(method, url, timeout=15.0, **kwargs)
    except requests.RequestException as exc:
        raise JiraAPIError(f"Network error reaching Jira: {exc}") from exc

    if response.status_code == 410:
        raise JiraAPIError(
            f"Endpoint {path} is no longer available. "
            "Use /rest/api/3/search/jql for issue searches.",
            status_code=410,
        )
    if response.status_code == 404:
        raise JiraAPIError(f"Not found: {path}", status_code=404)
    if response.status_code == 401:
        raise JiraAPIError(
            "Jira auth failed — check JIRA_EMAIL and JIRA_API_TOKEN.",
            status_code=401,
        )
    if not response.ok:
        raise JiraAPIError(
            f"Jira returned {response.status_code} for {path}: {response.text[:500]}",
            status_code=response.status_code,
        )

    if not response.content:
        return {}
    return response.json()


def _safe_name(field):
    return field.get("name") if field else None


def _safe_display_name(field):
    return field.get("displayName") if field else "Unassigned"


def _extract_plain_text(adf_body):
    if not adf_body:
        return ""

    def walk(node):
        texts = []
        if node.get("type") == "text":
            texts.append(node.get("text", ""))
        for child in node.get("content", []):
            texts.extend(walk(child))
        return texts

    return " ".join(walk(adf_body)).strip()


def _flatten_issue(issue):
    fields = issue.get("fields", {})
    return {
        "key": issue.get("key"),
        "summary": fields.get("summary"),
        "status": _safe_name(fields.get("status")),
        "priority": _safe_name(fields.get("priority")),
        "issue_type": _safe_name(fields.get("issuetype")),
        "assignee": _safe_display_name(fields.get("assignee")),
        "updated": fields.get("updated"),
    }


@mcp.tool()
def list_projects() -> list[dict]:
    """List all Jira projects the account can see."""
    try:
        data = _request("GET", "/rest/api/3/project/search", params={"maxResults": 50})
        return [
            {
                "key": p["key"],
                "name": p["name"],
                "project_type": p.get("projectTypeKey", "unknown"),
            }
            for p in data.get("values", [])
        ]
    except JiraAPIError as exc:
        return [{"error": str(exc)}]


@mcp.tool()
def search_issues(jql: str, max_results: int = DEFAULT_MAX_RESULTS) -> list[dict]:
    """Search issues with a JQL query. max_results caps at 100."""
    try:
        max_results = max(1, min(max_results, 100))
        payload = {
            "jql": jql,
            "maxResults": max_results,
            "fields": ["summary", "status", "priority", "assignee", "issuetype", "updated"],
        }
        data = _request("POST", "/rest/api/3/search/jql", json=payload)
        return [_flatten_issue(issue) for issue in data.get("issues", [])]
    except JiraAPIError as exc:
        return [{"error": str(exc)}]


@mcp.tool()
def get_issue_details(issue_key: str) -> dict:
    """Get full details for a single issue by key, e.g. ABC-12."""
    try:
        data = _request(
            "GET",
            f"/rest/api/3/issue/{issue_key}",
            params={
                "fields": "summary,description,status,priority,assignee,reporter,"
                "issuetype,created,updated,labels,components,fixVersions"
            },
        )
        fields = data.get("fields", {})
        return {
            "key": data.get("key"),
            "summary": fields.get("summary"),
            "description": _extract_plain_text(fields.get("description")),
            "status": _safe_name(fields.get("status")),
            "priority": _safe_name(fields.get("priority")),
            "issue_type": _safe_name(fields.get("issuetype")),
            "assignee": _safe_display_name(fields.get("assignee")),
            "reporter": _safe_display_name(fields.get("reporter")),
            "labels": fields.get("labels", []),
            "created": fields.get("created"),
            "updated": fields.get("updated"),
        }
    except JiraAPIError as exc:
        return {"error": str(exc)}


@mcp.tool()
def get_issue_comments(issue_key: str) -> list[dict]:
    """Get comments on an issue. Returns author, body, and created time."""
    try:
        data = _request(
            "GET", f"/rest/api/3/issue/{issue_key}/comment", params={"maxResults": 50}
        )
        return [
            {
                "author": _safe_display_name(comment.get("author")),
                "body": _extract_plain_text(comment.get("body")),
                "created": comment.get("created"),
            }
            for comment in data.get("comments", [])
        ]
    except JiraAPIError as exc:
        return [{"error": str(exc)}]


@mcp.tool()
def add_issue_comment(issue_key: str, comment: str) -> dict:
    """Post a comment on an issue. Write operation."""
    try:
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {"type": "paragraph", "content": [{"type": "text", "text": comment}]}
                ],
            }
        }
        data = _request("POST", f"/rest/api/3/issue/{issue_key}/comment", json=payload)
        return {
            "comment_id": data.get("id"),
            "issue_key": issue_key,
            "created": data.get("created"),
        }
    except JiraAPIError as exc:
        return {"error": str(exc)}


@mcp.tool()
def update_issue_status(issue_key: str, status: str) -> dict:
    """Move an issue to a new status using its workflow transition. Write operation."""
    try:
        data = _request("GET", f"/rest/api/3/issue/{issue_key}/transitions")
        transitions = [{"id": t["id"], "name": t["name"]} for t in data.get("transitions", [])]
        match = next((t for t in transitions if t["name"].lower() == status.lower()), None)
        if match is None:
            available = ", ".join(t["name"] for t in transitions) or "none"
            return {
                "error": f"Cannot transition {issue_key} to '{status}'. "
                f"Valid options: {available}"
            }
        _request(
            "POST",
            f"/rest/api/3/issue/{issue_key}/transitions",
            json={"transition": {"id": match["id"]}},
        )
        return {"issue_key": issue_key, "new_status": match["name"]}
    except JiraAPIError as exc:
        return {"error": str(exc)}


if __name__ == "__main__":
    mcp.run(transport="stdio")
