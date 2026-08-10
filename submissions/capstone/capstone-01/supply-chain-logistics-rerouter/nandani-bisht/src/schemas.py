from typing import Optional
from pydantic import BaseModel, Field

class ShipmentMetadata(BaseModel):
    """Structured shipment information extracted from the incident manifest text."""
    shipment_id: str = Field(
        description="The unique identifier for the shipment (e.g., SH-4002)."
    )
    cargo_weight_tons: int = Field(
        description="The total weight of the cargo in tons."
    )
    cargo_type: str = Field(
        description="The description of the cargo type (e.g., industrial electronics)."
    )
    target_warehouse_id: str = Field(
        description="The ID of the target warehouse originally scheduled for delivery (e.g., WH-WEST-202)."
    )
    has_perishables: bool = Field(
        description="Boolean indicating if the cargo contains perishable items (e.g., perishable cooling components)."
    )
    maximum_tolerable_delay_hours: Optional[int] = Field(
        default=None,
        description="The maximum delay hours the shipment can tolerate before becoming critical. Use null if not explicitly mentioned in the text."
    )
    