import json
import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from src.schemas import ShipmentMetadata

load_dotenv()

DATA_DIR = Path("data")

def query_warehouse_inventory_tool(warehouse_id: str) -> dict:
    with open(DATA_DIR / "inventory_status.json") as f:
        inventory = json.load(f)
    if warehouse_id not in inventory:
        return {"error": True, "message": f"Warehouse not found: {warehouse_id}"}
    return inventory[warehouse_id]

def get_alternative_routes_tool(disrupted_port_id: str) -> list:
    with open(DATA_DIR / "route_options.json") as f:
        routes = json.load(f)
    return routes.get(disrupted_port_id, [])

def _llm():
    return ChatGroq(model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))

def extract_shipment_metadata(manifest_text: str) -> ShipmentMetadata:
    llm = _llm().with_structured_output(ShipmentMetadata)
    prompt = (
        "Extract shipment details from this incident report. "
        "If a max tolerable delay isn't mentioned, set it to null.\n\n"
        f"{manifest_text}"
    )
    return llm.invoke(prompt)

def generate_operations_brief(state: dict) -> str:
    llm = _llm()
    prompt = (
        f"Write a short logistics operations brief (3-4 sentences).\n"
        f"Incident: {state['incident_id']}\n"
        f"Decision: {state['routing_decision']}\n"
        f"Selected route: {state.get('selected_route')}\n"
        f"Warehouse info: {state.get('warehouse_db_context')}\n"
        f"Explain what happened, what was decided, and why."
    )
    return llm.invoke(prompt).content
