"""
Weather router — GET /api/weather

Step 19: Full real-weather pipeline.
Flow:
  Query (location)
    -> LocationService.resolve_location(...) -> canonical LocationResult
    -> WeatherService.get_weather(...) -> real Open-Meteo forecast + air quality
    -> normalized WeatherResponse
"""

import logging
from fastapi import APIRouter, Query, HTTPException, status
from backend.schemas.weather import WeatherResponse
from backend.services.location_service import location_service
from backend.services.weather_service import weather_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/weather",
    response_model=WeatherResponse,
    summary="Get weather data for location",
    description="Resolves location and returns real normalized weather data from Open-Meteo.",
)
async def get_weather(
    location: str = Query(
        ...,
        min_length=1,
        max_length=100,
        description="City name or location query",
        examples=["Jaipur", "Mumbai", "London"],
    )
):
    """
    Return normalized weather data for the given location query.

    1. Resolves query into canonical LocationResult via LocationService.
    2. Fetches and normalizes live forecast + air quality via WeatherService.
    3. Handles 400 Bad Request, 404 Not Found, and 502/503 Provider Failures.
    """
    clean_location = location.strip()
    if not clean_location:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Location parameter cannot be empty or whitespace only.",
        )

    # 1. Resolve location
    try:
        location_result = await location_service.resolve_location(clean_location)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Location resolution service temporarily unavailable. Please try again shortly.",
        )

    if not location_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location '{clean_location}' could not be resolved. Please try a major city name.",
        )

    # 2. Fetch real weather
    try:
        weather_data = await weather_service.get_weather(location_result, clean_location)
    except Exception as exc:
        logger.error(
            "WEATHER_502 location=%s exc_type=%s exc=%s",
            clean_location,
            type(exc).__name__,
            str(exc),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Weather data provider temporarily unavailable. Please try again shortly.",
        )

    return weather_data
