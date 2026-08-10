from fastmcp import FastMCP

from tools import (
    validate_city_input_tool,
    get_weather_forecast_tool,
    normalize_weather_data_tool,
    calculate_weather_risk_tool,
    save_travel_advisory_tool,
)

from resources import (
    travel_checklist,
    advisory_rules,
    normalized_forecast_schema,
)

from prompts import (
    travel_readiness_prompt,
    weather_risk_summary_prompt,
    packing_recommendation_prompt,
)


mcp = FastMCP(
    name="Weather Travel Advisory MCP Server"
)


mcp.tool(name="validate_city_input_tool")(validate_city_input_tool)
mcp.tool(name="get_weather_forecast_tool")(get_weather_forecast_tool)
mcp.tool(name="normalize_weather_data_tool")(normalize_weather_data_tool)
mcp.tool(name="calculate_weather_risk_tool")(calculate_weather_risk_tool)
mcp.tool(name="save_travel_advisory_tool")(save_travel_advisory_tool)


mcp.resource("resource://travel/checklist")(travel_checklist)

mcp.resource("resource://travel/advisory-rules")(advisory_rules)

mcp.resource("resource://weather/normalized-forecast-schema")(normalized_forecast_schema)


mcp.prompt()(travel_readiness_prompt)

mcp.prompt()(weather_risk_summary_prompt)

mcp.prompt()(packing_recommendation_prompt)


if __name__ == "__main__":
    mcp.run()