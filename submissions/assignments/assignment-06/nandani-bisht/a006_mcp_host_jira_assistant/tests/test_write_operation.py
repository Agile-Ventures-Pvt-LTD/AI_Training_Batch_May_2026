import pytest

from conftest import make_assistant_message, make_tool_call
from host import run_query
from test_query_execution import FakeGroqAgent, FakeMCPClient


@pytest.mark.asyncio
async def test_write_operation_add_comment_flags_write_action():
    tool_call = make_tool_call(
        "call_1",
        "add_issue_comment",
        {"issue_key": "ABC-5", "comment": "QA validation is pending"},
    )
    scripted = [
        make_assistant_message(content=None, tool_calls=[tool_call]),
        make_assistant_message(
            content="I added a comment to ABC-5 noting that QA validation is pending. "
            "This was a write action.",
            tool_calls=None,
        ),
    ]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient(
        {"add_issue_comment": '{"comment_id": "10001", "issue_key": "ABC-5"}'}
    )

    result = await run_query(
        "Add a comment to ABC-5 saying QA validation is pending.", mcp_client, llm_agent
    )

    assert result.tools_used == ["add_issue_comment"]
    assert result.write_action_performed is True
    assert "write action" in result.final_answer.lower()


@pytest.mark.asyncio
async def test_write_operation_update_status_flags_write_action():
    tool_call = make_tool_call(
        "call_1", "update_issue_status", {"issue_key": "ABC-9", "status": "Done"}
    )
    scripted = [
        make_assistant_message(content=None, tool_calls=[tool_call]),
        make_assistant_message(content="ABC-9 has been moved to Done.", tool_calls=None),
    ]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient(
        {"update_issue_status": '{"issue_key": "ABC-9", "new_status": "Done"}'}
    )

    result = await run_query("Mark ABC-9 as done", mcp_client, llm_agent)

    assert result.write_action_performed is True
    assert result.tools_used == ["update_issue_status"]


@pytest.mark.asyncio
async def test_read_only_query_does_not_flag_write_action():
    tool_call = make_tool_call("call_1", "list_projects", {})
    scripted = [
        make_assistant_message(content=None, tool_calls=[tool_call]),
        make_assistant_message(content="You have 3 projects: ABC, DEF, GHI.", tool_calls=None),
    ]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient(
        {"list_projects": '[{"key": "ABC"}, {"key": "DEF"}, {"key": "GHI"}]'}
    )

    result = await run_query("List all Jira projects", mcp_client, llm_agent)

    assert result.write_action_performed is False
