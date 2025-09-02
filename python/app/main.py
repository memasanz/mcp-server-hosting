#from api_key_auth import ensure_valid_api_key
#app = FastAPI(title="Hello Work API", version="0.1.0")
#app = FastAPI(docs_url=None, redoc_url=None, dependencies=[Depends(ensure_valid_api_key)])

""" tools for MCP Streamable HTTP server using NWS API."""

import argparse
from typing import Any
from datetime import datetime
import os

import httpx
import uvicorn
from fastapi import status, HTTPException, Depends

from mcp.server.fastmcp import FastMCP

from app.weather.tools import get_alerts, get_forecast
from app.powerpoint.tools import get_layout_names_from_blob_url, add_slide_from_blob_url
from app.api_key_auth import ensure_valid_api_key

# Initialize FastMCP server with extended timeouts
mcp = FastMCP(
    name="weather",
    json_response=True,     # Use JSON responses
    stateless_http=False,   # Use persistent connections
)

# Get the FastAPI app instance
app = mcp.streamable_http_app



mcp.tool()(get_alerts)
mcp.tool()(get_forecast)
mcp.tool()(get_layout_names_from_blob_url)
mcp.tool()(add_slide_from_blob_url)


# # Constants
# NWS_API_BASE = "https://api.weather.gov"
# USER_AGENT = "weather-app/1.0"


# async def make_nws_request(url: str) -> dict[str, Any] | None:
#     """Make a request to the NWS API with proper error handling."""
#     headers = {"User-Agent": USER_AGENT, "Accept": "application/geo+json"}
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url, headers=headers, timeout=30.0)
#             response.raise_for_status()
#             return response.json()
#         except Exception:
#             return None


# def format_alert(feature: dict) -> str:
#     """Format an alert feature into a readable string."""
#     props = feature["properties"]
#     return f"""
# Event: {props.get('event', 'Unknown')}
# Area: {props.get('areaDesc', 'Unknown')}
# Severity: {props.get('severity', 'Unknown')}
# Description: {props.get('description', 'No description available')}
# Instructions: {props.get('instruction', 'No specific instructions provided')}
# """


# @mcp.tool()
# async def get_alerts(state: str) -> str:
#     """Get weather alerts for a US state.

#     Args:
#         state: Two-letter US state code (e.g. CA, NY)
#     """
#     url = f"{NWS_API_BASE}/alerts/active/area/{state}"
#     data = await make_nws_request(url)

#     if not data or "features" not in data:
#         return "Unable to fetch alerts or no alerts found."

#     if not data["features"]:
#         return "No active alerts for this state."

#     alerts = [format_alert(feature) for feature in data["features"]]
#     return "\n---\n".join(alerts)


# @mcp.tool()
# async def get_forecast(latitude: float, longitude: float) -> str:
#     """Get weather forecast for a location.

#     Args:
#         latitude: Latitude of the location
#         longitude: Longitude of the location
#     """
#     # First get the forecast grid endpoint
#     points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
#     points_data = await make_nws_request(points_url)

#     if not points_data:
#         return "Unable to fetch forecast data for this location."

#     # Get the forecast URL from the points response
#     forecast_url = points_data["properties"]["forecast"]
#     forecast_data = await make_nws_request(forecast_url)

#     if not forecast_data:
#         return "Unable to fetch detailed forecast."

#     # Format the periods into a readable forecast
#     periods = forecast_data["properties"]["periods"]
#     forecasts = []
#     for period in periods[:5]:  # Only show next 5 periods
#         forecast = f"""
# {period['name']}:
# Temperature: {period['temperature']}°{period['temperatureUnit']}
# Wind: {period['windSpeed']} {period['windDirection']}
# Forecast: {period['detailedForecast']}
# """
#         forecasts.append(forecast)

#     return "\n---\n".join(forecasts)


if __name__ == "__main__":
    uvicorn.run(mcp.streamable_http_app, host="0.0.0.0", port=8000)