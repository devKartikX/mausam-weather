"""
Open-Meteo Geocoding Provider for Mausam (Step 17, extended Step 24).

Endpoint:
    https://geocoding-api.open-meteo.com/v1/search?name={query}&count=N&language=en&format=json

Licensing & Attribution note:
    Open-Meteo free tier is permitted for non-commercial & educational use (CC-BY 4.0).
    Attribution ("Geocoding data by Open-Meteo.com / GeoNames") must be provided in the
    eventual user-facing product UI footer/about section.
"""

from typing import List, Optional
import httpx

from backend.schemas.location import LocationResult
from backend.services.providers.base import GeocodingProvider


class OpenMeteoGeocodingProvider(GeocodingProvider):
    """
    Geocoding provider backed by the Open-Meteo Geocoding API.

    Implements both:
      - resolve()  → single best-match (used by the weather pipeline)
      - search()   → multi-result list (used by autocomplete)
    """

    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    TIMEOUT_SECONDS = 4.0
    HEADERS = {
        "User-Agent": "Mausam-PersonalizedWeather/0.2.0 (SIH Project; mail: contact@mausam.app)",
        "Accept": "application/json",
    }

    # Maximum results Open-Meteo accepts per request
    MAX_COUNT = 10

    def _parse_result(self, raw: dict) -> Optional[LocationResult]:
        """
        Convert a single Open-Meteo geocoding result dict into a LocationResult.
        Returns None if mandatory fields (name, latitude, longitude) are missing.
        """
        city = raw.get("name")
        if not city:
            return None

        lat_raw = raw.get("latitude")
        lon_raw = raw.get("longitude")
        if lat_raw is None or lon_raw is None:
            return None

        state = raw.get("admin1")
        country = raw.get("country", "")
        latitude = float(lat_raw)
        longitude = float(lon_raw)
        timezone = raw.get("timezone")

        # Construct clean displayName without inventing missing fields
        parts = [city]
        if state and state.lower() != city.lower():
            parts.append(state)
        if country:
            parts.append(country)
        display_name = ", ".join(parts)

        return LocationResult(
            city=city,
            state=state,
            country=country,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            displayName=display_name,
        )

    async def resolve(self, query: str) -> Optional[LocationResult]:
        """
        Query Open-Meteo Geocoding API with count=1 and a 4.0-second timeout.
        Returns the single best-match LocationResult, or None if no results.
        Raises httpx.HTTPError on network failures, timeouts, or 5xx provider errors.
        """
        params = {
            "name": query.strip(),
            "count": 1,
            "language": "en",
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS) as client:
            response = await client.get(self.GEOCODING_URL, params=params, headers=self.HEADERS)
            response.raise_for_status()
            data = response.json()

        results = data.get("results") or []
        if not results:
            return None

        return self._parse_result(results[0])

    async def search(self, query: str, count: int = 8) -> List[LocationResult]:
        """
        Query Open-Meteo Geocoding API for up to `count` autocomplete suggestions.

        - count is capped at MAX_COUNT (10) to avoid unbounded requests.
        - Returns an empty list if the provider returns no matches.
        - Raises httpx.HTTPError on network failures or timeouts.
        - Deduplication by (city, state, country) is handled by the caller (LocationService).
        """
        bounded_count = min(max(count, 1), self.MAX_COUNT)

        params = {
            "name": query.strip(),
            "count": bounded_count,
            "language": "en",
            "format": "json",
        }

        async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS) as client:
            response = await client.get(self.GEOCODING_URL, params=params, headers=self.HEADERS)
            response.raise_for_status()
            data = response.json()

        raw_results = data.get("results") or []
        parsed: List[LocationResult] = []
        for raw in raw_results:
            result = self._parse_result(raw)
            if result is not None:
                parsed.append(result)

        return parsed
