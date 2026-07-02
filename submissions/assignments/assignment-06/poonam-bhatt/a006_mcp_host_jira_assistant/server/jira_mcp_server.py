import os
import sys
import logging
from typing import Dict, Any, List, Optional
import requests
from dotenv import load_dotenv

# Try importing FastMCP from standalone package first, then from the official mcp SDK fallback
try:
    from fastmcp import FastMCP
except ImportError:
    try:
        from mcp.server.fastmcp import FastMCP
    except ImportError:
        print("Error: Could not import FastMCP. Please ensure mcp or fastmcp is installed.", file=sys.stderr)
        sys.exit(1)

# Add project root to sys.path to allow importing from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.logging_config import setup_logging

# Configure logging
setup_logging(logging.INFO)
logger = logging.getLogger("jira-mcp-server")

# Load environment variables
load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Initialize FastMCP Server
mcp = FastMCP("Jira Issue Assistant Server")

def get_jira_headers() -> Dict[str, str]:
    """Return standard headers for Jira Cloud API requests."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

def get_jira_auth() -> tuple:
    """Return Basic Authentication tuple for Jira Cloud API requests."""
    return (JIRA_EMAIL, JIRA_API_TOKEN)

def make_request(method: str, endpoint: str, json_data: Optional[Dict[str, Any]] = None) -> Any:
    """Helper method to make authenticated requests to Jira Cloud API."""
    if not JIRA_BASE_URL or not JIRA_EMAIL or not JIRA_API_TOKEN:
        raise ValueError(
            "Jira credentials are not fully configured. "
            "Please check JIRA_BASE_URL, JIRA_EMAIL, and JIRA_API_TOKEN in your environment."
        )
    
    # Normalize JIRA_BASE_URL (remove trailing slash)
    base_url = JIRA_BASE_URL.rstrip('/')
    url = f"{base_url}{endpoint}"
    
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=get_jira_headers(),
            auth=get_jira_auth(),
            json=json_data,
            timeout=15
        )
        
        # Raise HTTP errors if they occurred
        response.raise_for_status()
        
        if response.status_code == 204:
            return None
        return response.json()
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Jira API call to {url} failed: {e}")
        # Extract response content if available to provide a detailed error
        if e.response is not None:
            try:
                error_details = e.response.json()
                logger.error(f"Jira error details: {error_details}")
                # Format error messages nicely
                messages = error_details.get("errorMessages", [])
                errors = error_details.get("errors", {})
                if messages:
                    detail = "; ".join(messages)
                elif errors:
                    detail = "; ".join([f"{k}: {v}" for k, v in errors.items()])
                else:
                    detail = e.response.text
                raise ValueError(f"Jira API Error ({e.response.status_code}): {detail}")
            except Exception:
                raise ValueError(f"Jira API Error ({e.response.status_code}): {e.response.text}")
        raise ValueError(f"Connection to Jira failed: {str(e)}")

# Tools Exposing Jira APIs

@mcp.tool()
def list_projects() -> List[Dict[str, Any]]:
    """List all Jira projects accessible by the authenticated user.
    
    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing project key, name, id, and style.
    """
    logger.info("Calling list_projects")
    data = make_request("GET", "/rest/api/2/project")
    if not isinstance(data, list):
        return []
        
    projects = []
    for proj in data:
        projects.append({
            "key": proj.get("key"),
            "name": proj.get("name"),
            "id": proj.get("id"),
            "projectTypeKey": proj.get("projectTypeKey"),
            "style": proj.get("style", "classic")
        })
    return projects

@mcp.tool()
def search_issues(jql: str, max_results: int = 50, start_at: int = 0) -> List[Dict[str, Any]]:
    """Search for issues using Jira Query Language (JQL).
    
    Args:
        jql (str): The JQL query string (e.g. "project = DEMO AND status = 'To Do'").
        max_results (int): The maximum number of issues to return (default 50).
        start_at (int): The starting index for pagination (default 0).
        
    Returns:
        List[Dict[str, Any]]: List of matching issues with key, summary, status, priority, and assignee.
    """
    logger.info(f"Calling search_issues with JQL: {jql} (maxResults={max_results}, startAt={start_at})")
    payload = {
        "jql": jql,
        "maxResults": max_results,
        "startAt": start_at,
        "fields": ["summary", "status", "priority", "assignee", "updated", "created", "issuetype"]
    }
    data = make_request("POST", "/rest/api/3/search/jql", json_data=payload)
    issues_list = data.get("issues", [])
    
    results = []
    for issue in issues_list:
        fields = issue.get("fields", {})
        assignee = fields.get("assignee")
        assignee_name = assignee.get("displayName") if assignee else "Unassigned"
        
        status = fields.get("status")
        status_name = status.get("name") if status else "Unknown"
        
        priority = fields.get("priority")
        priority_name = priority.get("name") if priority else "None"
        
        issuetype = fields.get("issuetype")
        issuetype_name = issuetype.get("name") if issuetype else "Unknown"
        
        results.append({
            "key": issue.get("key"),
            "id": issue.get("id"),
            "summary": fields.get("summary"),
            "status": status_name,
            "priority": priority_name,
            "issuetype": issuetype_name,
            "assignee": assignee_name,
            "created": fields.get("created"),
            "updated": fields.get("updated")
        })
    return results

@mcp.tool()
def get_issue_details(issue_key: str) -> Dict[str, Any]:
    """Retrieve detailed information about a specific Jira issue.
    
    Args:
        issue_key (str): The Jira issue key (e.g. "ABC-12").
        
    Returns:
        Dict[str, Any]: Detailed issue data including description, reporter, assignee, status, and priority.
    """
    logger.info(f"Calling get_issue_details for issue: {issue_key}")
    data = make_request("GET", f"/rest/api/2/issue/{issue_key}")
    
    fields = data.get("fields", {})
    assignee = fields.get("assignee")
    assignee_name = assignee.get("displayName") if assignee else "Unassigned"
    
    reporter = fields.get("reporter")
    reporter_name = reporter.get("displayName") if reporter else "Unknown"
    
    status = fields.get("status")
    status_name = status.get("name") if status else "Unknown"
    
    priority = fields.get("priority")
    priority_name = priority.get("name") if priority else "None"
    
    issuetype = fields.get("issuetype")
    issuetype_name = issuetype.get("name") if issuetype else "Unknown"
    
    return {
        "key": data.get("key"),
        "id": data.get("id"),
        "summary": fields.get("summary"),
        "description": fields.get("description") or "No description provided.",
        "status": status_name,
        "priority": priority_name,
        "issuetype": issuetype_name,
        "assignee": assignee_name,
        "reporter": reporter_name,
        "created": fields.get("created"),
        "updated": fields.get("updated")
    }

@mcp.tool()
def get_issue_comments(issue_key: str) -> List[Dict[str, Any]]:
    """Retrieve all comments added to a specific Jira issue.
    
    Args:
        issue_key (str): The Jira issue key (e.g. "ABC-12").
        
    Returns:
        List[Dict[str, Any]]: A list of comment records containing author, creation date, and content.
    """
    logger.info(f"Calling get_issue_comments for issue: {issue_key}")
    data = make_request("GET", f"/rest/api/2/issue/{issue_key}/comment")
    
    comments = data.get("comments", [])
    results = []
    for comment in comments:
        author = comment.get("author", {})
        results.append({
            "id": comment.get("id"),
            "author": author.get("displayName", "Unknown"),
            "created": comment.get("created"),
            "body": comment.get("body")
        })
    return results

@mcp.tool()
def add_issue_comment(issue_key: str, comment_text: str) -> Dict[str, Any]:
    """Add a new comment to an existing Jira issue. (Write Action)
    
    Args:
        issue_key (str): The Jira issue key (e.g. "ABC-12").
        comment_text (str): The body text of the comment to add.
        
    Returns:
        Dict[str, Any]: Details of the created comment.
    """
    logger.info(f"Calling add_issue_comment for issue {issue_key}")
    payload = {
        "body": comment_text
    }
    data = make_request("POST", f"/rest/api/2/issue/{issue_key}/comment", json_data=payload)
    author = data.get("author", {})
    return {
        "id": data.get("id"),
        "author": author.get("displayName", "Unknown"),
        "created": data.get("created"),
        "body": data.get("body"),
        "status": "Comment added successfully"
    }

@mcp.tool()
def update_issue_status(issue_key: str, status_name: str) -> Dict[str, Any]:
    """Update/transition the status of a Jira issue (e.g. move to 'In Progress' or 'Done'). (Write Action)
    
    Args:
        issue_key (str): The Jira issue key (e.g. "ABC-12").
        status_name (str): The target status name or transition name (e.g., "In Progress", "Done").
        
    Returns:
        Dict[str, Any]: Success details or list of available transition options if matching fails.
    """
    logger.info(f"Calling update_issue_status for issue {issue_key} to target status: {status_name}")
    
    # 1. Fetch available transitions
    trans_data = make_request("GET", f"/rest/api/2/issue/{issue_key}/transitions")
    transitions = trans_data.get("transitions", [])
    
    matching_transition = None
    available_options = []
    
    # Normalize input
    target = status_name.strip().lower()
    
    # Find matching transition
    for trans in transitions:
        t_id = trans.get("id")
        t_name = trans.get("name", "")
        t_to = trans.get("to", {})
        t_to_name = t_to.get("name", "")
        
        available_options.append({
            "transition_id": t_id,
            "transition_name": t_name,
            "target_status": t_to_name
        })
        
        # Match by either transition name or target status name
        if t_name.strip().lower() == target or t_to_name.strip().lower() == target:
            matching_transition = trans
            break
            
    if not matching_transition:
        # Fuzzy match (e.g., target status name contains input)
        for trans in transitions:
            t_name = trans.get("name", "")
            t_to = trans.get("to", {})
            t_to_name = t_to.get("name", "")
            if target in t_name.strip().lower() or target in t_to_name.strip().lower():
                matching_transition = trans
                break
                
    if not matching_transition:
        return {
            "success": False,
            "error": f"No status transition matching '{status_name}' was found for {issue_key}.",
            "available_transitions": available_options,
            "guidance": "Please choose from one of the available transition names or target status names listed above."
        }
        
    # 2. Execute transition
    transition_id = matching_transition.get("id")
    transition_payload = {
        "transition": {
            "id": transition_id
        }
    }
    
    make_request("POST", f"/rest/api/2/issue/{issue_key}/transitions", json_data=transition_payload)
    
    return {
        "success": True,
        "issue_key": issue_key,
        "transition_id": transition_id,
        "transition_name": matching_transition.get("name"),
        "new_status": matching_transition.get("to", {}).get("name"),
        "status": f"Issue status updated successfully to {matching_transition.get('to', {}).get('name')}"
    }

if __name__ == "__main__":
    # In stdio mode, FastMCP runs standard loop
    logger.info("Starting Jira MCP Server in stdio mode...")
    mcp.run()




# Project: A006 Jira MCP Server
# Author: Poonam Bhatt
# Note: Using API v3 /search/jql for JQL queries due to Atlassian deprecation.
