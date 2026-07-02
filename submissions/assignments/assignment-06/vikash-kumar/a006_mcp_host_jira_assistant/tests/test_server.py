import os
import asyncio
from mcp_use import MCPAgent

from server.jira_mcp_server import (list_projects,search_issues,get_issue_details,get_issue_comments,add_issue_comment,update_issue_status)
from src.mcp_client import get_client as get_mcp_client
from src.llm import get_llm

def test_mcp_server_runs(mocker):
    mock_get = mocker.MagicMock()
    mock_get.json.return_value = [{"id": "1", "key": "ABC", "name": "Assignment 6"}]
    mock_get.status_code = 200
    mocker.patch("requests.get", return_value=mock_get)
    
    projects = list_projects()
    assert isinstance(projects, list)
    assert projects[0]["key"] == "ABC"

    mock_post = mocker.MagicMock()
    mock_post.json.return_value = {
        "issues": [{"key": "ABC-5","fields": {"summary": "Something","status": {"name": "In Progress"}}}]}
    mock_post.status_code = 200
    mocker.patch("requests.post", return_value=mock_post)
    
    issues = search_issues("status = 'In Progress'")
    assert isinstance(issues, list)
    assert issues[0]["key"] == "ABC-5"
    assert issues[0]["status"] == "In Progress"

    mock_get.json.return_value = {"key": "ABC-9",
        "fields": {"summary": "Groq LLM","status": {"name": "To Do"},"description": "Connect client"}}
    details = get_issue_details("ABC-9")
    assert details["key"] == "ABC-9"
    assert details["status"] == "To Do"

    mock_get.json.return_value = {"comments": [{"id": "1", "body": "Done"}]}
    comments = get_issue_comments("ABC-9")
    assert len(comments) == 1
    assert comments[0] == "Done"

    mock_post.status_code = 201
    res = add_issue_comment("ABC-5", "pending")
    assert res == "Comment added to ABC-5"

    mock_post.status_code = 204
    res = update_issue_status("ABC-9", "31")
    assert res == "Updated ABC-9 successfully"


def test_tool_discovery():
    async def run_discovery():
        client = get_mcp_client()
        await client.create_all_sessions()
        try:
            assert "jira" in client.get_server_names()
            session = client.get_session("jira")
            tools = await session.list_tools()
            tool_names = [t.name for t in tools]
            
            expected_tools = ["list_projects",
                "search_issues","get_issue_details","get_issue_comments","add_issue_comment","update_issue_status"]
            for name in expected_tools:
                assert name in tool_names
        finally:
            await client.close_all_sessions()

    asyncio.run(run_discovery())


def test_query_execution(mocker):
    async def run_test():
        client = get_mcp_client()
        llm = get_llm()
        agent = MCPAgent(llm=llm, client=client, system_prompt="System Prompt")
        
        mock_run = mocker.patch.object(agent, "run", return_value="Here is the list of projects.")
        response = await agent.run("List all Jira projects")
        assert response == "Here is the list of projects."
        mock_run.assert_called_once_with("List all Jira projects")

    asyncio.run(run_test())


def test_multi_tool_flow(mocker):
    async def run_test():
        client = get_mcp_client()
        llm = get_llm()
        agent = MCPAgent(llm=llm, client=client, system_prompt="System Prompt")
        
        mock_run = mocker.patch.object(agent, "run", return_value="Here is the summarized issue details and comments")
        response = await agent.run("Summarize ABC-9")
        assert "summarized" in response
        mock_run.assert_called_once_with("Summarize ABC-9")

    asyncio.run(run_test())


def test_write_operation(mocker):
    async def run_test():
        client = get_mcp_client()
        llm = get_llm()
        agent = MCPAgent(llm=llm, client=client, system_prompt="System Prompt")
        
        mock_run = mocker.patch.object(agent, "run", return_value="Successfully added comment to ABC-9")
        response = await agent.run("Add comment 'pending' to ABC-9")
        assert "Successfully" in response
        mock_run.assert_called_once_with("Add comment 'pending' to ABC-9")

    asyncio.run(run_test())
