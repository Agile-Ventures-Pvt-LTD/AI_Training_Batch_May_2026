# tests/test_client.py
import asyncio
from client import main

async def test():
    await main("I want to travel to Jaipur. Run all tools and prompts in order and save the final JSON advisory report.")

asyncio.run(test())