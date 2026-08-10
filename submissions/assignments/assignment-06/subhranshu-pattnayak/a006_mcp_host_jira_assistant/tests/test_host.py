import asyncio
import json
import os

from src.host import main
from src.utils import TEST_OUTPUT_PATH


QUERY_EXECUTION = "List all Jira projects"

QUERY_MULTI_TOOL = (
    "Summarize issue AIT-13 and include all comments."
)

QUERY_WRITE = (
    "Add the comment 'Automated pytest comment.' to issue AIT-13."
)


# Verifying the host executes a natural language query.
def test_query_execution():

    async def run():
        output, response = await main(
            QUERY_EXECUTION,
            test=True,
        )

        assert isinstance(output, dict)
        assert isinstance(response, str)

        assert output["user_query"] == QUERY_EXECUTION
        assert "list_projects" in output["tools_used"]
        assert output["write_action_performed"] is False

    asyncio.run(run())


# Verifying multiple tool calls.
def test_multi_tool_flow():

    async def run():
        output, response = await main(
            QUERY_MULTI_TOOL,
            test=True,
        )

        assert isinstance(output, dict)
        assert isinstance(response, str)

        assert "get_issue_details" in output["tools_used"]
        assert "get_issue_comments" in output["tools_used"]
        assert output["write_action_performed"] is False

    asyncio.run(run())


# Verifying write operations.
def test_write_operation():

    async def run():
        output, response = await main(
            QUERY_WRITE,
            test=True,
        )

        assert isinstance(output, dict)
        assert isinstance(response, str)

        assert "add_issue_comment" in output["tools_used"]
        assert output["write_action_performed"] is True

        assert os.path.exists(TEST_OUTPUT_PATH)

        with open(TEST_OUTPUT_PATH, "r", encoding="utf-8") as file:
            saved_output = json.load(file)

        assert saved_output == output

    asyncio.run(run())