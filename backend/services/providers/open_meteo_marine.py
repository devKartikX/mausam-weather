"""
Open-Meteo Marine Weather Provider for Mausam (Step 27).

Fetches marine conditions (wave height, wave direction, wave period)
using the Open-Meteo Marine API.
Inland locations return None values gracefully.
"""

import logging
from typing import Dict, Any, Optional
import httpx

from backend.schemas.location import LocationResult

logger = logging.getLogger(__name__)


class OpenMeteoMarineProvider:
    """Provider for fetching marine and surf telemetry from Open-Meteo."""

    MARINE_URL = "https://marine-api.open-meteo.com/v1/marine"
    TIMEOUT_SECONDS = 4.0

    async def get_marine_data(self, location: LocationResult) -> Optional[Dict[str, Any]]:
        """
        Fetch marine data for a canonical location.
        Returns a dict with waveHeight, waveDirection, wavePeriod or None if unavailable/inland.
        """
        params = {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "current": "wave_height,wave_direction,wave_period",
            "timezone": location.timezone or "Asia/Kolkata",
        }

        headers = {
            "User-Agent": "Mausam-PersonalizedWeather/0.2.0 (SIH Project; mail: contact@mausam.app)",
            "Accept": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS) as client:
                resp = await client.get(self.MARINE_URL, params=params, headers=headers)
                if resp.status_code != 200:
                    logger.debug("Marine API returned status %s for %s", resp.status_code, location.city)
                    return None
                data = resp.json()
                current = data.get("current", {})
                wave_height = current.get("wave_height")
                wave_dir = current.get("wave_direction")
                wave_period = current.get("wave_period")

                if wave_height is None:
                    # Inland location with no marine data
                    return None

                return {
                    "waveHeight": round(float(wave_height), 1),
                    "waveDirection": round(float(wave_dir)) if wave_dir is not None else None,
                    "wavePeriod": round(float(wave_period), 1) if wave_period is not None else None,
                    "seaSurfaceTemp": None,
                    "tidalInfo": None,
                }
        except Exception as e:
            logger.warning("Marine data request failed gracefully for %s: %s", location.city, e)
            return None
