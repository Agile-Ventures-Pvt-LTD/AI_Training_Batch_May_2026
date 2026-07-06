from pydantic import BaseModel,Field

class LangchainStructured(BaseModel):
    """Schema for langchain structured output."""
    shipment_id: str = Field(description="Shipment_id of the shippment provided by incident")
    cargo_weight_tons: int = Field(description="given thecargo weight in the ship of the given shipment_id in tons provided by incident")
    cargo_type: str = Field(description="type of cargo carried by the shipment  mentioned in incident")
    target_warehouse_id: str = Field(description="target warehouse id of the shippment provided by incident")
    has_perishables: bool = Field(description="if contains perishable goods, then true else false ")
    maximum_tolerable_delay_hours: int | None =Field(description="If the incident does not provide a maximum delay value, the field may be  null .")