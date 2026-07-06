from pydantic import BaseModel, Field
from typing import Optional

class ShipmentMetadata(BaseModel):
    shipment_id: str = Field(description= "The unique code for identifying the cargo shipment, e.g., SH-4002")
    cargo_weight_tons: int = Field(description = "The total weight of cargo(measured in tons only)")
    cargo_type: str = Field(description = "The detailed description or classification of goods being moved")
    target_warehouse_id: str = Field(description = "The target destination warehouse of the cargo, e.g., WH-WEST-202")
    has_perishables: bool = Field(description = "It will be true if the items are temperature sensitive, spoilable, otherwise set to false")
    maximum_tolerable_delay_hours: Optional[int] = Field(default = None, description = "Maximum extra hours, the cargo can move or kept, NULL if it is not mentioned")