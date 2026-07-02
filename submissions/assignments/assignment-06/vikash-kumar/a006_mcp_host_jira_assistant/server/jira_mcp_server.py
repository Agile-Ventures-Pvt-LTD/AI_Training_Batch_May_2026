from dotenv import load_dotenv
from fastmcp import FastMCP
import os
import requests

load_dotenv()

mcp=FastMCP("Jira assistant")

BASE_URL = os.getenv("JIRA_BASE_URL").rstrip("/")
EMAIL = os.getenv("JIRA_EMAIL")
TOKEN = os.getenv("JIRA_API_TOKEN")

AUTH = (EMAIL, TOKEN)

HEADERS = {"Accept": "application/json","Content-Type": "application/json"}

@mcp.tool
def list_projects():
    """It will list all the jira projects"""

    url=f"{BASE_URL}/rest/api/3/project"
    response=requests.get(url,headers=HEADERS,auth=AUTH)
    response.raise_for_status()
    projects = response.json()
    return [{"key": obj["key"],"name": obj["name"]} for obj in projects]

@mcp.tool
def search_issues(jql):
    """This tool will search the jira issues using JQL"""
    if not jql or not jql.strip():
        jql = "issuekey != null"
    url=f"{BASE_URL}/rest/api/3/search/jql"
    body={"jql": jql,"maxResults": 3,"fields": ["summary", "status"]}
    response = requests.post(url,json=body,headers=HEADERS,auth=AUTH)
    response.raise_for_status()
    issues = response.json().get("issues", [])
    if not issues:
        return "No issues found matching the query."
    return [{"key": issue["key"],"summary": issue["fields"]["summary"],"status": issue["fields"]["status"]["name"]}
                        for issue in issues]

@mcp.tool
def get_issue_comments(issue_key):
    """This tool will comments on for the jira issue"""
    url=f"{BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    response=requests.get(url,headers=HEADERS,auth=AUTH)
    response.raise_for_status()
    comments = response.json().get("comments", [])
    if not comments:
        return "No comments found."
    return [comment["body"] for comment in comments]

@mcp.tool
def get_issue_details(issue_key):
    """THis tool will get details of jira"""
    url=f"{BASE_URL}/rest/api/3/issue/{issue_key}"
    response=requests.get(url,headers=HEADERS,auth=AUTH)
    response.raise_for_status()
    issue = response.json()
    return {"key": issue["key"],
            "summary": issue["fields"]["summary"],
            "status": issue["fields"]["status"]["name"],
            "description": issue["fields"].get("description")}



@mcp.tool
def add_issue_comment(issue_key,text):
    """THis will add commnet on issue of jira"""
    url=f"{BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    body = {"body": {"type": "doc","version": 1,
            "content": [{"type": "paragraph","content": [
                        {"type": "text","text": text}]}]}}
    response = requests.post(url,json=body,headers=HEADERS,auth=AUTH)
    response.raise_for_status()
    return f"The comment is added{issue_key}"

@mcp.tool
def update_issue_status(issue_key, transition_id):
    """This will update the status of jira issue.
    """
    transitions_url = f"{BASE_URL}/rest/api/3/issue/{issue_key}/transitions"
    response = requests.get(transitions_url,headers=HEADERS,auth=AUTH)
    response.raise_for_status()
    transitions = response.json().get("transitions", [])

    matched_id = None
    for trans in transitions:
        if str(trans.get("id")) == str(transition_id):
            matched_id = trans["id"]
            break
        if trans.get("name", "").strip().lower() == str(transition_id).strip().lower():
            matched_id = trans["id"]
            break
        if trans.get("to", {}).get("name", "").strip().lower() == str(transition_id).strip().lower():
            matched_id = trans["id"]
            break

    body = {"transition": {"id": matched_id}}
    response = requests.post(transitions_url,json=body,headers=HEADERS,auth=AUTH)
    response.raise_for_status()
    return f"The issue is updated to the status with transition id {transition_id}"

if __name__ == "__main__":
    mcp.run()