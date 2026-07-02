import json
import os
import sys
import pytest

from conftest import make_assistant_message, make_tool_call
from host import QueryResult, ToolLoopExceededError, run_query
from test_query_execution import FakeGroqAgent, FakeMCPClient


@pytest.mark.asyncio
async def test_tool_error_response_surfaces_in_final_answer():
    tool_call = make_tool_call("call_1", "get_issue_details", {"issue_key": "FAKE-99"})
    error_payload = json.dumps({"error": "Not found: /rest/api/3/issue/FAKE-99"})

    scripted = [
        make_assistant_message(content=None, tool_calls=[tool_call]),
        make_assistant_message(
            content="FAKE-99 could not be found in Jira. The issue may not exist.",
            tool_calls=None,
        ),
    ]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient({"get_issue_details": error_payload})

    result = await run_query("Summarize FAKE-99", mcp_client, llm_agent)

    assert isinstance(result, QueryResult)
    assert result.tools_used == ["get_issue_details"]
    assert result.write_action_performed is False
    assert "FAKE-99" in result.final_answer


@pytest.mark.asyncio
async def test_tool_loop_exceeded_error_raised_at_cap():
    endless_call = make_tool_call("call_x", "list_projects", {})
    scripted = [make_assistant_message(content=None, tool_calls=[endless_call]) for _ in range(5)]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient({"list_projects": "[]"})

    with pytest.raises(ToolLoopExceededError):
        await run_query("loop me", mcp_client, llm_agent, max_iterations=2)


def test_groq_agent_raises_on_missing_api_key(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)

    import llm
    with pytest.raises(ValueError, match="GROQ_API_KEY"):
        llm.GroqAgent(api_key=None)


def test_build_messages_structure():
    from prompts import build_messages

    messages = build_messages("Show open bugs")

    assert len(messages) == 2
    assert messages[0]["role"] == "system"
    assert "Jira" in messages[0]["content"]
    assert messages[1]["role"] == "user"
    assert messages[1]["content"] == "Show open bugs"


def test_extract_plain_text_nested_adf():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "server"))
    from jira_mcp_server import _extract_plain_text

    adf = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {"type": "text", "text": "Hello "},
                    {"type": "text", "text": "world"},
                ],
            },
            {
                "type": "bulletList",
                "content": [
                    {
                        "type": "listItem",
                        "content": [
                            {
                                "type": "paragraph",
                                "content": [{"type": "text", "text": "item one"}],
                            }
                        ],
                    }
                ],
            },
        ],
    }

    result = _extract_plain_text(adf)
    assert "Hello" in result
    assert "world" in result
    assert "item one" in result


def test_extract_plain_text_returns_empty_for_none():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "server"))
    from jira_mcp_server import _extract_plain_text

    assert _extract_plain_text(None) == ""
    assert _extract_plain_text({}) == ""
