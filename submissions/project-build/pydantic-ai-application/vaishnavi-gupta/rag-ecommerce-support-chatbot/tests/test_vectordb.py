import asyncio
import pytest

from chromadb import chromadb


@pytest.mark.asyncio
async def test_chromadb_runs():
    """
    Verify that the vector DB runs successfully.
    """

    client = chromadb()

    try:
        await client.connect()

        assert client.session is not None
        
    finally:
        await client.disconnect()
