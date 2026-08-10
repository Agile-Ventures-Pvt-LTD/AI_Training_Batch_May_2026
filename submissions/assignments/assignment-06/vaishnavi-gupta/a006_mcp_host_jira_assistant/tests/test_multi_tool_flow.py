import os
import pytest
from dotenv import load_dotenv

from src.mcp_client import JiraMCPClient

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@pytest.mark.asyncio
async def test_multi_tool_flow():
    """
    Verify that multiple MCP tools can be executed
    sequentially for the same issue.
    """

    if not GROQ_API_KEY:
        pytest.skip(
            "GROQ_API_KEY is not configured in the .env file."
        )

    client = JiraMCPClient()

    try:
        await client.connect()

        # Step 1: Get issue details
        details = await client.call_tool(
            "get_issue_details",
            {
                "issue_key": GROQ_API_KEY,
            },
        )

        # Step 2: Get issue comments
        comments = await client.call_tool(
            "get_issue_comments",
            {
                "issue_key": GROQ_API_KEY,
            },
        )

        assert details is not None
        assert comments is not None

        assert hasattr(details, "content")
        assert hasattr(comments, "content")

    finally:
        await client.disconnect()

