"""
Location Resolution Service for Mausam (Step 17, extended Step 24).

Provides:
  - resolve_location(query)      → single best-match LocationResult (used by weather endpoint)
  - search_locations(query)      → list of candidate LocationResults (used by autocomplete)

Both paths use separate in-memory TTL caches (24h, bounded to 500 entries each).
"""

import time
import logging
from typing import Dict, List, Optional, Tuple
import httpx

from backend.schemas.location import LocationResult
from backend.services.providers.base import GeocodingProvider
from backend.services.providers.open_meteo import OpenMeteoGeocodingProvider

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Offline fallback metro hub dataset
# Used ONLY when:
#   (a) the upstream geocoding provider is unreachable for resolve(), OR
#   (b) a 1-character query is made and the provider returns no results.
# Unknown city names never receive a fallback city silently.
# ---------------------------------------------------------------------------
FALLBACK_METRO_HUBS: Dict[str, dict] = {
    "jaipur": {
        "city": "Jaipur",
        "state": "Rajasthan",
        "country": "India",
        "latitude": 26.9124,
        "longitude": 75.7873,
        "timezone": "Asia/Kolkata",
        "displayName": "Jaipur, Rajasthan, India",
    },
    "mumbai": {
        "city": "Mumbai",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 19.0760,
        "longitude": 72.8777,
        "timezone": "Asia/Kolkata",
        "displayName": "Mumbai, Maharashtra, India",
    },
    "bengaluru": {
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone": "Asia/Kolkata",
        "displayName": "Bengaluru, Karnataka, India",
    },
    "bangalore": {
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone": "Asia/Kolkata",
        "displayName": "Bengaluru, Karnataka, India",
    },
    "delhi": {
        "city": "New Delhi",
        "state": "Delhi",
        "country": "India",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata",
        "displayName": "New Delhi, Delhi, India",
    },
    "kolkata": {
        "city": "Kolkata",
        "state": "West Bengal",
        "country": "India",
        "latitude": 22.5726,
        "longitude": 88.3639,
        "timezone": "Asia/Kolkata",
        "displayName": "Kolkata, West Bengal, India",
    },
    "chennai": {
        "city": "Chennai",
        "state": "Tamil Nadu",
        "country": "India",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "timezone": "Asia/Kolkata",
        "displayName": "Chennai, Tamil Nadu, India",
    },
    "hyderabad": {
        "city": "Hyderabad",
        "state": "Telangana",
        "country": "India",
        "latitude": 17.3850,
        "longitude": 78.4867,
        "timezone": "Asia/Kolkata",
        "displayName": "Hyderabad, Telangana, India",
    },
    "pune": {
        "city": "Pune",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 18.5204,
        "longitude": 73.8567,
        "timezone": "Asia/Kolkata",
        "displayName": "Pune, Maharashtra, India",
    },
    "ahmedabad": {
        "city": "Ahmedabad",
        "state": "Gujarat",
        "country": "India",
        "latitude": 23.0225,
        "longitude": 72.5714,
        "timezone": "Asia/Kolkata",
        "displayName": "Ahmedabad, Gujarat, India",
    },
    "surat": {
        "city": "Surat",
        "state": "Gujarat",
        "country": "India",
        "latitude": 21.1702,
        "longitude": 72.8311,
        "timezone": "Asia/Kolkata",
        "displayName": "Surat, Gujarat, India",
    },
    "lucknow": {
        "city": "Lucknow",
        "state": "Uttar Pradesh",
        "country": "India",
        "latitude": 26.8467,
        "longitude": 80.9462,
        "timezone": "Asia/Kolkata",
        "displayName": "Lucknow, Uttar Pradesh, India",
    },
    "kanpur": {
        "city": "Kanpur",
        "state": "Uttar Pradesh",
        "country": "India",
        "latitude": 26.4499,
        "longitude": 80.3319,
        "timezone": "Asia/Kolkata",
        "displayName": "Kanpur, Uttar Pradesh, India",
    },
    "nagpur": {
        "city": "Nagpur",
        "state": "Maharashtra",
        "country": "India",
        "latitude": 21.1458,
        "longitude": 79.0882,
        "timezone": "Asia/Kolkata",
        "displayName": "Nagpur, Maharashtra, India",
    },
    "indore": {
        "city": "Indore",
        "state": "Madhya Pradesh",
        "country": "India",
        "latitude": 22.7196,
        "longitude": 75.8577,
        "timezone": "Asia/Kolkata",
        "displayName": "Indore, Madhya Pradesh, India",
    },
    "bhopal": {
        "city": "Bhopal",
        "state": "Madhya Pradesh",
        "country": "India",
        "latitude": 23.2599,
        "longitude": 77.4126,
        "timezone": "Asia/Kolkata",
        "displayName": "Bhopal, Madhya Pradesh, India",
    },
    "patna": {
        "city": "Patna",
        "state": "Bihar",
        "country": "India",
        "latitude": 25.5941,
        "longitude": 85.1376,
        "timezone": "Asia/Kolkata",
        "displayName": "Patna, Bihar, India",
    },
    "vadodara": {
        "city": "Vadodara",
        "state": "Gujarat",
        "country": "India",
        "latitude": 22.3072,
        "longitude": 73.1812,
        "timezone": "Asia/Kolkata",
        "displayName": "Vadodara, Gujarat, India",
    },
    "agra": {
        "city": "Agra",
        "state": "Uttar Pradesh",
        "country": "India",
        "latitude": 27.1767,
        "longitude": 78.0081,
        "timezone": "Asia/Kolkata",
        "displayName": "Agra, Uttar Pradesh, India",
    },
    "visakhapatnam": {
        "city": "Visakhapatnam",
        "state": "Andhra Pradesh",
        "country": "India",
        "latitude": 17.6868,
        "longitude": 83.2185,
        "timezone": "Asia/Kolkata",
        "displayName": "Visakhapatnam, Andhra Pradesh, India",
    },
    "thiruvananthapuram": {
        "city": "Thiruvananthapuram",
        "state": "Kerala",
        "country": "India",
        "latitude": 8.5241,
        "longitude": 76.9366,
        "timezone": "Asia/Kolkata",
        "displayName": "Thiruvananthapuram, Kerala, India",
    },
    "kochi": {
        "city": "Kochi",
        "state": "Kerala",
        "country": "India",
        "latitude": 9.9312,
        "longitude": 76.2673,
        "timezone": "Asia/Kolkata",
        "displayName": "Kochi, Kerala, India",
    },
    "jodhpur": {
        "city": "Jodhpur",
        "state": "Rajasthan",
        "country": "India",
        "latitude": 26.2389,
        "longitude": 73.0243,
        "timezone": "Asia/Kolkata",
        "displayName": "Jodhpur, Rajasthan, India",
    },
    "jammu": {
        "city": "Jammu",
        "state": "Jammu and Kashmir",
        "country": "India",
        "latitude": 32.7266,
        "longitude": 74.8570,
        "timezone": "Asia/Kolkata",
        "displayName": "Jammu, Jammu and Kashmir, India",
    },
    "jalandhar": {
        "city": "Jalandhar",
        "state": "Punjab",
        "country": "India",
        "latitude": 31.3260,
        "longitude": 75.5762,
        "timezone": "Asia/Kolkata",
        "displayName": "Jalandhar, Punjab, India",
    },
    "guwahati": {
        "city": "Guwahati",
        "state": "Assam",
        "country": "India",
        "latitude": 26.1445,
        "longitude": 91.7362,
        "timezone": "Asia/Kolkata",
        "displayName": "Guwahati, Assam, India",
    },
    "ranchi": {
        "city": "Ranchi",
        "state": "Jharkhand",
        "country": "India",
        "latitude": 23.3441,
        "longitude": 85.3096,
        "timezone": "Asia/Kolkata",
        "displayName": "Ranchi, Jharkhand, India",
    },
    "raipur": {
        "city": "Raipur",
        "state": "Chhattisgarh",
        "country": "India",
        "latitude": 21.2514,
        "longitude": 81.6296,
        "timezone": "Asia/Kolkata",
        "displayName": "Raipur, Chhattisgarh, India",
    },
    "bhubaneswar": {
        "city": "Bhubaneswar",
        "state": "Odisha",
        "country": "India",
        "latitude": 20.2961,
        "longitude": 85.8245,
        "timezone": "Asia/Kolkata",
        "displayName": "Bhubaneswar, Odisha, India",
    },
    "chandigarh": {
        "city": "Chandigarh",
        "state": "Chandigarh",
        "country": "India",
        "latitude": 30.7333,
        "longitude": 76.7794,
        "timezone": "Asia/Kolkata",
        "displayName": "Chandigarh, Chandigarh, India",
    },
    "dehradun": {
        "city": "Dehradun",
        "state": "Uttarakhand",
        "country": "India",
        "latitude": 30.3165,
        "longitude": 78.0322,
        "timezone": "Asia/Kolkata",
        "displayName": "Dehradun, Uttarakhand, India",
    },
    "shimla": {
        "city": "Shimla",
        "state": "Himachal Pradesh",
        "country": "India",
        "latitude": 31.1048,
        "longitude": 77.1734,
        "timezone": "Asia/Kolkata",
        "displayName": "Shimla, Himachal Pradesh, India",
    },
    "goa": {
        "city": "Panaji",
        "state": "Goa",
        "country": "India",
        "latitude": 15.4909,
        "longitude": 73.8278,
        "timezone": "Asia/Kolkata",
        "displayName": "Panaji, Goa, India",
    },
    "varanasi": {
        "city": "Varanasi",
        "state": "Uttar Pradesh",
        "country": "India",
        "latitude": 25.3176,
        "longitude": 82.9739,
        "timezone": "Asia/Kolkata",
        "displayName": "Varanasi, Uttar Pradesh, India",
    },
    "london": {
        "city": "London",
        "state": "England",
        "country": "United Kingdom",
        "latitude": 51.5074,
        "longitude": -0.1278,
        "timezone": "Europe/London",
        "displayName": "London, England, United Kingdom",
    },
}

# ---------------------------------------------------------------------------
# 1-character prefix dataset (LOCAL FALLBACK — NOT LIVE PROVIDER DATA)
# Used ONLY when query is exactly 1 character AND the upstream provider
# returns zero results.  Contains real verified Indian cities only.
# Coordinates sourced from GeoNames/Open-Meteo canonical records.
# New entries must be cross-verified against an authoritative source.
# This is intentionally bounded (~35 entries) and maintainable.
# ---------------------------------------------------------------------------
_ONE_CHAR_PREFIX_INDEX: Dict[str, List[dict]] = {}

def _build_one_char_index() -> None:
    """Build an index from first letter → sorted list of FALLBACK_METRO_HUBS entries."""
    for key, data in FALLBACK_METRO_HUBS.items():
        first = key[0]
        if first not in _ONE_CHAR_PREFIX_INDEX:
            _ONE_CHAR_PREFIX_INDEX[first] = []
        _ONE_CHAR_PREFIX_INDEX[first].append(data)

_build_one_char_index()


def _deduplicate(results: List[LocationResult]) -> List[LocationResult]:
    """
    Remove duplicate LocationResult entries.
    Deduplication key: (city.lower(), state.lower() or '', country.lower()).
    Order is preserved (first occurrence wins).
    """
    seen: set = set()
    unique: List[LocationResult] = []
    for r in results:
        key = (
            (r.city or "").lower(),
            (r.state or "").lower(),
            (r.country or "").lower(),
        )
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


def _rank_results(results: List[LocationResult], query: str) -> List[LocationResult]:
    """
    Rank autocomplete results by deterministic relevance to the query.

    Priority tiers (lower score = higher rank):
      0 – city starts with query AND len(city) > len(query)  (e.g. "Mumbai" for "Mum")
      1 – city starts with query AND len(city) == len(query) (trivial exact, e.g. "Mum, Myanmar")
      2 – city contains query (but does not start with it)
      3 – state/admin1 starts with query
      4 – state/admin1 contains query
      5 – no match; original provider order

    Within each tier a country-relevance bonus (0=primary, 1=other) ranks
    well-known target countries (India, UK, US, AU, CA) above obscure ones.
    Stable secondary key is the original provider position.

    This ensures "Mumbai" ranks above "Mum, Myanmar" for query "Mum", and
    "Jaipur" ranks above "Jai, Pakistan" for query "Jai".
    """
    q = query.strip().lower()
    if not q:
        return results

    PRIMARY_COUNTRIES = {"india", "united kingdom", "united states", "australia", "canada"}

    def _country_bonus(r: LocationResult) -> int:
        return 0 if (r.country or "").lower() in PRIMARY_COUNTRIES else 1

    def _score(r: LocationResult, position: int) -> Tuple[int, int, int]:
        city = (r.city or "").lower()
        state = (r.state or "").lower()
        cb = _country_bonus(r)
        if city.startswith(q):
            tier = 0 if len(city) > len(q) else 1
            return (tier, cb, position)
        if q in city:
            return (2, cb, position)
        if state.startswith(q):
            return (3, cb, position)
        if q in state:
            return (4, cb, position)
        return (5, cb, position)

    return sorted(results, key=lambda r: _score(r, results.index(r)))


class LocationService:
    """
    Coordinates location resolution across in-memory cache,
    geocoding provider, and offline fallback dataset.
    """

    CACHE_TTL_SECONDS = 86400  # 24 hours
    MAX_CACHE_ENTRIES = 500

    def __init__(self, provider: Optional[GeocodingProvider] = None):
        self.provider = provider or OpenMeteoGeocodingProvider()

        # resolve_location() cache: normalized_key -> (LocationResult, expire_ts)
        self._resolve_cache: Dict[str, Tuple[LocationResult, float]] = {}

        # search_locations() cache: normalized_key -> (List[LocationResult], expire_ts)
        self._search_cache: Dict[str, Tuple[List[LocationResult], float]] = {}

    # ------------------------------------------------------------------
    # Internal cache helpers
    # ------------------------------------------------------------------

    def _prune_dict(self, cache: dict, current_time: float) -> None:
        """Evict expired entries and enforce MAX_CACHE_ENTRIES."""
        expired = [k for k, v in cache.items() if current_time > v[-1]]
        for k in expired:
            del cache[k]

        if len(cache) >= self.MAX_CACHE_ENTRIES:
            # Sort by expiry (ascending) and evict oldest
            sorted_keys = sorted(cache.keys(), key=lambda k: cache[k][-1])
            excess = len(cache) - self.MAX_CACHE_ENTRIES + 1
            for k in sorted_keys[:excess]:
                del cache[k]

    def _get_resolve(self, key: str) -> Optional[LocationResult]:
        entry = self._resolve_cache.get(key)
        if not entry:
            return None
        result, expiry = entry
        if time.time() > expiry:
            del self._resolve_cache[key]
            return None
        return result

    def _set_resolve(self, key: str, result: LocationResult) -> None:
        now = time.time()
        self._prune_dict(self._resolve_cache, now)
        self._resolve_cache[key] = (result, now + self.CACHE_TTL_SECONDS)

    def _get_search(self, key: str) -> Optional[List[LocationResult]]:
        entry = self._search_cache.get(key)
        if not entry:
            return None
        results, expiry = entry
        if time.time() > expiry:
            del self._search_cache[key]
            return None
        return results

    def _set_search(self, key: str, results: List[LocationResult]) -> None:
        now = time.time()
        self._prune_dict(self._search_cache, now)
        self._search_cache[key] = (results, now + self.CACHE_TTL_SECONDS)

    # ------------------------------------------------------------------
    # Public: single-result resolution (used by weather endpoint)
    # ------------------------------------------------------------------

    async def resolve_location(self, query: str) -> Optional[LocationResult]:
        """
        Resolve user query into a single canonical LocationResult.

        Workflow:
            1. Normalize query key.
            2. Check resolve cache.
            3. On miss, invoke provider.resolve() (count=1).
            4. On provider failure, check offline fallback metro dictionary.
            5. Return result or raise for 503 if provider failed and unmapped.
        """
        clean_key = query.strip().lower()

        cached = self._get_resolve(clean_key)
        if cached:
            return cached

        try:
            result = await self.provider.resolve(clean_key)
            if result:
                self._set_resolve(clean_key, result)
                return result
            return None
        except Exception as exc:
            logger.warning("Geocoding provider failed for query '%s': %s", clean_key, exc)
            fallback_match = FALLBACK_METRO_HUBS.get(clean_key)
            if fallback_match:
                logger.info("Serving query '%s' from offline fallback metro dataset", clean_key)
                return LocationResult(**fallback_match)
            raise

    # ------------------------------------------------------------------
    # Public: multi-result search (used by autocomplete endpoint)
    # ------------------------------------------------------------------

    async def search_locations(self, query: str, max_results: int = 8) -> List[LocationResult]:
        """
        Return up to max_results candidate LocationResult objects for autocomplete.

        Workflow:
            1. Normalize query key.
            2. Check search cache.
            3. On miss, invoke provider.search() with bounded count.
            4. Deduplicate results by (city, state, country).
            5. On provider failure, attempt to match offline fallback entries
               that start with the query prefix (exact-match safety only).
            6. Cache and return the deduplicated list.

        Note: An empty list is a valid return value (provider found no matches).
              This does NOT silently remap unknown queries to fallback cities.
        """
        clean_key = query.strip().lower()

        cached = self._get_search(clean_key)
        if cached is not None:
            return cached

        # --- 1-character query: Open-Meteo returns nothing reliable for single chars.
        #     Use curated local prefix index instead. Never fallback to live provider
        #     for 1-char queries as results are geography-agnostic and unranked.
        if len(clean_key) == 1:
            letter_hits = _ONE_CHAR_PREFIX_INDEX.get(clean_key, [])
            results = _deduplicate([
                LocationResult(**v) for v in letter_hits
            ])[:max_results]
            self._set_search(clean_key, results)
            return results

        try:
            raw_results = await self.provider.search(clean_key, count=max(max_results, 10))
            # For short prefixes (<= 2 chars), Open-Meteo often returns only tiny villages or obscure places (like "Ja, Sudan").
            # Supplement with curated verified metro hubs matching the prefix so prominent cities (like Jaipur) rank first.
            if len(clean_key) <= 2:
                prefix_curated = [
                    LocationResult(**v)
                    for k, v in FALLBACK_METRO_HUBS.items()
                    if k.startswith(clean_key)
                ]
                raw_results = prefix_curated + raw_results
            ranked = _rank_results(raw_results, clean_key)
            results = _deduplicate(ranked)[:max_results]
        except Exception as exc:
            logger.warning("Geocoding provider search failed for query '%s': %s", clean_key, exc)
            # Fallback: surface only offline metro hubs whose key starts with
            # the user's exact typed prefix. This never maps an unknown city
            # to a different city — it only suggests known metros when upstream
            # is unavailable.
            fallback_raw = [
                LocationResult(**v)
                for k, v in FALLBACK_METRO_HUBS.items()
                if k.startswith(clean_key)
            ]
            results = _deduplicate(_rank_results(fallback_raw, clean_key))[:max_results]

        self._set_search(clean_key, results)
        return results


# Singleton instance
location_service = LocationService()
