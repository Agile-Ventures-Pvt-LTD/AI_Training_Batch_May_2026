import asyncio
from host import host
from output_manager import OutputManager


async def main():
    print("Jira MCP Agent")
    print("Type 'exit' to quit\n")

    while True:
        query = input("You: ")

        if query.lower() in ["exit", "quit", "q"]:
            print("Bye...")
            break

        try:
            response = await host.run(query)

            print("\nResponse:")
            print(response["final_answer"])
            print()
            
            output_manager = OutputManager()
            output_manager.save(response)

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())