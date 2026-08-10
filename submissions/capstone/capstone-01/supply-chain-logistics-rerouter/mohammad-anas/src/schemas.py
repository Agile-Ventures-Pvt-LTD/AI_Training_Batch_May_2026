from pydantic import BaseModel, Field,Optional
from enum import Enum

class ShipmentMetadata(BaseModel):
    shipment_id: str = Field(..., description="Shipment identifier")
    cargo_weight_tons: float = Field(..., description="Weight in tons")
    cargo_type: str = Field(..., description="Type of cargo")
    target_warehouse_id: str = Field(..., description="Intended warehouse")
    has_perishables: bool = Field(..., description="Contains perishable goods")
    maximum_tolerable_delay_hours: Optional[int] = Field(None, description="Maximum delay allowed, null if not specified")