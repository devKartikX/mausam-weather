"""
Utility helpers for weather mapping:
  - WMO weather code to condition & frontend Lucide icon mapping
  - Wind direction degree to 16-point compass heading conversion
  - AQI status category derivation (US AQI standard)
  - UV status category derivation
"""

from typing import Tuple

# WMO Weather interpretation code (WW) mapping
WMO_CODE_MAP = {
    0: ("Clear Sky", "Sun"),
    1: ("Mainly Clear", "Sun"),
    2: ("Partly Cloudy", "CloudSun"),
    3: ("Overcast", "Cloud"),
    45: ("Foggy", "CloudFog"),
    48: ("Depositing Rime Fog", "CloudFog"),
    51: ("Light Drizzle", "CloudDrizzle"),
    53: ("Moderate Drizzle", "CloudDrizzle"),
    55: ("Dense Drizzle", "CloudDrizzle"),
    56: ("Light Freezing Drizzle", "CloudDrizzle"),
    57: ("Dense Freezing Drizzle", "CloudDrizzle"),
    61: ("Slight Rain", "CloudRain"),
    63: ("Moderate Rain", "CloudRain"),
    65: ("Heavy Rain", "CloudRain"),
    66: ("Light Freezing Rain", "CloudRain"),
    67: ("Heavy Freezing Rain", "CloudRain"),
    71: ("Slight Snow Fall", "CloudSnow"),
    73: ("Moderate Snow Fall", "CloudSnow"),
    75: ("Heavy Snow Fall", "CloudSnow"),
    77: ("Snow Grains", "CloudSnow"),
    80: ("Slight Rain Showers", "CloudRain"),
    81: ("Moderate Rain Showers", "CloudRain"),
    82: ("Violent Rain Showers", "CloudRain"),
    85: ("Slight Snow Showers", "CloudSnow"),
    86: ("Heavy Snow Showers", "CloudSnow"),
    95: ("Thunderstorm", "CloudLightning"),
    96: ("Thunderstorm with Slight Hail", "CloudLightning"),
    99: ("Thunderstorm with Heavy Hail", "CloudLightning"),
}

COMPASS_DIRECTIONS = [
    "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
    "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
]


def map_wmo_code(code: int) -> Tuple[str, str]:
    """Return (condition_string, icon_name) for a given WMO weather code."""
    return WMO_CODE_MAP.get(code, ("Unknown", "CloudSun"))


def degrees_to_compass(degrees: float) -> str:
    """Convert meteorological wind direction in degrees to a 16-point compass heading."""
    val = int((degrees + 11.25) / 22.5)
    return COMPASS_DIRECTIONS[val % 16]


def derive_uv_status(uv_index: float) -> str:
    """Derive standard WHO UV status category."""
    if uv_index <= 2.9:
        return "Low"
    elif uv_index <= 5.9:
        return "Moderate"
    elif uv_index <= 7.9:
        return "High"
    elif uv_index <= 10.9:
        return "Very High"
    return "Extreme"


def derive_aqi_status(aqi_val: int) -> str:
    """Derive US EPA AQI category status."""
    if aqi_val <= 50:
        return "Good"
    elif aqi_val <= 100:
        return "Moderate"
    elif aqi_val <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi_val <= 200:
        return "Unhealthy"
    elif aqi_val <= 300:
        return "Very Unhealthy"
    return "Hazardous"
