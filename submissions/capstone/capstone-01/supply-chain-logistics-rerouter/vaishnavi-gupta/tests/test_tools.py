import asyncio
import pytest
import json

from src.tools import tool

from tools import (
    query_warehouse_inventory_tool,
    get_alternative_routes_tool
)


def test_warehouse_tool_valid_id():
    input = "WH-WEST-202"

    """
    Validate that:
    The warehouse is found.
    Warehouse name is returned.
    Utilization is returned.
    Operational status is returned.
    Risk tier is returned.
    """


def test_warehouse_tool_invalid_id():
    input = "WH-UNKNOWN-999"

    """
    Validate that:
    The application does not crash.
    A structured error is returned.

    """


def test_parse_incident_required_fields():
    input = "PORT-SEATTLE-02"
    
    """
    Validate that:
    Route options are returned.
    The result is a list.
    Each route contains {route_id} .
    Each route contains {warehouse_id} .
    Each route contains {added_delay_hours} .
    """


def test_routing_high_warehouse_utilization():
    warehouse_utilization = 92

    return ROUTE_CLARIFICATION
    

def test_routing_elevated_risk():
    risk_tier = ELEVATED

    return ROUTE_CLARIFICATION

    

def test_routing_valid_route():
    warehouse_utilization <= 85
    warehouse_status =  "ACTIVE"
    warehouse_risk =  "NORMAL"
    route_delay = "within allowed limits"

    return OPTIMAL_PATH_FOUND


def test_graph_retry_selects_next_route():
    """
    Validate that:
    The first route receives ROUTE_CLARIFICATION .
    current_route_index increases.
    Another route is selected.
    The graph continues execution.

    """
    

@pytest.mark.asyncio
async def test_tools_runs():
    """
    Verify that the tools run successfully.
    """

    tools = tool()

    try:
        await tools.connect()

        assert tools.session is not None
        
    finally:
        await tools.disconnect()


        await tools.connect()

    print("=" * 70)
    print("Supply Chain Logistics Rerouter")
    print("Type 'exit' to quit")
    print("=" * 70)

    while True:

        query = input("\nYou: ").strip()

        if query.lower() in ["exit", "quit"]:

            break

        response = await tools.chat(query)
        
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

        await tools.close()

        asyncio.run(tools())






