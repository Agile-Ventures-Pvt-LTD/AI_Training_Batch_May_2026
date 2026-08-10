import pytest
from src.tools.database import database_agent
from src.tools.weather import weather_agent


EXPECTED_TOOLS = {
    "database",
    "weather_forecast"
}


@pytest.mark.asyncio
async def database():
    """
    Verify that all  user queries are correctly solved.
    """

    client = database()

    try:
        await client.connect()

        tools = await client.list_tools()

        tool_names = {tool.name for tool in tools}

        missing_tools = EXPECTED_TOOLS - tool_names

        assert (
            not missing_tools
        ), f"Missing tools: {missing_tools}"

    finally:
        await client.disconnect()


@pytest.mark.asyncio
async def weather_forecast():
    """
    Verify that all the queries related to weather are solved.
    """

    client = weather_forecast()

    try:
        await client.connect()

        tools = await client.list_tools()

        tool_names = {tool.name for tool in tools}

        missing_tools = EXPECTED_TOOLS - tool_names

        assert (
            not missing_tools
        ), f"Missing tools: {missing_tools}"

    finally:
        await client.disconnect()

