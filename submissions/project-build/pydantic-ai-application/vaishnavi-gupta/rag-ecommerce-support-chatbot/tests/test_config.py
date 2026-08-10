import asyncio
import pytest

from src.config import config


@pytest.mark.asyncio
async def test_config_runs():
    """
    Verify that the config runs successfully.
    """

    client = config()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()
