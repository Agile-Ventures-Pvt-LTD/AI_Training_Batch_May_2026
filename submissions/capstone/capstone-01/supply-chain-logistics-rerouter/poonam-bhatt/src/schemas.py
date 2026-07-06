from pydantic import BaseModel, Field
from typing import Optional

class ShipmentMetadata(BaseModel):
    shipment_id: str = Field(description="The unique identifier of the shipment (e.g. SH-4002).")
    cargo_weight_tons: int = Field(description="The weight of the cargo in tons.")
    cargo_type: str = Field(description="The type of cargo (e.g. industrial electronics).")
    target_warehouse_id: str = Field(description="The ID of the target warehouse (e.g. WH-WEST-202).")
    has_perishables: bool = Field(description="True if the cargo contains perishable items, false otherwise.")
    maximum_tolerable_delay_hours: Optional[int] = Field(default=None, description="The maximum delay the shipment can tolerate in hours.")



### Author : Poonam Bhatt
### Capstone-01 : Supply chain logistics rerouter
### Date : 06/07/2026