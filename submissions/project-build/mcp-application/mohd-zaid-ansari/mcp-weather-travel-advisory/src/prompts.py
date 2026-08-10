import json 
import requests
from typing import Any, List, Dict, Optional 
from fastmcp import FastMCP
from pathlib import Path
import os
from dotenv import load_dotenv
from src.server import mcp

@mcp.prompt()
async def travel_readiness_prompt(destination:str, weather_risk:str, forecast_summary:str) -> str:
    """
    Analyze the weather for the {destination} give weather risk '{weather_risk}' and summary of forecast '{forecast_summary}'.
    """
    return f"""Analyze the weather for the {destination} give weather risk '{weather_risk}' and summary of forecast '{forecast_summary}'.
        Steps:
        1.Run the mcp tool for validating the destination.
        2.Get the weather forecast of the destination using mcp tool.
        3.Get the weather of the destination using mcp tool do know the weather_risk.
        4.Summarize the forecast on the basis of the detailed provided.

        Explain whether travel looks comfortable, manageable with precautions, 
        or risky due to weather.
        Keep the answer practical and easy to understand
"""
#=================================================================================================================================

@mcp.prompt()
async def weather_risk_summary_prompt(destination:str, weather_risk:str) -> str:
    """
    Analyze the weather for the {destination} give weather risk '{weather_risk}' and explain the risk level.
    """
    return f"""Analyze the weather for the {destination} give weather risk '{weather_risk}' and explain the risk level.
    Steps:
    1.Run the mcp tool for validating the destination.
    2.Get the weather forecast of the destination using mcp tool.
    3.Use mcp tool to get the Risk Level of the current destination for better travel guidance.
    4.Explain why you give that risk for the distination

    Use simple language and explain the main reason behind the risk level.
"""

#=================================================================================================================================

@mcp.prompt()
async def packing_recommendation_prompt(destination:str, weather_risk:str) -> str:
    """
    Analyze the weather for the {destination} give weather risk '{weather_risk}' and recommend essintials things to carry.
    """
    return f""" Analyze the weather for the {destination} give weather risk '{weather_risk}' and recommend essintials things to pack.
    Steps:
    1.Run the mcp tool for validating the destination.
    2.Get the weather forecast of the destination using mcp tool.
    3.Use mcp tool to get the Risk Level of the current destination for better travel guidance.
    4.Provide what all essentials things are necessary to pack for smooth travel.

    Suggest practical packing items for the destination based on the weather risk.
    Return a short list of useful packing suggestions.
"""