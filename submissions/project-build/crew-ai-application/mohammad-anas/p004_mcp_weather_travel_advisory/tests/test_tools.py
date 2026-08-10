from src.tools import register_tools


class DummyMCP:
    def __init__(self):
        self.tools = {}

    def tool(self, func):
        self.tools[func.__name__] = func
        return func


mcp = DummyMCP()
register_tools(mcp)

validate_city_input_tool = mcp.tools["validate_city_input_tool"]
normalize_weather_data_tool = mcp.tools["normalize_weather_data_tool"]
calculate_weather_risk_tool = mcp.tools["calculate_weather_risk_tool"]

def test_validate_city_input_tool_valid_city():
    result = validate_city_input_tool("Jaipur")

    assert result["success"] is True
    assert result["normalized_city_name"] == "Jaipur"
    
def test_validate_city_input_tool_city_with_space():
    result = validate_city_input_tool("New Delhi")

    assert result["success"] is True
    assert result["normalized_city_name"] == "New+Delhi"
    
def test_validate_city_input_tool_empty_city():
    result = validate_city_input_tool("")

    assert result["success"] is False

def test_validate_city_input_tool_short_city():
    result = validate_city_input_tool("A")

    assert result["success"] is False

def test_normalize_weather_data_tool_schema():
    raw = {
        "nearest_area": [
            {
                "areaName": [{"value": "Jaipur"}],
                "region": [{"value": "Rajasthan"}],
                "country": [{"value": "India"}],
            }
        ],
        "current_condition": [
            {
                "temp_C": "31",
                "humidity": "48",
                "precipMM": "0",
                "windspeedKmph": "12",
                "weatherDesc": [{"value": "Sunny"}],
            }
        ],
        "weather": [
            {
                "date": "2026-06-26",
                "maxtempC": "37",
                "mintempC": "27",
                "avgtempC": "32",
                "hourly": [
                    {
                        "chanceofrain": "60",
                        "precipMM": "1.2",
                        "windspeedKmph": "28",
                        "weatherDesc": [{"value": "Partly cloudy"}],
                    }
                ],
            }
        ],
    }

    result = normalize_weather_data_tool(raw)

    assert result["success"] is True
    assert result["destination"] == "Jaipur"
    assert result["current_weather"]["temperature_c"] == 31.0
    
def test_normalize_weather_data_tool_missing_fields():
    result = normalize_weather_data_tool({})

    assert result["success"] is False
    
def test_calculate_weather_risk_tool_low():
    result = calculate_weather_risk_tool(
        {
            "daily_forecast": [
                {
                    "max_temp_c": 30,
                    "total_precipitation_mm": 0,
                    "max_chance_of_rain": 10,
                    "max_wind_kmph": 10,
                }
            ]
        }
    )

    assert result["weather_risk"] == "LOW"
    
def test_calculate_weather_risk_tool_medium():
    result = calculate_weather_risk_tool(
        {
            "daily_forecast": [
                {
                    "max_temp_c": 36,
                    "total_precipitation_mm": 2,
                    "max_chance_of_rain": 20,
                    "max_wind_kmph": 15,
                }
            ]
        }
    )

    assert result["weather_risk"] == "MEDIUM"
    
def test_calculate_weather_risk_tool_high():
    result = calculate_weather_risk_tool(
        {
            "daily_forecast": [
                {
                    "max_temp_c": 42,
                    "total_precipitation_mm": 0,
                    "max_chance_of_rain": 10,
                    "max_wind_kmph": 10,
                }
            ]
        }
    )

    assert result["weather_risk"] == "HIGH"