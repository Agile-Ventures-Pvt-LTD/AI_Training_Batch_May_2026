from src.api_client import main
import asyncio

try:
    should_continue = asyncio.run(main())
    if should_continue is False:
        print("Bye Bye...")
except Exception as e:
    print(e)
    