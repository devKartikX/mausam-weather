"""
Open-Meteo Weather & Air Quality Provider for Mausam (Step 19).

Fetches:
  1. Forecast API: current observations, 10-hour forecast, 7-day daily forecast.
  2. Air Quality API: US AQI, PM2.5, PM10.

Executes both calls concurrently via httpx with a 5.0-second timeout.
Attribution note:
    Weather data by Open-Meteo.com under CC-BY 4.0 license.
"""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import httpx

from backend.schemas.location import LocationResult
from backend.services.utils import (
    map_wmo_code,
    degrees_to_compass,
    derive_uv_status,
    derive_aqi_status,
)

logger = logging.getLogger(__name__)


class OpenMeteoWeatherProvider:
    """Provider for fetching and normalizing weather and air-quality telemetry from Open-Meteo."""

    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"
    # Split timeout: generous connect budget for Render cold-start TLS handshakes,
    # tighter read budget so hung responses don't stall the request indefinitely.
    TIMEOUT = httpx.Timeout(connect=10.0, read=20.0, write=10.0, pool=10.0)

    async def get_raw_weather(self, location: LocationResult) -> Dict[str, Any]:
        """
        Fetch forecast and air quality data in parallel from Open-Meteo.
        If Air Quality fails, proceeds with forecast data and sets air quality to None.
        If Forecast fails, raises the exception to trigger 502/503.
        """
        tz = location.timezone or "Asia/Kolkata"
        forecast_params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation_probability,weather_code,wind_speed_10m,wind_direction_10m,visibility,uv_index",
            "hourly": "temperature_2m,weather_code,precipitation_probability",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code,sunrise,sunset",
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "precipitation_unit": "mm",
            "timezone": tz,
            "forecast_days": 7,
        }

        aq_params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": "pm10,pm2_5,us_aqi",
            "timezone": tz,
        }

        headers = {
            "User-Agent": "Mausam-PersonalizedWeather/0.2.0 (SIH Project; mail: contact@mausam.app)",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.TIMEOUT) as client:
            async def fetch_forecast():
                resp = await client.get(self.FORECAST_URL, params=forecast_params, headers=headers)
                resp.raise_for_status()
                return resp.json()

            async def fetch_air_quality():
                try:
                    resp = await client.get(self.AIR_QUALITY_URL, params=aq_params, headers=headers)
                    resp.raise_for_status()
                    return resp.json()
                except Exception as e:
                    logger.warning("Air quality API request failed gracefully: %s", e)
                    return None

            forecast_data, aq_data = await asyncio.gather(
                fetch_forecast(),
                fetch_air_quality(),
            )

        return self._normalize_weather(location, forecast_data, aq_data)

    def _normalize_weather(
        self,
        location: LocationResult,
        forecast_data: Dict[str, Any],
        aq_data: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Convert raw Open-Meteo payloads into normalized WeatherResponse dictionary."""
        current_raw = forecast_data.get("current", {})
        daily_raw = forecast_data.get("daily", {})
        hourly_raw = forecast_data.get("hourly", {})
        aq_current = aq_data.get("current", {}) if aq_data else {}

        # 1. Condition & Icon
        weather_code = current_raw.get("weather_code", 0)
        condition_str, icon_name = map_wmo_code(weather_code)

        # 2. Wind & UV
        wind_deg = float(current_raw.get("wind_direction_10m", 0.0))
        wind_dir = degrees_to_compass(wind_deg)
        uv_idx = float(current_raw.get("uv_index", 0.0))
        uv_status = derive_uv_status(uv_idx)

        # 3. High / Low from daily[0]
        daily_highs = daily_raw.get("temperature_2m_max", [])
        daily_lows = daily_raw.get("temperature_2m_min", [])
        high_temp = float(daily_highs[0]) if daily_highs else float(current_raw.get("temperature_2m", 0))
        low_temp = float(daily_lows[0]) if daily_lows else float(current_raw.get("temperature_2m", 0))

        # 4. Precipitation probability
        # Open-Meteo current endpoint supports precipitation_probability.
        # Fallback to hourly[0] if current is None.
        curr_pop = current_raw.get("precipitation_probability")
        if curr_pop is None:
            hourly_pops = hourly_raw.get("precipitation_probability", [])
            curr_pop = hourly_pops[0] if hourly_pops else 0
        curr_pop = int(curr_pop or 0)

        # 5. Visibility (m -> km)
        vis_meters = float(current_raw.get("visibility", 10000.0))
        vis_km = round(vis_meters / 1000.0, 1)

        # 6. Sunrise & Sunset formatting ("06:14 AM")
        daily_sunrises = daily_raw.get("sunrise", [])
        daily_sunsets = daily_raw.get("sunset", [])
        sunrise_str = self._format_sun_time(daily_sunrises[0]) if daily_sunrises else "06:00 AM"
        sunset_str = self._format_sun_time(daily_sunsets[0]) if daily_sunsets else "06:30 PM"

        # 7. Air Quality (US AQI)
        aqi_val = aq_current.get("us_aqi") if aq_current else None
        aqi_status = derive_aqi_status(int(aqi_val)) if aqi_val is not None else None
        pm25_val = float(aq_current.get("pm2_5")) if aq_current and aq_current.get("pm2_5") is not None else None
        pm10_val = float(aq_current.get("pm10")) if aq_current and aq_current.get("pm10") is not None else None

        # 8. Hourly (next 10 hours)
        hourly_list = []
        h_times = hourly_raw.get("time", [])
        h_temps = hourly_raw.get("temperature_2m", [])
        h_codes = hourly_raw.get("weather_code", [])
        h_pops = hourly_raw.get("precipitation_probability", [])

        # Find current hour index based on current_raw time or default to 0
        start_idx = 0
        curr_time_str = current_raw.get("time")
        if curr_time_str and curr_time_str in h_times:
            start_idx = h_times.index(curr_time_str)
        elif curr_time_str:
            try:
                curr_dt = datetime.fromisoformat(curr_time_str)
                hour_str = curr_dt.strftime("%Y-%m-%dT%H:00")
                if hour_str in h_times:
                    start_idx = h_times.index(hour_str)
            except Exception:
                pass

        for i in range(start_idx, min(start_idx + 10, len(h_times))):
            rel_i = i - start_idx
            time_label = "Now" if rel_i == 0 else self._format_hour_label(h_times[i])
            h_code = h_codes[i] if i < len(h_codes) else 0
            h_cond, h_icon = map_wmo_code(h_code)
            h_temp = float(h_temps[i]) if i < len(h_temps) else float(current_raw.get("temperature_2m", 0.0))
            h_pop = int(h_pops[i] or 0) if i < len(h_pops) else 0
            hourly_list.append({
                "time": time_label,
                "temp": round(h_temp),
                "condition": h_cond,
                "pop": h_pop,
                "icon": h_icon,
            })

        # 9. Daily (7 days)
        daily_list = []
        d_times = daily_raw.get("time", [])
        d_codes = daily_raw.get("weather_code", [])
        d_pops = daily_raw.get("precipitation_probability_max", [])

        for i in range(min(7, len(d_times))):
            day_label = "Today" if i == 0 else self._format_day_name(d_times[i])
            d_code = d_codes[i] if i < len(d_codes) else 0
            d_cond, d_icon = map_wmo_code(d_code)
            d_high = float(daily_highs[i]) if i < len(daily_highs) else float(high_temp)
            d_low = float(daily_lows[i]) if i < len(daily_lows) else float(low_temp)
            d_pop = int(d_pops[i] or 0) if i < len(d_pops) else 0
            daily_list.append({
                "day": day_label,
                "condition": d_cond,
                "high": round(d_high),
                "low": round(d_low),
                "pop": d_pop,
                "icon": d_icon,
            })

        # 10. Assemble complete normalized structure
        now_utc = datetime.now(timezone.utc).isoformat()
        return {
            "meta": {
                "source": "open-meteo",
                "generatedAt": now_utc,
                "cachedAt": None,
                "locationQuery": location.city,
                "isDemo": False,
            },
            "location": {
                "city": location.city,
                "state": location.state,
                "country": location.country,
                "latitude": location.latitude,
                "longitude": location.longitude,
                "timezone": location.timezone,
                "elevation": forecast_data.get("elevation"),
                "lastUpdated": current_raw.get("time"),
            },
            "current": {
                "temp": round(float(current_raw.get("temperature_2m", 0.0))),
                "condition": condition_str,
                "feelsLike": round(float(current_raw.get("apparent_temperature", 0.0))),
                "highTemp": round(high_temp),
                "lowTemp": round(low_temp),
                "humidity": int(current_raw.get("relative_humidity_2m", 0)),
                "windSpeed": round(float(current_raw.get("wind_speed_10m", 0.0)), 1),
                "windDirection": wind_dir,
                "rainProbability": curr_pop,
                "visibility": vis_km,
                "uvIndex": round(uv_idx, 1),
                "uvStatus": uv_status,
                "aqi": int(aqi_val) if aqi_val is not None else None,
                "aqiStatus": aqi_status,
                "pm25": pm25_val,
                "pm10": pm10_val,
                "sunrise": sunrise_str,
                "sunset": sunset_str,
                "icon": icon_name,
                "waveHeight": None,
                "seaSurfaceTemp": None,
                "tidalInfo": None,
            },
            "hourly": hourly_list,
            "daily": daily_list,
            "alerts": [],
        }

    def _format_sun_time(self, iso_str: str) -> str:
        """Format '2026-09-30T06:14' into '06:14 AM'."""
        try:
            dt = datetime.fromisoformat(iso_str)
            return dt.strftime("%I:%M %p")
        except Exception:
            return iso_str

    def _format_hour_label(self, iso_str: str) -> str:
        """Format '2026-09-30T19:00' into '7 PM' (cross-platform compatible)."""
        try:
            dt = datetime.fromisoformat(iso_str)
            hour_12 = dt.hour % 12 or 12
            am_pm = "AM" if dt.hour < 12 else "PM"
            return f"{hour_12} {am_pm}"
        except Exception:
            return iso_str

    def _format_day_name(self, date_str: str) -> str:
        """Format '2026-10-01' into 'Thu'."""
        try:
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%a")
        except Exception:
            return date_str
