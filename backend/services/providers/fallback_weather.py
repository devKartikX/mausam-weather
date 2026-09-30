"""
Deterministic City Weather Fallback Datasets for Mausam.

Used ONLY when Open-Meteo forecast API returns HTTP 429 (rate-limit on shared IP).
Provides realistic, deterministic static profiles for key major cities,
with mathematical fallback generator for any other city.

Metadata explicitly sets:
  meta.source = "fallback-simulated"
  meta.isDemo = true
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional
from backend.schemas.location import LocationResult

# ---------------------------------------------------------------------------
# Pre-defined deterministic static profiles for major cities
# Plausible climatological values matching typical conditions
# ---------------------------------------------------------------------------
CITY_PROFILES: Dict[str, Dict[str, Any]] = {
    "jaipur": {
        "temp": 31.0,
        "feelsLike": 32.0,
        "highTemp": 34.0,
        "lowTemp": 22.0,
        "condition": "Sunny",
        "icon": "Sun",
        "humidity": 38,
        "windSpeed": 12.0,
        "windDirection": "NW",
        "rainProbability": 5,
        "visibility": 9.5,
        "uvIndex": 7.2,
        "uvStatus": "High",
        "sunrise": "06:18 AM",
        "sunset": "06:32 PM",
        "hourly_temps": [31, 29, 28, 26, 25, 24, 23, 22, 25, 28],
        "daily_highs": [34, 35, 33, 34, 32, 33, 35],
        "daily_lows": [22, 23, 21, 22, 21, 22, 23],
        "daily_conditions": [
            ("Sunny", "Sun", 5),
            ("Clear & Warm", "Sun", 0),
            ("Partly Cloudy", "CloudSun", 10),
            ("Sunny", "Sun", 0),
            ("Scattered Clouds", "CloudSun", 15),
            ("Sunny & Clear", "Sun", 0),
            ("Sunny", "Sun", 5),
        ],
    },
    "mumbai": {
        "temp": 29.0,
        "feelsLike": 34.0,
        "highTemp": 32.0,
        "lowTemp": 26.0,
        "condition": "Humid & Partly Cloudy",
        "icon": "CloudSun",
        "humidity": 78,
        "windSpeed": 18.0,
        "windDirection": "SW",
        "rainProbability": 25,
        "visibility": 7.0,
        "uvIndex": 6.5,
        "uvStatus": "High",
        "sunrise": "06:28 AM",
        "sunset": "06:40 PM",
        "hourly_temps": [29, 29, 28, 28, 27, 27, 26, 26, 28, 30],
        "daily_highs": [32, 32, 31, 31, 32, 33, 32],
        "daily_lows": [26, 26, 25, 25, 26, 26, 26],
        "daily_conditions": [
            ("Partly Cloudy", "CloudSun", 25),
            ("Passing Showers", "CloudRain", 40),
            ("Partly Cloudy", "CloudSun", 20),
            ("Humid & Sunny", "CloudSun", 15),
            ("Passing Showers", "CloudRain", 35),
            ("Partly Cloudy", "CloudSun", 20),
            ("Humid", "CloudSun", 15),
        ],
    },
    "delhi": {
        "temp": 30.0,
        "feelsLike": 32.0,
        "highTemp": 33.0,
        "lowTemp": 21.0,
        "condition": "Hazy Sunshine",
        "icon": "Sun",
        "humidity": 45,
        "windSpeed": 10.0,
        "windDirection": "W",
        "rainProbability": 10,
        "visibility": 6.0,
        "uvIndex": 6.8,
        "uvStatus": "High",
        "sunrise": "06:14 AM",
        "sunset": "06:26 PM",
        "hourly_temps": [30, 28, 27, 25, 24, 23, 22, 21, 24, 27],
        "daily_highs": [33, 34, 32, 31, 33, 34, 33],
        "daily_lows": [21, 22, 20, 20, 21, 22, 21],
        "daily_conditions": [
            ("Hazy Sunshine", "Sun", 10),
            ("Sunny & Warm", "Sun", 5),
            ("Partly Cloudy", "CloudSun", 15),
            ("Clear", "Sun", 0),
            ("Sunny", "Sun", 5),
            ("Hazy Sunshine", "Sun", 10),
            ("Sunny", "Sun", 0),
        ],
    },
    "bengaluru": {
        "temp": 25.0,
        "feelsLike": 26.0,
        "highTemp": 28.0,
        "lowTemp": 19.0,
        "condition": "Pleasant & Breezy",
        "icon": "CloudSun",
        "humidity": 62,
        "windSpeed": 16.0,
        "windDirection": "E",
        "rainProbability": 20,
        "visibility": 9.0,
        "uvIndex": 7.0,
        "uvStatus": "High",
        "sunrise": "06:10 AM",
        "sunset": "06:22 PM",
        "hourly_temps": [25, 24, 23, 22, 21, 20, 19, 19, 22, 24],
        "daily_highs": [28, 29, 27, 28, 28, 27, 28],
        "daily_lows": [19, 19, 18, 19, 19, 18, 19],
        "daily_conditions": [
            ("Pleasant & Breezy", "CloudSun", 20),
            ("Partly Cloudy", "CloudSun", 15),
            ("Passing Showers", "CloudRain", 35),
            ("Pleasant", "CloudSun", 10),
            ("Scattered Clouds", "CloudSun", 20),
            ("Partly Cloudy", "CloudSun", 15),
            ("Sunny Intervals", "Sun", 10),
        ],
    },
    "chennai": {
        "temp": 31.0,
        "feelsLike": 36.0,
        "highTemp": 34.0,
        "lowTemp": 27.0,
        "condition": "Warm & Humid",
        "icon": "Sun",
        "humidity": 74,
        "windSpeed": 15.0,
        "windDirection": "SE",
        "rainProbability": 15,
        "visibility": 8.0,
        "uvIndex": 8.1,
        "uvStatus": "Very High",
        "sunrise": "05:58 AM",
        "sunset": "06:12 PM",
        "hourly_temps": [31, 30, 29, 29, 28, 28, 27, 27, 29, 31],
        "daily_highs": [34, 34, 35, 33, 34, 34, 33],
        "daily_lows": [27, 27, 28, 26, 27, 27, 27],
        "daily_conditions": [
            ("Warm & Humid", "Sun", 15),
            ("Mostly Sunny", "Sun", 10),
            ("Partly Cloudy", "CloudSun", 20),
            ("Passing Showers", "CloudRain", 30),
            ("Sunny & Hot", "Sun", 5),
            ("Partly Cloudy", "CloudSun", 15),
            ("Warm & Humid", "Sun", 10),
        ],
    },
    "kolkata": {
        "temp": 30.0,
        "feelsLike": 35.0,
        "highTemp": 33.0,
        "lowTemp": 25.0,
        "condition": "Partly Cloudy",
        "icon": "CloudSun",
        "humidity": 72,
        "windSpeed": 11.0,
        "windDirection": "S",
        "rainProbability": 30,
        "visibility": 7.5,
        "uvIndex": 6.9,
        "uvStatus": "High",
        "sunrise": "05:27 AM",
        "sunset": "05:41 PM",
        "hourly_temps": [30, 29, 28, 27, 26, 26, 25, 25, 27, 29],
        "daily_highs": [33, 33, 32, 34, 32, 33, 32],
        "daily_lows": [25, 25, 24, 25, 24, 25, 25],
        "daily_conditions": [
            ("Partly Cloudy", "CloudSun", 30),
            ("Afternoon Thundershower", "CloudLightning", 45),
            ("Passing Showers", "CloudRain", 40),
            ("Partly Cloudy", "CloudSun", 20),
            ("Humid & Sunny", "CloudSun", 15),
            ("Passing Showers", "CloudRain", 35),
            ("Partly Cloudy", "CloudSun", 25),
        ],
    },
    "london": {
        "temp": 16.0,
        "feelsLike": 15.0,
        "highTemp": 18.0,
        "lowTemp": 11.0,
        "condition": "Overcast & Mild",
        "icon": "Cloud",
        "humidity": 68,
        "windSpeed": 19.0,
        "windDirection": "SW",
        "rainProbability": 35,
        "visibility": 10.0,
        "uvIndex": 3.2,
        "uvStatus": "Moderate",
        "sunrise": "06:58 AM",
        "sunset": "06:44 PM",
        "hourly_temps": [16, 15, 14, 13, 12, 12, 11, 12, 14, 16],
        "daily_highs": [18, 17, 19, 16, 17, 18, 17],
        "daily_lows": [11, 10, 12, 9, 10, 11, 10],
        "daily_conditions": [
            ("Overcast & Mild", "Cloud", 35),
            ("Light Rain", "CloudRain", 55),
            ("Sunny Intervals", "CloudSun", 20),
            ("Passing Showers", "CloudRain", 45),
            ("Partly Cloudy", "CloudSun", 25),
            ("Breezy & Mild", "Cloud", 30),
            ("Light Showers", "CloudRain", 40),
        ],
    },
}

# Aliases for matching
ALIASES = {
    "new delhi": "delhi",
    "bangalore": "bengaluru",
    "calcutta": "kolkata",
    "madras": "chennai",
    "bombay": "mumbai",
}


def _get_profile_for_city(city: str) -> Dict[str, Any]:
    """Retrieve static profile for known city, or generate deterministic profile by city name hash."""
    norm = city.strip().lower()
    norm = ALIASES.get(norm, norm)
    if norm in CITY_PROFILES:
        return CITY_PROFILES[norm]

    # Deterministic fallback for any other city using a simple stable hash
    h = sum(ord(c) for c in norm)
    base_temp = 22 + (h % 12)
    return {
        "temp": float(base_temp),
        "feelsLike": float(base_temp + 1),
        "highTemp": float(base_temp + 4),
        "lowTemp": float(base_temp - 5),
        "condition": "Partly Cloudy",
        "icon": "CloudSun",
        "humidity": 50 + (h % 30),
        "windSpeed": 10.0 + (h % 12),
        "windDirection": ["N", "NE", "E", "SE", "S", "SW", "W", "NW"][h % 8],
        "rainProbability": (h * 7) % 40,
        "visibility": 8.0,
        "uvIndex": 5.0 + (h % 4),
        "uvStatus": "Moderate" if (h % 4) < 2 else "High",
        "sunrise": "06:15 AM",
        "sunset": "06:30 PM",
        "hourly_temps": [base_temp - (i % 4) for i in range(10)],
        "daily_highs": [base_temp + 4 + (i % 3) for i in range(7)],
        "daily_lows": [base_temp - 5 + (i % 2) for i in range(7)],
        "daily_conditions": [
            ("Partly Cloudy", "CloudSun", 15),
            ("Sunny", "Sun", 5),
            ("Scattered Clouds", "CloudSun", 20),
            ("Mostly Sunny", "Sun", 10),
            ("Passing Showers", "CloudRain", 35),
            ("Partly Cloudy", "CloudSun", 20),
            ("Sunny", "Sun", 5),
        ],
    }


def build_fallback_weather(
    location: LocationResult,
    original_query: str,
    real_aqi_data: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build a complete, normalized WeatherResponse dictionary using deterministic fallback data.
    
    Explicitly marked as simulated demo data:
      meta.source = "fallback-simulated"
      meta.isDemo = true
      meta.demoReason = "Live Open-Meteo forecast API rate-limited (HTTP 429) on shared IP"
    
    If real AQI data was successfully fetched, it is preserved.
    """
    profile = _get_profile_for_city(location.city)
    now_utc = datetime.now(timezone.utc).isoformat()

    # 10-hour forecast
    hour_labels = ["Now", "8 PM", "9 PM", "10 PM", "11 PM", "12 AM", "6 AM", "7 AM", "8 AM", "9 AM"]
    hourly_list = []
    for i, label in enumerate(hour_labels):
        temp_val = profile["hourly_temps"][i] if i < len(profile["hourly_temps"]) else profile["temp"]
        hourly_list.append({
            "time": label,
            "temp": round(float(temp_val)),
            "condition": profile["condition"],
            "pop": profile["rainProbability"],
            "icon": profile["icon"],
        })

    # 7-day forecast
    day_labels = ["Today", "Wed", "Thu", "Fri", "Sat", "Sun", "Mon"]
    daily_list = []
    for i, d_label in enumerate(day_labels):
        d_high = profile["daily_highs"][i] if i < len(profile["daily_highs"]) else profile["highTemp"]
        d_low = profile["daily_lows"][i] if i < len(profile["daily_lows"]) else profile["lowTemp"]
        if i < len(profile["daily_conditions"]):
            cond, icon, pop = profile["daily_conditions"][i]
        else:
            cond, icon, pop = profile["condition"], profile["icon"], profile["rainProbability"]

        daily_list.append({
            "day": d_label,
            "condition": cond,
            "high": round(float(d_high)),
            "low": round(float(d_low)),
            "pop": pop,
            "icon": icon,
        })

    # AQI: preserve real if succeeded, otherwise None
    aqi_val = None
    aqi_status = None
    pm25_val = None
    pm10_val = None
    if real_aqi_data:
        curr_aq = real_aqi_data.get("current", {})
        raw_aqi = curr_aq.get("us_aqi")
        if raw_aqi is not None:
            aqi_val = int(raw_aqi)
            from backend.services.utils import derive_aqi_status
            aqi_status = derive_aqi_status(aqi_val)
        pm25_val = curr_aq.get("pm2_5")
        pm10_val = curr_aq.get("pm10")

    return {
        "meta": {
            "source": "fallback-simulated",
            "generatedAt": now_utc,
            "cachedAt": None,
            "locationQuery": original_query,
            "isDemo": True,
            "isStale": False,
            "staleReason": None,
            "dataAgeSeconds": 0,
            "alertsAvailable": True,
        },
        "location": {
            "city": location.city,
            "state": location.state,
            "country": location.country,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timezone": location.timezone,
            "elevation": "Simulated",
            "lastUpdated": "Demo weather data",
        },
        "current": {
            "temp": round(profile["temp"]),
            "condition": profile["condition"],
            "feelsLike": round(profile["feelsLike"]),
            "highTemp": round(profile["highTemp"]),
            "lowTemp": round(profile["lowTemp"]),
            "humidity": profile["humidity"],
            "windSpeed": profile["windSpeed"],
            "windDirection": profile["windDirection"],
            "rainProbability": profile["rainProbability"],
            "visibility": profile["visibility"],
            "uvIndex": profile["uvIndex"],
            "uvStatus": profile["uvStatus"],
            "aqi": aqi_val,
            "aqiStatus": aqi_status,
            "pm25": pm25_val,
            "pm10": pm10_val,
            "sunrise": profile["sunrise"],
            "sunset": profile["sunset"],
            "icon": profile["icon"],
            "waveHeight": None,
            "seaSurfaceTemp": None,
            "tidalInfo": None,
        },
        "hourly": hourly_list,
        "daily": daily_list,
        "alerts": [],
    }
