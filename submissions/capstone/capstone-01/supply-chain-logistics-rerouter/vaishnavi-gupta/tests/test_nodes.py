import asyncio
import pytest
import json

from src.nodes import GraphState


@pytest.mark.asyncio
async def test_nodes_runs():
    """
    Verify that the nodes run successfully.
    """

    nodes = GraphState()

    try:
        await nodes.connect()

        assert nodes.session is not None
        
    finally:
        await nodes.disconnect()
         
        await nodes.connect()

    print("=" * 70)
    print("Supply Chain Logistics Rerouter")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        query = input("\nYou: ").strip()

        if query.lower() in ["exit", "quit"]:

            break

        response = await nodes.chat(query)
        
        output_dir = "outputs"
        output_dir.mkdir(exist_ok=True)
        file_path = output_dir / "test_results.txt"
        


        if file_path.exists():

            existing_data = json.loads(file_path.read_text(encoding="utf-8"))
        else:
             existing_data = []

        existing_data.append(response)

        file_path.write_text(
        json.dumps(existing_data, indent=4, default=str),
        encoding="utf-8"
)

        print("\nAssistant\n")

        print(json.dumps(response, indent=4))

    await nodes.close()

    asyncio.run(nodes())
