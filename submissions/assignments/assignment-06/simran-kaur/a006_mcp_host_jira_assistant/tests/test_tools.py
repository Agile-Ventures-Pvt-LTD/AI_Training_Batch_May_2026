from server.jira_mcp_server import (list_projects, search_issues, get_issue_details, get_issue_comments, add_issue_comment, update_issue_status
)

def test_tool_discovery():

    assert callable(list_projects)
    assert callable(search_issues)
    assert callable(get_issue_details)
    assert callable(get_issue_comments)
    assert callable(add_issue_comment)
    assert callable(update_issue_status)





def test_query_execution():
    
    result = list_projects()
    assert isinstance(result, list)
    



def test_multi_tool_flow():

    projects = list_projects()

    assert len(projects) > 0

    issues = search_issues("SCRUM")

    assert isinstance(issues, dict)



def test_write_operation():
    
    comment_issue = add_issue_comment("SCRUM-6", "Need urgent work")

    assert comment_issue is not None


