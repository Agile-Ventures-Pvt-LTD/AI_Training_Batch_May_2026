
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
load_dotenv()
from src.schemas import ShipmentMetadata


@pytest.mark.integration
def test_parse_incident_required_fields():
    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
    )
    structured_llm = llm.with_structured_output(ShipmentMetadata)
    prompt = ChatPromptTemplate.from_messages(
        [("system", "Extract shipment metadata."),
         ("human","""Shipment SH-4105 is delayed because the primary port is temporarily closed. The shipment contains 250 tons of consumer electronics and is scheduled for WH-SOUTH-303."""),
        ])

    chain = prompt | structured_llm
    result = chain.invoke({})
    assert result.shipment_id == "SH-4105"
    assert result.cargo_weight_tons == 250
    assert result.target_warehouse_id == "WH-SOUTH-303"
    assert result.has_perishables is False
