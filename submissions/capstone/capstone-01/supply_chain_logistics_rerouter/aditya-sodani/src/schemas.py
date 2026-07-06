from pydantic import BaseModel
from typing import Optional

class ShipmentMetadata(BaseModel):
    shipment_id: str
    cargo_weight_tons: int
    cargo_type : str
    target_warehouse_id : str
    has_perishables: bool
    maximum_tolerable_delay_hours: Optional[int]