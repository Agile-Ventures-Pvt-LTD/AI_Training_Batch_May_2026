import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

mcp = FastMCP("Jira Assistant")


auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}


#------------TOOL 1---list project--------------------------------------------------------------

@mcp.tool
def list_projects():

    try:
        print("Inside list_projects()")

        url = f"{JIRA_BASE_URL}/rest/api/3/project"

        response = requests.get(
                url,
                auth=auth,
                headers=headers,
                timeout=10
            )


        print("Status:", response.status_code)
        print("Body:", response.text)

        response.raise_for_status

        return response.json()

    except Exception as e:
        print("ERROR:", str(e))
        return {"error": str(e)}
        


#------------TOOL 2---search issues--------------------------------------------------------------

@mcp.tool
def search_issues(project_key: str = "SCRUM",
                    priority: str = "",
                    status: str = "",
                    assignee: str = ""):
    """
    Search all issues in a Jira project.
    """

    url = f"{JIRA_BASE_URL}/rest/api/3/search/jql"


    jql = f"project = {project_key}"

    if priority:
        jql += f' AND priority = "{priority}"'

    if status:
        jql += f'AND status ="{status}"'

    if assignee:
        jql += f'AND assignee ="{assignee}"'

    params = {
        "jql": jql,
        "fields": "summary,status,priority"
    }

    response = requests.get(
        url,
        params=params,
        auth=auth,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    return data


#------------TOOL 3---get issue details--------------------------------------------------------------

@mcp.tool
def get_issue_details(issue_key: str):

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}"

    response = requests.get(
        url,
        auth=auth,
        headers=headers,
        timeout=10
    )

    return response.json()


#------------TOOL 4---create issue--------------------------------------------------------------

@mcp.tool
def get_issue_comments(issue_key: str):

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"

    response = requests.get(
        url,
        auth=auth,
        headers=headers,
        timeout=10
    )

    return response.json()

#------------TOOL 5---add issue comment--------------------------------------------------------------
@mcp.tool
def add_issue_comment(issue_key: str, comment: str):

    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/comment"

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
                            "text": comment
                        }
                    ]
                }
            ]
        }
    }

    request_body = requests.post(
        url,
        json=payload,
        auth=auth,
        headers=headers,
        timeout=10
        
    )
    return request_body.json()

#-------------------TOOL 6 UPDATE STATUS--------------------------------------------

@mcp.tool
def update_issue_status(issue_key: str, status: str):

   
    url = f"{JIRA_BASE_URL}/rest/api/3/issue/{issue_key}/transitions"

    response = requests.get(
        url,
        auth=auth,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    transitions = response.json()["transitions"]

    transition_id = None

    for transition in transitions:
        if transition["name"].lower() == status.lower():
            transition_id = transition["id"]
            break

    if transition_id is None:
        return {
            "error": f"Status '{status}' is not available."
        }

 
    payload = {
        "transition": {
            "id": transition_id
        }
    }

    response = requests.post(
        url,
        json=payload,
        auth=auth,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    return {
        "message": f"Issue {issue_key} updated to {status}."
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
    
