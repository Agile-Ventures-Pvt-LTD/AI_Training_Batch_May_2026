import os
import pytest
from dotenv import load_dotenv

from src.mcp_client import JiraMCPClient

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TEST_COMMENT = os.getenv(
    "TEST_COMMENT",
    "Comment added by MCP pytest."
)


@pytest.mark.asyncio
async def test_write_operation():
    """
    Verify that a write operation (adding a comment)
    is successfully executed through the MCP server.
    """

    if not GROQ_API_KEY:
        pytest.skip(
            "GROQ_API_KEY is not configured in the .env file."
        )

    client = JiraMCPClient()

    try:
        await client.connect()

        result = await client.call_tool(
            "add_issue_comment",
            {
                "issue_key": GROQ_API_KEY,
                "comment": TEST_COMMENT,
            },
        )

        assert result is not None
        assert hasattr(result, "content")

        response_text = str(result.content)

        assert (
            "success" in response_text.lower()
            or "added" in response_text.lower()
            or "comment" in response_text.lower()
        )

    finally:
        await client.disconnect()

