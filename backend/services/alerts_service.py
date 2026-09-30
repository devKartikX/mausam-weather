"""
Alerts Service for Mausam (Step 27).

Manages official weather alerts retrieval and an independent short-TTL cache (5 minutes)
with bounded memory. Never serves stale emergency alerts.
"""

import time
import logging
from typing import List, Dict, Any, Tuple, Optional

from backend.schemas.location import LocationResult
from backend.services.providers.imd_alerts import IMDAlertsProvider

logger = logging.getLogger(__name__)


class AlertsService:
    """Service managing official alert fetching and short-TTL in-memory caching."""

    CACHE_TTL_SECONDS = 300  # 5 minutes (short TTL for emergency warnings)
    MAX_CACHE_ENTRIES = 200

    def __init__(self, provider: Optional[IMDAlertsProvider] = None):
        self.provider = provider or IMDAlertsProvider()
        # In-memory cache: cache_key -> (list_of_alerts, expiry_timestamp)
        self._cache: Dict[str, Tuple[List[Dict[str, Any]], float]] = {}

    def _make_cache_key(self, location: LocationResult) -> str:
        city = (location.city or "").lower().strip()
        state = (location.state or "").lower().strip()
        return f"{city}:{state}"

    def _prune_expired(self, current_time: float) -> None:
        expired_keys = [k for k, (_, expiry) in self._cache.items() if current_time > expiry]
        for k in expired_keys:
            del self._cache[k]

        if len(self._cache) >= self.MAX_CACHE_ENTRIES:
            sorted_keys = sorted(self._cache.keys(), key=lambda k: self._cache[k][1])
            excess = len(self._cache) - self.MAX_CACHE_ENTRIES + 1
            for k in sorted_keys[:excess]:
                del self._cache[k]

    async def get_alerts(self, location: LocationResult) -> Tuple[List[Dict[str, Any]], bool]:
        """
        Retrieve active alerts for location.
        Returns (alerts_list, is_available_flag).
        If provider fails, returns ([], False) indicating alerts service was unavailable.
        """
        key = self._make_cache_key(location)
        now = time.time()

        # Check cache
        if key in self._cache:
            alerts, expiry = self._cache[key]
            if now <= expiry:
                return alerts, True
            else:
                del self._cache[key]

        # Fetch fresh
        try:
            alerts = await self.provider.get_alerts_for_location(location)
            self._prune_expired(now)
            self._cache[key] = (alerts, now + self.CACHE_TTL_SECONDS)
            return alerts, True
        except Exception as exc:
            logger.warning("AlertsService failed to fetch alerts for %s: %s", location.city, exc)
            # Never return stale expired emergency alerts
            return [], False


# Singleton instance
alerts_service = AlertsService()
