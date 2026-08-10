# schema.py

from typing import Optional
from pydantic import BaseModel, Field

class ShipmentMetadata(BaseModel):
    shipment_id: str = Field(description="Shipment ID")
    cargo_weight_tons: int = Field(description="Cargo weight in tons")
    cargo_type: str = Field(description="Type of cargo")
    target_warehouse_id: str = Field(description="Target warehouse ID")
    has_perishables: bool = Field(description="Whether shipment has perishables")
    maximum_tolerable_delay_hours: Optional[int] = Field(default=None, description="Maximum shipment delay allowed in hours")
    
