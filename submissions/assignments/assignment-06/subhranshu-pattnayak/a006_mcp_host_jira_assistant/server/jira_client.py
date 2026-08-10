"""JIRA CLIENT PYTHON FILE"""
try:
    from .config import JIRA_API_TOKEN, JIRA_BASE_URL, JIRA_EMAIL
except ImportError:
    from config import JIRA_API_TOKEN, JIRA_BASE_URL, JIRA_EMAIL


from typing import Any

import requests
from requests.auth import HTTPBasicAuth


class JiraClient:
    """
    Wrapper around the Jira Cloud REST API.
    
    Responsibilities: Authentication, URL construction, HTTP requests, Response formatting.
    """

    API_VERSION = "3"
    JQL_ENDPOINT = "jql"
    COMMENT_ENDPOINT = "comment"
    TRANSITION_ENDPOINT = "transitions"
    PROJECT_ENDPOINT = "project"
    SEARCH_ENDPOINT = "search"
    ISSUE_ENDPOINT = "issue"

    def __init__(self) -> None:
        self.base_url = JIRA_BASE_URL
        self.email = JIRA_EMAIL
        self.api_token = JIRA_API_TOKEN
        self.auth = HTTPBasicAuth(self.email, self.api_token)
        self.headers = {
            "Accept": "application/json"
        }


    def _build_url(self, endpoint: str) -> str:
        """
        Construct a Jira REST endpoint URL.
        """
        
        return f"{self.base_url}/rest/api/{self.API_VERSION}/{endpoint}"

    def _request(
        self,
        method: str,
        endpoint: str,
        *,
        request_payload: dict[str, Any] | None = None,
        query_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Execute an HTTP request against the Jira REST API.
        """
        
        response = requests.request(
            method=method.upper(),
            url=self._build_url(endpoint),
            headers=self.headers,
            auth=self.auth,
            params=query_params,
            json=request_payload,
            timeout=30
        )
        try:
            response.raise_for_status()
            if not response.content:
                return {}
            
            return response.json()
        
        except requests.RequestException as e:
            raise RuntimeError(f"Jira request failed: {e}")
        except ValueError:
            raise RuntimeError("Failed to parse Jira response.")


    def list_projects(self) -> list[dict[str, Any]]:
        """
        Retrieve all Jira projects.
        """
        projects = self._request(
            method="GET",
            endpoint=self.PROJECT_ENDPOINT,
        )
        keys = ['id', 'key', 'name', 'projectTypeKey']
        return [{key: proj.get(key) for key in keys} for proj in projects]

    def search_issues(
        self,
        jql_query: str,
        max_results: int = 10,
    ) -> list[dict[str, Any]]:
        """
        Search Jira issues using JQL.
        """
        response = self._request(
            "POST",
            f"{self.SEARCH_ENDPOINT}/{self.JQL_ENDPOINT}",
            request_payload={
                "jql": jql_query,
                "maxResults": max_results,
                "fields": [
                    "summary", "status"
                ]
            }
        )['issues']
        issues = []
        for issue in response:
            issues.append({
                'id': issue['id'],
                'key': issue['key'],
                'summary': issue['fields']['summary'],
                'status': issue['fields']['status']['name']
            })
        return issues

    def get_issue_details(
        self,
        issue_key: str,
    ) -> dict[str, Any]:
        """
        Retrieve details of a specific issue.
        """
        details = self._request(
            method="GET",
            endpoint=f"{self.ISSUE_ENDPOINT}/{issue_key}",
        )
        return {
            'id': details['id'],
            'key': details['key'],
            'summary': details['fields']['summary'],
            'status': details['fields']['status'],
            'description': details['fields']['description']
        }

    def get_issue_comments(
        self,
        issue_key: str,
    ) -> list[dict[str, Any]]:
        """
        Retrieve all comments for an issue.
        """
        comments = self._request(
            method="GET",
            endpoint=f"{self.ISSUE_ENDPOINT}/{issue_key}/{self.COMMENT_ENDPOINT}"
        )['comments']
        
        keys = ['id', 'author', 'body', 'created', 'updated']
        comments = [{key: comm.get(key) for key in keys} for comm in comments]
        
        comment_list = []
        for comm in comments:
            comment_list.append(
                {key: comm.get(key) for key in keys}
            )
        for comm in comment_list:
            temp = {'emailAddress': comm['author']['emailAddress'], 'displayName': comm['author']['displayName']}
            comm['author'] = temp
            temp = comm['body']['content'][0]["content"]
            comm['content'] = temp
            del comm['body']

        return comment_list

    def add_issue_comment(
        self,
        issue_key: str,
        comment_text: str,
    ) -> dict[str, Any]:
        """
        Add a comment to an issue.
        """
        keys = ['id', 'author', 'body', 'created']
        comment = self._request(
            method="POST",
            endpoint=f"{self.ISSUE_ENDPOINT}/{issue_key}/{self.COMMENT_ENDPOINT}",
            request_payload={
                "body": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": comment_text,
                                }
                            ],
                        }
                    ],
                }
            },
        )
        del comment['author']['avatarUrls']
        return {k: comment[k] for k in keys}

    def _get_transition_id(
        self,
        issue_key: str,
        target_status: str,
    ) -> str | None:
        """
        Retrieve the transition ID corresponding to the requested status.
        """
        
        transitions = self._request(
            method="GET",
            endpoint=f"{self.ISSUE_ENDPOINT}/{issue_key}/{self.TRANSITION_ENDPOINT}",
        )['transitions']
        
        for transition in transitions:
            if transition['name'].strip().lower() == target_status.strip().lower():
                return transition['id']
        
        raise ValueError(
            f"No transition named '{target_status}' found."
        )

    def update_issue_status(
        self,
        issue_key: str,
        target_status: str,
    ) -> dict[str, Any]:
        """
        Transition an issue to another status.
        """
        transition_id = self._get_transition_id(
            issue_key=issue_key,
            target_status=target_status,
        )
        
        if transition_id is None:
            raise ValueError(
                f"Transition '{target_status}' not available for {issue_key}."
            )
        
        self._request(
            method="POST",
            endpoint=f"{self.ISSUE_ENDPOINT}/{issue_key}/{self.TRANSITION_ENDPOINT}",
            request_payload={
                'transition': {
                    'id': transition_id
                }
            }
        )
        
        return {
            "issue_key": issue_key,
            "updated_status": target_status,
            "success": True,
        }