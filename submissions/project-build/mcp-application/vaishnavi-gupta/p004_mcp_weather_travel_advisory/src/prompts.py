import json  
import requests  
from typing import List, Dict, Optional  
from fastmcp import FastMCP  
from pathlib import Path  
import os 
from dotenv import load_dotenv 
load_dotenv()

mcp = FastMCP("Weather Travel Advisory")


@mcp.prompt()                          # Creates a concise travel-readiness advisory.
async def travel_readiness() -> str:
    """
    Create a concise travel-readiness advisory for the destination.

    Destination: {destination}
    Forecast Summary: {forecast_summary}
    Weather Risk: {weather_risk}
    Recommended Actions: {recommended_actions}

    Explain whether travel looks comfortable, manageable with precautions,
    or risky due to weather.
    Keep the answer practical and easy to understand.

    """

@mcp.prompt()                       # Explains why the risk level is LOW, MEDIUM, or HIGH.
async def weather_risk_summary() -> str:
    """
    Explain the weather risk level for the destination.
    Destination: {destination}
    Risk Level: {weather_risk}
    Risk Factors: {risk_factors}
    Use simple language and explain the main reason behind the risk level.
    """


@mcp.prompt()                          # Generates practical packing suggestions.
async def packing_recommendation() -> str:
    """
    Suggest practical packing items for the destination based on the 
    weather risk.
    Destination: {destination}
    Risk Level: {weather_risk}
    Risk Factors: {risk_factors}
    Return a short list of useful packing suggestions
    """
   


if __name__ == "__main__":
    
    mcp.run()
