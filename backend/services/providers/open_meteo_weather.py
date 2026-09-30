"""
Open-Meteo Weather & Air Quality Provider for Mausam (Step 19).

Fetches:
  1. Forecast API: current observations, 10-hour forecast, 7-day daily forecast.
  2. Air Quality API: US AQI, PM2.5, PM10.

Requests are made sequentially (forecast first, then AQI) for production
reliability — the critical forecast is isolated from AQI failures.
Transient failures are retried up to 3 times with exponential backoff.

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

# Transient error types that warrant a retry
_TRANSIENT_EXCEPTIONS = (
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.PoolTimeout,
    httpx.ConnectError,
    httpx.RemoteProtocolError,
)


async def _fetch_with_retry(
    client: httpx.AsyncClient,
    url: str,
    params: dict,
    headers: dict,
    label: str,
    max_attempts: int = 3,
) -> httpx.Response:
    """
    Fetch a URL with bounded exponential-backoff retry for transient errors.

    Retries: ConnectTimeout, ReadTimeout, ConnectError, RemoteProtocolError.
    Does NOT retry: 4xx client errors, 5xx server errors (except 503/429 on attempt 1).
    Raises on permanent failure.
    """
    last_exc = None
    for attempt in range(1, max_attempts + 1):
        try:
            logger.debug(
                "FETCH attempt=%d/%d label=%s url=%s",
                attempt, max_attempts, label, url,
            )
            resp = await client.get(url, params=params, headers=headers)

            # Retry on 429 / 503 only on first attempt
            if resp.status_code in (429, 503) and attempt < max_attempts:
                delay = 0.5 * (2 ** (attempt - 1))
                logger.warning(
                    "RETRY label=%s status=%d attempt=%d delay=%.1fs",
                    label, resp.status_code, attempt, delay,
                )
                await asyncio.sleep(delay)
                continue

            resp.raise_for_status()
            logger.debug("FETCH OK label=%s status=%d", label, resp.status_code)
            return resp

        except _TRANSIENT_EXCEPTIONS as e:
            last_exc = e
            if attempt < max_attempts:
                delay = 0.5 * (2 ** (attempt - 1))
                logger.warning(
                    "RETRY label=%s exc_type=%s attempt=%d delay=%.1fs exc=%s",
                    label, type(e).__name__, attempt, delay, e,
                )
                await asyncio.sleep(delay)
            else:
                logger.error(
                    "FETCH FAILED label=%s exc_type=%s after %d attempts: %s",
                    label, type(e).__name__, max_attempts, e,
                )
        except httpx.HTTPStatusError as e:
            # Non-transient HTTP error — do not retry
            logger.error(
                "FETCH HTTP_ERROR label=%s status=%d url=%s",
                label, e.response.status_code, url,
            )
            raise

    raise last_exc


class OpenMeteoWeatherProvider:
    """Provider for fetching and normalizing weather and air-quality telemetry from Open-Meteo."""

    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality"

    # Explicit per-phase timeout — generous connect for Render cold-start TLS,
    # bounded read so slow responses don't stall indefinitely.
    TIMEOUT = httpx.Timeout(connect=15.0, read=30.0, write=15.0, pool=15.0)

    async def get_raw_weather(self, location: LocationResult) -> Dict[str, Any]:
        """
        Fetch forecast (required) then air quality (optional) from Open-Meteo.

        Requests are sequential: forecast is fetched and validated first so that
        AQI failures cannot disrupt the critical forecast path.

        If Air Quality fails, proceeds with forecast data and sets AQI to None.
        If Forecast fails after retries, raises the exception to trigger 502/503.
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
            # --- Critical: Forecast (with retry) ---
            logger.info(
                "WEATHER_FETCH city=%s lat=%.4f lon=%.4f tz=%s",
                location.city, location.latitude, location.longitude, tz,
            )
            forecast_resp = await _fetch_with_retry(
                client, self.FORECAST_URL, forecast_params, headers, "forecast"
            )
            forecast_data = forecast_resp.json()
            logger.info("FORECAST_OK city=%s keys=%s", location.city, list(forecast_data.keys())[:6])

            # --- Optional: Air Quality (with retry, fails gracefully) ---
            aq_data: Optional[Dict[str, Any]] = None
            try:
                aq_resp = await _fetch_with_retry(
                    client, self.AIR_QUALITY_URL, aq_params, headers, "air_quality"
                )
                aq_data = aq_resp.json()
                logger.debug("AQI_OK city=%s", location.city)
            except Exception as e:
                logger.warning(
                    "AQI_SKIP city=%s exc_type=%s exc=%s (proceeding without AQI)",
                    location.city, type(e).__name__, e,
                )
                aq_data = None

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

        # 7. Air Quality (US AQI) — optional, gracefully null
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
