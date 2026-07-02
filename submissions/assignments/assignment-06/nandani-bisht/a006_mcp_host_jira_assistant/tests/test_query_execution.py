import os
import pytest

from conftest import make_assistant_message, make_tool_call
from host import QueryResult, run_query


class FakeGroqAgent:
    def __init__(self, scripted_messages):
        self._scripted_messages = list(scripted_messages)
        self.calls = []

    def next_step(self, messages, tools):
        self.calls.append((list(messages), tools))
        return self._scripted_messages.pop(0)


class FakeMCPClient:
    def __init__(self, tool_results):
        self._tool_results = tool_results
        self.called_tools = []

    async def list_tools_for_groq(self):
        return [
            {
                "type": "function",
                "function": {"name": name, "description": "", "parameters": {}},
            }
            for name in self._tool_results
        ]

    async def call_tool(self, name, arguments):
        self.called_tools.append((name, arguments))
        return self._tool_results[name]


@pytest.mark.asyncio
async def test_query_execution_single_tool_call():
    tool_call = make_tool_call(
        "call_1", "search_issues", {"jql": "priority = High AND statusCategory != Done"}
    )
    scripted = [
        make_assistant_message(content=None, tool_calls=[tool_call]),
        make_assistant_message(
            content="There are 2 open high-priority issues: ABC-1 and ABC-3.",
            tool_calls=None,
        ),
    ]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient({"search_issues": '[{"key": "ABC-1"}, {"key": "ABC-3"}]'})

    result = await run_query("Show all open high-priority issues.", mcp_client, llm_agent)

    assert isinstance(result, QueryResult)
    assert result.user_query == "Show all open high-priority issues."
    assert result.tools_used == ["search_issues"]
    assert "ABC-1" in result.final_answer
    assert result.write_action_performed is False
    assert mcp_client.called_tools == [
        ("search_issues", {"jql": "priority = High AND statusCategory != Done"})
    ]


@pytest.mark.asyncio
async def test_query_execution_no_tool_needed():
    scripted = [make_assistant_message(content="Hello! How can I help with Jira today?", tool_calls=None)]
    llm_agent = FakeGroqAgent(scripted)
    mcp_client = FakeMCPClient({})

    result = await run_query("hi", mcp_client, llm_agent)

    assert result.tools_used == []
    assert result.write_action_performed is False
    assert result.final_answer == "Hello! How can I help with Jira today?"


def test_save_result_to_outputs_writes_valid_json(tmp_path, monkeypatch):
    import json
    import host

    monkeypatch.setattr(host, "OUTPUTS_DIR", str(tmp_path))
    monkeypatch.setattr(host, "HISTORY_FILE", str(tmp_path / "query_history.json"))

    result = QueryResult(
        user_query="Show open issues",
        tools_used=["search_issues"],
        final_answer="Found 2 open issues.",
        write_action_performed=False,
    )

    saved_path = host.save_result_to_outputs(result)

    assert os.path.exists(saved_path)
    with open(saved_path) as f:
        saved_data = json.load(f)
    assert saved_data == result.model_dump()

    history_path = tmp_path / "query_history.json"
    assert history_path.exists()
    with open(history_path) as f:
        history = json.load(f)
    assert len(history) == 1
    assert history[0]["user_query"] == "Show open issues"

    second_result = QueryResult(
        user_query="Show high priority issues",
        tools_used=["search_issues"],
        final_answer="Found 1 high priority issue.",
        write_action_performed=False,
    )
    host.save_result_to_outputs(second_result)
    with open(history_path) as f:
        history = json.load(f)
    assert len(history) == 2
