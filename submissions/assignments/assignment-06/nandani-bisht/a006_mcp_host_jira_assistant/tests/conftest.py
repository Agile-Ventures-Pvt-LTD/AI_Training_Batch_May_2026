import json
import os
import sys
from types import SimpleNamespace

import pytest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TESTS_DIR)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "src"))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "server"))
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault("JIRA_BASE_URL", "https://dummy.atlassian.net")
os.environ.setdefault("JIRA_EMAIL", "dummy@example.com")
os.environ.setdefault("JIRA_API_TOKEN", "dummy-token")
os.environ.setdefault("GROQ_API_KEY", "dummy-groq-key")
os.environ.setdefault("GROQ_MODEL", "llama-3.3-70b-versatile")

EXPECTED_TOOL_NAMES = [
    "list_projects",
    "search_issues",
    "get_issue_details",
    "get_issue_comments",
    "add_issue_comment",
    "update_issue_status",
]


def make_tool_call(call_id, name, arguments):
    return SimpleNamespace(
        id=call_id,
        type="function",
        function=SimpleNamespace(name=name, arguments=json.dumps(arguments)),
    )


def make_assistant_message(content, tool_calls):
    def model_dump(exclude_none=False):
        dumped = {"role": "assistant", "content": content}
        if tool_calls:
            dumped["tool_calls"] = [
                {
                    "id": tc.id,
                    "type": tc.type,
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in tool_calls
            ]
        if exclude_none:
            dumped = {k: v for k, v in dumped.items() if v is not None}
        return dumped

    msg = SimpleNamespace(content=content, tool_calls=tool_calls)
    msg.model_dump = model_dump
    return msg


@pytest.fixture
def expected_tool_names():
    return EXPECTED_TOOL_NAMES
