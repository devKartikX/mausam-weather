"""
Weather Service for Mausam (Step 19).

Coordinates fetching real weather from OpenMeteoWeatherProvider and provides
a 15-minute in-memory TTL cache keyed by rounded coordinates and timezone.
"""

import time
import logging
from datetime import datetime, timezone
from typing import Dict, Tuple, Any, Optional

from backend.schemas.location import LocationResult
from backend.services.providers.open_meteo_weather import OpenMeteoWeatherProvider
from backend.services.providers.open_meteo_marine import OpenMeteoMarineProvider
from backend.services.alerts_service import alerts_service

logger = logging.getLogger(__name__)


class WeatherService:
    """Service managing weather data retrieval, marine telemetry, alerts, and stale fallback caching."""

    CACHE_TTL_SECONDS = 900       # 15 minutes fresh cache
    STALE_MAX_AGE_SECONDS = 3600  # Up to 60 minutes stale cache fallback if provider fails
    MAX_CACHE_ENTRIES = 500       # Bounded in-memory size

    def __init__(
        self,
        provider: Optional[OpenMeteoWeatherProvider] = None,
        marine_provider: Optional[OpenMeteoMarineProvider] = None,
    ):
        self.provider = provider or OpenMeteoWeatherProvider()
        self.marine_provider = marine_provider or OpenMeteoMarineProvider()
        # In-memory cache: cache_key -> (response_dict, expiry_time, cached_at_iso, timestamp_epoch)
        self._cache: Dict[str, Tuple[Dict[str, Any], float, str, float]] = {}

    def _make_cache_key(self, location: LocationResult) -> str:
        lat = round(location.latitude, 3)
        lon = round(location.longitude, 3)
        tz = location.timezone or "Asia/Kolkata"
        return f"{lat}:{lon}:{tz}"

    def _prune_expired(self, current_time: float) -> None:
        """Evict all entries that exceed the maximum stale window (60 min)."""
        expired_keys = [
            k for k, (_, _, _, created_at) in self._cache.items()
            if (current_time - created_at) > self.STALE_MAX_AGE_SECONDS
        ]
        for k in expired_keys:
            del self._cache[k]

        if len(self._cache) >= self.MAX_CACHE_ENTRIES:
            sorted_keys = sorted(self._cache.keys(), key=lambda k: self._cache[k][3])
            excess = len(self._cache) - self.MAX_CACHE_ENTRIES + 1
            for k in sorted_keys[:excess]:
                del self._cache[k]

    def _get_fresh_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        entry = self._cache.get(key)
        if not entry:
            return None
        data, expiry, cached_at, created_at = entry
        now = time.time()
        if now <= expiry:
            res = dict(data)
            res["meta"] = {
                **res.get("meta", {}),
                "cachedAt": cached_at,
                "isStale": False,
                "staleReason": None,
                "dataAgeSeconds": int(now - created_at),
            }
            return res
        return None

    def _get_stale_from_cache(self, key: str, reason: str) -> Optional[Dict[str, Any]]:
        entry = self._cache.get(key)
        if not entry:
            return None
        data, _, cached_at, created_at = entry
        now = time.time()
        age = now - created_at
        if age <= self.STALE_MAX_AGE_SECONDS:
            res = dict(data)
            res["meta"] = {
                **res.get("meta", {}),
                "cachedAt": cached_at,
                "isStale": True,
                "staleReason": reason,
                "dataAgeSeconds": int(age),
                # Stale weather must never claim active emergency alerts
                "alertsAvailable": False,
            }
            # Clear alerts on stale cache fallback to prevent outdated emergency warnings
            res["alerts"] = []
            return res
        return None

    def _set_in_cache(self, key: str, data: Dict[str, Any]):
        now = time.time()
        self._prune_expired(now)
        now_iso = datetime.now(timezone.utc).isoformat()
        self._cache[key] = (data, now + self.CACHE_TTL_SECONDS, now_iso, now)

    async def get_weather(self, location: LocationResult, original_query: str) -> Dict[str, Any]:
        """
        Retrieve normalized weather for the given canonical location.
        Enriches with marine conditions and official alerts.
        Supports 60-minute stale fallback if live provider fails.
        """
        key = self._make_cache_key(location)
        fresh = self._get_fresh_from_cache(key)
        if fresh:
            fresh["meta"]["locationQuery"] = original_query
            return fresh

        # Attempt live fetch
        try:
            # 1. Fetch core weather & air quality
            normalized = await self.provider.get_raw_weather(location)
            normalized["meta"]["locationQuery"] = original_query

            # 2. Fetch marine conditions (additive; fails gracefully for inland)
            try:
                marine_data = await self.marine_provider.get_marine_data(location)
                if marine_data and marine_data.get("waveHeight") is not None:
                    normalized["current"]["waveHeight"] = marine_data["waveHeight"]
                    normalized["current"]["waveDirection"] = marine_data.get("waveDirection")
                    normalized["current"]["wavePeriod"] = marine_data.get("wavePeriod")
            except Exception as e:
                logger.debug("Marine fetch failed gracefully: %s", e)

            # 3. Fetch official alerts (additive; fails gracefully)
            try:
                alerts, alerts_ok = await alerts_service.get_alerts(location)
                normalized["alerts"] = alerts
                normalized["meta"]["alertsAvailable"] = alerts_ok
            except Exception as e:
                logger.debug("Alerts fetch failed gracefully: %s", e)
                normalized["alerts"] = []
                normalized["meta"]["alertsAvailable"] = False

            # Cache only real live responses (do not cache demo fallback as successful live data)
            if not normalized.get("meta", {}).get("isDemo", False):
                self._set_in_cache(key, normalized)
            else:
                # Optionally cache demo data with short 60s TTL to prevent spamming rate-limited provider
                now = time.time()
                self._cache[key] = (normalized, now + 60, datetime.now(timezone.utc).isoformat(), now)

            return normalized

        except Exception as provider_error:
            logger.warning("Weather provider failed for %s: %s", location.city, provider_error)
            # Attempt stale cache fallback (up to 60 minutes)
            stale = self._get_stale_from_cache(key, reason=str(provider_error))
            if stale:
                logger.info("Serving stale cached weather for %s (age %ss)", location.city, stale["meta"].get("dataAgeSeconds"))
                stale["meta"]["locationQuery"] = original_query
                return stale
            # No valid stale cache available -> re-raise
            raise provider_error


# Singleton instance
weather_service = WeatherService()
