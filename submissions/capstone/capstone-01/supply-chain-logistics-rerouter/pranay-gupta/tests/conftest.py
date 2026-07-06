import json
from unittest.mock import MagicMock
from pathlib import Path

import pytest

from src.schemas import ShipmentMetadata
from src.config import DATA_DIR


@pytest.fixture
def inventory_data():
    with open(DATA_DIR / "inventory_status.json", "r") as handle:
        return json.load(handle)


@pytest.fixture
def route_options_data():
    with open(DATA_DIR / "route_options.json", "r") as handle:
        return json.load(handle)


@pytest.fixture
def sample_incidents_data():
    with open(DATA_DIR / "sample_incidents.json", "r") as handle:
        return json.load(handle)


@pytest.fixture
def incident_001():
    return {
        "incident_id": "INC-001",
        "manifest_text": (
            "CRITICAL DISRUPTION: Cargo container SH-4002 is stranded "
            "outside the Port of Seattle due to an active worker strike. "
            "The vessel is carrying 550 tons of industrial electronics "
            "originally scheduled for delivery to WH-WEST-202. "
            "The shipment contains perishable cooling components and "
            "cannot sustain delays exceeding 72 hours."
        ),
        "disrupted_port_id": "PORT-SEATTLE-02",
    }


@pytest.fixture
def incident_002():
    return {
        "incident_id": "INC-002",
        "manifest_text": (
            "Shipment SH-4105 is delayed because the primary port is "
            "temporarily closed. The shipment contains 250 tons of "
            "consumer electronics and is scheduled for WH-SOUTH-303. "
            "The cargo must reach its destination within 48 hours."
        ),
        "disrupted_port_id": "PORT-SEATTLE-02",
    }


@pytest.fixture
def incident_003():
    return {
        "incident_id": "INC-003",
        "manifest_text": (
            "Cargo SH-4208 contains 700 tons of industrial machinery. "
            "The primary maritime route is unavailable and delivery "
            "was planned for WH-EAST-101."
        ),
        "disrupted_port_id": "PORT-SEATTLE-02",
    }


def create_mock_llm(
    metadata: ShipmentMetadata = None,
    brief: str = "Mock operations brief for testing.",
):
    if metadata is None:
        metadata = ShipmentMetadata(
            shipment_id="SH-TEST",
            cargo_weight_tons=500,
            cargo_type="electronics",
            target_warehouse_id="WH-WEST-202",
            has_perishables=False,
            maximum_tolerable_delay_hours=72,
        )

    llm = MagicMock()

    structured_llm = MagicMock()
    structured_llm.invoke.return_value = metadata
    llm.with_structured_output.return_value = structured_llm

    response = MagicMock()
    response.content = brief
    llm.invoke.return_value = response

    return llm


def create_mock_retriever(rules_text: str = "Mock logistics rules for testing."):
    retriever = MagicMock()
    mock_doc = MagicMock()
    mock_doc.page_content = rules_text
    retriever.invoke.return_value = [mock_doc]
    return retriever


@pytest.fixture
def mock_llm():
    return create_mock_llm


@pytest.fixture
def mock_retriever():
    return create_mock_retriever


@pytest.fixture
def seattle_routes():
    return [
        {
            "route_id": "ROUTE-WEST-01",
            "alternative_port": "Port-West",
            "warehouse_id": "WH-WEST-202",
            "added_delay_hours": 48,
        },
        {
            "route_id": "ROUTE-SOUTH-02",
            "alternative_port": "Port-South",
            "warehouse_id": "WH-SOUTH-303",
            "added_delay_hours": 72,
        },
        {
            "route_id": "ROUTE-CENTRAL-03",
            "alternative_port": "Port-Central",
            "warehouse_id": "WH-CENTRAL-404",
            "added_delay_hours": 96,
        },
    ]