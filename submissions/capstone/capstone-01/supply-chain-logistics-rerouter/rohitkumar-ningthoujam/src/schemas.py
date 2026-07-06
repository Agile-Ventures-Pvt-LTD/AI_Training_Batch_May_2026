from pydantic import BaseModel, Field
from typing import List, Optional


class ShipmentMetadata(BaseModel):
    shipment_id : str=""
    target_warehouse_id : str=""
    cargo_weight_tons : str=""
    cargo_type: str=""
    has_perishables: str=""
    maximun_tolerable_delay_hours: int = 0

class Finaresult_schema(BaseModel):
    incident_id: str=""
    original_incident_summary:str= 
    parsed_metadata:dict= {}
    rag_validation_rules_applied : List[str] = []
    routes_evaluated : List[str] = []
    final_selected_route: dict = {}
    queried_warehouse_metrics: dict= {},
    graph_routing_metadata : dict = {}
    final_operations_brief: str=""


    
