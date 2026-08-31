from pydantic import BaseModel

class ShipmentMetaData(BaseModel):
    shipment_id:str
    cargo_weight_tons:int
    target_warehouse_id:str
    has_perishables: bool
    maximum_tolerable_delay_hours:int|None

class OperationReports(BaseModel):
    original_incident_summary:str
    final_operations_brief:str

