import time
import asyncio
from agent import agent

async def main():
    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit", "q"]:
            print("Bye...")
            break

        try:
            result = await agent.run(query)
            time.sleep(10)
            response = result.output
            print("Response : ", response.response)
        
        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())