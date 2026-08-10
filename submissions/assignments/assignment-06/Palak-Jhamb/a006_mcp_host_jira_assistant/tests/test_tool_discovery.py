from server.jira_mcp_server import search_issues,get_issue_comments,get_issue_details,add_issue_comment,list_projects

def test_list_projects():
    result=list_projects()
    assert len(result)>0
    assert "id" in result[0]
    assert "key" in result[0]
    assert "name" in result[0]
    assert "project_type" in result[0]
    

def test_search():
    result = search_issues("project = MCP0 AND priority = High")
    assert len(result) > 0
    assert "id" in result[0]
    assert "key" in result[0]


def test_get_issue_comments():
    result=get_issue_comments('MCP0-3')
    assert len(result) > 0
    assert "comment" in result[0]

def test_get_issue_details():
    result=get_issue_details("MCP0-3")
    assert result 

def test_add_issue_comment():
    result=add_issue_comment('MCP0-1','This is my first comment for this issue')
    assert result['id'] is not None
    assert result['message']== 'Comment added successfully to MCP0-1'