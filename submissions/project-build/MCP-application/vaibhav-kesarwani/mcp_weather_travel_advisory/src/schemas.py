from pydantic import BaseModel, Field
from typing import Optional

class CityInput(BaseModel):
    city_name: str = Field(description="Name of the city to validate")


class CityOutput(BaseModel):
    success: bool
    original_city_name: Optional[str] = None
    normalized_city_name: Optional[str] = None
    message: Optional[str] = None