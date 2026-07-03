import asyncio
import pytest

from src.database import database


@pytest.mark.asyncio
async def test_database_runs():
    """
    Verify that the database runs successfully.
    """

    client = database()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()
