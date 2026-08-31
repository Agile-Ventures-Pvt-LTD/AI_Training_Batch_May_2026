import pytest
from pydantic import ValidationError
from src.tools import (
    validate_city_input,
    get_weather_from_wttr,
    normalize_weather_data,
    assess_weather_risk,
)
from src.schemas import CityInput, CityOutput

@pytest.mark.integration
def validate_city_input_tool(city_name: str) -> dict:    
    try:
        input_data = CityInput(city_name=city_name)
        result = validate_city_input(input_data)
        return result.dict()
    except ValidationError as e:
        return CityOutput(success=False, message=str(e)).dict()
    

@pytest.mark.integration
def get_weather_forecast_tool(normalized_city_name: str) -> dict:    
    return get_weather_from_wttr(normalized_city_name)


@pytest.mark.integration
def normalize_weather_data_tool(raw_weather_data: dict) -> dict:
    return normalize_weather_data(raw_weather_data)


@pytest.mark.integration
def assess_weather_risk_tool(normalized_weather_data: dict) -> dict:
    return assess_weather_risk(normalized_weather_data)
