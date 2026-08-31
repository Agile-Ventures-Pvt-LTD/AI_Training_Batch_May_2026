import os
from unittest.mock import MagicMock, patch

from src.llm import GroqLLM


@patch.dict(
    os.environ,
    {
        "GROQ_API_KEY": "dummy_key",
        "GROQ_MODEL": "llama-3.3-70b-versatile",
    },
)
@patch("src.llm.Groq")
def test_groq_llm_initialization(mock_groq):
    llm = GroqLLM()

    mock_groq.assert_called_once_with(api_key="dummy_key")
    assert llm.model_name == "llama-3.3-70b-versatile"


def test_format_mcp_tools():
    tool = MagicMock()

    tool.name = "search_issues"
    tool.description = "Search Jira issues"
    tool.inputSchema = {
        "type": "object",
        "properties": {
            "jql": {
                "type": "string"
            }
        }
    }

    llm = GroqLLM()

    formatted = llm.format_mcp_tools([tool])

    assert len(formatted) == 1

    assert formatted[0]["type"] == "function"

    assert formatted[0]["function"]["name"] == "search_issues"

    assert formatted[0]["function"]["description"] == "Search Jira issues"

    assert formatted[0]["function"]["parameters"] == tool.inputSchema


@patch("src.llm.Groq")
def test_generate_chat_response(mock_groq):
    mock_client = MagicMock()

    mock_groq.return_value = mock_client

    llm = GroqLLM()

    messages = [
        {
            "role": "user",
            "content": "List projects"
        }
    ]

    tools = [
        {
            "type": "function",
            "function": {
                "name": "list_projects",
                "description": "List Jira projects",
                "parameters": {}
            }
        }
    ]

    llm.generate_chat_response(
        messages=messages,
        tools=tools,
    )

    mock_client.chat.completions.create.assert_called_once()

    kwargs = mock_client.chat.completions.create.call_args.kwargs

    assert kwargs["messages"] == messages

    assert kwargs["tools"] == tools

    assert kwargs["tool_choice"] == "auto"

    assert kwargs["temperature"] == 0.0