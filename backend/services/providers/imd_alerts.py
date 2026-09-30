"""
Alerts Provider for Mausam (Step 27, hardened in Step 28).

Fetches official Indian disaster/weather alerts from NDMA's Sachet CAP public feed,
which aggregates IMD and SDMA CAP alert feeds across Indian states and districts.

Matching strategy (Step 28):
  PRIMARY: Coordinate-based proximity matching using the alert's `centroid` field.
    - Each Sachet alert carries a `centroid` field in "longitude,latitude" format.
    - We compute the Haversine distance between the alert centroid and the selected
      location's coordinates.
    - If the distance is <= ALERT_RADIUS_KM (300 km), the alert is considered
      relevant to the location.
    - 300 km is chosen to cover state-level warnings (e.g., IMD district bulletins
      issued for multiple districts across a state) while avoiding false positives
      from distant states.
  FALLBACK (centroid missing/unparseable): Skip the alert entirely. Do NOT use
    crude city-name substring matching, which conflates mandal codes (e.g.
    "ctr-nagari") with city names and generates false positives.

This strategy is deterministic and explainable: an alert matches iff its official
centroid is within 300 km of the selected location. City-to-district ambiguity is
eliminated because the matching is purely geographic.

Why 300 km:
  - IMD Chennai's Tamil Nadu bulletin centroid (79.45, 11.54) is ~194 km from
    Chennai city (80.27, 13.08) → correctly matched.
  - Andhra Pradesh SDMA mandal alerts near Tirupati (~70 km from Chennai) →
    correctly matched.
  - Jaipur (26.91, 75.79) has no alerts within 300 km on typical days → correctly
    returns empty list.
  - London (51.51, -0.13) → skipped immediately (non-India filter) → empty list.

Limitations:
  - City-district boundary is not used (Sachet does not expose district codes linked
    to Open-Meteo city names in a reliable way).
  - Alerts with a missing or malformed centroid are silently skipped (correct; we
    must not guess geography).
  - Warning messages in regional languages (Telugu, Kannada, etc.) are passed through
    as-is; no translation is attempted.
"""

import logging
import math
from typing import List, Dict, Any
import httpx

from backend.schemas.location import LocationResult

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Alert matching constants
# ---------------------------------------------------------------------------
# Maximum straight-line distance (km) between an alert centroid and the selected
# city for the alert to be considered relevant to that location.
ALERT_RADIUS_KM = 300

# Minimum distance from India bounding box (approx). Non-India countries are
# skipped immediately without an HTTP request.
_INDIA_LAT_RANGE = (6.0, 37.5)
_INDIA_LON_RANGE = (68.0, 97.5)


class IMDAlertsProvider:
    """
    Provider fetching official CAP alerts from Sachet (NDMA / IMD CAP gateway).
    Free of private API credentials, provides real-time official warnings.

    Matching is coordinate-based: alerts whose centroid is within ALERT_RADIUS_KM
    of the selected location are returned. See module docstring for rationale.
    """

    SACHET_URL = "https://sachet.ndma.gov.in/cap_public_website/FetchAllAlertDetails"
    TIMEOUT_SECONDS = 4.0

    # Severity color → product alert level
    SEVERITY_LEVEL_MAP = {
        "red": "severe",
        "orange": "warning",
        "yellow": "advisory",
        "green": "advisory",
    }

    # ---------------------------------------------------------------------------
    # Haversine distance
    # ---------------------------------------------------------------------------

    @staticmethod
    def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Return great-circle distance between two lat/lon points in kilometres."""
        R = 6371.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = (
            math.sin(dphi / 2) ** 2
            + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        )
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    # ---------------------------------------------------------------------------
    # Centroid parsing
    # ---------------------------------------------------------------------------

    @staticmethod
    def _parse_centroid(centroid_str: str):
        """
        Parse Sachet centroid field format: "longitude,latitude"
        Returns (lat, lon) tuple or None if unparseable.
        Note: Sachet stores centroid as "lon,lat" (not "lat,lon").
        """
        if not centroid_str:
            return None
        try:
            parts = centroid_str.strip().split(",")
            if len(parts) != 2:
                return None
            lon = float(parts[0])
            lat = float(parts[1])
            # Basic sanity bounds
            if not (-90 <= lat <= 90 and -180 <= lon <= 180):
                return None
            return (lat, lon)
        except (ValueError, AttributeError):
            return None

    # ---------------------------------------------------------------------------
    # Alert time formatting
    # ---------------------------------------------------------------------------

    @staticmethod
    def _format_time_window(start_time: str, end_time: str) -> str:
        """
        Build a human-readable validity window string.

        `effective_start_time` = when the alert becomes active.
        `effective_end_time`   = when the alert expires.

        We show "Until <end-time>" as the primary label (answers the most
        user-relevant question: "until when is this alert valid?").
        We never label end-time as issue-time.
        """
        if end_time:
            # Format: "Wed Sep 30 18:50:00 IST 2026"
            parts = end_time.strip().split()
            # parts: ['Wed', 'Sep', '30', '18:50:00', 'IST', '2026']
            if len(parts) >= 4:
                time_part = parts[3]  # e.g. "18:50:00"
                tz_part = parts[4] if len(parts) > 4 else ""
                date_part = f"{parts[1]} {parts[2]}"  # e.g. "Sep 30"
                return f"Until {time_part} {tz_part} ({date_part})".strip()
        return "Active"

    # ---------------------------------------------------------------------------
    # Main entry point
    # ---------------------------------------------------------------------------

    async def get_alerts_for_location(self, location: LocationResult) -> List[Dict[str, Any]]:
        """
        Fetch Sachet CAP alerts and filter by coordinate proximity to location.

        Returns:
            List of normalized alert dicts (may be empty).
            Raises Exception on network/provider failure (caller converts to unavailable).

        Matching:
            1. Non-India locations: immediately return [] without HTTP request.
            2. Parse each alert's centroid as (lat, lon).
            3. Compute Haversine distance to location coordinates.
            4. Include alert if distance <= ALERT_RADIUS_KM.
            5. Skip alerts with missing/malformed centroid silently.
        """
        # Non-India fast path: Sachet only covers India
        if location.country and "india" not in location.country.lower():
            return []

        # Verify location has usable coordinates
        if location.latitude is None or location.longitude is None:
            logger.warning(
                "AlertsProvider: location '%s' has no coordinates — skipping",
                location.city,
            )
            return []

        city_lat = location.latitude
        city_lon = location.longitude

        headers = {
            "User-Agent": "Mausam-PersonalizedWeather/0.2.0 (SIH Project; mail: contact@mausam.app)",
            "Accept": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.TIMEOUT_SECONDS, verify=False) as client:
            resp = await client.get(self.SACHET_URL, headers=headers)
            resp.raise_for_status()
            raw_alerts = resp.json()

        if not isinstance(raw_alerts, list):
            logger.warning("Sachet response is not a list; got %s", type(raw_alerts))
            return []

        matched_alerts: List[Dict[str, Any]] = []

        for item in raw_alerts:
            # --- Primary matching: coordinate proximity ---
            centroid_str = item.get("centroid") or ""
            parsed = self._parse_centroid(centroid_str)

            if parsed is None:
                # Centroid missing or malformed — skip; do not guess geography
                logger.debug(
                    "Alert %s has no parseable centroid '%s' — skipped",
                    item.get("alert_id_sdma_autoinc"),
                    centroid_str,
                )
                continue

            alert_lat, alert_lon = parsed
            distance_km = self._haversine_km(city_lat, city_lon, alert_lat, alert_lon)

            if distance_km > ALERT_RADIUS_KM:
                continue  # Too far away

            # --- Build normalized alert object ---
            color = (item.get("severity_color") or "yellow").lower()
            level = self.SEVERITY_LEVEL_MAP.get(color, "advisory")
            disaster = item.get("disaster_type") or "Weather Alert"
            source = item.get("alert_source") or "IMD"
            start_time = item.get("effective_start_time") or ""
            end_time = item.get("effective_end_time") or ""
            time_str = self._format_time_window(start_time, end_time)

            # Alert ID: prefer CAP identifier, fall back to SDMA autoinc
            alert_id = str(item.get("identifier") or item.get("alert_id_sdma_autoinc") or "unknown")

            # Warning message: use official text; if regional language, still pass through
            area_desc = item.get("area_description") or ""
            warning_msg = item.get("warning_message") or (
                f"Official {disaster} advisory issued for {area_desc}."
            )

            matched_alerts.append({
                "id": alert_id,
                "level": level,
                "badge": f"{color.upper()} ALERT",
                "title": f"{disaster} Warning ({source})",
                "time": time_str,
                "description": warning_msg,
                # Extra debug metadata (not in WeatherAlertSchema; stripped at schema layer)
                "_distanceKm": round(distance_km, 1),
                "_centroid": centroid_str,
            })

        logger.info(
            "Sachet alerts for %s (lat=%.3f, lon=%.3f): %d/%d within %d km",
            location.city,
            city_lat,
            city_lon,
            len(matched_alerts),
            len(raw_alerts),
            ALERT_RADIUS_KM,
        )

        return matched_alerts
