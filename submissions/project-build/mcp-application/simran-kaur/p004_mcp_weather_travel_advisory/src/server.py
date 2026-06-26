

from __future__ import annotations
import os
from typing import Any, Optional, Dict
from dotenv import load_dotenv
from fastmcp import FastMCP
import httpx
import requests
from tools import validate_city_input, get_weather_forecast, norm_weather_data, calculate_weather_risk, save_travel_advisory

from resources import travel_checklist, travel_advisory, weather_norm_schema

from prompts import travel_readiness,weather_risk_summary,packing_recommendation

load_dotenv()


# city_name = "Jaipur"
# url = f"https://wttr.in/{city_name}?format=j1"
# response = requests.get(url, timeout=10)
# data = response.json()



mcp = FastMCP()

@mcp.tool
def validate_city_input_tool(
        city_name: str
):
    """Validates the city name entered by the user.
    This tool does not call the weather API.

    arguments:
        city_name: it take city name as argument"""
    
    return validate_city_input(city_name)



@mcp.tool
def get_weather_forecast_tool(
        normalised_city_name: str) -> Dict[str, any]:
    """
    Calls the wttr.in JSON API and returns the raw weather response.
    This is the only tool that should call the external weather API.
    
    argument: 
        normalised_city_name: it is the normalised city name

    """
    return get_weather_forecast(normalised_city_name)

@mcp.tool
def normalize_weather_data_tool(
        raw_weather_data: Dict[str, any]
):
    """Converts raw wttr.in JSON into a clean internal weather schema.
        This tool must not call the external API.

        argument:
            raw_weather_data: it is the dictionary containing weather details

    """
    return norm_weather_data(raw_weather_data)

@mcp.tool
def calculate_weather_risk_tool(
        normalized_weather_data: Dict[str,any]
):
    """Calculates deterministic travel weather risk from normalized weather data.
    This tool must not call the API and must not use an LLM.

    argument: 
        normalised_weather_data: it is a normalised data in dictionary form 
    """
    return calculate_weather_risk(normalized_weather_data)


@mcp.tool
def save_travel_advisory_tool(
        report: Dict[str, any]
):
    """Saves the final advisory report as JSON.
        argument:
                report: it is the dictionary report input
    """
    return save_travel_advisory(report)



#============== RESOURCES==================

@mcp.resource(" resource://travel/checklist")
async def travel_checklist_resource() -> str:
    """
    Provides a static travel-readiness checklist.
    """
    return travel_checklist()


@mcp.resource("resource://travel/advisory-rules")
async def travel_advisory_resource() -> str:
    """
    Provides static rules for interpreting weather risk.
    """
    return travel_advisory()

    
@mcp.resource("resource://weather/normalized-forecast-schema")
async def weather_norm_schema_resource() -> Dict[str, any]:
    """The resource purpose is to describes the normalized forecast schema expected by this project."""

    return weather_norm_schema()


#=============== PROMPTS=================

@mcp.prompt()
async def travel_readiness_prompt(
        destination: str,
        weather_risk: str, 
        forecast_summary: str,
        recommended_actions: list) -> str:
    """
    Creates a concise travel-readiness advisory.'.
    """
    return travel_readiness(destination, weather_risk, forecast_summary, recommended_actions)


@mcp.prompt()
async def weather_risk_summary_prompt(
        destination: str,
        weather_risk: str,
        risk_factors: list) -> str:
    """
    Explains why the risk level is LOW, MEDIUM, or HIGH.

    """
    return weather_risk_summary(destination,weather_risk,risk_factors)


@mcp.prompt()
async def packing_recommendation_(
        destination: str,
        weather_risk: str,
        risk_factors: list
):
    """Generates practical packing suggestions."""
    return packing_recommendation(destination, weather_risk, risk_factors)
