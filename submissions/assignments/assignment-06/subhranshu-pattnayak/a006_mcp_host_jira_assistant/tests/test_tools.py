from server.jira_mcp_server import (
    list_projects,
    search_issues,
    get_issue_details,
    get_issue_comments,
    add_issue_comment,
    update_issue_status
)


TEST_PROJECT_KEY = "AIT"
TEST_ISSUE_KEY = "AIT-13"
TEST_COMMENT = "Automated pytest comment."


# Verify the list_projects tool.
def test_list_projects():
    projects = list_projects()
    
    assert isinstance(projects, list)
    assert len(projects) > 0
    assert any(
        project["key"] == TEST_PROJECT_KEY
        for project in projects
    )


# Verify search_issues tool.
def test_search_issues():
    issues = search_issues(
        f"project = {TEST_PROJECT_KEY} AND statusCategory != Done"
    )
    assert isinstance(issues, list)


# Verify get_issue_details tool.
def test_get_issue_details():
    issue = get_issue_details(TEST_ISSUE_KEY)
    
    assert isinstance(issue, dict)
    assert issue["key"] == TEST_ISSUE_KEY
    assert "summary" in issue
    assert "status" in issue


# Verify get_issue_comments tool.
def test_get_issue_comments():
    comments = get_issue_comments(TEST_ISSUE_KEY)
    assert isinstance(comments, list)


# Verify add_issue_comment tool.
def test_add_issue_comment():
    result = add_issue_comment(
        TEST_ISSUE_KEY,
        TEST_COMMENT,
    )
    
    assert isinstance(result, dict)
    assert result["id"] is not None


# Verify updating issue status.
def test_update_issue_status():
    result = update_issue_status(
        TEST_ISSUE_KEY,
        "In Progress",
    )
    
    assert isinstance(result, dict)
    assert result["success"] is True