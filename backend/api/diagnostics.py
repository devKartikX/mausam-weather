"""
Temporary production diagnostic endpoint — GET /api/diag/weather

Tests Open-Meteo connectivity from the deployed environment.
Returns safe diagnostic information (no secrets, no user data).
Remove this endpoint after the production issue is resolved.
"""

import sys
import asyncio
import traceback
import httpx
from datetime import datetime, timezone
from fastapi import APIRouter

router = APIRouter()

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

# Jaipur test coordinates
TEST_PARAMS_FORECAST = {
    "latitude": 26.91962,
    "longitude": 75.78781,
    "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m,wind_direction_10m,visibility,uv_index",
    "hourly": "temperature_2m,weather_code,precipitation_probability",
    "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code,sunrise,sunset",
    "temperature_unit": "celsius",
    "wind_speed_unit": "kmh",
    "precipitation_unit": "mm",
    "timezone": "Asia/Kolkata",
    "forecast_days": 7,
}
TEST_PARAMS_AQI = {
    "latitude": 26.91962,
    "longitude": 75.78781,
    "current": "pm10,pm2_5,us_aqi",
    "timezone": "Asia/Kolkata",
}


async def _probe(client: httpx.AsyncClient, label: str, url: str, params: dict) -> dict:
    """Probe a single endpoint and return safe diagnostic info."""
    result = {"endpoint": label, "url": url}
    try:
        resp = await client.get(url, params=params)
        result["http_status"] = resp.status_code
        result["ok"] = resp.status_code == 200
        if resp.status_code == 200:
            data = resp.json()
            result["keys"] = list(data.keys())[:10]
        else:
            result["body_preview"] = resp.text[:200]
    except httpx.ConnectTimeout as e:
        result["error_type"] = "ConnectTimeout"
        result["error"] = str(e)
    except httpx.ReadTimeout as e:
        result["error_type"] = "ReadTimeout"
        result["error"] = str(e)
    except httpx.ConnectError as e:
        result["error_type"] = "ConnectError"
        result["error"] = str(e)
    except httpx.RemoteProtocolError as e:
        result["error_type"] = "RemoteProtocolError"
        result["error"] = str(e)
    except Exception as e:
        result["error_type"] = type(e).__name__
        result["error"] = str(e)
        result["traceback"] = traceback.format_exc()[-800:]
    return result


@router.get("/diag/weather")
async def diagnose_weather():
    """
    Safe read-only diagnostic: tests Open-Meteo connectivity from this environment.
    Returns exception types and HTTP statuses — no secrets, no user data.
    """
    env_info = {
        "python_version": sys.version,
        "httpx_version": httpx.__version__,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }

    timeout = httpx.Timeout(connect=15.0, read=30.0, write=15.0, pool=15.0)

    results = []
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            # Run sequentially to isolate each failure
            forecast_result = await _probe(client, "forecast", FORECAST_URL, TEST_PARAMS_FORECAST)
            results.append(forecast_result)

            aqi_result = await _probe(client, "air_quality", AIR_QUALITY_URL, TEST_PARAMS_AQI)
            results.append(aqi_result)
    except Exception as e:
        results.append({
            "error_type": type(e).__name__,
            "error": str(e),
            "phase": "AsyncClient creation or outer exception",
        })

    # Also test normalization if forecast succeeded
    normalization_result = None
    forecast_ok = any(r.get("endpoint") == "forecast" and r.get("ok") for r in results)
    if forecast_ok:
        try:
            from backend.services.providers.open_meteo_weather import OpenMeteoWeatherProvider
            from backend.schemas.location import LocationResult
            loc = LocationResult(
                city="Jaipur", state="Rajasthan", country="India",
                latitude=26.91962, longitude=75.78781,
                timezone="Asia/Kolkata", displayName="Jaipur, Rajasthan, India"
            )
            provider = OpenMeteoWeatherProvider()
            normalized = await provider.get_raw_weather(loc)
            from backend.schemas.weather import WeatherResponse
            validated = WeatherResponse(**normalized)
            normalization_result = {"ok": True, "temp": normalized.get("current", {}).get("temp")}
        except Exception as e:
            normalization_result = {
                "ok": False,
                "error_type": type(e).__name__,
                "error": str(e),
                "traceback": traceback.format_exc()[-1000:],
            }

    return {
        "env": env_info,
        "probes": results,
        "normalization": normalization_result,
    }
