
# Project Build -  Weather and Travel Advisory MCP Server Using wttr.in API
## Participant Name

Simran Kaur

## Project Title
 Weather and Travel Advisory MCP Server Using wttr.in API
## Description

The objective of this project is to help participants understand how MCP servers 
expose:
1. Tools
2. Resources
3. Prompts
Participants must build an MCP server that can:
1. Accept a destination city.
2. Fetch weather data from wttr.in.
3. Normalize the weather response into a clean schema.
4. Calculate weather-based travel risk.
5. Use MCP resources for checklist, advisory rules, and forecast schema.
6. Use MCP prompts for travel readiness, risk explanation, and packing 
suggestions.
7. Save the final travel advisory report as JSON



## 
## How to Run

### 1. Clone the Repository

```bash
git clone <repository-url>
cd credit-card-agent-assignment
```

### 2. Create Virtual Environment


```bash
uv venv 
```

Activate:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```


### 3. Configure Environment Variables

Create a `.env` file:

```env
WTTR_PRIMARY_URL=https://wttr.in
WTTR_FALLBACK_URL=https://wttr.is
OUTPUT_PATH=outputs
```

### 4. Run the Application

```bash
python -m app
```

### 5. Run Tests


```bash
pytest tests/test_tools.py

```

## Libraries / Packages Required


```text

fastmcp>=3.1.0
ipython>=9.10.0
requests>=2.32.5
python-dotenv>=1.2.2
mcp-use>=1.6.0
langchain-groq>=1.1.2
pypdf>=6.7.5
pydantic-ai>=1.78.0
pytest>=8.0.0
```

 

## Output Explanation

### Example User Query


```

### Example Output

```text
The final answer should include:
Expected answer:
```text
   Example report:
{
"destination": "Jaipur",
"region": "Rajasthan",
"country": "India",
"forecast_days": 3,
"current_weather": {
"temperature_c": 31.0,
"humidity": 48,
"precipitation_mm": 0.0,
"wind_speed_kmph": 12.0,
"weather_description": "Sunny"
},
"daily_forecast": [
{
"date": "2026-06-26",
"max_temp_c": 37.0,
"min_temp_c": 27.0,
"avg_temp_c": 32.0,
"total_precipitation_mm": 1.2,
"max_wind_kmph": 28.0,
"max_chance_of_rain": 60,
"weather_description": "Partly cloudy"
}
],
"weather_risk": "MEDIUM",
"risk_factors": [
"Maximum temperature is expected to be above 35°C.",
"Wind speed may be moderately high during the forecast period."
],
"recommended_actions": [
"Carry water and avoid long outdoor exposure during afternoon 
hours.",
"Use sun protection if travelling outdoors."
],
"packing_suggestions": [
"Water bottle",
"Light cotton clothing",
"Sunscreen",
"Cap or hat"
],
"travel_readiness_advisory": "Travel appears manageable with basic 
weather precautions.",
"weather_risk_explanation": "The risk level is medium because 
moderate heat and wind indicators are present.",
"resources_used": [
"resource://travel/checklist",
"resource://travel/advisory-rules",
"resource://weather/normalized-forecast-schema"
],
"tools_used": [
"validate_city_input_tool",
"get_weather_forecast_tool",
"normalize_weather_data_tool",
"calculate_weather_risk_tool",
"save_travel_advisory_tool"
],
"prompts_used": [
"travel_readiness_prompt",
"weather_risk_summary_prompt",
"packing_recommendation_prompt"
]
}
```