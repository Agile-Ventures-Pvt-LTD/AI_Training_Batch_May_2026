import pytest

from conftest import make_assistant_message, make_tool_call
from host import run_query
from test_query_execution import FakeGroqAgent, FakeMCPClient


@pytest.mark.asyncio
async def test_multi_tool_flow_summarize_issue_with_comments():
    first_call = make_tool_call("call_1", "get_issue_details", {"issue_key": "ABC-12"})
    second_call = make_tool_call("call_2", "get_issue_comments", {"issue_key": "ABC-12"})

    scripted = [
        make_assistant_message(content=None, tool_calls=[first_call]),
        make_assistant_message(content=None, tool_calls=[second_call]),
        make_assistant_message(
            content="ABC-12 is a login bug marked High priority. QA left one comment "
            "confirming the fix is pending validation.",
            tool_calls=None,
        ),
    ]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient(
        {
            "get_issue_details": '{"key": "ABC-12", "summary": "Login bug", "priority": "High"}',
            "get_issue_comments": '[{"author": "QA", "body": "Fix pending validation"}]',
        }
    )

    result = await run_query("Summarize ABC-12 including comments", mcp_client, llm_agent)

    assert result.tools_used == ["get_issue_details", "get_issue_comments"]
    assert result.write_action_performed is False
    assert "ABC-12" in result.final_answer
    assert mcp_client.called_tools == [
        ("get_issue_details", {"issue_key": "ABC-12"}),
        ("get_issue_comments", {"issue_key": "ABC-12"}),
    ]


@pytest.mark.asyncio
async def test_multi_tool_flow_respects_iteration_cap():
    from host import ToolLoopExceededError

    endless_call = make_tool_call("call_x", "search_issues", {"jql": "project = ABC"})
    scripted = [make_assistant_message(content=None, tool_calls=[endless_call]) for _ in range(10)]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient({"search_issues": "[]"})

    with pytest.raises(ToolLoopExceededError):
        await run_query("loop forever", mcp_client, llm_agent, max_iterations=3)
